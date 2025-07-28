# --------------- Imports ---------------

from threading import RLock
from typing import Any
from collections import OrderedDict
from typing import Optional, List

import time

# --------------- Main Application ---------------

class Cache():
    __slots__ = ("MAX_CACHE_SIZE", "TTL" "shard_count", "evict_strat")

    def __init__(self, MAX_CACHE_SIZE: int = 1, TTL: int = 600, shard_count: int = 1, evict_strat: str = "lru"):
        self.cache = []
        self.MAX_CACHE_SIZE = MAX_CACHE_SIZE
        self.TTL = TTL
        self.shard_count = shard_count
        self.evict_strat = evict_strat

    def _get_shard_size(self) -> List[int]:
        base = self.MAX_CACHE_SIZE // self.shard_count
        remainder = self.MAX_CACHE_SIZE % self.shard_count
        shards = []

        for i in range(self.shard_count):
            size = base + (1 if i < remainder else 0)
            shards.append(size)

        return shards
    
    def _create_caches(self) -> None:
        shard_size = self._get_shard_size()
        cache_list = []

        if self.evict_strat is "lru":
            for i in range(shard_size):
                cache_list.append(i)
        elif self.evict_strat is "fifo":
            for i in range(shard_size):
                cache_list.append(i)
        elif self.evict_strat is "random":
            for i in range(shard_size):
                cache_list.append(i)
        else:
            raise Exception
        
        return cache_list