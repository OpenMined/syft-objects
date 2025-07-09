"""Clean API wrapper for SyftObject that exposes only the desired methods."""

from typing import Any, Optional
from datetime import datetime
from pathlib import Path


class CleanSyftObject:
    """Clean API wrapper that exposes only the methods we want users to see."""
    
    def __init__(self, syft_obj):
        """Initialize with a raw SyftObject instance."""
        # Use object.__setattr__ to bypass our custom __setattr__
        object.__setattr__(self, '_CleanSyftObject__obj', syft_obj)
    
    # ===== Getter Methods =====
    def get_uid(self) -> str:
        """Get the object's unique identifier"""
        return str(self._CleanSyftObject__obj.uid)
    
    def get_name(self) -> str:
        """Get the object's name"""
        return self._CleanSyftObject__obj.name
    
    def get_description(self) -> str:
        """Get the object's description"""
        return self._CleanSyftObject__obj.description
    
    def get_created_at(self) -> datetime:
        """Get the object's creation timestamp"""
        return self._CleanSyftObject__obj.created_at
    
    def get_updated_at(self) -> datetime:
        """Get the object's last update timestamp"""
        return self._CleanSyftObject__obj.updated_at
    
    def get_metadata(self) -> dict:
        """Get the object's metadata"""
        return self._CleanSyftObject__obj.metadata.copy()
    
    def get_file_type(self) -> str:
        """Get the file type (extension) of the object"""
        if self._CleanSyftObject__obj.is_folder:
            return "folder"
        # Extract extension from private URL
        parts = self._CleanSyftObject__obj.private_url.split("/")[-1].split(".")
        if len(parts) > 1:
            return parts[-1]
        return ""
    
    def get_info(self) -> dict:
        """Get a dictionary of object information"""
        return {
            "uid": str(self._CleanSyftObject__obj.uid),
            "name": self._CleanSyftObject__obj.name,
            "description": self._CleanSyftObject__obj.description,
            "created_at": self._CleanSyftObject__obj.created_at.isoformat() if self._CleanSyftObject__obj.created_at else None,
            "updated_at": self._CleanSyftObject__obj.updated_at.isoformat() if self._CleanSyftObject__obj.updated_at else None,
            "is_folder": self._CleanSyftObject__obj.is_folder,
            "metadata": self._CleanSyftObject__obj.metadata,
            "permissions": {
                "read": self.get_read_permissions(),
                "write": self.get_write_permissions(),
                "admin": self.get_admin_permissions()
            },
            "owner_email": self.get_owner()
        }
    
    def get_path(self) -> str:
        """Get the primary (mock) path of the object"""
        return self._CleanSyftObject__obj.mock_path
    
    def get_read_permissions(self) -> list[str]:
        """Get read permissions for the syftobject (discovery)"""
        return self._CleanSyftObject__obj.syftobject_permissions.copy()
    
    def get_write_permissions(self) -> list[str]:
        """Get write permissions for the object (currently same as admin)"""
        # For now, write permissions are managed at the file level
        # Return the owner's email as they have write access
        owner = self.get_owner()
        return [owner] if owner != "unknown" else []
    
    def get_admin_permissions(self) -> list[str]:
        """Get admin permissions for the object"""
        # Admin permissions are typically the owner's email
        owner = self.get_owner()
        return [owner] if owner != "unknown" else []
    
    def get_urls(self) -> dict:
        """Get all URLs for the object"""
        return {
            "private": self._CleanSyftObject__obj.private_url,
            "mock": self._CleanSyftObject__obj.mock_url,
            "syftobject": self._CleanSyftObject__obj.syftobject
        }
    
    def get_owner(self) -> str:
        """Get the owner email by reverse engineering from the object's file paths"""
        # First try to get from metadata (preferred method)
        metadata = self.get_metadata()
        if 'owner_email' in metadata:
            return metadata['owner_email']
        if 'email' in metadata:
            return metadata['email']
        
        # Fall back to extracting from URL structure
        # URLs typically look like: syft://user@example.com/path/to/file
        private_url = self._CleanSyftObject__obj.private_url
        if private_url and "://" in private_url:
            # Extract the part after :// and before the first /
            url_part = private_url.split("://")[1]
            if "/" in url_part:
                # Get the datasite part (everything before the first /)
                datasite_part = url_part.split("/")[0]
                # If it contains @, it's likely an email
                if "@" in datasite_part:
                    return datasite_part
        
        # Try mock URL as fallback
        mock_url = self._CleanSyftObject__obj.mock_url
        if mock_url and "://" in mock_url:
            url_part = mock_url.split("://")[1]
            if "/" in url_part:
                datasite_part = url_part.split("/")[0]
                if "@" in datasite_part:
                    return datasite_part
        
        return "unknown"
    
    # ===== Setter Methods =====
    def set_name(self, name: str) -> None:
        """Set the object's name"""
        self._CleanSyftObject__obj.name = name
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_description(self, description: str) -> None:
        """Set the object's description"""
        self._CleanSyftObject__obj.description = description
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_metadata(self, metadata: dict) -> None:
        """Set the object's metadata (replaces existing)"""
        self._CleanSyftObject__obj.metadata = metadata.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    # ===== Accessor Properties =====
    @property
    def mock(self):
        """Access mock-related properties and methods"""
        return MockAccessor(self._CleanSyftObject__obj)
    
    @property
    def private(self):
        """Access private-related properties and methods"""
        return PrivateAccessor(self._CleanSyftObject__obj)
    
    @property
    def syftobject_config(self):
        """Access syftobject configuration properties and methods"""
        return SyftObjectConfigAccessor(self._CleanSyftObject__obj)
    
    # ===== Actions =====
    def delete_obj(self, user_email: str = None) -> bool:
        """Delete this object with permission checking"""
        # If no user_email provided, try to get it from SyftBox client
        if not user_email:
            try:
                from .client import get_syftbox_client
                client = get_syftbox_client()
                if client and hasattr(client, 'email'):
                    user_email = client.email
            except:
                pass
        
        return self._CleanSyftObject__obj.delete_obj(user_email)
    
    def set_read_permissions(self, read: list[str]) -> None:
        """Set read permissions for the syftobject (discovery)"""
        self._CleanSyftObject__obj.syftobject_permissions = read.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_write_permissions(self, write: list[str]) -> None:
        """Set write permissions for the object files"""
        # Set write permissions for both mock and private files
        self._CleanSyftObject__obj.mock_write_permissions = write.copy()
        self._CleanSyftObject__obj.private_write_permissions = write.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_admin_permissions(self, admin: list[str]) -> None:
        """Set admin permissions for the object"""
        # Admin permissions control who can modify the object metadata and permissions
        # Store in metadata for now
        if "admin_permissions" not in self._CleanSyftObject__obj.metadata:
            self._CleanSyftObject__obj.metadata["admin_permissions"] = []
        self._CleanSyftObject__obj.metadata["admin_permissions"] = admin.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    @property
    def type(self) -> str:
        """Get the object type"""
        return self._CleanSyftObject__obj.object_type
    
    # ===== Special Methods =====
    def __repr__(self) -> str:
        """String representation"""
        return f"<SyftObject uid={self.get_uid()} name='{self.get_name()}'>"
    
    def __str__(self) -> str:
        """String representation"""
        return self.__repr__()
    
    def _repr_html_(self) -> str:
        """Rich HTML representation for Jupyter notebooks"""
        # Delegate to the wrapped object's display
        return self._CleanSyftObject__obj._repr_html_()
    
    def __dir__(self):
        """Show only the clean API methods"""
        return [
            # Getters
            'get_uid', 'get_name', 'get_description', 'get_created_at',
            'get_updated_at', 'get_metadata', 'get_file_type', 'get_info',
            'get_path', 'get_read_permissions', 'get_write_permissions', 'get_admin_permissions', 'get_urls', 'get_owner',
            # Setters
            'set_name', 'set_description', 'set_metadata',
            'set_read_permissions', 'set_write_permissions', 'set_admin_permissions',
            # Accessors
            'mock', 'private', 'syftobject_config',
            # Actions
            'delete_obj',
            # Type
            'type'
        ]
    
    def __getattr__(self, name):
        """Block access to internal attributes"""
        if name == '_obj':
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


