# syft-objects models - Core SyftObject class and related models

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
import yaml

from pydantic import BaseModel, Field, model_validator

from .client import get_syftbox_client, extract_local_path_from_syft_url
from .permissions import set_file_permissions_wrapper
from .display import create_html_display
from .data_accessor import DataAccessor


def utcnow():
    """Get current UTC timestamp"""
    return datetime.now(tz=timezone.utc)


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
    
    def get_permissions(self) -> list[str]:
        """Get read permissions for mock data"""
        return self._syft_object.mock_permissions
    
    def get_write_permissions(self) -> list[str]:
        """Get write permissions for mock data"""
        return self._syft_object.mock_write_permissions
    
    def set_permissions(self, read: list[str] = None, write: list[str] = None) -> None:
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
    
    def get_permissions(self) -> list[str]:
        """Get read permissions for private data"""
        return self._syft_object.private_permissions
    
    def get_write_permissions(self) -> list[str]:
        """Get write permissions for private data"""
        return self._syft_object.private_write_permissions
    
    def set_permissions(self, read: list[str] = None, write: list[str] = None) -> None:
        """Set permissions for private data"""
        self._syft_object.set_permissions("private", read=read, write=write)
    
    def save(self, file_path: str = None, create_syftbox_permissions: bool = True) -> None:
        """Save the syft object - moved from main object to private accessor"""
        if file_path:
            self._syft_object._save_yaml(file_path, create_syftbox_permissions)
        else:
            # Use existing syftobject path
            syftobject_path = self._syft_object._syftobject_path
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
        return self._syft_object._syftobject_path
    
    def get_url(self) -> str:
        """Get the syft:// URL for the .syftobject.yaml file"""
        return self._syft_object.syftobject
    
    def get_permissions(self) -> list[str]:
        """Get read permissions for the syftobject file (discovery permissions)"""
        return self._syft_object.syftobject_permissions
    
    def set_permissions(self, read: list[str]) -> None:
        """Set discovery permissions for the syftobject file"""
        self._syft_object.set_permissions("syftobject", read=read)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"SyftObjectConfigAccessor(url='{self.get_url()}', path='{self.get_path()}')"


