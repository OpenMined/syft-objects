# syft-objects - Distributed file discovery and addressing system 

__version__ = "0.3.8"

# Core imports
from .models import SyftObject
from .data_accessor import DataAccessor
from .factory import syobj
from .collections import ObjectsCollection
from .utils import scan_for_syft_objects, load_syft_objects_from_directory
from .client import check_syftbox_status, get_syft_objects_port, get_syft_objects_url
from .auto_install import ensure_syftbox_app_installed
from .backed import SingleSyftObjBacked, MultiSyftObjBacked

# Create global objects collection instance
objects = ObjectsCollection()

# Export main classes and functions
__all__ = [
    "SyftObject", 
    "DataAccessor",
    "syobj", 
    "objects", 
    "ObjectsCollection",
    "scan_for_syft_objects",
    "load_syft_objects_from_directory",
    "get_syft_objects_port",
    "get_syft_objects_url",
    "SingleSyftObjBacked",
    "MultiSyftObjBacked"
]

# Check SyftBox status - only show banner if there are issues or delays
check_syftbox_status()

# Ensure app is installed and server is healthy
# This will auto-install if needed and attempt to start the server
try:
    from .auto_install import ensure_server_healthy
    ensure_server_healthy(timeout_minutes=0.5)  # Quick check on import
except Exception:
    # Don't fail import if server check fails
    pass

# Import _print_startup_banner here to avoid circular imports
from .client import _print_startup_banner
_print_startup_banner(only_if_needed=True)
