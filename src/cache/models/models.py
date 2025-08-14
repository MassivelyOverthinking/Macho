# --------------- Imports ---------------

from threading import RLock
from typing import Any
from collections import OrderedDict
from typing import Optional

import time
import random

# --------------- Entry Model ---------------

class CacheEntry():
    __slots__ = ("value", "expiry")

    def __init__(self, value: Any, ttl: float):
        self.value = value
        self.expiry = time.time() + ttl

    def is_expired(self) -> bool:
        return time.time() > self.expiry
    
# --------------- Caching Models ---------------
    
class BaseCache():
    __slots__ = ("max_cache_size", "default_ttl", "cache", "lock", "hits", "misses", "evictions")

    def __init__(self, max_cache_size: int, default_ttl: float):
        self.max_cache_size = max_cache_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[Any, CacheEntry] = OrderedDict()
        self.lock = RLock()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def _purge_expired(self) -> None:
        for key in list(self.cache.keys()):
            if self.cache[key].is_expired():
                self.evictions += 1
                del self.cache[key]
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()

    @property
    def capacity(self) -> int:
        return len(self.cache)
    
    @property
    def size(self) -> int:
        return self.max_cache_size
    
    @property
    def ttl(self) -> int:
        return self.default_ttl
    
    @property
    def hit_ratio(self) -> float:
        return self.hits / (self.hits + self.misses)
        
    
class LRUCache(BaseCache):
    def __init__(self, max_cache_size: int, default_ttl: float):
        super().__init__(max_cache_size, default_ttl)

    def add(self, key: Any, value: Any) -> None:
        with self.lock:
            self._purge_expired()

            self.cache.pop(key, None)

            while len(self.cache) >= self.max_cache_size:
                self.cache.popitem(last=False)
            self.cache[key] = CacheEntry(value, self.default_ttl)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                self.cache.pop(key, None)
                self.misses += 1
                return None
            self.cache.move_to_end(key)
            self.hits += 1
            return entry.value
        
class FIFOCache(BaseCache):
    def __init__(self, max_cache_size: int, default_ttl: float):
        super().__init__(max_cache_size, default_ttl)

    def add(self, key: Any, value: Any) -> None:
        with self.lock:
            self._purge_expired()

            self.cache.pop(key, None)

            while len(self.cache) >= self.max_cache_size:
                self.cache.popitem()
            self.cache[key] = CacheEntry(value, self.default_ttl)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                self.cache.pop(key, None)
                self.misses += 1
                return None
            self.hits += 1
            return entry.value

class RandomCache(BaseCache):
    def __init__(self, max_cache_size: int, default_ttl: float):
        super().__init__(max_cache_size, default_ttl)

    def add(self, key: Any, value: Any) -> None:
        with self.lock:
            self._purge_expired()

            self.cache.pop(key, None)

            while len(self.cache) >= self.max_cache_size:
                random_key = random.choice(list(self.cache.keys()))
                self.cache.pop(random_key)
            self.cache[key] = CacheEntry(value, self.default_ttl)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                self.cache.pop(key, None)
                self.misses += 1
                return None
            self.hits += 1
            return entry.value
    

    
        