"""
Enhanced accessor classes for syft objects - provides structured access to mock, private, and syftobject config data
"""

from pathlib import Path
from typing import Any, Union, BinaryIO, TextIO, List
from .data_accessor import DataAccessor


class MockAccessor(DataAccessor):
    """Accessor for mock data with permission management methods."""
    
    def __init__(self, syft_url: str, syft_object: 'SyftObject'):
        super().__init__(syft_url, syft_object)
    
    def get_path(self) -> str:
        """Get the local file path for mock data"""
        return self.path
    
    def get_url(self) -> str:
        """Get the syft:// URL for mock data"""
        return self.url
    
    def get_permissions(self) -> List[str]:
        """Get read permissions for mock data"""
        return self._syft_object.mock_permissions
    
    def get_write_permissions(self) -> List[str]:
        """Get write permissions for mock data"""
        return self._syft_object.mock_write_permissions
    
    def set_permissions(self, read: List[str] = None, write: List[str] = None) -> None:
        """Set permissions for mock data"""
        self._syft_object.set_permissions("mock", read=read, write=write)


class PrivateAccessor(DataAccessor):
    """Accessor for private data with permission management methods."""
    
    def __init__(self, syft_url: str, syft_object: 'SyftObject'):
        super().__init__(syft_url, syft_object)
    
    def get_path(self) -> str:
        """Get the local file path for private data"""
        return self.path
    
    def get_url(self) -> str:
        """Get the syft:// URL for private data"""
        return self.url
    
    def get_permissions(self) -> List[str]:
        """Get read permissions for private data"""
        return self._syft_object.private_permissions
    
    def get_write_permissions(self) -> List[str]:
        """Get write permissions for private data"""
        return self._syft_object.private_write_permissions
    
    def set_permissions(self, read: List[str] = None, write: List[str] = None) -> None:
        """Set permissions for private data"""
        self._syft_object.set_permissions("private", read=read, write=write)
    
    def save(self, file_path: str = None, create_syftbox_permissions: bool = True) -> None:
        """Save the syft object - moved from main object to private accessor"""
        if file_path:
            self._syft_object._save_yaml(file_path, create_syftbox_permissions)
        else:
            # Use existing syftobject path
            syftobject_path = self._syft_object.syftobject_path
            if syftobject_path:
                self._syft_object._save_yaml(syftobject_path, create_syftbox_permissions)
            else:
                raise ValueError("No file path provided and no existing syftobject path found")


class SyftObjectConfigAccessor:
    """Accessor for syftobject configuration and metadata."""
    
    def __init__(self, syft_object: 'SyftObject'):
        self._syft_object = syft_object
    
    def get_path(self) -> str:
        """Get the local file path for the .syftobject.yaml file"""
        return self._syft_object.syftobject_path
    
    def get_url(self) -> str:
        """Get the syft:// URL for the .syftobject.yaml file"""
        return self._syft_object.syftobject
    
    def get_permissions(self) -> List[str]:
        """Get read permissions for the syftobject file (discovery permissions)"""
        return self._syft_object.syftobject_permissions
    
    def set_permissions(self, read: List[str]) -> None:
        """Set discovery permissions for the syftobject file"""
        self._syft_object.set_permissions("syftobject", read=read)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"SyftObjectConfigAccessor(url='{self.get_url()}', path='{self.get_path()}')"