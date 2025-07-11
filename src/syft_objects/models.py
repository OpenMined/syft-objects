"""
Core models for SyftObjects.
"""

import os
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
import syft_perm as sp

def utcnow() -> datetime:
    """Get current UTC datetime"""
    return datetime.utcnow()

def detect_user_email() -> str:
    """Auto-detect the user's email from various sources"""
    email = None
    
    # Try multiple ways to detect logged-in email
    email = os.getenv("SYFTBOX_EMAIL")
    
    if not email:
        # Try to get from SyftBox client config
        config_path = os.path.expanduser("~/.syftbox/config.json")
        if os.path.exists(config_path):
            try:
                import json
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    email = config.get("email")
            except:
                pass
    
    # Default fallback
    if not email:
        email = "unknown@syftbox.local"
    
    return email

class SyftObject(BaseModel):
    """
    Core SyftObject model with file-backed storage and permission management.
    """
    
    # === Core Fields ===
    uid: str  # Unique identifier
    name: str
    description: Optional[str] = None
    object_type: str = "file"  # "file" or "folder"
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    
    # === URLs ===
    mock: Optional[str] = None  # syft:// URL for mock data
    private: Optional[str] = None  # syft:// URL for private data
    syftobject: Optional[str] = None  # syft:// URL for .syftobject.yaml
    
    # === Metadata ===
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # === Internal Fields ===
    _yaml_path: Optional[Path] = None  # Path to .syftobject.yaml file
    
    @property
    def mock_path(self) -> Optional[str]:
        """Get local file path for mock data"""
        if not self.mock:
            return None
        try:
            from .client import SyftBoxURL, SYFTBOX_AVAILABLE, get_syftbox_client
            if SYFTBOX_AVAILABLE:
                client = get_syftbox_client()
                if client:
                    syft_url_obj = SyftBoxURL(self.mock)
                    return str(syft_url_obj.to_local_path(datasites_path=client.datasites))
        except Exception:
            pass
        return None
    
    @property
    def private_path(self) -> Optional[str]:
        """Get local file path for private data"""
        if not self.private:
            return None
        try:
            from .client import SyftBoxURL, SYFTBOX_AVAILABLE, get_syftbox_client
            if SYFTBOX_AVAILABLE:
                client = get_syftbox_client()
                if client:
                    syft_url_obj = SyftBoxURL(self.private)
                    return str(syft_url_obj.to_local_path(datasites_path=client.datasites))
        except Exception:
            pass
        return None
    
    @property
    def syftobject_path(self) -> Optional[str]:
        """Get local file path for .syftobject.yaml"""
        if self._yaml_path:
            return str(self._yaml_path)
        if not self.syftobject:
            return None
        try:
            from .client import SyftBoxURL, SYFTBOX_AVAILABLE, get_syftbox_client
            if SYFTBOX_AVAILABLE:
                client = get_syftbox_client()
                if client:
                    syft_url_obj = SyftBoxURL(self.syftobject)
                    return str(syft_url_obj.to_local_path(datasites_path=client.datasites))
        except Exception:
            pass
        return None
    
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
    
    def _sync_to_disk(self) -> None:
        """Sync object to disk"""
        if not self._yaml_path:
            return
        
        # Create parent directory if it doesn't exist
        self._yaml_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get dict representation excluding private fields
        data = self.dict(exclude={'_yaml_path'})
        
        # Write to file
        with open(self._yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)
    
    def _create_syftbox_permissions(self, file_path: Path) -> None:
        """Create SyftBox permission files for this object"""
        try:
            # Get owner email from metadata or detect from environment
            owner_email = self.metadata.get('email') or detect_user_email()
            
            # Set permissions on the syftobject.yaml file
            sp.set_file_permissions(
                str(file_path),
                read_users=self.metadata.get('_original_permissions', {}).get('discovery_read', ['public']),
                write_users=[owner_email],
                admin_users=[owner_email]
            )
            
            # Set permissions on mock file if it exists
            mock_path = self.mock_path
            if mock_path and Path(mock_path).exists():
                sp.set_file_permissions(
                    mock_path,
                    read_users=self.metadata.get('_original_permissions', {}).get('mock_read', ['public']),
                    write_users=self.metadata.get('_original_permissions', {}).get('mock_write', [owner_email]),
                    admin_users=[owner_email]
                )
            
            # Set permissions on private file if it exists
            private_path = self.private_path
            if private_path and Path(private_path).exists():
                sp.set_file_permissions(
                    private_path,
                    read_users=self.metadata.get('_original_permissions', {}).get('private_read', [owner_email]),
                    write_users=self.metadata.get('_original_permissions', {}).get('private_write', [owner_email]),
                    admin_users=[owner_email]
                )
        except Exception as e:
            print(f"Warning: Could not create SyftBox permission files: {e}")
    
    def delete(self) -> bool:
        """Delete this object and its associated files"""
        try:
            # Delete mock file
            mock_path = self.mock_path
            if mock_path and Path(mock_path).exists():
                Path(mock_path).unlink()
            
            # Delete private file
            private_path = self.private_path
            if private_path and Path(private_path).exists():
                Path(private_path).unlink()
            
            # Delete syftobject.yaml file
            syftobj_path = self.syftobject_path
            if syftobj_path and Path(syftobj_path).exists():
                Path(syftobj_path).unlink()
            
            return True
        except Exception as e:
            print(f"Warning: Error deleting object: {e}")
            return False