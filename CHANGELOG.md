# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-19

### Added
- **ObjectsCollection**: New interactive collection interface for browsing syft objects
- **Global `objects` variable**: Easy access to all available syft objects via `syo.objects`
- **Dynamic loading**: Objects collection automatically refreshes when accessed
- **Interactive HTML table**: Beautiful Jupyter interface with search, selection, and code generation
- **Unique filenames**: UID-based filenames prevent collisions when creating objects with same name
- **Horizontal scrolling**: Full URL display without truncation in the objects table
- **Silent operation**: Status messages only show during import, not on every access

### Changed
- **Improved table layout**: Better column widths with narrow checkbox/index columns
- **Enhanced user experience**: Copy-paste friendly URLs and better visual design
- **Automatic refresh**: New objects appear immediately without kernel restart

### Fixed
- **Filename collisions**: Objects with same name now create unique files
- **Caching issues**: Objects collection always shows current state
- **Status message spam**: Reduced verbose output during normal operation

### Technical Improvements
- **Lazy loading**: Objects loaded on-demand for better performance
- **Error handling**: Graceful handling of missing files and datasites
- **Memory efficiency**: Fresh data loading without unnecessary caching

## [0.1.0] - 2024-12-01

### Added
- Initial release of syft-objects
- SyftObject class with mock/private pattern
- syobj() function for creating objects
- YAML serialization and deserialization
- SyftBox integration for file management
- Permission system with granular access control
- HTML display for Jupyter notebooks 