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
    
    def get_read_permissions(self) -> List[str]:
        """Get read permissions for mock data"""
        return self._syft_object.mock_permissions
    
    def get_write_permissions(self) -> List[str]:
        """Get write permissions for mock data"""
        return self._syft_object.mock_write_permissions
    
    def get_admin_permissions(self) -> List[str]:
        """Get admin permissions for mock data"""
        return self._syft_object.metadata.get("admin_permissions", [])
    
    def set_read_permissions(self, read: List[str]) -> None:
        """Set read permissions for mock data"""
        self._syft_object.mock_permissions = read
    
    def set_write_permissions(self, write: List[str]) -> None:
        """Set write permissions for mock data"""
        self._syft_object.mock_write_permissions = write
    
    def set_admin_permissions(self, admin: List[str]) -> None:
        """Set admin permissions for mock data"""
        self._syft_object.metadata["admin_permissions"] = admin
    
    def is_folder(self) -> bool:
        """Check if the mock is a folder"""
        mock_path = self.get_path()
        if mock_path and Path(mock_path).exists():
            return Path(mock_path).is_dir()
        return False

    def get_editor_url(self, base_url: str = "http://localhost:8004") -> str:
        """Get the editor URL for folder mocks"""
        if self.is_folder():
            path = self.get_path()
            if path:
                return f"{base_url}/editor?path={path}"
        return None


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
    
    def get_read_permissions(self) -> List[str]:
        """Get read permissions for private data"""
        return self._syft_object.private_permissions
    
    def get_write_permissions(self) -> List[str]:
        """Get write permissions for private data"""
        return self._syft_object.private_write_permissions
    
    def get_admin_permissions(self) -> List[str]:
        """Get admin permissions for private data"""
        return self._syft_object.metadata.get("admin_permissions", [])
    
    def set_read_permissions(self, read: List[str]) -> None:
        """Set read permissions for private data"""
        self._syft_object.private_permissions = read
    
    def set_write_permissions(self, write: List[str]) -> None:
        """Set write permissions for private data"""
        self._syft_object.private_write_permissions = write
    
    def set_admin_permissions(self, admin: List[str]) -> None:
        """Set admin permissions for private data"""
        self._syft_object.metadata["admin_permissions"] = admin
    
    def is_folder(self) -> bool:
        """Check if the private is a folder"""
        private_path = self.get_path()
        if private_path and Path(private_path).exists():
            return Path(private_path).is_dir()
        return False

    def get_editor_url(self, base_url: str = "http://localhost:8004") -> str:
        """Get the editor URL for folder privates"""
        if self.is_folder():
            path = self.get_path()
            if path:
                return f"{base_url}/editor?path={path}"
        return None
    


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
    
    def get_read_permissions(self) -> List[str]:
        """Get read permissions for the syftobject file (discovery permissions)"""
        return self._syft_object.syftobject_permissions
    
    def get_write_permissions(self) -> List[str]:
        """Get write permissions for the syftobject file (admin only)"""
        return self._syft_object.metadata.get("admin_permissions", [])
    
    def get_admin_permissions(self) -> List[str]:
        """Get admin permissions for the syftobject file"""
        return self._syft_object.metadata.get("admin_permissions", [])
    
    def set_read_permissions(self, read: List[str]) -> None:
        """Set discovery permissions for the syftobject file"""
        self._syft_object.syftobject_permissions = read
    
    def set_write_permissions(self, write: List[str]) -> None:
        """Set write permissions for the syftobject file (updates admin)"""
        self._syft_object.metadata["admin_permissions"] = write
    
    def set_admin_permissions(self, admin: List[str]) -> None:
        """Set admin permissions for the syftobject file"""
        self._syft_object.metadata["admin_permissions"] = admin
    
    def __repr__(self) -> str:
        """String representation"""
        return f"SyftObjectConfigAccessor(url='{self.get_url()}', path='{self.get_path()}')"