# --------------- Imports ---------------

from threading import RLock
from typing import Any
from collections import OrderedDict
from typing import Optional, List

import time

# --------------- Main Application ---------------

class Cache():
    __slots__ = ("max_cache_size", "ttl" "shard_count", "evict_strat", "bloom")

    def __init__(
            self, max_cache_size: int = 100,
            ttl: float = 600.0,
            shard_count: int = 1,
            strategy: str = "lru",
            bloom: bool = False
        ):
        self.cache = []
        self.max_cache_size = max_cache_size
        self.ttl = ttl
        self.shard_count = shard_count
        self.strategy = strategy
        self.bloom = bloom

    def _get_shard_size(self) -> List[int]:
        base = self.max_cache_size // self.shard_count
        remainder = self.max_cache_size % self.shard_count
        shards = []

        for i in range(self.shard_count):
            size = base + (1 if i < remainder else 0)
            shards.append(size)

        return shards
    
    def _create_caches(self) -> None:
        shard_size = self._get_shard_size()
        cache_list = []
        
        return cache_list