# --------------- Imports ---------------

from typing import Any

# --------------- Custom Exceptions ---------------

class BloomFilterException(Exception):
    """
    Error raised when value not present in Bloom Filter.
    """
    def __init__(self, key: Any):
        super().__init__(f"Key: {key} is propably not present (filtered by Bloom Filter)")
        self.key = key