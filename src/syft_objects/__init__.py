# syft-objects - Distributed file discovery and addressing system 

import os
import shutil
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, List, Union
from uuid import UUID, uuid4
import time
import hashlib

from pydantic import BaseModel, Field

# Try to import SyftBox client for proper file management
try:
    from syft_core import Client as SyftBoxClient
    from syft_core.url import SyftBoxURL
    SYFTBOX_AVAILABLE = True
except ImportError:
    SyftBoxClient = None
    SyftBoxURL = None
    SYFTBOX_AVAILABLE = False


def _utcnow():
    """Get current UTC timestamp"""
    return datetime.now(tz=timezone.utc)


class SyftObject(BaseModel):
    """
    A distributed object with mock/real pattern for file discovery and addressing
    """
    # Mandatory metadata
    uid: UUID = Field(default_factory=uuid4, description="Unique identifier for the object")
    private: str = Field(description="Syft:// path to the private object")
    mock: str = Field(description="Syft:// path to the public/mock object")
    created_at: datetime = Field(default_factory=_utcnow, description="Creation timestamp")
    
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
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    
    def _repr_html_(self) -> str:
        """Rich HTML representation for Jupyter notebooks"""
        return self._create_html_display()
    
    def _create_html_display(self) -> str:
        """Create a beautiful HTML display for the SyftObject"""
        # Get file operations info from metadata if available
        file_ops = self.metadata.get("_file_operations", {})
        files_moved = file_ops.get("files_moved_to_syftbox", [])
        created_files = file_ops.get("created_files", [])
        syftbox_available = file_ops.get("syftbox_available", False)
        syftobject_yaml_path = file_ops.get("syftobject_yaml_path")
        
        # Check if files exist locally
        mock_file_exists = self._check_file_exists(self.mock)
        private_file_exists = self._check_file_exists(self.private)
        
        # Permission badge colors
        def permission_badge(users, perm_type="read"):
            if not users:
                return '<span class="syft-badge syft-badge-none">None</span>'
            elif "public" in users or "*" in users:
                return '<span class="syft-badge syft-badge-public">Public</span>'
            elif len(users) == 1:
                return f'<span class="syft-badge syft-badge-user">{users[0]}</span>'
            else:
                return f'<span class="syft-badge syft-badge-multiple">{len(users)} users</span>'
        
        # File status badges
        def file_badge(exists, url, file_type="file"):
            if exists:
                return '<span class="syft-badge syft-badge-available">✓ Available</span>'
            else:
                return '<span class="syft-badge syft-badge-unavailable">⚠ Not accessible</span>'
        
        # Generate metadata rows
        updated_row = ""
        if self.updated_at:
            updated_row = f'<div class="syft-meta-row"><span class="syft-meta-key">Updated</span><span class="syft-meta-value">{self.updated_at.strftime("%Y-%m-%d %H:%M UTC")}</span></div>'
        
        description_row = ""
        if self.description:
            description_row = f'<div class="syft-meta-row"><span class="syft-meta-key">Description</span><span class="syft-meta-value">{str(self.description)}</span></div>'
        
        # Show basic file information without buttons
        mock_info = ""
        if mock_file_exists:
            mock_path = self._get_local_file_path(self.mock)
            if mock_path:
                mock_info = f'<div class="syft-file-info">Path: {mock_path}</div>'
        
        private_info = ""
        if private_file_exists:
            private_path = self._get_local_file_path(self.private)
            if private_path:
                private_info = f'<div class="syft-file-info">Path: {private_path}</div>'
        
        html = f'''
        <style>
        .syft-object {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            border: 2px solid #e0e7ff;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        .syft-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .syft-title {{
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin: 0;
            flex-grow: 1;
        }}
        .syft-uid {{
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 12px;
            color: #64748b;
            background: #f1f5f9;
            padding: 4px 8px;
            border-radius: 6px;
        }}
        .syft-section {{
            margin-bottom: 20px;
        }}
        .syft-section-title {{
            font-size: 16px;
            font-weight: 600;
            color: #374151;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        }}
        .syft-section-title::before {{
            content: '';
            width: 4px;
            height: 20px;
            background: #3b82f6;
            margin-right: 10px;
            border-radius: 2px;
        }}
        .syft-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
                 .syft-files {{
             display: grid;
             grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
             gap: 15px;
         }}
        .syft-file-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}
        .syft-file-header {{
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .syft-file-type {{
            font-weight: 600;
            color: #374151;
        }}
        .syft-file-url {{
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 11px;
            color: #6b7280;
            word-break: break-all;
            margin: 8px 0;
            background: #f9fafb;
            padding: 6px 8px;
            border-radius: 4px;
        }}
        .syft-permissions {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }}
        .syft-perm-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e5e7eb;
        }}
        .syft-perm-label {{
            font-weight: 500;
            font-size: 13px;
            color: #374151;
        }}
        .syft-badge {{
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
        }}
        .syft-badge-public {{
            background: #dcfce7;
            color: #166534;
        }}
        .syft-badge-user {{
            background: #dbeafe;
            color: #1d4ed8;
        }}
        .syft-badge-multiple {{
            background: #fef3c7;
            color: #92400e;
        }}
        .syft-badge-none {{
            background: #fee2e2;
            color: #dc2626;
        }}
        .syft-badge-available {{
            background: #dcfce7;
            color: #166534;
        }}
        .syft-badge-unavailable {{
            background: #fef3c7;
            color: #92400e;
        }}
                          .syft-file-info {{
             font-family: 'Monaco', 'Menlo', monospace;
             font-size: 11px;
             color: #6b7280;
             margin-top: 8px;
             padding: 6px 8px;
             background: #f9fafb;
             border-radius: 4px;
             word-break: break-all;
         }}
         .syft-metadata-file {{
             border-left: 3px solid #8b5cf6;
         }}
         .syft-metadata-file .syft-file-type {{
             color: #8b5cf6;
         }}
        .syft-metadata {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
        }}
        .syft-meta-row {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid #f3f4f6;
        }}
        .syft-meta-row:last-child {{
            border-bottom: none;
        }}
        .syft-meta-key {{
            font-weight: 500;
            color: #374151;
        }}
        .syft-meta-value {{
            color: #6b7280;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 12px;
        }}
        .syft-file-ops {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px;
            margin-top: 10px;
        }}
        .syft-file-ops-title {{
            font-weight: 600;
            color: #374151;
            font-size: 13px;
            margin-bottom: 8px;
        }}
                 .syft-file-ops-list {{
             font-size: 11px;
             color: #6b7280;
             font-family: 'Monaco', 'Menlo', monospace;
         }}
         </style>
        
        <div class="syft-object">
            <div class="syft-header">
                <h3 class="syft-title">🔐 {self.name or 'Syft Object'}</h3>
                <span class="syft-uid">{str(self.uid)[:8]}...</span>
            </div>
            
            <div class="syft-grid">
                                <div class="syft-section">
                    <div class="syft-section-title">📁 Files</div>
                    <div class="syft-files">
                        <div class="syft-file-card">
                            <div class="syft-file-header">
                                <span class="syft-file-type">🔍 Mock (Demo)</span>
                                {file_badge(mock_file_exists, self.mock)}
                            </div>
                            <div class="syft-file-url">{self.mock}</div>
                            {mock_info}
                        </div>
                        
                        <div class="syft-file-card">
                            <div class="syft-file-header">
                                <span class="syft-file-type">🔐 Private (Real)</span>
                                {file_badge(private_file_exists, self.private)}
                            </div>
                            <div class="syft-file-url">{self.private}</div>
                            {private_info}
                        </div>
                        
                        <div class="syft-file-card syft-metadata-file">
                            <div class="syft-file-header">
                                <span class="syft-file-type">📋 Metadata (.syftobject.yaml)</span>
                                <span class="syft-badge syft-badge-available">✓ Saved</span>
                            </div>
                            <div class="syft-file-url">Object metadata and permissions</div>
                            {f'<div class="syft-file-info">Path: {syftobject_yaml_path}</div>' if syftobject_yaml_path else ''}
                        </div>
                    </div>
                </div>
                
                <div class="syft-section">
                    <div class="syft-section-title">🎯 Permissions</div>
                    <div class="syft-permissions">
                        <div class="syft-perm-row">
                            <span class="syft-perm-label">Discovery</span>
                            {permission_badge(self.syftobject_permissions)}
                        </div>
                        <div class="syft-perm-row">
                            <span class="syft-perm-label">Mock Read</span>
                            {permission_badge(self.mock_permissions)}
                        </div>
                        <div class="syft-perm-row">
                            <span class="syft-perm-label">Mock Write</span>
                            {permission_badge(self.mock_write_permissions)}
                        </div>
                        <div class="syft-perm-row">
                            <span class="syft-perm-label">Private Read</span>
                            {permission_badge(self.private_permissions)}
                        </div>
                        <div class="syft-perm-row">
                            <span class="syft-perm-label">Private Write</span>
                            {permission_badge(self.private_write_permissions)}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="syft-section">
                <div class="syft-section-title">📋 Metadata</div>
                <div class="syft-metadata">
                                         <div class="syft-meta-row">
                         <span class="syft-meta-key">Created</span>
                         <span class="syft-meta-value">{self.created_at.strftime('%Y-%m-%d %H:%M UTC') if self.created_at else 'Unknown'}</span>
                     </div>
                     {updated_row}
                     {description_row}
                     {self._render_custom_metadata()}
                </div>
                
                {self._render_file_operations(files_moved, created_files, syftbox_available)}
            </div>
        </div>
        '''
        
        return html
    
    def _render_custom_metadata(self) -> str:
        """Render custom metadata fields (excluding system fields)"""
        system_fields = {"_file_operations"}
        custom_metadata = {k: v for k, v in self.metadata.items() if k not in system_fields}
        
        if not custom_metadata:
            return ""
        
        html = ""
        for key, value in custom_metadata.items():
            html += f'''
            <div class="syft-meta-row">
                <span class="syft-meta-key">{key}</span>
                <span class="syft-meta-value">{str(value)}</span>
            </div>
            '''
        return html
    
    def _render_file_operations(self, files_moved, created_files, syftbox_available) -> str:
        """Render file operations section"""
        if not files_moved and not created_files:
            return ""
        
        status_icon = "✅" if syftbox_available else "⚠️"
        status_text = "SyftBox Integration Active" if syftbox_available else "SyftBox Not Available"
        
        ops_html = f'''
        <div class="syft-file-ops">
            <div class="syft-file-ops-title">{status_icon} File Operations - {status_text}</div>
            <div class="syft-file-ops-list">
        '''
        
        if files_moved:
            ops_html += "Moved to SyftBox locations:<br>"
            for move_info in files_moved:
                ops_html += f"  • {move_info}<br>"
        
        if created_files and not files_moved:
            ops_html += "Created in tmp/ directory:<br>"
            for file_path in created_files:
                ops_html += f"  • {file_path}<br>"
            if not syftbox_available:
                ops_html += "  (Install syft-core for SyftBox integration)<br>"
        
        ops_html += "</div></div>"
        return ops_html
    
    def _check_file_exists(self, syft_url: str) -> bool:
        """Check if a file exists locally (for display purposes)"""
        try:
            if SYFTBOX_AVAILABLE:
                syftbox_client = _get_syftbox_client()
                if syftbox_client:
                    from syft_core.url import SyftBoxURL
                    syft_url_obj = SyftBoxURL(syft_url)
                    local_path = syft_url_obj.to_local_path(datasites_path=syftbox_client.datasites)
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
            if SYFTBOX_AVAILABLE:
                syftbox_client = _get_syftbox_client()
                if syftbox_client:
                    from syft_core.url import SyftBoxURL
                    syft_url_obj = SyftBoxURL(syft_url)
                    local_path = syft_url_obj.to_local_path(datasites_path=syftbox_client.datasites)
                    if local_path.exists():
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
    def load_yaml(cls, file_path: str | Path) -> 'SyftObject':
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
        self._create_syftpub_file(
            target_path=syftobject_file_path.parent,
            file_pattern=syftobject_file_path.name,
            read_users=self.syftobject_permissions,
            write_users=[]  # Discovery files are read-only
        )
        
        # Create permissions for mock and private paths (if they are local paths)
        mock_path = self._extract_local_path_from_syft_url(self.mock)
        if mock_path:
            self._create_syftpub_file(
                target_path=mock_path.parent,
                file_pattern=mock_path.name,
                read_users=self.mock_permissions,
                write_users=self.mock_write_permissions
            )
        
        private_path = self._extract_local_path_from_syft_url(self.private)
        if private_path:
            self._create_syftpub_file(
                target_path=private_path.parent,
                file_pattern=private_path.name,
                read_users=self.private_permissions,
                write_users=self.private_write_permissions
            )

    def _extract_local_path_from_syft_url(self, syft_url: str) -> Optional[Path]:
        """Extract local path from a syft:// URL if it points to a local SyftBox path"""
        if not SYFTBOX_AVAILABLE:
            return None
        
        try:
            # Try to get SyftBox client and convert URL to local path
            client = SyftBoxClient.load()
            syft_url_obj = SyftBoxURL(syft_url)
            return syft_url_obj.to_local_path(datasites_path=client.datasites)
        except Exception:
            return None

    def _create_syftpub_file(self, target_path: Path, file_pattern: str, 
                             read_users: list[str], write_users: list[str]) -> None:
        """Create a syft.pub.yaml file with the correct SyftBox format"""
        # Ensure target directory exists
        target_path.mkdir(parents=True, exist_ok=True)
        syftpub_path = target_path / "syft.pub.yaml"
        
        # Create the access dictionary based on permissions and users
        access_dict = {}
        
        # Convert read users to SyftBox format
        if read_users:
            formatted_read_users = []
            for user in read_users:
                if user in ["public", "*"]:
                    formatted_read_users.append("*")
                else:
                    formatted_read_users.append(user)
            if formatted_read_users:
                access_dict["read"] = formatted_read_users
        
        # Convert write users to SyftBox format
        if write_users:
            formatted_write_users = []
            for user in write_users:
                if user in ["public", "*"]:
                    formatted_write_users.append("*")
                else:
                    formatted_write_users.append(user)
            if formatted_write_users:
                access_dict["write"] = formatted_write_users
                # Users who can write typically also get admin permissions
                access_dict["admin"] = formatted_write_users
        
        # If no permissions specified, default to empty (no access)
        if not access_dict:
            return
        
        # Create the rule for this file pattern  
        new_rule = {
            "pattern": "**" if file_pattern == "**" else file_pattern,
            "access": access_dict
        }
        
        # Read existing syft.pub.yaml file if it exists
        existing_content = {"rules": []}
        if syftpub_path.exists():
            try:
                with open(syftpub_path, 'r') as f:
                    existing_content = yaml.safe_load(f) or {"rules": []}
            except Exception as e:
                print(f"Warning: Could not read existing syft.pub.yaml: {e}")
                existing_content = {"rules": []}
        
        # Ensure rules is a list
        if "rules" not in existing_content:
            existing_content["rules"] = []
        elif not isinstance(existing_content["rules"], list):
            existing_content["rules"] = []
        
        # Remove any existing rules for this pattern to avoid duplicates
        existing_content["rules"] = [
            rule for rule in existing_content["rules"] 
            if rule.get("pattern") != new_rule["pattern"]
        ]
        
        # Add the new rule
        existing_content["rules"].append(new_rule)
        
        # Write the updated syft.pub.yaml file
        with open(syftpub_path, 'w') as f:
            yaml.dump(existing_content, f, default_flow_style=False, sort_keys=False, indent=2)