class SyftObject(BaseModel):
    """
    A distributed object with mock/real pattern for file discovery and addressing
    """
    # Mandatory metadata
    uid: UUID = Field(default_factory=uuid4, description="Unique identifier for the object")
    private_url: str = Field(description="Syft:// path to the private object", alias="private")
    mock_url: str = Field(description="Syft:// path to the public/mock object", alias="mock")
    syftobject: str = Field(description="Syft:// path to the .syftobject.yaml metadata file")
    created_at: datetime = Field(default_factory=utcnow, description="Creation timestamp")
    
    # Object type - new field for folder support
    object_type: str = Field(
        default="file", 
        description="Type of object: 'file' or 'folder'"
    )
    
    # Permission metadata - who can access what (read/write granularity)
    syftobject_permissions: list[str] = Field(
        default_factory=lambda: ["public"], 
        description="Who can read the .syftobject.yaml file (know the object exists)"
    )
    mock_permissions: list[str] = Field(
        default_factory=lambda: ["public"], 
        description="Who can read the mock/fake version of the object"
    )
    mock_write_permissions: list[str] = Field(
        default_factory=list,
        description="Who can write/update the mock/fake version of the object"
    )
    private_permissions: list[str] = Field(
        default_factory=list, 
        description="Who can read the private/real data"
    )
    private_write_permissions: list[str] = Field(
        default_factory=list,
        description="Who can write/update the private/real data"
    )
    
    # Recommended metadata
    name: Optional[str] = Field(None, description="Human-readable name for the object")
    description: Optional[str] = Field(None, description="Description of the object")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    # Arbitrary metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata")
    
    @property
    def _is_folder(self) -> bool:
        """Check if this object represents a folder. (Hidden from public API)"""
        return self.object_type == "folder"
    
    @property
    def type(self) -> str:
        """Alias for get_type() to maintain some compatibility"""
        return self.get_type()
    
    # Data accessor properties
    @property
    def private(self) -> PrivateAccessor:
        """Get data accessor for private data with enhanced permission methods"""
        return PrivateAccessor(self.private_url, self)
    
    @property
    def mock(self) -> MockAccessor:
        """Get data accessor for mock data with enhanced permission methods"""
        return MockAccessor(self.mock_url, self)
    
    @property
    def syftobject_config(self) -> SyftObjectConfigAccessor:
        """Get accessor for syftobject configuration and metadata"""
        return SyftObjectConfigAccessor(self)
    
    # Setter methods for all getters
    def set_name(self, name: str) -> None:
        """Set the human-readable name for this object"""
        self.name = name
    
    def set_description(self, description: str) -> None:
        """Set the description of this object"""
        self.description = description
    
    def set_metadata(self, metadata: dict) -> None:
        """Set the arbitrary metadata dictionary"""
        self.metadata = metadata.copy()
    
    def set_updated_at(self, timestamp: datetime = None) -> None:
        """Set the last update timestamp (defaults to current UTC time)"""
        self.updated_at = timestamp or utcnow()
    
    def set_type(self, object_type: str) -> None:
        """Set the object type (file or folder)"""
        if object_type not in ["file", "folder"]:
            raise ValueError(f"Invalid object type: {object_type}. Must be 'file' or 'folder'")
        self.object_type = object_type
    
    # New API methods with get_ prefixes
    def get_uid(self) -> str:
        """Get the unique identifier for this object"""
        return str(self.uid)
    
    def get_name(self) -> str:
        """Get the human-readable name for this object"""
        return self.name or ""
    
    def get_description(self) -> str:
        """Get the description of this object"""
        return self.description or ""
    
    def get_created_at(self) -> str:
        """Get the creation timestamp as ISO string"""
        return self.created_at.isoformat() if self.created_at else ""
    
    def get_updated_at(self) -> str:
        """Get the last update timestamp as ISO string"""
        return self.updated_at.isoformat() if self.updated_at else ""
    
    def get_type(self) -> str:
        """Get the object type (file or folder)"""
        return self.object_type
    
    def get_file_type(self) -> str:
        """Get the file extension from mock/private URLs"""
        # Folders don't have file extensions
        if self._is_folder:
            return ""
            
        try:
            # Try to extract file extension from private URL first, then mock URL
            for url in [self.private_url, self.mock_url]:
                if not url:
                    continue
                
                # Get just the filename from the URL
                filename = url.split("/")[-1]
                
                # Check if filename has an extension (dot not at start)
                if "." in filename and not filename.startswith("."):
                    parts = filename.split(".")
                    if len(parts) > 1 and parts[-1]:  # Ensure there's an actual extension
                        return f".{parts[-1].lower()}"
            return ""
        except:
            return ""
    
    def get_metadata(self) -> dict:
        """Get the arbitrary metadata dictionary"""
        return self.metadata.copy()
    
    def get_permissions(self) -> dict:
        """Get all permission settings for this object"""
        return {
            "syftobject": self.syftobject_permissions.copy(),
            "mock_read": self.mock_permissions.copy(),
            "mock_write": self.mock_write_permissions.copy(),
            "private_read": self.private_permissions.copy(),
            "private_write": self.private_write_permissions.copy()
        }
    
    def get_urls(self) -> dict:
        """Get all syft:// URLs for this object"""
        return {
            "private": self.private_url,
            "mock": self.mock_url,
            "syftobject": self.syftobject
        }
    
    def get_path(self) -> dict:
        """Get all local file paths for this object"""
        return {
            "private": self._get_local_file_path(self.private_url),
            "mock": self._get_local_file_path(self.mock_url),
            "syftobject": self.syftobject_path
        }
    
    def get_info(self) -> dict:
        """Get comprehensive information about this object"""
        return {
            "uid": self.get_uid(),
            "name": self.get_name(),
            "description": self.get_description(),
            "type": self.get_type(),
            "created_at": self.get_created_at(),
            "updated_at": self.get_updated_at(),
            "urls": self.get_urls(),
            "paths": self.get_path(),
            "permissions": self.get_permissions(),
            "metadata": self.get_metadata()
        }

    # Internal/hidden properties for backward compatibility - moved from public API
    @property
    def _private_path(self) -> str:
        """Get the full local file path for the private object (internal use)"""
        return self._get_local_file_path(self.private_url)
    
    @property
    def _mock_path(self) -> str:
        """Get the full local file path for the mock object (internal use)"""
        return self._get_local_file_path(self.mock_url)
    
    @property
    def _syftobject_path(self) -> str:
        """Get the full local file path for the .syftobject.yaml file (internal use)"""
        # First try to get path from the syftobject field
        if hasattr(self, 'syftobject') and self.syftobject:
            return self._get_local_file_path(self.syftobject)
        
        # Fall back to metadata if available
        file_ops = self.metadata.get("_file_operations", {})
        syftobject_yaml_path = file_ops.get("syftobject_yaml_path")
        if syftobject_yaml_path:
            return syftobject_yaml_path
        return ""
    
    # Backward compatibility properties for internal code
    @property
    def private_path(self) -> str:
        """DEPRECATED: Use private.get_path() instead"""
        return self._private_path
    
    @property
    def mock_path(self) -> str:
        """DEPRECATED: Use mock.get_path() instead"""
        return self._mock_path
    
    @property
    def syftobject_path(self) -> str:
        """DEPRECATED: Use syftobject_config.get_path() instead"""
        return self._syftobject_path
    
    
    @model_validator(mode='after')
    def _validate_urls(self):
        """Validate URLs match object type"""
        if self._is_folder:
            # Folders must end with /
            if not self.private_url.endswith('/'):
                self.private_url += '/'
            if not self.mock_url.endswith('/'):
                self.mock_url += '/'
        else:
            # Files must NOT end with /
            if self.private_url.endswith('/'):
                raise ValueError("File URLs cannot end with /")
            if self.mock_url.endswith('/'):
                raise ValueError("File URLs cannot end with /")
        return self
    
    @model_validator(mode='after')
    def _validate_file_extensions(self):
        """Validate that mock and private files have matching extensions"""
        # Skip validation for folders - they don't have extensions
        if self._is_folder:
            return self
            
        def extract_extension(url: str) -> str:
            """Extract file extension from a URL filename"""
            if not url:
                return ""
            
            # Get just the filename from the URL
            filename = url.split("/")[-1]
            
            # Check if filename has an extension (dot not at start)
            if "." in filename and not filename.startswith("."):
                parts = filename.split(".")
                if len(parts) > 1 and parts[-1]:  # Ensure there's an actual extension
                    return parts[-1].lower()
            return ""
        
        mock_ext = extract_extension(self.mock_url)
        private_ext = extract_extension(self.private_url)
        
        # Only validate if BOTH files have extensions - they must match
        if mock_ext and private_ext and mock_ext != private_ext:
            raise ValueError(
                f"Mock and private files must have matching extensions. "
                f"Mock file has '.{mock_ext}' but private file has '.{private_ext}'. "
                f"Mock: {self.mock_url}, Private: {self.private_url}"
            )
        
        return self
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True  # Allow using both field name and alias
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    
    def __getattribute__(self, name):
        """Intercept attribute access to hide internal fields from direct access"""
        # Define which attributes should be hidden from direct access
        hidden_attrs = {
            'uid', 'name', 'description', 'created_at', 'updated_at', 'metadata',
            'private_url', 'mock_url', 'syftobject', 'object_type',
            'syftobject_permissions', 'mock_permissions', 'mock_write_permissions',
            'private_permissions', 'private_write_permissions'
        }
        
        # Define deprecated attributes that should redirect to new API
        deprecated_attrs = {
            'private_path': 'private.get_path()',
            'mock_path': 'mock.get_path()', 
            'syftobject_path': 'syftobject_config.get_path()'
        }
        
        # Allow access from internal methods and special cases
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller = frame.f_back
            # Allow access from within the class methods
            if 'self' in caller.f_locals and caller.f_locals.get('self') is self:
                return super().__getattribute__(name)
            # Allow access from the same module
            caller_module = caller.f_globals.get('__name__', '')
            if caller_module == 'syft_objects.models':
                return super().__getattribute__(name)
            # Allow access from syft_objects internals for backward compatibility
            if caller_module.startswith('syft_objects.'):
                if name in deprecated_attrs:
                    # Still allow internal access to deprecated properties
                    return super().__getattribute__(name)
                return super().__getattribute__(name)
        
        # Block direct access to hidden attributes
        if name in hidden_attrs:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'. "
                f"Use 'get_{name}()' instead."
            )
        
        # Block access to deprecated attributes with helpful message
        if name in deprecated_attrs:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'. "
                f"Use '{deprecated_attrs[name]}' instead."
            )
        
        return super().__getattribute__(name)
    
    def __dir__(self):
        """Override dir() to only show the public API methods"""
        # Get default attributes
        attrs = set(super().__dir__())
        
        # Remove hidden fields
        hidden_fields = {
            'uid', 'name', 'description', 'created_at', 'updated_at', 'metadata',
            'private_url', 'mock_url', 'syftobject', 'object_type',
            'syftobject_permissions', 'mock_permissions', 'mock_write_permissions',
            'private_permissions', 'private_write_permissions',
            # Hide deprecated path properties
            'private_path', 'mock_path', 'syftobject_path',
            # Hide methods that should be private
            'can_delete', 'load_yaml', 'validate_urls', 'validate_file_extensions',
            'from_orm', 'model_construct', 'model_copy',
            # Also hide many pydantic internals
            'model_config', 'model_fields', 'model_computed_fields', 'model_extra',
            'model_fields_set', 'model_post_init', 'model_validate', 'model_validate_json',
            'model_dump', 'model_dump_json', 'model_json_schema', 'model_parametrized_name',
            'model_rebuild', 'model_validate_strings', 'copy', 'dict', 'json', 'parse_file',
            'parse_obj', 'parse_raw', 'schema', 'schema_json', 'update_forward_refs',
            'validate', 'construct', '__fields__', '__fields_set__', '__config__',
        }
        
        # Keep only public API
        public_attrs = attrs - hidden_fields
        
        # Make sure we include our public methods
        public_methods = {
            'get_uid', 'get_name', 'get_description', 'get_created_at', 'get_updated_at',
            'get_type', 'get_file_type', 'get_metadata', 'get_permissions', 'get_urls',
            'get_path', 'get_info', 'set_name', 'set_description', 'set_metadata',
            'set_updated_at', 'set_type', 'delete_obj', 'set_permissions',
            'mock', 'private', 'syftobject_config', '_repr_html_', '_is_folder',
            'type', '_save_yaml', '_create_syftbox_permissions',
            '_check_file_exists', '_can_delete', 'get_owner_email', '_load_yaml',
            '_validate_urls', '_validate_file_extensions', '_from_orm', 
            '_model_construct', '_model_copy'
        }
        
        return sorted(list(public_attrs | public_methods))
    
    def _repr_html_(self) -> str:
        """Rich HTML representation for Jupyter notebooks"""
        return create_html_display(self)
    
    def _check_file_exists(self, syft_url: str) -> bool:
        """Check if a file exists locally (for display purposes)"""
        try:
            syftbox_client = get_syftbox_client()
            if syftbox_client:
                local_path = extract_local_path_from_syft_url(syft_url)
                if local_path:
                    return local_path.exists()
            
            # Fallback: check if it's in tmp directory
            from pathlib import Path
            filename = syft_url.split("/")[-1]
            tmp_path = Path("tmp") / filename
            return tmp_path.exists()
        except Exception:
            return False
    
    def _get_local_file_path(self, syft_url: str) -> str:
        """Get the local file path for a syft:// URL"""
        try:
            # Check for folder paths in metadata first
            if self._is_folder and "_folder_paths" in self.metadata:
                folder_paths = self.metadata["_folder_paths"]
                if syft_url == self.private_url and "private" in folder_paths:
                    return folder_paths["private"]
                elif syft_url == self.mock_url and "mock" in folder_paths:
                    return folder_paths["mock"]
            
            syftbox_client = get_syftbox_client()
            if syftbox_client:
                local_path = extract_local_path_from_syft_url(syft_url)
                if local_path and local_path.exists():
                    return str(local_path.absolute())
            
            # Fallback: check if it's in tmp directory
            from pathlib import Path
            filename = syft_url.split("/")[-1].rstrip('/')  # Remove trailing slash for folders
            tmp_path = Path("tmp") / filename
            if tmp_path.exists():
                return str(tmp_path.absolute())
            
            return ""
        except Exception:
            return ""
    
    def _get_file_preview(self, file_path: str, max_chars: int = 1000) -> str:
        """Get a preview of file content (first N characters)"""
        try:
            from pathlib import Path
            path = Path(file_path)
            
            if not path.exists():
                return f"File not found: {file_path}"
            
            # Try to read as text
            try:
                content = path.read_text(encoding='utf-8')
                if len(content) <= max_chars:
                    return content
                else:
                    return content[:max_chars] + f"\n\n... (truncated, showing first {max_chars} characters of {len(content)} total)"
            except UnicodeDecodeError:
                # If it's a binary file, show file info instead
                size = path.stat().st_size
                return f"Binary file: {path.name}\nSize: {size} bytes\nPath: {file_path}\n\n(Binary files cannot be previewed as text)"
        except Exception as e:
            return f"Error reading file: {str(e)}"


    def _save_yaml(self, file_path: str | Path, create_syftbox_permissions: bool = True) -> None:
        """Save the syft object to a YAML file - internal method, use private.save() instead"""
        file_path = Path(file_path)
        
        # Ensure the file ends with .syftobject.yaml
        if not file_path.name.endswith('.syftobject.yaml'):
            if file_path.suffix == '.yaml':
                # Replace .yaml with .syftobject.yaml
                file_path = file_path.with_suffix('.syftobject.yaml')
            elif file_path.suffix == '':
                # Add .syftobject.yaml extension
                file_path = file_path.with_suffix('.syftobject.yaml')
            else:
                # Add .syftobject.yaml to existing extension
                file_path = Path(str(file_path) + '.syftobject.yaml')
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict and handle datetime/UUID serialization
        data = self.model_dump(mode='json')
        
        # Write to YAML file
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True, indent=2)
        
        # Create SyftBox permission files if requested
        if create_syftbox_permissions:
            self._create_syftbox_permissions(file_path)

    @classmethod
    def _load_yaml(cls, file_path: str | Path) -> 'SyftObject':
        """Load a syft object from a .syftobject.yaml file"""
        file_path = Path(file_path)
        
        # Validate that the file has the correct extension
        if not file_path.name.endswith('.syftobject.yaml'):
            raise ValueError(f"File must have .syftobject.yaml extension, got: {file_path.name}")
        
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def _create_syftbox_permissions(self, syftobject_file_path: Path) -> None:
        """Create SyftBox permission files for the syft object"""
        # Create permissions for the .syftobject.yaml file itself (discovery)
        set_file_permissions_wrapper(str(syftobject_file_path), self.syftobject_permissions)
        
        # Create permissions for mock and private files
        set_file_permissions_wrapper(self.mock_url, self.mock_permissions, self.mock_write_permissions)
        set_file_permissions_wrapper(self.private_url, self.private_permissions, self.private_write_permissions)

    def set_permissions(self, file_type: str, read: list[str] = None, write: list[str] = None, syftobject_file_path: str | Path = None) -> None:
        """
        Update permissions for a file in this object (mock, private, or syftobject).
        Uses the minimal permission utilities from permissions.py.
        """
        if file_type == "mock":
            if read is not None:
                self.mock_permissions = read
            if write is not None:
                self.mock_write_permissions = write
            # Update syft.pub.yaml if possible
            set_file_permissions_wrapper(self.mock_url, self.mock_permissions, self.mock_write_permissions)
        elif file_type == "private":
            if read is not None:
                self.private_permissions = read
            if write is not None:
                self.private_write_permissions = write
            # Update syft.pub.yaml if possible
            set_file_permissions_wrapper(self.private_url, self.private_permissions, self.private_write_permissions)
        elif file_type == "syftobject":
            if read is not None:
                self.syftobject_permissions = read
            # Discovery files are read-only, so use syftobject_path or provided path
            if syftobject_file_path:
                set_file_permissions_wrapper(str(syftobject_file_path), self.syftobject_permissions)
            elif self.syftobject:
                set_file_permissions_wrapper(self.syftobject, self.syftobject_permissions)
        else:
            raise ValueError(f"Invalid file_type: {file_type}. Must be 'mock', 'private', or 'syftobject'.")
    
    def delete_obj(self, user_email: str = None) -> bool:
        """
        Delete this syft-object and all its associated files.
        
        For folder objects, this will delete the entire directory structure.
        For file objects, this will delete the individual files.
        
        Args:
            user_email: Email of the user attempting deletion. If None, will try to get from SyftBox client.
        
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        # Check permissions first
        if not self.can_delete(user_email):
            raise PermissionError(f"User {user_email or 'unknown'} does not have permission to delete object {self.uid} owned by {self.get_owner_email()}")
        
        try:
            if self._is_folder:
                return self._delete_folder_object()
            else:
                return self._delete_file_object()
        except Exception as e:
            return False
    
    def _delete_folder_object(self) -> bool:
        """Delete a folder-type syft-object by removing its directory structure."""
        try:
            from pathlib import Path
            import shutil
            
            # Try multiple strategies to find the folder path
            folder_path = None
            
            # Strategy 1: Use syftobject_path parent directory (most reliable for syft-queue jobs)
            if self.syftobject_path:
                syftobject_path = Path(self.syftobject_path)
                if syftobject_path.exists():
                    folder_path = syftobject_path.parent
                    pass  # Found folder path via syftobject_path
            
            # Strategy 2: For syft-queue jobs, search across all status directories
            if not folder_path and hasattr(self, 'metadata') and self.metadata and self.metadata.get('type') == 'SyftBox Job':
                # Search in syft-queues directories for this job UID
                job_uid = str(self.uid)
                
                # Common syft-queue base paths
                potential_bases = [
                    Path.home() / "SyftBox" / "datasites",
                    Path("/tmp"),  # fallback
                ]
                
                for base in potential_bases:
                    if base.exists():
                        # Search for job directories with this UID across all status folders
                        for queue_dir in base.rglob("**/syft-queues"):
                            for status_dir in ["inbox", "running", "completed", "failed"]:
                                status_path = queue_dir / f"*_queue" / "jobs" / status_dir
                                for job_dir in status_path.parent.glob(f"jobs/{status_dir}/*"):
                                    if job_dir.is_dir() and job_uid in job_dir.name:
                                        folder_path = job_dir
                                        pass  # Found syft-queue job folder
                                        break
                                if folder_path:
                                    break
                            if folder_path:
                                break
                    if folder_path:
                        break
            
            # Strategy 3: Check if private_path is a directory
            if not folder_path and self.private_path:
                private_path = Path(self.private_path)
                if private_path.exists() and private_path.is_dir():
                    folder_path = private_path
                    pass  # Found folder path via private_path (is_dir)
                elif private_path.exists() and private_path.is_file():
                    # If private_path is a file, use its parent directory
                    folder_path = private_path.parent
                    pass  # Found folder path via private_path parent
            
            # Strategy 4: Check folder paths in metadata
            if not folder_path and hasattr(self, 'metadata') and self.metadata:
                folder_paths = self.metadata.get('_folder_paths', {})
                if 'private' in folder_paths:
                    metadata_path = Path(folder_paths['private'])
                    pass  # Found folder path via metadata
                    
                    # Check if the metadata path actually exists
                    if metadata_path.exists() and metadata_path.is_dir():
                        folder_path = metadata_path
                        pass  # Metadata path exists and is valid
                    else:
                        pass  # Metadata path doesn't exist, checking if job moved
                        
                        # The metadata path is stale - search for the job in current location
                        job_uid = str(self.uid)
                        potential_bases = [
                            Path.home() / "SyftBox" / "datasites",
                            Path("/tmp"),  # fallback
                        ]
                        
                        for base in potential_bases:
                            if base.exists():
                                # Search for job directories with this UID across all status folders
                                for queue_dir in base.rglob("**/syft-queues"):
                                    for status_dir in ["running", "completed", "failed", "inbox"]:  # prioritize current status
                                        for job_dir in queue_dir.rglob(f"*/jobs/{status_dir}/*{job_uid}*"):
                                            if job_dir.is_dir():
                                                folder_path = job_dir
                                                pass  # Found job in status folder
                                                break
                                        if folder_path:
                                            break
                                    if folder_path:
                                        break
                            if folder_path:
                                break
            
            if folder_path and folder_path.exists() and folder_path.is_dir():
                shutil.rmtree(str(folder_path))
                
                # Refresh the objects collection
                try:
                    from .collections import objects
                    if objects:
                        objects.refresh()
                except ImportError:
                    pass
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def _delete_file_object(self) -> bool:
        """Delete a file-type syft-object by removing its individual files."""
        try:
            from pathlib import Path
            import shutil
            deleted_files = []
            
            # Delete private file/directory if it exists
            if self.private_path:
                private_path = Path(self.private_path)
                if private_path.exists():
                    if private_path.is_file():
                        private_path.unlink()
                        deleted_files.append("private")
                    elif private_path.is_dir():
                        shutil.rmtree(str(private_path))
                        deleted_files.append("private_directory")
            
            # Delete mock file/directory if it exists
            if self.mock_path:
                mock_path = Path(self.mock_path)
                if mock_path.exists():
                    if mock_path.is_file():
                        mock_path.unlink()
                        deleted_files.append("mock")
                    elif mock_path.is_dir():
                        shutil.rmtree(str(mock_path))
                        deleted_files.append("mock_directory")
            
            # Delete syftobject file if it exists
            if self.syftobject_path:
                syftobject_path = Path(self.syftobject_path)
                if syftobject_path.exists():
                    syftobject_path.unlink()
                    deleted_files.append("syftobject")
            
            if deleted_files:
                # Refresh the objects collection
                try:
                    from .collections import objects
                    if objects:
                        objects.refresh()
                except ImportError:
                    pass
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def _can_delete(self, user_email: str = None) -> bool:
        """
        Check if a user has permission to delete this object.
        User must have write access to all object components (private, mock, syftobject).
        """
        if not user_email:
            # Try to get current user email from SyftBox client
            try:
                from .client import get_syftbox_client
                client = get_syftbox_client()
                if client and hasattr(client, 'email'):
                    user_email = client.email
                else:
                    # No user email available - deny deletion
                    return False
            except:
                return False
        
        # Extract object owner email from private URL
        owner_email = self.get_owner_email()
        
        # User must be the owner/admin to delete the object
        if user_email != owner_email:
            return False
        
        # Additional check: user must have write permissions for all components
        # Check private write permissions
        if self.private_write_permissions and user_email not in self.private_write_permissions:
            return False
        
        # Check mock write permissions  
        if self.mock_write_permissions and user_email not in self.mock_write_permissions:
            return False
        
        # For syftobject file, we require the user to be the owner (already checked above)
        # since syftobject permissions are usually public for discovery
        
        return True
    
    @classmethod
    def _from_orm(cls, *args, **kwargs):
        """Private method for ORM compatibility"""
        return super().from_orm(*args, **kwargs)
    
    @classmethod
    def _model_construct(cls, *args, **kwargs):
        """Private method for model construction"""
        return super().model_construct(*args, **kwargs)
    
    def _model_copy(self, *args, **kwargs):
        """Private method for model copying"""
        return super().model_copy(*args, **kwargs)
    
    def get_owner_email(self) -> str:
        """Extract the owner email from the private URL."""
        try:
            if self.private_url.startswith("syft://"):
                parts = self.private_url.split("/")
                if len(parts) >= 3:
                    return parts[2]
        except:
            pass
        return "unknown@example.com"
 