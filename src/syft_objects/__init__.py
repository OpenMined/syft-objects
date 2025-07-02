# syft-objects - Distributed file discovery and addressing system 

__version__ = "0.3.4"

# Core imports
from .models import SyftObject
from .factory import syobj
from .collections import ObjectsCollection
from .utils import scan_for_syft_objects, load_syft_objects_from_directory
from .client import get_syft_objects_port, get_syft_objects_url

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

# Initialize SyftBox status and app installation lazily when needed
def _ensure_syftbox_ready():
    """Lazy initialization of SyftBox status - call this when actually needed"""
    from .client import check_syftbox_status, _print_startup_banner
    from .auto_install import ensure_syftbox_app_installed
    
    check_syftbox_status()
    ensure_syftbox_app_installed(silent=True)
    _print_startup_banner(only_if_needed=True)

# Only do basic initialization on import, heavy operations are done lazily
try:
    from .client import _initialize_syftbox
    _initialize_syftbox()  # This just sets up imports, no network calls
except Exception:
    pass  # Silently fail if there are issues
