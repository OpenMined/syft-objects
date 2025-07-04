# Relative Path Support in Syft-Objects

Syft-objects now supports relative paths, making your data objects portable and easier to share. This feature allows you to create self-contained project directories that can be moved, copied, or shared without breaking file references.

## Overview

The relative path feature introduces:
- **Relative path fields** for all file references (private, mock, and metadata files)
- **Automatic base path detection** when loading objects
- **Multiple fallback strategies** for finding files if they've been moved
- **Backward compatibility** with existing absolute syft:// URLs

## How It Works

### Path Resolution Strategy

When resolving file paths, syft-objects tries multiple strategies in order:

1. **Relative Path** - If a base_path and relative URL are set, try this first
2. **Absolute syft:// URL** - The traditional absolute URL approach
3. **Absolute Fallback** - A stored absolute path for recovery
4. **Search Heuristics** - Smart searching in common locations

### Key Fields

New fields added to SyftObject:
- `base_path` - The base directory for resolving relative paths
- `private_url_relative` - Relative path to private file
- `mock_url_relative` - Relative path to mock file  
- `syftobject_relative` - Relative path to metadata file
- `*_absolute_fallback` - Absolute fallback paths for recovery

## Usage Examples

### Creating Objects with Relative Paths

```python
from syft_objects import syobj

# Create an object with relative paths enabled
dataset = syobj(
    "My Dataset",
    private_file="data/private/training.csv",
    mock_file="data/mock/training_mock.csv",
    metadata={
        "use_relative_paths": True,
        "base_path": ".",  # Current directory as base
        "save_to": "metadata/dataset.syftobject.yaml"
    }
)
```

### Loading Objects with Auto-Detection

```python
from syft_objects import SyftObject

# Load an object - base_path is auto-detected
obj = SyftObject.load_yaml("project/metadata/dataset.syftobject.yaml")

# The base_path is automatically set to the parent of the .syftobject.yaml file
print(obj.base_path)  # "project/metadata"
```

### Portable Project Structure

Recommended project structure for portability:

```
my_project/
├── data/
│   ├── private/
│   │   └── dataset.csv
│   └── public/
│       └── dataset_mock.csv
├── metadata/
│   └── dataset.syftobject.yaml
└── README.md
```

With relative paths, you can move the entire `my_project` directory anywhere and the objects will still work.

### Example .syftobject.yaml with Relative Paths

```yaml
base_path: ..  # Relative to the metadata directory
private_url: syft://user@example.com/private/dataset.csv
private_url_relative: ../data/private/dataset.csv
private_url_absolute_fallback: /home/user/projects/my_project/data/private/dataset.csv
mock_url: syft://user@example.com/public/dataset_mock.csv
mock_url_relative: ../data/public/dataset_mock.csv
mock_url_absolute_fallback: /home/user/projects/my_project/data/public/dataset_mock.csv
# ... other fields ...
```

## Benefits

1. **Portability** - Move or copy entire project directories without breaking references
2. **Collaboration** - Share projects with others who can use them immediately
3. **Version Control** - Check in projects with relative paths that work for everyone
4. **Flexibility** - Mix relative and absolute paths as needed
5. **Resilience** - Multiple fallback strategies ensure files can be found

## Migration Guide

### For New Objects

Simply add `use_relative_paths: True` to your metadata:

```python
obj = syobj(
    "Dataset",
    metadata={"use_relative_paths": True}
)
```

### For Existing Objects

Load and re-save with relative paths:

```python
# Load existing object
obj = SyftObject.load_yaml("dataset.syftobject.yaml")

# Re-save with relative paths
obj.save_yaml("dataset.syftobject.yaml", use_relative_paths=True)
```

## Advanced Features

### Custom Base Paths

You can specify custom base paths for complex project structures:

```python
obj = syobj(
    "Dataset",
    metadata={
        "use_relative_paths": True,
        "base_path": "../shared_data"  # Relative to current directory
    }
)
```

### Path Resolution Utilities

```python
from syft_objects.client import resolve_relative_path, find_syftobject_files

# Resolve a relative path
absolute = resolve_relative_path("base/dir", "../file.txt")

# Find all syft objects in a directory
objects = find_syftobject_files("my_project")
```

## Best Practices

1. **Use consistent project structures** - This makes relative paths predictable
2. **Keep related files together** - Store data files near their metadata
3. **Use descriptive paths** - Make relative paths self-documenting
4. **Test portability** - Verify objects work after moving directories
5. **Document base paths** - If using custom base paths, document them

## Backward Compatibility

The relative path feature is fully backward compatible:
- Existing objects without relative paths continue to work
- Absolute syft:// URLs are still supported and used as fallbacks
- You can mix relative and absolute paths in the same object
- The system automatically falls back to absolute paths if relative paths fail

## Troubleshooting

### Files Not Found
If files aren't found with relative paths:
1. Check that `base_path` is set correctly
2. Verify relative paths are correct relative to base_path
3. Look for typos in filenames
4. Use `obj._resolve_path('private_url')` to debug path resolution

### Path Resolution Order
To see how paths are resolved:
```python
# Check which path is actually being used
resolved = obj._resolve_path('private_url')
print(f"Resolved to: {resolved}")
```

### Updating Paths
If files have moved, update the relative paths:
```python
obj._update_relative_paths()  # Auto-update based on current locations
obj.save_yaml("updated.syftobject.yaml")
```