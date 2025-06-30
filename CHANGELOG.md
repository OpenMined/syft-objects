# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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