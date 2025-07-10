# syft-objects models - Core SyftObject class and related models

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, List
from uuid import UUID, uuid4
import yaml
import os

from pydantic import BaseModel, Field, model_validator

from .client import get_syftbox_client, extract_local_path_from_syft_url
from .display import create_html_display
from .data_accessor import DataAccessor
from ._validation import MockRealValidationError


def utcnow():
    """Get current UTC timestamp"""
    return datetime.now(tz=timezone.utc)


class SyftObject(BaseModel):
    """
    A distributed object with mock/real pattern for file discovery and addressing.
    This implementation is file-backed - all attributes are stored in and read from
    the .syftobject.yaml file on disk.
    """
    # Path to the .syftobject.yaml file (internal use only)
    _yaml_path: Optional[Path] = None
    
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
    
    # Permissions are now managed by syft-perm on the actual files/folders
    # Removed: syftobject_permissions, mock_permissions, mock_write_permissions, 
    # private_permissions, private_write_permissions
    
    # Recommended metadata
    name: Optional[str] = Field(None, description="Human-readable name for the object")
    description: Optional[str] = Field(None, description="Description of the object")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    # Arbitrary metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata")
    
    def __init__(self, **data):
        """Initialize a file-backed SyftObject"""
        # Extract yaml path if provided
        yaml_path = data.pop('_yaml_path', None)
        
        # Initialize with BaseModel
        super().__init__(**data)
        
        # Set the yaml path
        if yaml_path:
            self._yaml_path = Path(yaml_path) if not isinstance(yaml_path, Path) else yaml_path
        
        # If we have a yaml path, sync to disk immediately
        if self._yaml_path:
            self._sync_to_disk()
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Override setattr to sync changes to disk"""
        # Handle internal attributes normally
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        
        # Set the attribute using parent class
        super().__setattr__(name, value)
        
        # Sync to disk if we have a yaml path
        if hasattr(self, '_yaml_path') and self._yaml_path:
            self._sync_to_disk()
    
    def _sync_to_disk(self) -> None:
        """Sync current state to the yaml file"""
        if not self._yaml_path:
            return
        
        # Ensure directory exists
        self._yaml_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict and handle datetime/UUID serialization
        data = self.model_dump(mode='json')
        
        # Write to YAML file
        with open(self._yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True, indent=2)
    
    @classmethod
    def from_yaml(cls, file_path: str | Path) -> 'SyftObject':
        """Load a SyftObject from a yaml file with file-backed storage"""
        file_path = Path(file_path)
        
        # Validate that the file has the correct extension
        if not file_path.name.endswith('.syftobject.yaml'):
            raise ValueError(f"File must have .syftobject.yaml extension, got: {file_path.name}")
        
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Remove old permission fields for backward compatibility
        permission_fields = [
            'syftobject_permissions', 'mock_permissions', 'mock_write_permissions',
            'private_permissions', 'private_write_permissions'
        ]
        for field in permission_fields:
            data.pop(field, None)
        
        # Add the yaml path to the data
        data['_yaml_path'] = file_path
        
        return cls(**data)
    
    def refresh(self) -> None:
        """Refresh attributes from disk"""
        if not self._yaml_path or not self._yaml_path.exists():
            return
        
        with open(self._yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Update all attributes
        for key, value in data.items():
            if hasattr(self, key) and not key.startswith('_'):
                # Use object.__setattr__ to avoid triggering sync
                object.__setattr__(self, key, value)
    
    @property
    def is_folder(self) -> bool:
        """Check if this object represents a folder."""
        return self.object_type == "folder"
    
    # Data accessor properties
    @property
    def private(self) -> DataAccessor:
        """Get data accessor for private data with .obj, .file, .path, .url properties"""
        return DataAccessor(self.private_url, self)
    
    @property
    def mock(self) -> DataAccessor:
        """Get data accessor for mock data with .obj, .file, .path, .url properties"""
        return DataAccessor(self.mock_url, self)
    
    # Convenience properties for backward compatibility
    @property
    def private_path(self) -> str:
        """Get the full local file path for the private object"""
        return self._get_local_file_path(self.private_url)
    
    @property
    def mock_path(self) -> str:
        """Get the full local file path for the mock object"""
        return self._get_local_file_path(self.mock_url)
    
    @property
    def syftobject_path(self) -> str:
        """Get the full local file path for the .syftobject.yaml file"""
        # If we have a yaml path set, use it
        if self._yaml_path:
            return str(self._yaml_path.absolute())
        
        # First try to get path from the syftobject field
        if hasattr(self, 'syftobject') and self.syftobject:
            return self._get_local_file_path(self.syftobject)
        
        # Fall back to metadata if available
        file_ops = self.metadata.get("_file_operations", {})
        syftobject_yaml_path = file_ops.get("syftobject_yaml_path")
        if syftobject_yaml_path:
            return syftobject_yaml_path
        return ""
    
    @property
    def file_type(self) -> str:
        """Get the file extension from mock/private URLs"""
        # Folders don't have file extensions
        if self.is_folder:
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
    
    @model_validator(mode='after')
    def _validate_urls(self):
        """Validate URLs match object type"""
        if self.is_folder:
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
        if self.is_folder:
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
            raise MockRealValidationError(
                f"Mock file has '.{mock_ext}' but private file has '.{private_ext}'. "
                f"Mock: {self.mock_url}, Private: {self.private_url}",
                file_type="extension",
                suggestion="Ensure mock and private files have matching extensions"
            )
        
        return self
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True  # Allow using both field name and alias
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    
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
            if self.is_folder and "_folder_paths" in self.metadata:
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


    def save_yaml(self, file_path: str | Path, create_syftbox_permissions: bool = True) -> None:
        """Save the syft object to a YAML file with .syftobject.yaml extension and create SyftBox permission files"""
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
        
        # Update the yaml path
        self._yaml_path = file_path
        
        # Sync to disk
        self._sync_to_disk()
        
        # Create SyftBox permission files if requested
        if create_syftbox_permissions:
            self._create_syftbox_permissions(file_path)

    @classmethod
    def _load_yaml(cls, file_path: str | Path) -> 'SyftObject':
        """Load a syft object from a .syftobject.yaml file"""
        # This now uses from_yaml which provides file-backed storage
        return cls.from_yaml(file_path)


    
    def delete_obj(self, user_email: str = None) -> bool:
        """Delete this object with permission checking"""
        if not self.can_delete(user_email):
            return False
        return self.delete()
    
    def can_delete(self, user_email: str = None) -> bool:
        """Check if a user can delete this object"""
        if not user_email:
            return False
        
        # Get owner email from metadata or URLs
        owner_email = self.get_owner_email()
        
        # If we couldn't get owner from metadata, try extracting from URLs
        if owner_email == 'unknown':
            owner_email = self._extract_owner_from_urls()
        
        # Normalize emails for comparison (lowercase and strip whitespace)
        normalized_user = user_email.lower().strip() if user_email else None
        normalized_owner = owner_email.lower().strip() if owner_email and owner_email != 'unknown' else None
        
        return normalized_user and normalized_owner and normalized_user == normalized_owner
    
    def get_owner_email(self) -> str:
        """Get the owner email from metadata"""
        # Check for new format first, then fall back to old format
        owner = self.metadata.get('owner_email', self.metadata.get('email', 'unknown'))
        
        # If still unknown, try to extract from URLs
        if owner == 'unknown':
            owner = self._extract_owner_from_urls()
            
        return owner
    
    def _extract_owner_from_urls(self) -> str:
        """Extract owner email from syft:// URLs"""
        # Try to extract from private URL first, then mock URL
        for url in [self.private_url, self.mock_url]:
            if url and "://" in url:
                # Extract the part after :// and before the first /
                url_part = url.split("://")[1]
                if "/" in url_part:
                    # Get the datasite part (everything before the first /)
                    datasite_part = url_part.split("/")[0]
                    # If it contains @, it's likely an email
                    if "@" in datasite_part:
                        return datasite_part
        return 'unknown'
    
    def delete(self) -> bool:
        """
        Delete this syft-object and all its associated files.
        
        For syft-queue jobs, this will delegate to the syft-queue deletion API.
        For regular syft-objects, this will delete the object files directly.
        
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            # Check if this is a syft-queue job and delegate if so
            if hasattr(self, 'metadata') and self.metadata and self.metadata.get('type') == 'SyftBox Job':
                return self._delete_syft_queue_job()
            else:
                return self._delete_standard_object()
        except Exception as e:
            print(f"Error deleting object {self.uid}: {e}")
            return False
    
    def _delete_syft_queue_job(self) -> bool:
        """Delete a syft-queue job by calling the syft-queue API."""
        try:
            import requests
            
            # Try to find syft-queue server port
            syft_queue_ports = [8005, 8006, 8007, 8008]  # Common syft-queue ports
            
            for port in syft_queue_ports:
                try:
                    response = requests.delete(f"http://localhost:{port}/api/jobs/{self.uid}", timeout=5.0)
                    if response.status_code == 200:
                        print(f"✅ Successfully deleted syft-queue job: {self.name if hasattr(self, 'name') else self.uid}")
                        # Refresh the objects collection
                        try:
                            from .collections import objects
                            if objects:
                                objects.refresh()
                        except ImportError:
                            pass
                        return True
                    elif response.status_code == 404:
                        # Job not found on this syft-queue instance, try next port
                        continue
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    # Server not running on this port, try next
                    continue
            
            # If syft-queue API isn't available, fall back to manual deletion
            print(f"⚠️  Could not reach syft-queue API, falling back to manual deletion")
            return self._delete_job_directory()
            
        except Exception as e:
            print(f"Error calling syft-queue API: {e}")
            return self._delete_job_directory()
    
    def _delete_job_directory(self) -> bool:
        """Manually delete a syft-queue job directory."""
        try:
            # Extract job directory from syftobject path
            if hasattr(self, 'syftobject_path') and self.syftobject_path:
                from pathlib import Path
                job_dir = Path(self.syftobject_path).parent
                if job_dir.exists() and job_dir.is_dir():
                    import shutil
                    shutil.rmtree(str(job_dir))
                    print(f"✅ Deleted syft-queue job directory: {job_dir}")
                    
                    # Refresh the objects collection
                    try:
                        from .collections import objects
                        if objects:
                            objects.refresh()
                    except ImportError:
                        pass
                    return True
            return False
        except Exception as e:
            print(f"Error deleting job directory: {e}")
            return False
    
    def _delete_standard_object(self) -> bool:
        """Delete a standard syft-object by removing its files."""
        try:
            from pathlib import Path
            deleted_files = []
            
            # Delete private file if it exists
            if hasattr(self, 'private_path') and self.private_path:
                private_path = Path(self.private_path)
                if private_path.exists():
                    private_path.unlink()
                    deleted_files.append("private")
            
            # Delete mock file if it exists
            if hasattr(self, 'mock_path') and self.mock_path:
                mock_path = Path(self.mock_path)
                if mock_path.exists():
                    mock_path.unlink()
                    deleted_files.append("mock")
            
            # Delete syftobject file if it exists
            if hasattr(self, 'syftobject_path') and self.syftobject_path:
                syftobject_path = Path(self.syftobject_path)
                if syftobject_path.exists():
                    syftobject_path.unlink()
                    deleted_files.append("syftobject")
            
            if deleted_files:
                print(f"✅ Deleted syft-object files: {', '.join(deleted_files)}")
                
                # Refresh the objects collection
                try:
                    from .collections import objects
                    if objects:
                        objects.refresh()
                except ImportError:
                    pass
                return True
            else:
                print(f"⚠️  No files found to delete for object {self.uid}")
                return False
                
        except Exception as e:
            print(f"Error deleting standard object: {e}")
            return False