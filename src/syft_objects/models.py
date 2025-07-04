# syft-objects models - Core SyftObject class and related models

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
import yaml

from pydantic import BaseModel, Field, model_validator
import os

from .client import get_syftbox_client, extract_local_path_from_syft_url
from .permissions import set_file_permissions_wrapper
from .display import create_html_display
from .data_accessor import DataAccessor


def utcnow():
    """Get current UTC timestamp"""
    return datetime.now(tz=timezone.utc)


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
    
    # New fields for relative path support
    base_path: Optional[str] = Field(None, description="Base path for resolving relative URLs")
    private_url_relative: Optional[str] = Field(None, description="Relative path to private object")
    mock_url_relative: Optional[str] = Field(None, description="Relative path to mock object")
    syftobject_relative: Optional[str] = Field(None, description="Relative path to .syftobject.yaml")
    
    # Fallback absolute paths (for recovery)
    private_url_absolute_fallback: Optional[str] = Field(None, description="Absolute fallback for private")
    mock_url_absolute_fallback: Optional[str] = Field(None, description="Absolute fallback for mock")
    syftobject_absolute_fallback: Optional[str] = Field(None, description="Absolute fallback for syftobject")
    
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
        # Use new resolution logic
        resolved = self._resolve_path('private_url')
        return str(resolved) if resolved else ""
    
    @property
    def mock_path(self) -> str:
        """Get the full local file path for the mock object"""
        # Use new resolution logic
        resolved = self._resolve_path('mock_url')
        return str(resolved) if resolved else ""
    
    @property
    def syftobject_path(self) -> str:
        """Get the full local file path for the .syftobject.yaml file"""
        # Use new resolution logic
        resolved = self._resolve_path('syftobject')
        if resolved:
            return str(resolved)
        
        # Fall back to metadata if available
        file_ops = self.metadata.get("_file_operations", {})
        syftobject_yaml_path = file_ops.get("syftobject_yaml_path")
        if syftobject_yaml_path:
            return syftobject_yaml_path
        return ""
    
    @property
    def file_type(self) -> str:
        """Get the file extension from mock/private URLs"""
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
    def validate_file_extensions(self):
        """Validate that mock and private files have matching extensions"""
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
    
    def _repr_html_(self) -> str:
        """Rich HTML representation for Jupyter notebooks"""
        return create_html_display(self)
    
    def _check_file_exists(self, syft_url: str) -> bool:
        """Check if a file exists locally (for display purposes)"""
        try:
            # Determine which URL field this is
            url_field = None
            if syft_url == self.private_url:
                url_field = 'private_url'
            elif syft_url == self.mock_url:
                url_field = 'mock_url'
            elif syft_url == self.syftobject:
                url_field = 'syftobject'
            
            if url_field:
                # Use new resolution logic
                resolved = self._resolve_path(url_field)
                return resolved is not None
            
            # Fallback for unknown URLs
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
            syftbox_client = get_syftbox_client()
            if syftbox_client:
                local_path = extract_local_path_from_syft_url(syft_url)
                if local_path and local_path.exists():
                    return str(local_path.absolute())
            
            # Fallback: check if it's in tmp directory
            from pathlib import Path
            filename = syft_url.split("/")[-1]
            tmp_path = Path("tmp") / filename
            if tmp_path.exists():
                return str(tmp_path.absolute())
            
            return ""
        except Exception:
            return ""
    
    def _resolve_path(self, url_field: str) -> Optional[Path]:
        """Resolve a path using multiple strategies:
        1. Try relative path if base_path exists
        2. Try absolute syft:// URL
        3. Try absolute fallback path
        4. Search common locations
        """
        # Strategy 1: Relative path
        relative_field = f"{url_field}_relative"
        if self.base_path and hasattr(self, relative_field):
            relative_url = getattr(self, relative_field)
            if relative_url:
                # Handle both absolute and relative base paths
                base = Path(self.base_path)
                if not base.is_absolute():
                    # If base_path is relative, resolve it from current working directory
                    base = Path.cwd() / base
                
                candidate = base / relative_url
                if candidate.exists():
                    return candidate.absolute()
        
        # Strategy 2: Absolute syft:// URL (current behavior)
        absolute_url = getattr(self, url_field, None)
        if absolute_url:
            try:
                local_path = extract_local_path_from_syft_url(absolute_url)
                if local_path and local_path.exists():
                    return local_path.absolute()
            except:
                pass
        
        # Strategy 3: Absolute fallback
        fallback_field = f"{url_field}_absolute_fallback"
        if hasattr(self, fallback_field):
            fallback = getattr(self, fallback_field, None)
            if fallback:
                fallback_path = Path(fallback)
                if fallback_path.exists():
                    return fallback_path.absolute()
        
        # Strategy 4: Search heuristics
        return self._search_for_file(url_field)
    
    def _search_for_file(self, url_field: str) -> Optional[Path]:
        """Search for a file using heuristics when other methods fail"""
        # Get the filename from the URL
        url = getattr(self, url_field, None)
        if not url:
            return None
        
        filename = url.split("/")[-1]
        
        # Search locations in order of likelihood
        search_paths = [
            Path("tmp"),  # Current tmp directory
            Path.cwd(),  # Current working directory
            Path.home() / "SyftBox" / "datasites",  # Default SyftBox location
        ]
        
        # If we have a base_path, also search relative to it
        if self.base_path:
            base = Path(self.base_path)
            if not base.is_absolute():
                base = Path.cwd() / base
            search_paths.insert(0, base)
            search_paths.append(base.parent)
        
        # Search for the file
        for search_dir in search_paths:
            if search_dir.exists():
                # Direct check
                candidate = search_dir / filename
                if candidate.exists():
                    return candidate.absolute()
                
                # Recursive search (limited depth)
                try:
                    for path in search_dir.rglob(filename):
                        if path.is_file():
                            return path.absolute()
                except:
                    pass
        
        return None
    
    def _update_relative_paths(self):
        """Update relative paths based on current file locations"""
        if not self.base_path:
            return
        
        base = Path(self.base_path)
        if not base.is_absolute():
            base = Path.cwd() / base
        
        # Update relative paths for each URL field
        for url_field in ['private_url', 'mock_url', 'syftobject']:
            resolved_path = self._resolve_path(url_field)
            if resolved_path:
                try:
                    # Calculate relative path from base to file
                    relative_path = os.path.relpath(resolved_path, base)
                    setattr(self, f"{url_field}_relative", relative_path)
                    
                    # Also update absolute fallback
                    setattr(self, f"{url_field}_absolute_fallback", str(resolved_path))
                except:
                    pass
    
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


    def save_yaml(self, file_path: str | Path, create_syftbox_permissions: bool = True, use_relative_paths: bool = None) -> None:
        """Save the syft object to a YAML file with .syftobject.yaml extension and create SyftBox permission files
        
        Args:
            file_path: Path to save the .syftobject.yaml file
            create_syftbox_permissions: Whether to create SyftBox permission files
            use_relative_paths: Whether to use relative paths (None = auto-detect based on existing base_path)
        """
        file_path = Path(file_path).absolute()
        
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
        
        # Handle relative paths
        if use_relative_paths is None:
            # Auto-detect: use relative paths if base_path is already set
            use_relative_paths = self.base_path is not None
        
        if use_relative_paths:
            # Only set base_path if it's not already set
            if not self.base_path:
                # Set base_path to the directory containing the .syftobject.yaml file
                self.base_path = str(file_path.parent)
            # Update relative paths
            self._update_relative_paths()
        
        # Convert to dict and handle datetime/UUID serialization
        data = self.model_dump(mode='json', exclude_none=True)
        
        # Write to YAML file
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True, indent=2)
        
        # Create SyftBox permission files if requested
        if create_syftbox_permissions:
            self._create_syftbox_permissions(file_path)

    @classmethod
    def load_yaml(cls, file_path: str | Path) -> 'SyftObject':
        """Load a syft object from a .syftobject.yaml file"""
        file_path = Path(file_path).absolute()
        
        # Validate that the file has the correct extension
        if not file_path.name.endswith('.syftobject.yaml'):
            raise ValueError(f"File must have .syftobject.yaml extension, got: {file_path.name}")
        
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Auto-detect base path if not specified and if there are relative paths to resolve
        if ('base_path' not in data or data['base_path'] is None) and any(
            key in data for key in ['private_url_relative', 'mock_url_relative', 'syftobject_relative']
        ):
            data['base_path'] = str(file_path.parent)
        
        # Create the object
        obj = cls(**data)
        
        # If we have relative paths but the current base_path doesn't work, try the file's directory
        if obj.base_path and any(getattr(obj, f"{field}_relative", None) for field in ['private_url', 'mock_url', 'syftobject']):
            # Test if the relative paths work from the current base_path
            test_working = False
            for field in ['private_url', 'mock_url']:
                relative_path = getattr(obj, f"{field}_relative", None)
                if relative_path:
                    base = Path(obj.base_path)
                    if not base.is_absolute():
                        base = Path.cwd() / base
                    test_file = base / relative_path
                    if test_file.exists():
                        test_working = True
                        break
            
            # If the original base_path doesn't work, try using the file's directory
            if not test_working:
                # Update base_path to the file's directory and recalculate relative paths
                obj.base_path = str(file_path.parent)
        
        # Update relative paths based on current file locations
        obj._update_relative_paths()
        
        return obj

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