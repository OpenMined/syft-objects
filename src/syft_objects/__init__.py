"""
SyftObjects - Distributed objects with mock/real pattern for file discovery and addressing.
"""

from .models import SyftObject
from .factory import syobj
from .clean_api import wrap_syft_object
from .collections import objects
from .client import get_syftbox_client, SyftBoxURL, SYFTBOX_AVAILABLE

__version__ = "0.10.38"

__all__ = [
    "SyftObject",
    "syobj",
    "wrap_syft_object",
    "objects",
    "get_syftbox_client",
    "SyftBoxURL",
    "SYFTBOX_AVAILABLE",
]
