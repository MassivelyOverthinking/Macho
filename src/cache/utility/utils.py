# --------------- Imports ---------------

from typing import List, Optional, Union

from ..models.models import BaseCache, LRUCache, FIFOCache, RandomCache

# --------------- Utility Functions ---------------

cache_list = {
    "lru": LRUCache,
    "fifo": FIFOCache,
    "random": RandomCache
}

def check_cache_list(policy: str) -> BaseCache:
    if not isinstance(policy, str):
        raise TypeError(f"The Policy parameter must be of type: Str")
    
    policy = policy.casefold()

    if policy in cache_list:
        return cache_list[policy]
    else:
        raise ValueError(f"Eviction Strategy {policy} not supported")
    
    
# --------------- Cache Creation ---------------
    
def _create_single_cache(policy: str) -> BaseCache:
    cache_class = check_cache_list(policy=policy)
    return cache_class
    
def _create_sharded_cache(num: int, shards_capacity: List[int], policy: str) -> List[BaseCache]:
    shards_list = []

    cache_class = check_cache_list(policy=policy)

    for n in range(num):
        cap = shards_capacity[num]      # Pick the capacity num from list
        new_cache = cache_class(cap)    # Create new class instance with capacity
        shards_list.append(new_cache)   # Append new cache class to final list

    return shards_list

def create_cache(shards: int = 1, policy: str = "lru", shards_capacity: Optional[List[int]] = None) -> Union[BaseCache, List[BaseCache]]:
    if shards == 1:
        return _create_single_cache(policy=policy)
    else:
        if shards_capacity is None:
            raise ValueError("Must provide 'shards_capacity' when creating shared cache")
        return _create_sharded_cache(
            num=shards,
            shards_capacity=shards_capacity,
            policy=policy
        )
