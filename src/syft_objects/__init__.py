# syft-objects - Distributed file discovery and addressing system 

__version__ = "0.6.27"

# Internal imports (hidden from public API)
from . import models as _models
from . import data_accessor as _data_accessor
from . import factory as _factory
from . import collections as _collections
from . import utils as _utils
from . import client as _client
from . import auto_install as _auto_install
from . import permissions as _permissions
from . import file_ops as _file_ops
from . import display as _display

# Public API - only expose essential user-facing functionality
from .factory import syobj
from .collections import ObjectsCollection

# Create global objects collection instance
objects = ObjectsCollection()

# Create clearer API endpoints
def create_object(name=None, **kwargs):
    """Create a new SyftObject with explicit naming.
    
    This is an alias for syobj() with a clearer name.
    
    Args:
        name: Optional name for the object
        **kwargs: All the same arguments as syobj:
            - private_contents: String content for private file
            - mock_contents: String content for mock file
            - private_file: Path to private file
            - mock_file: Path to mock file
            - private_folder: Path to private folder
            - mock_folder: Path to mock folder
            - discovery_read: List of who can discover
            - mock_read: List of who can read mock
            - mock_write: List of who can write mock
            - private_read: List of who can read private
            - private_write: List of who can write private
            - metadata: Additional metadata dict
    
    Returns:
        SyftObject: The newly created object
    """
    return syobj(name, **kwargs)

def delete_object(identifier):
    """Delete a SyftObject by index or UID.
    
    Args:
        identifier: Either an integer index or string UID
        
    Returns:
        bool: True if deletion was successful, False otherwise
        
    Raises:
        IndexError: If index is out of range
        KeyError: If UID is not found
        TypeError: If identifier is not int or str
    """
    if isinstance(identifier, int):
        # Delete by index
        if 0 <= identifier < len(objects):
            obj = objects[identifier]
            result = obj.delete()
            if result:
                # Refresh the collection after successful deletion
                objects.refresh()
            return result
        else:
            raise IndexError(f"Index {identifier} out of range. Collection has {len(objects)} objects.")
    elif isinstance(identifier, str):
        # Delete by UID
        try:
            obj = objects[identifier]  # This uses the UID lookup
            result = obj.delete()
            if result:
                # Refresh the collection after successful deletion
                objects.refresh()
            return result
        except KeyError:
            raise KeyError(f"Object with UID '{identifier}' not found")
    else:
        raise TypeError(f"Identifier must be int (index) or str (UID), not {type(identifier).__name__}")

# Export the essential public API
__all__ = [
    "syobj",         # Original factory function (kept for compatibility)
    "create_object", # Clearer name for creating objects
    "delete_object", # Explicit deletion function
    "objects",       # Global collection instance
]

# Internal setup (hidden from user)
_client.check_syftbox_status()
_auto_install.ensure_syftbox_app_installed(silent=True)

# Import startup banner (hidden)
from .client import _print_startup_banner
_print_startup_banner(only_if_needed=True)

# Clean up namespace - remove any accidentally exposed internal modules
import sys
_current_module = sys.modules[__name__]
_internal_modules = ['models', 'data_accessor', 'factory', 'collections', 'utils', 
                     'client', 'auto_install', 'permissions', 'file_ops', 'display',
                     'ObjectsCollection', 'sys']  # Hide all internal modules and classes
for _attr_name in _internal_modules:
    if hasattr(_current_module, _attr_name):
        delattr(_current_module, _attr_name)

# Already defined above - remove this duplicate
# __all__ is defined earlier in the file
