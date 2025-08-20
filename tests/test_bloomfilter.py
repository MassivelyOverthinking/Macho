# --------------- Imports ---------------

import unittest
import time

from src.cache.bloom_filter import BloomFilter

# --------------- Test BloomFilter ---------------

class TestBloomFilter(unittest.TestCase):

    def test_bloomfilter_hash_consistency(self):
        item = "consistent_hash"
        bloom = BloomFilter(10, 0.5)
        hash1 = bloom._hash(item, 0)
        hash2 = bloom._hash(item, 0)

        self.assertEqual(hash1, hash2)