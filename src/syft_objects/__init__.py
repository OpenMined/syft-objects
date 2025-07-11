"""
SyftObjects - Distributed objects with mock/real pattern for file discovery and addressing.
"""

# syft-objects - Distributed file discovery and addressing system 

__version__ = "0.10.47"

# Internal imports (hidden from public API)
from . import models as _models
from . import data_accessor as _data_accessor
from . import config as _config
from . import prompts as _prompts
from . import mock_analyzer as _mock_analyzer
from . import factory as _factory
from . import file_ops as _file_ops
from . import clean_api as _clean_api
from . import collections as _collections
from . import accessors as _accessors
from . import client as _client

# Import and ensure auto-install runs if needed
from . import auto_install as _auto_install

# Public API exports (after auto-install check)
from .models import SyftObject
from .factory import syobj, create_object
from .clean_api import CleanSyftObject
from .collections import ObjectsCollection  
from .client import get_syftbox_client

# Create the global objects instance
objects = _collections.ObjectsCollection()

__all__ = [
    "__version__",
    "syobj", 
    "create_object",
    "objects",
    "get_syftbox_client",
    "SyftObject",
    "CleanSyftObject",
    "ObjectsCollection"
]
