# --------------- Imports ---------------


from typing import List
from cache.models.models import CacheEntry

# --------------- Main Application ---------------

class Cache():
    __slots__ = ("max_cache_size", "ttl" "shard_count", "evict_strat", "bloom", "probability")

    def __init__(
            self, max_cache_size: int = 100,
            ttl: float = 600.0,
            shard_count: int = 1,
            strategy: str = "lru",
            bloom: bool = False,
            probability: float = 0.5
        ):
        self.cache = []
        self.max_cache_size = max_cache_size
        self.ttl = ttl
        self.shard_count = shard_count
        self.strategy = strategy

    def add(self, entry: CacheEntry) -> None:
        if self.shard_count > 1:
            num = hash(entry) / self.shard_count
            self.cache[num].add(entry)
        else:
            self.cache[0].add(entry)

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