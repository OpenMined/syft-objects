# syft-objects - Distributed file discovery and addressing system 

__version__ = "0.6.26"

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

# Export only the essential public API
__all__ = [
    "syobj",     # Factory function for creating objects
    "objects",   # Global collection instance
]

# Internal setup (hidden from user)
_client.check_syftbox_status()
_auto_install.ensure_syftbox_app_installed(silent=True)

# Import startup banner (hidden)
from .client import _print_startup_banner
_print_startup_banner(only_if_needed=True)
