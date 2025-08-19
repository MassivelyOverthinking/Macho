# --------------- Imports ---------------

import unittest
import time

from src.cache.models import FIFOCache
from src.cache.errors import MetricsLifespanException

# --------------- Test FIFOCache ---------------

class TestFIFOCache(unittest.TestCase):

    def test_initialization(self):
        cache = FIFOCache(5, 10.0)
        cache.add("a", 1)
        cache.add("b", 3)
        cache.add("c", 5)

        self.assertEqual(cache.max_cache_size, 5)
        self.assertEqual(cache.ttl, 10.0)
        self.assertEqual(cache.current_size, 3)

    def test_cache_get(self):
        cache = FIFOCache(5, 5.0)
        cache.add("a", 1)
        cache.add("b", 3)
        cache.add("c", 4)

        self.assertEqual(cache.get("b"), 3)

    def test_fifocache_expiration_purge(self):
        cache = FIFOCache(10, 5.0)
        cache.add("a", 1)
        cache.add("b", 1)
        cache.add("c", 1)
        time.sleep(5.0)
        cache.add("d", 1)
        cache.add("e", 1)

        self.assertEqual(cache.current_size, 2)

    def test_fifiocache_eviction(self):
        cache = FIFOCache(3, 5.0)
        cache.add("a", 1)
        cache.add("b", 1)
        cache.add("c", 1)
        cache.add("d", 1)
        cache.add("e", 1)

        self.assertIn("c", cache)
        self.assertIn("d", cache)
        self.assertIn("e", cache)
        self.assertNotIn("a", cache)
        self.assertNotIn("b", cache)


if __name__ == "__main__":
    unittest.main()