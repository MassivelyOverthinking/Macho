# --------------- Imports ---------------

import unittest
import time

from src.cache.models import LRUCache
from src.cache.errors import MetricsLifespanException

# --------------- Test LRUCache ---------------

class TestLRUCache(unittest.TestCase):

    def test_initialization(self):
        cache = LRUCache(5, 10.0)
        cache.add("a", 1)
        cache.add("b", 3)
        cache.add("c", 5)

        self.assertEqual(cache.max_cache_size, 5)
        self.assertEqual(cache.ttl, 10.0)
        self.assertEqual(cache.current_size, 3)

    def test_cache_get(self):
        cache = LRUCache(5, 5.0)
        cache.add("a", 1)
        cache.add("b", 3)
        cache.add("c", 4)

        self.assertEqual(cache.get("b"), 3)

    def test_cache_expiration_purge(self):
        cache = LRUCache(10, 5.0)
        cache.add("a", 1)
        cache.add("b", 1)
        cache.add("c", 1)
        time.sleep(5.0)
        cache.add("d", 1)
        cache.add("e", 1)

        self.assertEqual(cache.current_size, 2)

    def test_lru_eviction(self):
        cache = LRUCache(3, 5.0)
        cache.add("a", 1)
        cache.add("b", 2)
        cache.add("c", 3)
        entry = cache.get("b")  # B is now in position 0
        cache.add("d", 4)
        cache.add("e", 5)
        entry2 = cache.get("b")
        cache.add("f", 6)

        self.assertIn("b", cache)
        self.assertIn("e", cache)
        self.assertIn("f", cache)
        self.assertNotIn("a", cache)
        self.assertNotIn("c", cache)
        self.assertNotIn("d", cache)

    def test_cache_clear(self):
        cache = LRUCache(10, 10.0)
        cache.add("a", 1)
        cache.add("b", 2)
        cache.add("c", 3)
        cache.add("d", 4)
        cache.add("e", 5)
        cache.clear()

        self.assertEqual(cache.current_size, 0)

    def test_lifespan_exception(self):
        cache = LRUCache(10, 10.0)

        with self.assertRaises(MetricsLifespanException):
            _ = cache.metric_lifespan

if __name__ == "__main__":
    unittest.main()