# ===== Accessor Classes =====
class MockAccessor:
    """Accessor for mock-related properties and methods"""
    
    def __init__(self, syft_obj):
        self._CleanSyftObject__obj = syft_obj
    
    def get_path(self) -> str:
        """Get the local file path for the mock data"""
        return self._CleanSyftObject__obj.mock_path
    
    def get_url(self) -> str:
        """Get the syft:// URL for the mock data"""
        return self._CleanSyftObject__obj.mock_url
    
    def get_read_permissions(self) -> list[str]:
        """Get read permissions for the mock data"""
        return self._CleanSyftObject__obj.mock_permissions.copy()
    
    def get_write_permissions(self) -> list[str]:
        """Get write permissions for the mock data"""
        return self._CleanSyftObject__obj.mock_write_permissions.copy()
    
    def get_admin_permissions(self) -> list[str]:
        """Get admin permissions for the mock data (same as object admin)"""
        admin_perms = self._CleanSyftObject__obj.metadata.get("admin_permissions", [])
        return admin_perms.copy() if admin_perms else []
    
    def set_read_permissions(self, read: list[str]) -> None:
        """Set read permissions for the mock data"""
        self._CleanSyftObject__obj.mock_permissions = read.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_write_permissions(self, write: list[str]) -> None:
        """Set write permissions for the mock data"""
        self._CleanSyftObject__obj.mock_write_permissions = write.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_admin_permissions(self, admin: list[str]) -> None:
        """Set admin permissions for the mock data (updates object admin)"""
        self._CleanSyftObject__obj.metadata["admin_permissions"] = admin.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def get_note(self) -> Optional[str]:
        """Get the mock note describing the mock data characteristics"""
        return self._CleanSyftObject__obj.metadata.get("mock_note")
    
    def set_note(self, note: str) -> None:
        """Set the mock note"""
        self._CleanSyftObject__obj.metadata["mock_note"] = note
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def move_path(self, new_path: str, user_email: str = None) -> bool:
        """Move the mock file to a new location (requires admin permissions)
        
        Args:
            new_path: New syft:// URL or local path for the mock file
            user_email: Email of the user attempting the move (optional, will try to detect)
            
        Returns:
            bool: True if successful, False otherwise
        """
        from .file_ops import move_object_to_syftbox_location
        from .client import get_syftbox_client, extract_local_path_from_syft_url
        
        try:
            client = get_syftbox_client()
            
            # Check admin permissions
            if not user_email and client and hasattr(client, 'email'):
                user_email = client.email
            
            admin_perms = self.get_admin_permissions()
            if user_email and user_email not in admin_perms:
                return False  # Not authorized
            
            # Get current local path
            current_local = extract_local_path_from_syft_url(
                self._CleanSyftObject__obj.mock_url,
                client.datasites if client else None
            )
            
            if not current_local or not current_local.exists():
                return False
            
            # Determine target URL
            if new_path.startswith("syft://"):
                target_url = new_path
            else:
                # Convert local path to syft URL
                # Extract email from current URL
                parts = self._CleanSyftObject__obj.mock_url.split("/")
                email = parts[2] if len(parts) > 2 else "unknown"
                # Determine if public or private based on current permissions
                is_public = "public" in self._CleanSyftObject__obj.mock_permissions
                prefix = "public" if is_public else "private"
                target_url = f"syft://{email}/{prefix}/objects/{Path(new_path).name}"
            
            # Move the file
            if move_object_to_syftbox_location(current_local, target_url, client):
                # Update the URL in the model
                self._CleanSyftObject__obj.mock_url = target_url
                from .models import utcnow
                self._CleanSyftObject__obj.updated_at = utcnow()
                return True
            
            return False
        except Exception:
            return False


