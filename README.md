# 📦 Macho - Memory Adept Caching Operations

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI - 0.1.0](https://img.shields.io/badge/PyPI-coming--soon-yellow)](https://pypi.org/)

---

## What is Macho

Macho is a lightweigh, high-performance in-memory caching system designed with customizability at its core. Unlike heavyweight distributed caching systems (Redis & Memocached), Macho is entirely self-contained, running directly in your local Python environment without any external dependencies.
Macho enables Python developers to define and fine-tune how their cache behaves, offering powerful and flexible control over evictions, storage and general data life-cycle - all within a compact and memory-efficient infrastructure.

## Core Philosophy

Configuration first, Complexity never!
Macho was intentionally constructed for Python developers that desire full control over their caching operations without the overhead of an external server or complex delpoyment.

## ❓ Why use Macho Caching?

Macho currently aims to fill the gaps between built-in Python caching solutions and full-scale caching servers by offering:
* ✅ **In-memory speed** without any external server requirements.
* 🔧 **Full user configuration** over cache behavior and functionality.
* 🧩 **Modular design** for extensibility and experimentation
* 🐍 **Pure Python implementation**, great prototyping or ligthweight production services.

## ⚙️ Key Features

* ⚡ **Bloom Filter Suppoert**: Probabilistically reduce costly cache lookups and improve performance.
* 🔀 **Sharding**: Partition your cache into independent shards for better concurreny.
* 🔃 **Custom Eviction Strategies**: Currently supports **LRU**, **FIFO** and **Random** (More coming soon).
* ⏳ **Time-to-live (TTL)**: Configure per-cache expiration with automatic clean-up.
* 📊 **Metrics & Data**: Collect cache usage metrics and data for optimization and analysis.

**Macho is designed to provide Python developers with a lightweight in-memory alternative to major caching systems without compromising on individual customisation**

---

## 🔮 The Future of Macho
Here is a current roadmap for future versions:
* 🔁 Addtional probabilistic data structures (e.g., **XOR-filter**, **Cuckoo-filter**).
* 📈 New eviction policies (**LFU**, **MFU**)
* 🧰 CLI tooling for cache inspection and management.
* 📊 Advanced metrics and performance analysis.
* 🖥️ Improved Streamlit-based UI dashboard for data visualisation. 

## 🤝 Contribution
Macho is open to contributions from the Python community! If you'd like to report a bug, request features, or possibly contribute code, please feel free to open and issue or pull request!

## 📄 Licensing
The project is licensed under the MIT License.