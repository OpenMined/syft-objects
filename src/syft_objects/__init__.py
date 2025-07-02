# syft-objects - Distributed file discovery and addressing system 

__version__ = "0.3.2"

# Core imports
from .models import SyftObject
from .factory import syobj
from .collections import ObjectsCollection
from .utils import scan_for_syft_objects, load_syft_objects_from_directory
from .client import check_syftbox_status, get_syft_objects_port, get_syft_objects_url
from .auto_install import ensure_syftbox_app_installed

# Create global objects collection instance
objects = ObjectsCollection()

# Export main classes and functions
__all__ = [
    "SyftObject", 
    "syobj", 
    "objects", 
    "ObjectsCollection",
    "scan_for_syft_objects",
    "load_syft_objects_from_directory",
    "get_syft_objects_port",
    "get_syft_objects_url"
]

# Check SyftBox status once during import
check_syftbox_status()

# Ensure syft-objects app is installed in SyftBox (if SyftBox is present)
ensure_syftbox_app_installed()
