"""Clean API wrapper for SyftObject to hide Pydantic complexity"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import warnings


class CleanSyftObject:
    """A clean API wrapper around SyftObject that exposes only essential functionality.
    
    This wrapper hides all the Pydantic internals and provides a simple, intuitive
    interface matching the HTML widget functionality.
    """
    
    def __init__(self, syft_object):
        """Initialize with a raw SyftObject instance"""
        self._obj = syft_object
    
    # === CORE PROPERTIES ===
    
    @property
    def name(self) -> str:
        """The object's name"""
        return self._obj.name
    
    @property
    def uid(self) -> str:
        """Unique identifier for this object"""
        return str(self._obj.uid)
    
    @property
    def description(self) -> str:
        """Human-readable description"""
        return self._obj.description or ""
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """User-defined metadata dictionary"""
        return self._obj.metadata or {}
    
    @metadata.setter
    def metadata(self, value: Dict[str, Any]):
        """Update metadata"""
        self._obj.metadata = value
        self._obj.save_yaml()
    
    @property
    def created_at(self) -> datetime:
        """When this object was created"""
        return self._obj.created_at
    
    @property
    def updated_at(self) -> Optional[datetime]:
        """When this object was last modified"""
        return self._obj.updated_at
    
    @property
    def type(self) -> str:
        """File type extension (e.g., '.txt', '.csv') or 'folder'"""
        if self._obj.is_folder:
            return "folder"
        return self._obj.file_type or "unknown"
    
    # === DATA ACCESS ===
    
    @property
    def mock(self):
        """Access mock data (public/shareable version).
        
        Returns a DataAccessor that supports:
        - Reading: obj.mock() or obj.mock.read()
        - Writing: obj.mock.write(data)
        - For DataFrames: obj.mock.df
        - For text: obj.mock.text
        """
        return self._obj.mock
    
    @property
    def private(self):
        """Access private data (sensitive version).
        
        Returns a DataAccessor that supports:
        - Reading: obj.private() or obj.private.read()
        - Writing: obj.private.write(data)
        - For DataFrames: obj.private.df
        - For text: obj.private.text
        """
        return self._obj.private
    
    # === PERMISSIONS ===
    
    @property
    def permissions(self) -> Dict[str, List[str]]:
        """Get all permissions in a simple dictionary format"""
        return {
            "discovery": list(self._obj.syftobject_permissions or []),
            "mock_read": list(self._obj.mock_permissions or []),
            "mock_write": list(self._obj.mock_write_permissions or []),
            "private_read": list(self._obj.private_permissions or []),
            "private_write": list(self._obj.private_write_permissions or [])
        }
    
    def set_permissions(self, **kwargs) -> None:
        """Update permissions for this object.
        
        Args:
            discovery: List of emails who can discover this object
            mock_read: List of emails who can read the mock
            mock_write: List of emails who can write the mock
            private_read: List of emails who can read the private data
            private_write: List of emails who can write the private data
            
        Example:
            obj.set_permissions(
                mock_read=["public"],
                mock_write=["alice@example.com"],
                private_read=["alice@example.com", "bob@example.com"]
            )
        """
        # Map friendly names to internal names
        mapping = {
            "discovery": "syftobject_permissions",
            "mock_read": "mock_permissions", 
            "mock_write": "mock_write_permissions",
            "private_read": "private_permissions",
            "private_write": "private_write_permissions"
        }
        
        # Convert and apply
        internal_kwargs = {}
        for key, value in kwargs.items():
            if key in mapping:
                internal_kwargs[mapping[key]] = value
            else:
                warnings.warn(f"Unknown permission type: {key}")
        
        if internal_kwargs:
            self._obj.set_permissions(**internal_kwargs)
    
    # === URLS & PATHS ===
    
    @property
    def urls(self) -> Dict[str, str]:
        """Get syft:// URLs for all components"""
        return {
            "mock": self._obj.mock_url,
            "private": self._obj.private_url,
            "metadata": self._obj.syftobject
        }
    
    @property
    def paths(self) -> Dict[str, Optional[str]]:
        """Get local filesystem paths for all components"""
        return {
            "mock": self._obj.mock_path,
            "private": self._obj.private_path,
            "metadata": self._obj.syftobject_path
        }
    
    # === ACTIONS ===
    
    def delete(self) -> bool:
        """Delete this object and all its files.
        
        Returns:
            bool: True if deletion was successful
        """
        return self._obj.delete()
    
    def save(self) -> None:
        """Save any changes to the metadata file"""
        self._obj.save_yaml()
    
    def info(self) -> Dict[str, Any]:
        """Get detailed information about this object (like Info button in UI)"""
        return {
            "name": self.name,
            "uid": self.uid,
            "description": self.description,
            "type": self.type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata,
            "permissions": self.permissions,
            "urls": self.urls,
            "paths": self.paths,
            "is_folder": self._obj.is_folder
        }
    
    # === DISPLAY ===
    
    def _repr_html_(self):
        """Jupyter notebook HTML representation"""
        return self._obj._repr_html_()
    
    def __repr__(self):
        """String representation"""
        return f"<SyftObject {self.name} ({self.uid[:8]}...)>"
    
    def __str__(self):
        """Human-readable string"""
        return f"SyftObject '{self.name}' ({self.type})"
    
    # === PRIVATE HELPER ===
    
    def _raw(self):
        """Access the underlying raw SyftObject (for advanced users only)"""
        warnings.warn(
            "Accessing raw SyftObject exposes internal Pydantic API. "
            "Consider using the clean API methods instead.",
            stacklevel=2
        )
        return self._obj


def wrap_syft_object(obj) -> CleanSyftObject:
    """Wrap a raw SyftObject in the clean API"""
    return CleanSyftObject(obj)