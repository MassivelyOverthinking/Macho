# --------------- Imports ---------------

from typing import List, Optional, Union

from ..models import BaseCache, LRUCache, FIFOCache, RandomCache

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
    
def _create_single_cache(capacity_num: int, ttl: float, policy: str) -> BaseCache:
    cache_class = check_cache_list(policy=policy)
    return cache_class(max_cache_size=capacity_num, default_ttl=ttl)

    
def _create_sharded_cache(ttl: float, num: int, shards_capacity: List[int], policy: str) -> List[BaseCache]:
    shards_list = []

    cache_class = check_cache_list(policy=policy)

    for n in range(num):
        cap = shards_capacity[n]                                        # Pick the capacity num from list
        new_cache = cache_class(max_cache_size=cap, default_ttl=ttl)    # Create new class instance with capacity
        shards_list.append(new_cache)                                   # Append new cache class to final list

    return shards_list


def create_cache(
    max_capacity: int,
    ttl: float,
    shards: int, 
    policy: str,
    shards_capacity: Optional[List[int]] = None
    ) -> Union[BaseCache, List[BaseCache]]:
    if shards == 1:
        return _create_single_cache(
        capacity_num=max_capacity,
        ttl=ttl,
        policy=policy
        )
    else:
        if shards_capacity is None:
            raise ValueError("Must provide 'shards_capacity' when creating shared cache")
        return _create_sharded_cache(
            ttl=ttl,
            num=shards,
            shards_capacity=shards_capacity,
            policy=policy
        )
