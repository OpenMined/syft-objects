# 🔐 Syft Objects

**Share files with explicit mock vs private control**

[![PyPI version](https://badge.fury.io/py/syft-objects.svg)](https://badge.fury.io/py/syft-objects)

## Quick Start

```python
import syft_objects as syo

# Create an object with demo and real content
obj = syo.syobj(
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
- **Mock**: What everyone sees (demo/sample data)
- **Private**: What authorized users see (real data)

**Example**:
```python
obj = syo.syobj(
    name="Customer Analysis", 
    mock_contents="Sample: 100 customers, avg age 42, 60% retention rate",
    private_contents="Full: 47,293 customers, avg age 41.7, 58.3% retention, avg LTV $1,247"
)
```

## Interactive Object Browser

The `syo.objects` collection provides a beautiful interactive interface:

```python
# Browse all objects with search and selection
syo.objects

# Search by name, email, description, or metadata
syo.objects.search("financial")
syo.objects.search("customer")

# Filter by email
syo.objects.filter_by_email("andrew")

# Get specific objects
selected = [syo.objects[i] for i in [0, 1, 5]]

# Refresh after creating new objects
syo.objects.refresh()
```

### Interactive Features

- **🔍 Real-time search** across names, emails, descriptions, and metadata
- **☑️ Multi-select** with checkboxes
- **📋 Code generation** - click "Generate Code" to get copy-paste Python
- **📊 10-column table** with all object details
- **🔄 Auto-refresh** - new objects appear immediately
- **📱 Responsive design** with horizontal scrolling

## Rich Object Display

Each object shows beautifully in Jupyter with:

- **📁 File information** with availability status
- **🎯 Permission levels** with color-coded badges  
- **📋 Metadata** including creation/update times
- **🖱️ Interactive buttons** to view content inline
- **📄 Smart truncation** for long content (first 1000 chars)

## Permission Control

```python
obj = syo.syobj(
    name="Financial Report",
    mock_contents="Q4 Summary: Revenue up 10%", 
    private_contents="Q4: $2.5M revenue, $400K profit, 23.7% margin",
    discovery_read=["public"],           # Who knows it exists
    mock_read=["employee@company.com"],  # Who sees demo
    private_read=["cfo@company.com"]     # Who sees real data
)
```

## File-Based Objects

```python
# Use existing files
obj = syo.syobj(
    name="Dataset Analysis",
    mock_file="sample_100_rows.csv",      # Demo file
    private_file="full_50k_rows.csv"      # Real file  
)
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

- **🎯 One function**: `syo.syobj()` - simple and clean
- **🔒 Explicit control**: You decide what goes in mock vs private
- **🎨 Beautiful display**: Rich HTML widgets in Jupyter
- **🔍 Interactive browsing**: Search and select objects easily  
- **🆔 Unique filenames**: No collisions with UID-based naming
- **⚡ Real-time updates**: New objects appear immediately
- **📊 Comprehensive table**: 10 columns with all object details
- **🖱️ Inline content**: View file contents directly in notebook
- **🎯 Permission system**: Fine-grained access control

## Quick Reference

```python
import syft_objects as syo

# Create objects
obj = syo.syobj(name="My Data", mock_contents="Demo", private_contents="Real")

# Browse interactively
syo.objects                    # Show interactive table
syo.objects[0]                 # Get first object  
syo.objects[:3]                # Get first 3 objects
len(syo.objects)               # Count objects

# Search and filter
syo.objects.search("keyword")           # Search everywhere
syo.objects.filter_by_email("user")    # Filter by email
syo.objects.get_by_indices([0,1,5])    # Get specific objects

# Utilities
syo.objects.list_unique_emails()       # List all emails
syo.objects.refresh()                  # Refresh collection
```

## License

Apache License 2.0
