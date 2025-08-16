# --------------- Imports ---------------

from threading import RLock
from typing import Any, Dict, Optional
from collections import OrderedDict, deque
from statistics import median

from ..errors import MetricsLifespanException, MetricsLatencyException

import time
import random
import sys

# --------------- Entry Model ---------------

class CacheEntry():
    __slots__ = ("value", "expiry", "creation")

    def __init__(self, value: Any, ttl: float):
        self.value = value
        self.creation = time.monotonic()
        self.expiry = self.creation + ttl

    def lifespan(self) -> float:
        return time.monotonic() - self.creation

    def is_expired(self) -> bool:
        return time.monotonic() > self.expiry
    
    def __repr__(self):
        return f"<CacheEntry(value={self.value}, expires_in={self.expiry - time.monotonic():.2f}s)>"
    
# --------------- Caching Models ---------------
    
class BaseCache():
    __slots__ = (
        "max_cache_size",
        "default_ttl",
        "cache",
        "lock",
        "hits",
        "misses",
        "evictions",
        "lifespan",
        "add_latency",
        "get_latency"
    )

    def __init__(self, max_cache_size: int, default_ttl: float):
        self.max_cache_size = max_cache_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[Any, CacheEntry] = OrderedDict()
        self.lock = RLock()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.lifespan = deque(maxlen=1000)
        self.add_latency = deque(maxlen=1000)
        self.get_latency = deque(maxlen=1000)


    def _purge_expired(self) -> None:
        for key in list(self.cache.keys()):
            if self.cache[key].is_expired():
                self.evictions += 1
                ls = self.cache[key].lifespan()
                self.lifespan.append(ls)
                del self.cache[key]
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
            self.evictions = 0
            self.lifespan.clear()
            self.add_latency.clear()
            self.get_latency.clear()

    @property
    def current_size(self) -> int:
        return len(self.cache)
    
    @property
    def max_size(self) -> int:
        return self.max_cache_size
    
    @property
    def ttl(self) -> int:
        return self.default_ttl
    
    @property
    def hit_ratio(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
    
    @property
    def metric_lifespan(self) -> Dict[str, float]:
        if not self.lifespan:
            raise MetricsLifespanException()
        
        max_value = max(self.lifespan)
        min_value = min(self.lifespan)
        count = len(self.lifespan)
        total_value = sum(self.lifespan)
        avg_lifespan = total_value / count
        median_value = median(self.lifespan)
        
        return {
            "max": max_value,
            "min": min_value,
            "count": count,
            "total": total_value,
            "average": avg_lifespan,
            "median": median_value
        }
    
    @property
    def memory_size(self):
        size = sys.getsizeof(self.cache)
        for k, v in self.cache.items():
            size += (sys.getsizeof(k) + sys.getsizeof(v))
        return size
    
    @property
    def latencies(self):
        latencies = {}

        if self.add_latency:
            latencies["add_latency_seconds"] = sum(self.add_latency) / len(self.add_latency)
            latencies["max_add_latency"] = max(self.add_latency)
            latencies["min_add_latency"] = min(self.add_latency)
        else:
            raise MetricsLatencyException("No data related to 'add' latency currently available")
        
        if self.get_latency:
            latencies["get_latency_seconds"] = sum(self.get_latency) / len(self.get_latency)
            latencies["max_get_latency"] = max(self.get_latency)
            latencies["min_get_latency"] = min(self.get_latency)
        else:
            raise MetricsLatencyException("No data related to 'get' latency currently available")

        return latencies
    
    def __contains__(self, key: Any) -> bool:
        with self.lock:
            entry = self.cache.get(key)
            return entry is not None and not entry.is_expired()
        
    def __len__(self) -> int:
        return self.current_size
    
    def __iter__(self):
        with self.lock:
            for key, entry in self.cache.items():
                if not entry.is_expired():
                    yield key, entry.value
        
    
class LRUCache(BaseCache):
    def __init__(self, max_cache_size: int, default_ttl: float):
        super().__init__(max_cache_size, default_ttl)

    def add(self, key: Any, value: Any) -> None:
        with self.lock:
            start_time = time.monotonic()
            self._purge_expired()

            self.cache.pop(key, None)

            while len(self.cache) >= self.max_cache_size:
                removed = self.cache.popitem(last=False)
                self.evictions += 1
                self.lifespan.append(removed[1].lifespan())
            self.cache[key] = CacheEntry(value, self.default_ttl)
            end_time = time.monotonic()
            self.add_latency.append(end_time - start_time)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            start_time = time.monotonic()
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                self.cache.pop(key, None)
                self.misses += 1
                return None
            self.cache.move_to_end(key)
            self.hits += 1
            end_time = time.monotonic()
            self.get_latency.append(end_time - start_time)
            return entry.value
        
class FIFOCache(BaseCache):
    def __init__(self, max_cache_size: int, default_ttl: float):
        super().__init__(max_cache_size, default_ttl)

    def add(self, key: Any, value: Any) -> None:
        with self.lock:
            start_time = time.monotonic()
            self._purge_expired()

            self.cache.pop(key, None)

            while len(self.cache) >= self.max_cache_size:
                removed = self.cache.popitem()
                self.evictions += 1
                self.lifespan.append(removed[1].lifespan())
            self.cache[key] = CacheEntry(value, self.default_ttl)
            end_time = time.monotonic()
            self.add_latency.append(end_time - start_time)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            start_time = time.monotonic()
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                self.cache.pop(key, None)
                self.misses += 1
                return None
            self.hits += 1
            end_time = time.monotonic()
            self.get_latency.append(end_time - start_time)
            return entry.value

class RandomCache(BaseCache):
    def __init__(self, max_cache_size: int, default_ttl: float):
        super().__init__(max_cache_size, default_ttl)

    def add(self, key: Any, value: Any) -> None:
        with self.lock:
            start_time = time.monotonic()
            self._purge_expired()

            self.cache.pop(key, None)

            while len(self.cache) >= self.max_cache_size:
                random_key = random.choice(list(self.cache.keys()))
                removed = self.cache.pop(random_key)
                self.evictions += 1
                self.lifespan.append(removed[1].lifespan())
            self.cache[key] = CacheEntry(value, self.default_ttl)
            end_time = time.monotonic()
            self.add_latency.append(end_time - start_time)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            start_time = time.monotonic()
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                self.cache.pop(key, None)
                self.misses += 1
                return None
            self.hits += 1
            end_time = time.monotonic()
            self.get_latency.append(end_time - start_time)
            return entry.value
    

    
        