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

## Reference-Only Mode

**New in v0.3.5**: Keep files in their original location without copying to SyftBox.

```python
# Files stay in place (not copied to SyftBox)
obj = syo.syobj(
    name="Large Dataset",
    private_file="/path/to/my/large_dataset.csv",
    reference_only=True,  # 🔑 Key flag!
    metadata={"save_to": "dataset_metadata.syftobject.yaml"}
)

# Or via metadata
obj = syo.syobj(
    name="My Data",
    private_file="important_data.txt",
    metadata={"reference_only": True}
)
```

**Benefits:**
- ✅ Files stay in their original location
- ✅ No unnecessary copying or moving
- ✅ Perfect for large datasets or files you want to keep in place
- ✅ Still get all SyftObjects benefits (permissions, metadata, etc.)

## Installation

```bash
pip install syft-objects
```

For SyftBox integration:
```bash
pip install syft-objects[syftbox]
```

### 🚀 SyftBox Auto-Installation

When you import `syft-objects`, it automatically checks if you have SyftBox installed locally and sets up the syft-objects app for you:

```python
import syft_objects as syo  # Auto-installs to SyftBox if detected
```

**What happens automatically:**
- ✅ **Detects SyftBox**: Checks for `~/SyftBox/` directory
- ✅ **Verifies app**: Looks for existing `~/SyftBox/apps/syft-objects/`  
- ✅ **Auto-clones**: If missing, runs `git clone https://github.com/OpenMined/syft-objects.git`
- ✅ **Silent operation**: Only shows messages during installation
- ✅ **Graceful fallback**: Works fine without SyftBox too

**Requirements for auto-installation:**
- SyftBox installed locally (creates `~/SyftBox/` directory)
- Git available in your system PATH
- Internet connection for cloning

**Manual installation** (if needed):
```bash
cd ~/SyftBox/apps/
git clone https://github.com/OpenMined/syft-objects.git
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

## Syft Objects

A distributed file discovery and addressing system for SyftBox.

Syft Objects allows you to discover, share, and access data objects across the SyftBox network through a simple Python interface and web UI.

## Features

- **🔍 Object Discovery**: Automatically find and catalog distributed syft objects
- **🌐 Web Interface**: Modern, responsive UI for browsing and managing objects
- **🐍 Python API**: Simple and intuitive Python interface
- **🔒 Privacy-First**: Respects SyftBox privacy and permission models
- **⚡ Real-time**: Live updates and synchronization
- **📱 Mobile-Friendly**: Works seamlessly on all devices

## Web Interface

The syft-objects package includes a modern web UI for browsing and managing objects:

### Features
- **Browse Objects**: View all syft objects in a clean table format
- **Search & Filter**: Search by keywords and filter by email addresses
- **Object Details**: View detailed information including metadata, permissions, and file previews
- **Real-time Status**: Monitor SyftBox connection status
- **Refresh**: Manually refresh the objects collection

### Running the Web UI

Launch the integrated web interface using the provided script:

```bash
./run.sh
```

This will start a combined backend/frontend server. The UI will be available at `http://localhost:8003` (or the port specified by `SYFTBOX_ASSIGNED_PORT`).

### API Endpoints

The backend provides a REST API:
- `GET /api/status` - Get application and SyftBox status
- `GET /api/objects` - List objects with search/filter support
- `GET /api/objects/{uid}` - Get detailed object information  
- `GET /api/objects/refresh` - Refresh the objects collection
- `GET /api/metadata/emails` - Get unique email addresses

## Installation

### Option 1: Direct Installation

```bash
pip install syft-objects
```

### Option 2: Auto-Installation via SyftBox

If you have SyftBox installed, syft-objects will automatically install itself as a SyftBox app when you first import it:

```python
import syft_objects  # This triggers auto-installation if SyftBox is present
```

#### Auto-Installation Details

When you import syft-objects, it will:

1. **Check for SyftBox**: Detect if SyftBox is installed on your system
2. **Locate Apps Directory**: Find your `~/SyftBox/apps/` directory
3. **Auto-Clone**: Automatically clone the syft-objects repository if not present
4. **Graceful Fallback**: Work normally even if SyftBox is not available

**Requirements for Auto-Installation:**
- SyftBox must be installed and configured
- Git must be available in your system PATH
- Internet connection for cloning the repository

**Manual Installation (if auto-install fails):**
```bash
cd ~/SyftBox/apps/
git clone https://github.com/OpenMined/syft-objects.git
```

The auto-installation feature makes it seamless to get started with syft-objects in SyftBox environments while maintaining compatibility with standalone usage.

## Port Discovery

When syft-objects runs as a SyftBox app, it uses dynamic port assignment via the `SYFTBOX_ASSIGNED_PORT` environment variable. The system automatically:

1. **Port Assignment**: SyftBox assigns a port via `SYFTBOX_ASSIGNED_PORT` 
2. **Port Persistence**: The `run.sh` script saves the assigned port to a `.port` file
3. **Dynamic Discovery**: The Python API automatically discovers the port by checking:
   - Current working directory: `./.port`
   - SyftBox apps directory: `~/SyftBox/apps/syft-objects/.port`
   - Package directory: `<package_path>/.port`
4. **Fallback**: Uses port 8003 if no port file is found

This ensures the widget and API calls always connect to the correct server instance.

**Usage:**
```python
import syft_objects as syo

# Widget automatically uses the correct port
syo.objects.widget()  # Uses dynamic port discovery

# Manual port/URL access
port = syo.get_syft_objects_port()  # Get current port
url = syo.get_syft_objects_url("api/objects")  # Get API URL
```
