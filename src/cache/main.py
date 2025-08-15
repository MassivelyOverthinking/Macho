# --------------- Imports ---------------


from typing import List, Union, Any, Optional

from .models import BaseCache
from .utility import create_cache, hash_value
from .bloom_filter import BloomFilter
from .errors import BloomFilterException

# --------------- Main Application ---------------

class Cache():
    __slots__ = ("max_cache_size", "ttl", "shard_count", "strategy", "bloom", "probability")

    def __init__(
            self, 
            max_cache_size: int = 100,
            ttl: float = 600.0,
            shard_count: int = 1,
            strategy: str = "lru",
            bloom: bool = False,
            probability: float = 0.5
        ):

        if not isinstance(max_cache_size, int):
            raise TypeError("Parameter 'max_cache_size' must be of type: int")
        if not isinstance(ttl, float):
            raise TypeError("Parameter 'ttl' must be of type: float")
        if not isinstance(shard_count, int):
            raise TypeError("Parameter 'shard_count' must be of type: int")
        if not shard_count > 0:
            raise ValueError("Shard count value must be positive")
        if not isinstance(strategy, str):
            raise TypeError("Parameter 'strategy' must be of type: str")
        if not isinstance(bloom, bool):
            raise TypeError("Parameter 'bloom' must be of type: bool")
        if not isinstance(probability, float):
            raise TypeError("Parameter 'probability' must be of type: float")
        if not 0.00 < probability < 1.00:
            raise ValueError("Probability value must be between 0.00 - 1.00")

        self.max_cache_size = max_cache_size
        self.ttl = ttl
        self.shard_count = shard_count
        self.strategy = strategy
        self.bloom = bloom
        self.probability = probability

        if self.bloom and self.shard_count > 1:
            shard_sizes = self._get_shard_size()
            self.bloom_filter = [BloomFilter(size, self.probability) for size in shard_sizes]
        elif self.bloom and self.shard_count == 1:
            self.bloom_filter = BloomFilter(self.max_cache_size, self.probability)
        else:
            self.bloom_filter = None

        self.cache = self._create_caches()

    def add(self, key: Any, entry: Any) -> None:
        if self.shard_count > 1:
            num = hash_value(key, self.shard_count)
            if self.bloom_filter:
                self.bloom_filter[num].add(key)
            self.cache[num].add(key=key, value=entry)
        else:
            if self.bloom_filter:
                self.bloom_filter.add(key)
            self.cache.add(key=key, value=entry)

    def get(self, key: Any) -> Optional[Any]:
        if self.shard_count > 1:
            num = hash_value(key, self.shard_count)
            if self.bloom_filter and not self.bloom_filter[num].check(key):
                raise BloomFilterException(key=key)
            return self.cache[num].get(key)
        else:
            if self.bloom_filter and not self.bloom_filter.check(key):
                raise BloomFilterException(key=key)
            return self.cache.get(key)
        
    def clear(self) -> None:
        if isinstance(self.cache, list):
            for shard in self.cache:
                shard.clear()
        else:
            self.cache.clear()

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
    
    def __repr__(self):
        return (f"<Cache(size={self.max_cache_size}, ttl={self.ttl}, eviction strategy={self.strategy})>")