def _get_syftbox_client() -> Optional[SyftBoxClient]:
    """Get SyftBox client if available, otherwise return None"""
    if not SYFTBOX_AVAILABLE:
        return None
    try:
        return SyftBoxClient.load()
    except Exception:
        return None


def _move_file_to_syftbox_location(local_file: Path, syft_url: str, syftbox_client: Optional[SyftBoxClient] = None) -> bool:
    """Move a local file to the location specified by a syft:// URL"""
    if not SYFTBOX_AVAILABLE or not syftbox_client:
        return False
    
    try:
        syft_url_obj = SyftBoxURL(syft_url)
        target_path = syft_url_obj.to_local_path(datasites_path=syftbox_client.datasites)
        
        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move the file
        shutil.move(str(local_file), str(target_path))
        return True
    except Exception as e:
        print(f"Warning: Could not move file to SyftBox location: {e}")
        return False


def _copy_file_to_syftbox_location(local_file: Path, syft_url: str, syftbox_client: Optional[SyftBoxClient] = None) -> bool:
    """Copy a local file to the location specified by a syft:// URL"""
    if not SYFTBOX_AVAILABLE or not syftbox_client:
        return False
    
    try:
        syft_url_obj = SyftBoxURL(syft_url)
        target_path = syft_url_obj.to_local_path(datasites_path=syftbox_client.datasites)
        
        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(str(local_file), str(target_path))
        return True
    except Exception as e:
        print(f"Warning: Could not copy file to SyftBox location: {e}")
        return False


