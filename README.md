# 🔐 Syft Objects

**Distributed file discovery and addressing with granular permission control**

[![PyPI version](https://badge.fury.io/py/syft-objects.svg)](https://badge.fury.io/py/syft-objects)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## ✨ What is Syft Objects?

Syft Objects is a **distributed file discovery system** that lets you share files with **explicit mock vs private content control** and **granular permission management**. Perfect for data science, research, and any scenario where you need to share different versions of files with different people.

```python
from syft_objects import syobj

# Create an object with explicit mock vs private content
obj = syobj(
    name="Customer Analysis",
    mock_contents="Sample: 100 customers, avg age 42",
    private_contents="Full: 47,293 customers, avg age 41.7, LTV $1,247",
    discovery_read=["public"],           # Who knows it exists
    mock_read=["team@company.com"],      # Who sees demo
    private_read=["admin@company.com"]   # Who sees real data
)

# Beautiful HTML display in Jupyter
obj
```

## 🚀 Key Features

### 🎯 **Explicit Content Control**
- **Mock content**: What everyone sees (demo version)
- **Private content**: What authorized users see (real data)
- **No magic**: You control exactly what goes where

### 🔒 **Granular Permissions**
- **Discovery**: Who knows the object exists
- **Mock**: Who can read/write demo content
- **Private**: Who can read/write real data

### 📱 **Beautiful Jupyter Display**
- Rich HTML widgets with permission badges
- File path display for all three file types
- Clean, organized layout
- No external dependencies

### 🌐 **Distributed by Design**
- Works across many locations (not centralized)
- SyftBox integration for proper distributed storage
- Lightweight for search and discovery

## 📦 Installation

```bash
pip install syft-objects
```

**For SyftBox integration:**
```bash
pip install syft-objects[syftbox]
```

## 🎯 Quick Start

### Basic Usage

```python
from syft_objects import syobj

# Simple content sharing
obj = syobj(
    name="AI Model Results",
    mock_contents="Model achieved good performance",
    private_contents="Accuracy: 94.5%, F1: 0.92, Cost: $127"
)
```

### File-Based Sharing

```python
# Use existing files
obj = syobj(
    name="Customer Database",
    mock_file="sample_100_rows.csv",      # Demo file
    private_file="full_50k_rows.csv",     # Real dataset
    mock_read=["analyst@company.com"],
    private_read=["admin@company.com"]
)
```

### Restricted Discovery

```python
# Control who even knows it exists
obj = syobj(
    name="Confidential Report",
    mock_contents="Q4 summary available",
    private_contents="Revenue: $2.5M, detailed breakdown...",
    discovery_read=["director@company.com"],  # Only director knows it exists
    mock_read=["manager@company.com"],        # Manager sees summary
    private_read=["ceo@company.com"]          # CEO sees details
)
```

## 📚 Documentation

- **[Quick Start Guide](https://openmined.github.io/syft-objects/quickstart/)** - Get up and running in 5 minutes
- **[Tutorial Notebook](https://openmined.github.io/syft-objects/tutorial/)** - Interactive Jupyter tutorial
- **[API Reference](https://openmined.github.io/syft-objects/api/)** - Complete function documentation
- **[SyftBox Integration](https://openmined.github.io/syft-objects/syftbox/)** - Distributed storage setup

## 🎨 Design Philosophy

### Ultra-Clean API
- **One function**: `syobj()` - that's it
- **Clear parameters**: `mock_contents` vs `private_contents`
- **Explicit permissions**: `discovery_read`, `mock_read`, `private_read`

### No Surprises
- You specify exactly what goes in mock vs private
- No auto-generation or magic content creation
- Full control over permissions and access

### Jupyter-First
- Beautiful HTML widgets out of the box
- File paths displayed clearly
- Permission badges for easy understanding

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[SyftBox](https://github.com/OpenMined/syftbox)** - Distributed storage backend
- **[Syft](https://github.com/OpenMined/PySyft)** - Privacy-preserving machine learning
- **[OpenMined](https://www.openmined.org/)** - Privacy-preserving AI ecosystem

---

<div align="center">
<strong>Built with ❤️ by <a href="https://www.openmined.org/">OpenMined</a></strong>
</div>
