# --------------- Imports ---------------


from typing import List, Union

from .models.models import BaseCache
from .utility.utils import create_cache

# --------------- Main Application ---------------

class Cache():
    __slots__ = ("max_cache_size", "ttl" "shard_count", "strategy", "bloom", "probability")

    def __init__(
            self, 
            max_cache_size: int = 100,
            ttl: float = 600.0,
            shard_count: int = 1,
            strategy: str = "lru",
            bloom: bool = False,
            probability: float = 0.5
        ):
        self.cache = self._create_caches()
        self.max_cache_size = max_cache_size
        self.ttl = ttl
        self.shard_count = shard_count
        self.strategy = strategy
        self.bloom = bloom
        self.probability = probability

    def add(self, entry: any) -> None:
        if self.shard_count > 1:
            num = hash(entry) / self.shard_count
            self.cache[num].add(value=entry)
        else:
            self.cache.add(value=entry)

    def _get_shard_size(self) -> List[int]:
        base = self.max_cache_size // self.shard_count
        remainder = self.max_cache_size % self.shard_count
        shards = []

        for i in range(self.shard_count):
            size = base + (1 if i < remainder else 0)
            shards.append(size)

        return shards
    
    def _create_caches(self) -> Union[BaseCache, List[BaseCache]]:
        if self.shard_count == 1:
            shard_size = None
        else:
            shard_size = self._get_shard_size()
        
        return create_cache(
            max_capacity=self.max_cache_size,
            ttl=self.ttl,
            shards=self.shard_count,
            policy=self.strategy,
            shards_capacity=shard_size
        )