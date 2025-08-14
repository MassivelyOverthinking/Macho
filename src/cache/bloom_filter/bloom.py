# --------------- Imports ---------------

import math
import mmh3

from bitarray import bitarray
from typing import Any

# --------------- Bloom Filter Mechanism ---------------

class BloomFilter(object):
    def __init__(self, items_count, probability):
        self.probability = probability
        self.size = self.get_size(items_count, probability)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, item: Any) -> None:
        for i in range(self.hash_count):
            digest = self._hash(item, i) % self.size

            self.bit_array[digest] = True

    def check(self, item: Any) -> None:
        for i in range(self.hash_count):
            digest = self._hash(item, i) % self.size
            if not self.bit_array[digest]:
                return False
        return True
    
    def _hash(self, item: Any, seed: Any) -> int:
        return mmh3.hash(item, seed)

    @staticmethod
    def get_size(n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)
    
    @staticmethod
    def get_hash_count(m, n):
        k = (m/n) * math.log(2)
        return int(k)
