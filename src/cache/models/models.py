# --------------- Imports ---------------

from threading import RLock
from typing import Any
from collections import OrderedDict
from typing import Optional

import time

# --------------- Caching Models ---------------

class CacheEntry():
    __slots__ = ("value", "expiry")

    def __init__(self, value: Any, ttl: float):
        self.value = value
        self.expiry = time.time() + ttl

    def is_expired(self) -> bool:
        return time.time() > self.expiry
    
class BaseCache():
    __slots__ = ("MAX_CACHE_SIZE", "DEFAULT_TTL", "cache", "lock")

    def __init__(self, MAX_CACHE_SIZE: int = 64, DEFAULT_TTL: float = 600.0):
        self.MAX_CACHE_SIZE = MAX_CACHE_SIZE
        self.DEFAULT_TTL = DEFAULT_TTL
        self.cache: OrderedDict[Any, CacheEntry] = OrderedDict()
        self.lock = RLock()

    def _purge_expired(self) -> None:
        for key in list(self.cache.keys()):
            if self.cache[key].is_expired():
                del self.cache[key]
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()

    @property
    def capacity(self) -> int:
        return len(self.cache)
    
    @property
    def size(self) -> int:
        return self.MAX_CACHE_SIZE
    
    @property
    def ttl(self) -> int:
        return self.DEFAULT_TTL
    
class LRUCache(BaseCache):
    def __init__(self, MAX_CACHE_SIZE = 64, DEFAULT_TTL = 600):
        super().__init__(MAX_CACHE_SIZE, DEFAULT_TTL)

    def add(self, key: Any, value: Any) -> None:
        with self.lock:
            self._purge_expired

            self.cache.pop(key, None)

            while len(self.cache) >= self.MAX_CACHE_SIZE:
                self.cache.popitem(last=False)
            self.cache[key] = CacheEntry(value, self.DEFAULT_TTL)

    def get(self, key: Any) -> Optional[CacheEntry]:
        with self.lock:
            entry = self.cache.get(key)
            if entry is None or entry.is_expired():
                self.cache.pop(key, None)
                return None
            self.cache.move_to_end(key)
            return entry.value

    
        