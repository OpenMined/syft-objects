# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.18] - 2024-12-30

### Added
- **Enhanced Create Object API**: Added new parameters to `create_object()` function:
  - `move_files_to_syftbox`: Control whether files are copied/moved to SyftBox (default: False)
  - `mock_note`: Optional note explaining mock data differences
  - `suggest_mock_notes`: Whether to suggest mock notes (uses config if not specified)
- **File Management Options**: When `move_files_to_syftbox=True`, user files are copied and generated files are moved
- **Improved Documentation**: Enhanced docstring with detailed parameter explanations

### Changed
- **API Enhancement**: `create_object()` now accepts keyword-only parameters for better API clarity
- **Metadata Handling**: `move_files_to_syftbox` setting is automatically stored in object metadata

## [0.10.10] - 2024-12-30

### Fixed
- **CleanSyftObject AttributeError**: Fixed `'CleanSyftObject' object has no attribute 'name'` error in ObjectsCollection
- **HTML Display**: Fixed widget generation for CleanSyftObject instances in Jupyter notebooks
- **Backward Compatibility**: Maintained compatibility with both CleanSyftObject and regular SyftObject instances

### Technical
- Updated `_objects_data_json()` method to handle both CleanSyftObject and SyftObject instances
- Added proper attribute access methods for CleanSyftObject (using getters vs direct access)
- Fixed mock_path and private_path access for CleanSyftObject instances

## [0.3.2] - 2024-12-30

### Changed
- **🏗️ MAJOR REFACTORING**: Split monolithic 1857-line file into well-organized package modules
- **Better Architecture**: Restructured from single file to 9 focused modules:
  - `models.py` - SyftObject class and core models (232 lines)
  - `factory.py` - syobj() factory function (286 lines) 
  - `collections.py` - ObjectsCollection class (270 lines)
  - `display.py` - HTML rendering and rich display (315 lines)
  - `client.py` - SyftBox client utilities (81 lines)
  - `permissions.py` - Permission management integration (49 lines)
  - `file_ops.py` - File operations and URL generation (71 lines)
  - `utils.py` - Utility functions for scanning (52 lines)
  - `__init__.py` - Clean imports and exports (22 lines)

### Improved
- **Maintainability**: Logical separation of concerns
- **Readability**: Each module has single responsibility  
- **Testability**: Easier to test individual components
- **Extensibility**: Simpler to add new features
- **Debugging**: Faster to locate and fix issues
- **Collaboration**: Multiple developers can work on different modules

### Technical
- Preserved 100% API compatibility - no breaking changes
- Used TYPE_CHECKING for circular import prevention
- Proper module dependencies and clean interfaces
- Average module size reduced to ~140 lines (much more manageable)
- All existing functionality maintained

## [0.3.1] - 2024-12-19

### Changed
- **Dependency Update**: Now uses `syft-perm` package from PyPI instead of local permissions.py
- **Cleaner Architecture**: Removed duplicate permission management code
- **Better Modularity**: Permission utilities now maintained as separate package

### Removed
- Local `permissions.py` file (replaced by `syft-perm` dependency)

## [0.3.0] - 2024-12-19

### Added
- **Inline Content Display**: View file contents directly in Jupyter notebooks
  - "View Demo" and "View Real" buttons show content inline  
  - Smart truncation for long content (first 1000 characters)
  - Copy file path to clipboard functionality
  - Binary file detection and handling
  - Close button to hide content display
- **Enhanced Object Display**: Improved HTML rendering with interactive buttons
- **Better Error Handling**: Graceful handling of missing files and binary content
- **Tutorial Notebook**: Complete examples showing inline content display features

### Improved
- Object display now includes interactive content viewing
- Better file path handling and clipboard integration
- More robust content preview system
- Enhanced user experience in Jupyter environments

## [0.2.0] - 2024-12-19

### Added
- **Interactive Objects Collection**: Global `objects` variable for easy access
- **Real-time Discovery**: No caching - always shows fresh objects
- **Advanced Search**: Search across names, emails, descriptions, created/updated dates, and metadata
- **Rich HTML Table**: 10-column interactive table with horizontal scrolling
- **Multi-select Interface**: Checkboxes and code generation
- **Metadata Support**: Display and search custom metadata fields
- **Timestamp Fields**: Created and updated date tracking
- **Unique Filenames**: UID-based naming prevents collisions

### Improved
- Silent operation after import (no status message spam)
- Better table layout with fixed column widths
- Enhanced search functionality across all fields
- Improved user experience with responsive design

### Changed
- Removed caching behavior for real-time updates
- Status messages now only appear during import
- Table columns optimized for better space usage

## [0.1.0] - 2024-12-01

### Added
- Initial release of syft-objects
- SyftObject class with mock/private pattern
- syobj() function for creating objects
- YAML serialization and deserialization
- SyftBox integration for file management
- Permission system with granular access control
- HTML display for Jupyter notebooks 