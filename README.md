# 🔐 Syft Objects

**Share files with explicit mock vs private control**

[![PyPI version](https://badge.fury.io/py/syft-objects.svg)](https://badge.fury.io/py/syft-objects)

## Quick Start

```python
import syft_objects as syo

# Create an object with demo and real content
obj = syobj(
    name="AI Results",
    mock_contents="Model achieved good performance",
    private_contents="Accuracy: 94.5%, Cost: $127"
)

# Browse all your objects interactively
syo.objects

# Search for specific objects
syo.objects.search("financial")
```

## What It Does

**Mock vs Private Pattern**: Every object has two versions:
- **Mock**: What everyone sees (demo/sample)
- **Private**: What authorized users see (real data)

**Example**:
```python
obj = syobj(
    name="Customer Data",
    mock_contents="Sample: 100 customers, avg age 42",
    private_contents="Full: 47,293 customers, avg age 41.7, LTV $1,247"
)
```

## Interactive Object Browser

```python
# Browse all objects with search and selection
syo.objects

# Search by name, email, description, or metadata
syo.objects.search("financial")

# Filter by email
syo.objects.filter_by_email("andrew")

# Get specific objects
selected = [syo.objects[i] for i in [0, 1, 5]]
```

## Installation

```bash
pip install syft-objects
```

For SyftBox integration:
```bash
pip install syft-objects[syftbox]
```

## Key Features

- **One function**: `syobj()` - simple and clean
- **Explicit control**: You decide what goes in mock vs private
- **Beautiful display**: Rich HTML widgets in Jupyter
- **Interactive browsing**: Search and select objects easily
- **Unique filenames**: No collisions when creating objects with same name
- **Real-time updates**: New objects appear immediately

## License

Apache License 2.0
