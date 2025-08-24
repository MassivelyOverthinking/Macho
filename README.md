# 📦 Macho - Memory Adept Caching Operations

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI - 0.1.0](https://img.shields.io/badge/PyPI-coming--soon-yellow)](https://pypi.org/)

---

## What is Macho

Macho functions as a completely self-contained in-memory caching system with extensive configurable functionality.

Amongst other configurable features, Macho offers user-defined eviction strategies: 'LRU', 'FIFO', 'Random' that handles cache entry evictions.

Stash is a '__slots__'-based Python class-decorator developed to assist Python developers in 
significantly reducing memory overhead when initiating individual classes. It dynamically creates a new optimised class with necessary dunder-methods behind the scene (__init__, __repr__, __eq__), and also adds user-specified methods to ensure custom functionality. The application also supports immutability through 'Freeze' parameter, disabling user's ability to set attribute values post-initialisation for better memory efficiency.

## ❓ Why use Macho Caching?

Unlike current major caching frameworks/libs (Redis) Macho is contained entirely in-memory and therefore requires no external use of internet connectivity for functionality. Additionally, Macho focuses exclusively on developer configuration, allowing users to customize caching operations to suit individual needs and specific situations. These features are:

* ⚡ **Bloom Filter**: A probabilistic data structure to significantly reduce cache membership checks.
* 🚀 **Sharding**: Splits the current cache into multiple 'shards' to help balance large entry loads.
* 🔐 **Eviction Strategies**: User-defined strategies for entry evictions: 'LRU', 'FIFO', 'Random'.
* 🧼 **Time-to-live**: Specify the exact time-interval individual entries exist in memory.s

**Stash is designed to help you write lean, efficient and Pythonic code**

## 📋 Key Features
* 🎁 Simple-to-use Python class decorator for memory optimisation.
* 🛠️ Dynamically creates __slots__-based classes to minimize memory overhead.
* ⚗️ Adds essential dunder methods (__init__, __repr__, __eq__).
* 🔄 Allows user to specify class-methods to preserve and inherit.
* ❄️ Supports attribute Freeze-functionality (_frozen) for increased memory efficiency.
* 📊 Retains original class metadata for analysis, debugging and introspection.

---

## ❓ The Future of Macho
* Addtional support for probabilistic data structures (XOR-filter, Cuckoo-filter).
* New eviction strategies (LFU, MFU)
* CLI support
* Expansion on current caching metrics for better optimization and analysis.
* Improved Streamlit UI for better visualisation. 