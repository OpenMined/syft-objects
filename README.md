# 🔐 Syft Objects

**Share files with explicit mock vs private control**

[![PyPI version](https://badge.fury.io/py/syft-objects.svg)](https://badge.fury.io/py/syft-objects)

## 🚀 Quick Start

```python
from syft_objects import create_object

# Create an object with demo and real content
obj = create_object(
    name="AI Results",
    mock_contents="Model achieved good performance",
    private_contents="Accuracy: 94.5%, Cost: $127"
)

# Display the object in Jupyter with interactive buttons
obj  # Shows rich HTML display with View Demo/Real buttons
```

## 🎯 What It Does

**Mock vs Private Pattern**: Every object has two versions:
- **Mock**: What everyone sees (demo/sample data)
- **Private**: What authorized users see (real data)

### Example Use Case

```python
from syft_objects import create_object

# Share customer analysis with different levels of detail
analysis = create_object(
    name="Customer Analysis", 
    mock_contents="Sample: 100 customers, avg age 42, 60% retention rate",
    private_contents="Full: 47,293 customers, avg age 41.7, 58.3% retention, avg LTV $1,247",
    
    # Permission control
    discovery_read=["public"],           # Who knows it exists
    mock_read=["employee@company.com"],  # Who sees demo
    private_read=["cfo@company.com"]     # Who sees real data
)

# In Jupyter, this shows a beautiful widget with:
# - File availability status
# - Permission badges (discovery, mock, private)
# - Interactive buttons to view content inline
# - Copy file path functionality
analysis
```

## 📊 Interactive Display Features

When displayed in Jupyter, objects show a rich HTML widget with:

### 🖱️ Interactive Buttons
- **View Demo** → Shows mock content inline (first 1000 chars)
- **View Real** → Shows private content inline  
- **📋 Copy** → Copies file path to clipboard
- **✕ Close** → Hides content display

### 📄 Smart Content Handling
- Automatic truncation for content over 1000 characters
- Binary file detection with appropriate messaging
- Error handling for missing files
- No external file viewers needed

### 🎨 Rich Metadata Display
- Color-coded permission badges
- Creation and update timestamps
- File type and owner information
- Beautiful responsive design

## 🔒 Permission Control

```python
# Fine-grained access control
report = create_object(
    name="Financial Report",
    mock_contents="Q4 Summary: Revenue up 10%", 
    private_contents="Q4: $2.5M revenue, $400K profit, 23.7% margin",
    
    # Control who can discover, view mock, and view private
    discovery_read=["public"],                    # Everyone can know it exists
    mock_read=["employee@company.com"],           # Employees see summary
    mock_write=["manager@company.com"],           # Managers can edit mock
    private_read=["cfo@company.com"],             # CFO sees real numbers
    private_write=["cfo@company.com", "ceo@company.com"]  # C-suite can edit
)
```

## 📁 File-Based Objects

```python
# Use existing files instead of inline content
dataset = create_object(
    name="Dataset Analysis",
    mock_file="sample_100_rows.csv",      # Demo file path
    private_file="full_50k_rows.csv",     # Real file path
    discovery_read=["public"]
)

# Supports both files and folders
model = create_object(
    name="ML Model",
    mock_file="demo_model/",              # Demo folder
    private_file="production_model/",     # Production folder
    mock_note="This is a simplified model for demonstration"
)
```

## 🌐 Web Interface

Access your objects through a modern web UI:

```bash
# Start the web server
./run.sh
```

Visit `http://localhost:8004` to:
- Browse all objects in a searchable table
- View detailed object information
- Edit files with syntax highlighting
- Manage permissions interactively

### API Endpoints

- `GET /api/objects` - List all objects with search/filter
- `GET /api/object/{uid}` - Get object details
- `GET /api/object/{uid}/view` - View object in web UI
- `PUT /api/object/{uid}/metadata` - Update object metadata
- `PUT /api/objects/{uid}/permissions` - Update permissions
- `DELETE /api/objects/{uid}` - Delete an object

## 📦 Installation

```bash
pip install syft-objects
```

For SyftBox integration:
```bash
pip install syft-objects[syftbox]
```

### 🤖 SyftBox Auto-Installation

When you import `syft_objects`, it automatically sets up the SyftBox app if SyftBox is installed:

```python
import syft_objects  # Auto-installs to ~/SyftBox/apps/ if needed
```

## 🛠️ Advanced Features

### Mock Notes

Add context about what makes mock data different:

```python
obj = create_object(
    name="Sales Data",
    mock_contents="Sample sales data from 2023",
    private_contents="Complete sales records 2020-2024",
    mock_note="Mock data includes only public transactions with anonymized customer IDs"
)
```

### Metadata

Attach custom metadata:

```python
obj = create_object(
    name="Research Results",
    mock_contents="Summary findings...",
    private_contents="Detailed analysis...",
    metadata={
        "experiment_id": "EXP-2024-001",
        "department": "R&D",
        "classification": "confidential"
    }
)
```

### Programmatic Access

```python
from syft_objects import Client

# Create a client to interact with objects
client = Client()

# List all objects
objects = client.list_objects()

# Search objects
results = client.search_objects(query="financial")

# Get specific object
obj = client.get_object("object-uid-here")

# Update permissions programmatically
client.update_permissions(
    uid="object-uid-here",
    mock_read=["new-user@company.com"]
)
```

## 🎨 Widget Customization

The Jupyter widget display includes:
- **Permission badges** with color coding
- **File status** indicators (available/not found)
- **Inline content** viewing up to 1000 characters
- **Copy functionality** for file paths
- **Responsive design** for different screen sizes

## 🔑 Key Features Summary

- **🎯 Simple API**: One main function - `create_object()`
- **🔒 Explicit control**: Clear mock vs private separation
- **🎨 Beautiful display**: Rich HTML widgets in Jupyter
- **🖱️ Interactive**: View content inline, copy paths
- **📊 Smart truncation**: Handles long content gracefully
- **🌐 Web UI**: Full-featured web interface
- **🔍 Search**: Find objects by name, metadata, or content
- **⚡ Real-time**: Updates reflected immediately
- **🎯 Permissions**: Fine-grained access control
- **📁 Flexible**: Support for files, folders, and inline content

## License

Apache License 2.0