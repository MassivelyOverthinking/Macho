# --------------- Imports ---------------

from threading import RLock
from typing import Any

import time

# --------------- Global Cache ---------------

_global_cache_manager = pass

def get_global_cache():
    return _global_cache_manager

# --------------- Caching Models ---------------

class CacheEntry():
    __slots__ = ("Value", "ttl")

    def __init__(self, value: Any, ttl: float):
        self.Value = value
        self.ttl = time.time() + ttl

    def is_expired(self):
        if self.ttl < time.time():
            return True
        return False