def _generate_syftbox_urls(email: str, filename: str, syftbox_client: Optional[SyftBoxClient] = None) -> tuple[str, str]:
    """Generate proper syft:// URLs for private and mock files"""
    if syftbox_client:
        # Generate URLs that point to actual SyftBox structure
        private_url = f"syft://{email}/private/objects/{filename}"
        mock_url = f"syft://{email}/public/objects/{filename}"
    else:
        # Fallback to generic URLs
        private_url = f"syft://{email}/SyftBox/datasites/{email}/private/objects/{filename}"
        mock_url = f"syft://{email}/SyftBox/datasites/{email}/public/objects/{filename}"
    
    return private_url, mock_url


def syobj(
    name: Optional[str] = None,
    *,  # Force keyword-only arguments after this
    mock_contents: Optional[str] = None,
    private_contents: Optional[str] = None,
    mock_file: Optional[str] = None,
    private_file: Optional[str] = None,
    discovery_read: Optional[list[str]] = None,
    mock_read: Optional[list[str]] = None,
    mock_write: Optional[list[str]] = None,
    private_read: Optional[list[str]] = None,
    private_write: Optional[list[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> SyftObject:
    """
    🔐 **Share files with explicit mock vs private control** 
    
    ┌─────────────────────────────────────────────────────────────┐
    │  EXAMPLES - Direct & Practical                             │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  🚀 BASIC USAGE:                                           │
    │     syobj(                                                  │
    │         name="AI Results",                                  │
    │         mock_contents="Model achieved good performance",    │
    │         private_contents="Accuracy: 94.5%, Cost: $127"     │
    │     )                                                       │
    │                                                             │
    │  📁 FILE CONTROL:                                          │
    │     syobj(                                                  │
    │         name="Customer Data",                               │
    │         mock_file="sample_100_rows.csv",      # Demo file  │
    │         private_file="full_50k_rows.csv"      # Real file  │
    │     )                                                       │
    │                                                             │
    │  🎯 PERMISSION CONTROL:                                     │
    │     syobj(                                                  │
    │         name="Financial Report",                            │
    │         mock_contents="Q4 Summary: Revenue up 10%",        │
    │         private_contents="Q4: $2.5M revenue, $400K...",    │
    │         discovery_read=["public"],           # Who knows it │
    │         mock_read=["employee@company.com"],  # Who sees demo│
    │         private_read=["cfo@company.com"]     # Who sees real│
    │     )                                                       │
    │                                                             │
    │  ⚙️ METADATA OPTIONS:                                      │
    │     syobj(                                                  │
    │         name="Production Model",                            │
    │         mock_contents="Model ready",                        │
    │         metadata={"version": "2.1", "author": "ML Team"}   │
    │     )                                                       │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
    
    **PARAMETERS:**
    
    name: Object name
    mock_contents: What everyone sees (demo version)
    private_contents: What authorized users see (real data)
    mock_file: Demo file path
    private_file: Real file path
    discovery_read: Who knows it exists (default: ["public"])
    mock_read: Who sees demo (default: ["public"])
    mock_write: Who edits demo (default: [])
    private_read: Who sees real data (default: [your_email])
    private_write: Who edits real data (default: [your_email])
    metadata: Optional settings & custom fields
    
    **You control exactly what goes where. No surprises.**
    """
    import os
    import hashlib
    from pathlib import Path
    
    # === SETUP ===
    if metadata is None:
        metadata = {}
    
    # Extract optional settings from metadata with defaults
    description = metadata.get("description")
    save_to = metadata.get("save_to")
    email = metadata.get("email")
    create_syftbox_permissions = metadata.get("create_syftbox_permissions", True)
    auto_save = metadata.get("auto_save", True)
    move_files_to_syftbox = metadata.get("move_files_to_syftbox", True)
    
    # Create clean metadata dict for the SyftObject (exclude system settings)
    system_keys = {"description", "save_to", "email", "create_syftbox_permissions", "auto_save", "move_files_to_syftbox"}
    clean_metadata = {k: v for k, v in metadata.items() if k not in system_keys}
    
    # === CREATE TEMP DIRECTORY ===
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    # === SYFTBOX CLIENT SETUP ===
    syftbox_client = _get_syftbox_client()
    
    # === EMAIL AUTO-DETECTION ===
    if email is None:
        # Try multiple ways to detect logged-in email
        email = os.getenv("SYFTBOX_EMAIL")
        if not email and syftbox_client:
            try:
                email = str(syftbox_client.email)
            except:
                pass
        if not email:
            # Check SyftBox config file
            home = Path.home()
            syftbox_config = home / ".syftbox" / "config.yaml"
            if syftbox_config.exists():
                try:
                    import yaml
                    with open(syftbox_config) as f:
                        config = yaml.safe_load(f)
                        email = config.get("email")
                except:
                    pass
        if not email:
            # Try git config as fallback
            try:
                import subprocess
                result = subprocess.run(["git", "config", "user.email"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    email = result.stdout.strip()
            except:
                pass
        if not email:
            email = "user@example.com"  # Final fallback
    
    # === VALIDATE INPUT ===
    has_mock_content = mock_contents is not None or mock_file is not None
    has_private_content = private_contents is not None or private_file is not None
    
    if not has_mock_content and not has_private_content:
        # Auto-generate minimal object
        unique_hash = hashlib.md5(f"{time.time()}_{os.getpid()}".encode()).hexdigest()[:8]
        if name is None:
            name = f"Auto Object {unique_hash}"
        auto_content = f"Auto-generated content for {name} (created at {datetime.now().isoformat()})"
        mock_contents = f"[DEMO] {auto_content[:50]}..."
        private_contents = auto_content
    
    # === AUTO-GENERATE NAME ===
    if name is None:
        if mock_contents or private_contents:
            content_sample = (mock_contents or private_contents or "")[:20]
            content_hash = hashlib.md5(content_sample.encode()).hexdigest()[:8]
            name = f"Content {content_hash}"
        elif mock_file or private_file:
            file_path = Path(mock_file or private_file)
            name = file_path.stem.replace("_", " ").title()
        else:
            name = "Syft Object"
    
    # === DETERMINE BASE FILENAME ===
    base_filename = f"{name.lower().replace(' ', '_')}.txt"
    
    created_files = []  # Track files we create for cleanup/reference
    files_moved_to_syftbox = []  # Track files moved to SyftBox
    
    # === HANDLE PRIVATE CONTENT/FILE ===
    if private_contents is not None:
        # Create private file from content
        private_filename = base_filename
        private_file_path = tmp_dir / private_filename
        private_file_path.write_text(private_contents)
        created_files.append(private_file_path)
        private_source_path = private_file_path
    elif private_file is not None:
        # Use existing private file
        private_source_path = Path(private_file)
        if not private_source_path.exists():
            raise FileNotFoundError(f"Private file not found: {private_file}")
        private_filename = private_source_path.name
    else:
        # No private data specified - create auto-generated content
        private_filename = base_filename
        private_file_path = tmp_dir / private_filename
        private_file_path.write_text(f"Auto-generated private content for {name}")
        created_files.append(private_file_path)
        private_source_path = private_file_path
    
    # === HANDLE MOCK CONTENT/FILE ===
    if mock_contents is not None:
        # Create mock file from content
        mock_filename = f"{Path(base_filename).stem}_mock{Path(base_filename).suffix}"
        mock_file_path = tmp_dir / mock_filename
        mock_file_path.write_text(mock_contents)
        created_files.append(mock_file_path)
        mock_source_path = mock_file_path
    elif mock_file is not None:
        # Use existing mock file
        mock_source_path = Path(mock_file)
        if not mock_source_path.exists():
            raise FileNotFoundError(f"Mock file not found: {mock_file}")
        mock_filename = mock_source_path.name
    else:
        # No mock data specified - auto-generate from private or create generic
        mock_filename = f"{Path(base_filename).stem}_mock{Path(base_filename).suffix}"
        mock_file_path = tmp_dir / mock_filename
        
        if private_contents:
            # Create mock from private content (truncated)
            mock_content = private_contents[:50] + "..." if len(private_contents) > 50 else private_contents
            mock_file_path.write_text(f"[MOCK DATA] {mock_content}")
        elif private_file and private_source_path.exists():
            # Create mock from private file
            try:
                original_content = private_source_path.read_text()
                mock_content = original_content[:50] + "..." if len(original_content) > 50 else original_content
                mock_file_path.write_text(f"[MOCK DATA] {mock_content}")
            except:
                # Binary file - create simple mock
                mock_file_path.write_text(f"[MOCK DATA] Binary file: {private_source_path.name}")
        else:
            # Generic mock
            mock_file_path.write_text(f"[MOCK DATA] Demo version of {name}")
        
        created_files.append(mock_file_path)
        mock_source_path = mock_file_path
    
    # === GENERATE SYFT:// URLS ===
    final_private_path, _ = _generate_syftbox_urls(email, private_filename, syftbox_client)
    final_mock_path, _ = _generate_syftbox_urls(email, mock_filename, syftbox_client)
    
    # === MOVE FILES TO SYFTBOX LOCATIONS ===
    if move_files_to_syftbox and syftbox_client:
        # Handle private file
        if private_file and private_source_path != Path(private_file):
            # We created the file, so move it
            if _move_file_to_syftbox_location(private_source_path, final_private_path, syftbox_client):
                files_moved_to_syftbox.append(f"{private_source_path} → {final_private_path}")
        elif private_file:
            # Copy existing file
            if _copy_file_to_syftbox_location(private_source_path, final_private_path, syftbox_client):
                files_moved_to_syftbox.append(f"{private_source_path} → {final_private_path}")
        else:
            # Move created file
            if _move_file_to_syftbox_location(private_source_path, final_private_path, syftbox_client):
                files_moved_to_syftbox.append(f"{private_source_path} → {final_private_path}")
        
        # Handle mock file
        if mock_file and mock_source_path != Path(mock_file):
            # We created the file, so move it
            if _move_file_to_syftbox_location(mock_source_path, final_mock_path, syftbox_client):
                files_moved_to_syftbox.append(f"{mock_source_path} → {final_mock_path}")
        elif mock_file:
            # Copy existing file
            if _copy_file_to_syftbox_location(mock_source_path, final_mock_path, syftbox_client):
                files_moved_to_syftbox.append(f"{mock_source_path} → {final_mock_path}")
        else:
            # Move created file
            if _move_file_to_syftbox_location(mock_source_path, final_mock_path, syftbox_client):
                files_moved_to_syftbox.append(f"{mock_source_path} → {final_mock_path}")
    
    # === PERMISSION HANDLING ===
    final_discovery_read = discovery_read or ["public"]
    final_mock_read = mock_read or ["public"]
    final_mock_write = mock_write or []
    final_private_read = private_read or [email]
    final_private_write = private_write or [email]
    
    # === AUTO-GENERATE DESCRIPTION ===
    if description is None:
        if mock_contents or private_contents:
            description = f"Object '{name}' with explicit mock and private content"
        elif mock_file or private_file:
            description = f"Object '{name}' with explicit mock and private files"
        else:
            description = f"Auto-generated object: {name}"
    
    # === CREATE SYFT OBJECT ===
    syft_obj = SyftObject(
        private=final_private_path,
        mock=final_mock_path,
        name=name,
        description=description,
        updated_at=_utcnow(),
        metadata=clean_metadata,
        syftobject_permissions=final_discovery_read,
        mock_permissions=final_mock_read,
        mock_write_permissions=final_mock_write,
        private_permissions=final_private_read,
        private_write_permissions=final_private_write
    )
    
    # === TRACK FILE OPERATIONS (for HTML display) ===
    # Store file operation info in syft object metadata for display
    file_operations = {
        "files_moved_to_syftbox": files_moved_to_syftbox,
        "created_files": [str(f) for f in created_files],
        "syftbox_available": bool(syftbox_client and SYFTBOX_AVAILABLE),
        "syftobject_yaml_path": None  # Will be set during save
    }
    clean_metadata["_file_operations"] = file_operations
    
    # === AUTO-SAVE ===
    if auto_save:
        # Determine save location - start in tmp directory for cleanliness
        if save_to:
            save_path = save_to
        else:
            # Auto-generate from object name and save in tmp directory initially
            safe_name = name.lower().replace(" ", "_").replace("-", "_")
            save_path = tmp_dir / f"{safe_name}.syftobject.yaml"
        
        # Save the syftobject.yaml file (initially creates permissions for temp location)
        syft_obj.save_yaml(save_path, create_syftbox_permissions=False)  # Don't create permissions yet
        
        # Move .syftobject.yaml file to SyftBox location if available
        final_syftobj_path = save_path
        if move_files_to_syftbox and syftbox_client and not str(save_path).startswith("syft://"):
            # Generate syft:// URL for the syftobject.yaml file (typically in public discovery area)
            syftobj_filename = Path(save_path).name
            syftobj_url = f"syft://{email}/public/objects/{syftobj_filename}"
            
            if _move_file_to_syftbox_location(Path(save_path), syftobj_url, syftbox_client):
                files_moved_to_syftbox.append(f"{save_path} → {syftobj_url}")
                
                # Update the final path to the SyftBox location for permission creation
                if SYFTBOX_AVAILABLE:
                    try:
                        syft_url_obj = SyftBoxURL(syftobj_url)
                        final_syftobj_path = syft_url_obj.to_local_path(datasites_path=syftbox_client.datasites)
                    except:
                        pass
        
        # Track the final syftobject.yaml file path for display
        clean_metadata["_file_operations"]["syftobject_yaml_path"] = str(final_syftobj_path)
        
        # Update the syft object's metadata with the file operations info
        syft_obj.metadata.update(clean_metadata)
        
        # Create SyftBox permission files in the final location
        if create_syftbox_permissions:
            syft_obj._create_syftbox_permissions(Path(final_syftobj_path))
    
    return syft_obj


# syobj() is the only function - clean and simple!


# === UTILITY FUNCTIONS ===
def check_permission(user_email: str, allowed_users: list[str]) -> bool:
    """
    Check if a user has permission to access a resource
    
    Args:
        user_email: The email of the user requesting access
        allowed_users: List of users/groups allowed to access the resource
                      "public" means everyone can access
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    if not allowed_users:  # Empty list means no access
        return False
    
    if "public" in allowed_users:  # Public access
        return True
    
    if user_email in allowed_users:  # User explicitly allowed
        return True
    
    # Could extend this to handle groups, wildcards, etc.
    return False


def filter_objects_by_permission(objects: list[SyftObject], user_email: str, 
                                permission_type: str = "syftobject") -> list[SyftObject]:
    """
    Filter syft objects based on user permissions
    
    Args:
        objects: List of SyftObject instances
        user_email: Email of the user requesting access
        permission_type: Type of permission to check ("syftobject", "mock", "private")
    
    Returns:
        List of objects the user has permission to access
    """
    filtered = []
    
    for obj in objects:
        if permission_type == "syftobject":
            permissions = obj.syftobject_permissions
        elif permission_type == "mock":
            permissions = obj.mock_permissions
        elif permission_type == "private":
            permissions = obj.private_permissions
        else:
            raise ValueError(f"Invalid permission type: {permission_type}")
        
        if check_permission(user_email, permissions):
            filtered.append(obj)
    
    return filtered


def scan_for_syft_objects(directory: str | Path, recursive: bool = True) -> list[Path]:
    """
    Scan a directory for .syftobject.yaml files
    
    Args:
        directory: Directory to scan
        recursive: Whether to scan subdirectories recursively
    
    Returns:
        List of paths to .syftobject.yaml files
    """
    directory = Path(directory)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    if recursive:
        return list(directory.rglob("*.syftobject.yaml"))
    else:
        return list(directory.glob("*.syftobject.yaml"))


def load_syft_objects_from_directory(directory: str | Path, recursive: bool = True) -> list[SyftObject]:
    """
    Load all syft objects from a directory
    
    Args:
        directory: Directory to scan
        recursive: Whether to scan subdirectories recursively
    
    Returns:
        List of loaded SyftObject instances
    """
    syft_files = scan_for_syft_objects(directory, recursive)
    objects = []
    
    for file_path in syft_files:
        try:
            obj = SyftObject.load_yaml(file_path)
            objects.append(obj)
        except Exception as e:
            print(f"Warning: Failed to load {file_path}: {e}")
    
    return objects


def create_syftbox_permissions_for_existing_object(syftobject_file_path: str | Path) -> None:
    """
    Create SyftBox permission files for an existing .syftobject.yaml file
    
    Args:
        syftobject_file_path: Path to the existing .syftobject.yaml file
    """
    obj = SyftObject.load_yaml(syftobject_file_path)
    obj._create_syftbox_permissions(Path(syftobject_file_path))