class PrivateAccessor:
    """Accessor for private-related properties and methods"""
    
    def __init__(self, syft_obj):
        self._CleanSyftObject__obj = syft_obj
    
    def get_path(self) -> str:
        """Get the local file path for the private data"""
        return self._CleanSyftObject__obj.private_path
    
    def get_url(self) -> str:
        """Get the syft:// URL for the private data"""
        return self._CleanSyftObject__obj.private_url
    
    def get_read_permissions(self) -> list[str]:
        """Get read permissions for the private data"""
        return self._CleanSyftObject__obj.private_permissions.copy()
    
    def get_write_permissions(self) -> list[str]:
        """Get write permissions for the private data"""
        return self._CleanSyftObject__obj.private_write_permissions.copy()
    
    def get_admin_permissions(self) -> list[str]:
        """Get admin permissions for the private data (same as object admin)"""
        admin_perms = self._CleanSyftObject__obj.metadata.get("admin_permissions", [])
        return admin_perms.copy() if admin_perms else []
    
    def set_read_permissions(self, read: list[str]) -> None:
        """Set read permissions for the private data"""
        self._CleanSyftObject__obj.private_permissions = read.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_write_permissions(self, write: list[str]) -> None:
        """Set write permissions for the private data"""
        self._CleanSyftObject__obj.private_write_permissions = write.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_admin_permissions(self, admin: list[str]) -> None:
        """Set admin permissions for the private data (updates object admin)"""
        self._CleanSyftObject__obj.metadata["admin_permissions"] = admin.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def move_path(self, new_path: str, user_email: str = None) -> bool:
        """Move the private file to a new location (requires admin permissions)
        
        Args:
            new_path: New syft:// URL or local path for the private file
            user_email: Email of the user attempting the move (optional, will try to detect)
            
        Returns:
            bool: True if successful, False otherwise
        """
        from .file_ops import move_object_to_syftbox_location
        from .client import get_syftbox_client, extract_local_path_from_syft_url
        
        try:
            client = get_syftbox_client()
            
            # Check admin permissions
            if not user_email and client and hasattr(client, 'email'):
                user_email = client.email
            
            admin_perms = self.get_admin_permissions()
            if user_email and user_email not in admin_perms:
                return False  # Not authorized
            
            # Get current local path
            current_local = extract_local_path_from_syft_url(
                self._CleanSyftObject__obj.private_url,
                client.datasites if client else None
            )
            
            if not current_local or not current_local.exists():
                return False
            
            # Determine target URL
            if new_path.startswith("syft://"):
                target_url = new_path
            else:
                # Convert local path to syft URL
                # Extract email from current URL
                parts = self._CleanSyftObject__obj.private_url.split("/")
                email = parts[2] if len(parts) > 2 else "unknown"
                # Private files are always in private directory
                target_url = f"syft://{email}/private/objects/{Path(new_path).name}"
            
            # Move the file
            if move_object_to_syftbox_location(current_local, target_url, client):
                # Update the URL in the model
                self._CleanSyftObject__obj.private_url = target_url
                from .models import utcnow
                self._CleanSyftObject__obj.updated_at = utcnow()
                return True
            
            return False
        except Exception:
            return False
    


