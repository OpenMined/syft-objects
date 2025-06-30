# syft-objects - Distributed file discovery and addressing system 

__version__ = "0.3.2"

# Core imports
from .models import SyftObject
from .factory import syobj
from .collections import ObjectsCollection
from .utils import scan_for_syft_objects, load_syft_objects_from_directory
from .client import check_syftbox_status

# Create global objects collection instance
objects = ObjectsCollection()

# Export main classes and functions
__all__ = [
    "SyftObject", 
    "syobj", 
    "objects", 
    "ObjectsCollection",
    "scan_for_syft_objects",
    "load_syft_objects_from_directory"
]

# Check SyftBox status once during import
check_syftbox_status()
