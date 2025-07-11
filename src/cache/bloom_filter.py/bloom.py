# --------------- Imports ---------------

import math
import hashlib

from bitarray import bitarray

# --------------- Bloom Filter Mechanism ---------------

class BloomFilter(object):
    def __init__(self, items_count, probability):
        pass

    @classmethod
    def get_size(self, n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)
    
    @classmethod
    def hash_count(self, m, n):
        k = (m/n) * math.log(2)
        return int(k)