class SyftObjectConfigAccessor:
    """Accessor for syftobject configuration properties and methods"""
    
    def __init__(self, syft_obj):
        self._CleanSyftObject__obj = syft_obj
    
    def get_path(self) -> str:
        """Get the local file path for the syftobject configuration"""
        return self._CleanSyftObject__obj.syftobject_path
    
    def get_url(self) -> str:
        """Get the syft:// URL for the syftobject configuration"""
        return self._CleanSyftObject__obj.syftobject
    
    def get_read_permissions(self) -> list[str]:
        """Get read permissions for the syftobject configuration (discovery)"""
        return self._CleanSyftObject__obj.syftobject_permissions.copy()
    
    def get_write_permissions(self) -> list[str]:
        """Get write permissions for the syftobject configuration"""
        # SyftObject config write permissions are typically admin-only
        admin_perms = self._CleanSyftObject__obj.metadata.get("admin_permissions", [])
        return admin_perms.copy() if admin_perms else []
    
    def get_admin_permissions(self) -> list[str]:
        """Get admin permissions for the syftobject configuration"""
        admin_perms = self._CleanSyftObject__obj.metadata.get("admin_permissions", [])
        return admin_perms.copy() if admin_perms else []
    
    def set_read_permissions(self, read: list[str]) -> None:
        """Set read permissions for the syftobject configuration (discovery)"""
        self._CleanSyftObject__obj.syftobject_permissions = read.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_write_permissions(self, write: list[str]) -> None:
        """Set write permissions for the syftobject configuration (updates admin)"""
        self._CleanSyftObject__obj.metadata["admin_permissions"] = write.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def set_admin_permissions(self, admin: list[str]) -> None:
        """Set admin permissions for the syftobject configuration"""
        self._CleanSyftObject__obj.metadata["admin_permissions"] = admin.copy()
        from .models import utcnow
        self._CleanSyftObject__obj.updated_at = utcnow()
    
    def move_path(self, new_path: str, user_email: str = None) -> bool:
        """Move the syftobject config file to a new location (requires admin permissions)
        
        Args:
            new_path: New syft:// URL or local path for the .syftobject.yaml file
            user_email: Email of the user attempting the move (optional, will try to detect)
            
        Returns:
            bool: True if successful, False otherwise
        """
        from .file_ops import move_object_to_syftbox_location
        from .client import get_syftbox_client, extract_local_path_from_syft_url
        
        try:
            client = get_syftbox_client()
            
            # Check admin permissions
            if not user_email and client and hasattr(client, 'email'):
                user_email = client.email
            
            admin_perms = self.get_admin_permissions()
            if user_email and user_email not in admin_perms:
                return False  # Not authorized
            
            # Get current local path
            current_local = extract_local_path_from_syft_url(
                self._CleanSyftObject__obj.syftobject,
                client.datasites if client else None
            )
            
            if not current_local or not current_local.exists():
                return False
            
            # Determine target URL
            if new_path.startswith("syft://"):
                target_url = new_path
            else:
                # Convert local path to syft URL
                # Extract email from current URL
                parts = self._CleanSyftObject__obj.syftobject.split("/")
                email = parts[2] if len(parts) > 2 else "unknown"
                # SyftObject configs are typically public
                is_public = "public" in self._CleanSyftObject__obj.syftobject_permissions
                prefix = "public" if is_public else "private"
                
                # Ensure .syftobject.yaml extension
                path_obj = Path(new_path)
                if not path_obj.name.endswith('.syftobject.yaml'):
                    # Replace extension or add it
                    new_name = path_obj.stem + '.syftobject.yaml'
                    target_url = f"syft://{email}/{prefix}/objects/{new_name}"
                else:
                    target_url = f"syft://{email}/{prefix}/objects/{path_obj.name}"
            
            # Move the file
            if move_object_to_syftbox_location(current_local, target_url, client):
                # Update the URL in the model
                self._CleanSyftObject__obj.syftobject = target_url
                # Update the yaml path if it exists
                if hasattr(self._CleanSyftObject__obj, '_yaml_path') and self._CleanSyftObject__obj._yaml_path:
                    new_local = extract_local_path_from_syft_url(target_url, client.datasites if client else None)
                    if new_local:
                        self._CleanSyftObject__obj._yaml_path = new_local
                from .models import utcnow
                self._CleanSyftObject__obj.updated_at = utcnow()
                return True
            
            return False
        except Exception:
            return False


def wrap_syft_object(obj) -> CleanSyftObject:
    """Wrap a SyftObject in the clean API wrapper."""
    if isinstance(obj, CleanSyftObject):
        return obj
    return CleanSyftObject(obj)