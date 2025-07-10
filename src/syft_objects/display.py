# syft-objects display - HTML rendering and rich display functionality

from typing import TYPE_CHECKING
import html
from pathlib import Path

if TYPE_CHECKING:
    from .models import SyftObject


def create_html_display(syft_obj: 'SyftObject') -> str:
    """Create a beautiful HTML display for the SyftObject"""
    # Try to use the new single object viewer if server is available
    try:
        import requests
        from .client import get_syft_objects_url
        
        # Check if server is available
        base_url = get_syft_objects_url()
        health_response = requests.get(f"{base_url}/health", timeout=0.5)
        
        if health_response.status_code == 200:
            # Server is available, return iframe to the single object viewer
            viewer_url = f"{base_url}/api/object/{syft_obj.uid}/view"
            return f'''
            <div style="width: 100%; height: 420px; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
                <iframe src="{viewer_url}" style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
            '''
    except:
        # Server not available, fall back to static display
        pass
    
    # Generate the static display that matches the localhost version
    return create_static_display(syft_obj)


def create_static_display(syft_obj: 'SyftObject') -> str:
    """Create a static HTML display that matches the localhost viewer's appearance"""
    
    # Import accessor classes
    from .accessors import MockAccessor, PrivateAccessor, SyftObjectConfigAccessor
    
    # Get basic object info
    name = syft_obj.name or 'Syft Object'
    uid = str(syft_obj.uid)
    description = syft_obj.description or ''
    created_at = syft_obj.created_at.strftime('%Y-%m-%d %H:%M UTC') if syft_obj.created_at else 'Unknown'
    updated_at = syft_obj.updated_at.strftime('%Y-%m-%d %H:%M UTC') if syft_obj.updated_at else 'Unknown'
    
    # Get file type and owner
    file_type = syft_obj.file_type or 'Unknown'
    object_type = 'Folder' if syft_obj.is_folder else 'File'
    
    # Extract owner email
    owner_email = 'Unknown'
    if syft_obj.metadata.get('owner_email'):
        owner_email = syft_obj.metadata['owner_email']
    elif syft_obj.metadata.get('email'):
        owner_email = syft_obj.metadata['email']
    else:
        # Try to extract from URL
        try:
            parts = syft_obj.private_url.split('/')
            if len(parts) > 2 and '@' in parts[2]:
                owner_email = parts[2]
        except:
            pass
    
    # Get mock note
    mock_note = syft_obj.metadata.get('mock_note', '')
    
    # Get file paths
    mock_path = syft_obj.mock_path or 'Not found'
    private_path = syft_obj.private_path or 'Not found'
    syftobject_path = syft_obj.syftobject_path or 'Not found'
    
    # Check file existence
    mock_exists = syft_obj._check_file_exists(syft_obj.mock_url)
    private_exists = syft_obj._check_file_exists(syft_obj.private_url)
    
    # Check if paths point to folders or files
    mock_is_folder = False
    private_is_folder = False
    
    if mock_exists and mock_path != 'Not found':
        mock_is_folder = Path(mock_path).is_dir() if Path(mock_path).exists() else False
    
    if private_exists and private_path != 'Not found':
        private_is_folder = Path(private_path).is_dir() if Path(private_path).exists() else False
    
    # Get file/folder previews
    mock_preview = ''
    private_preview = ''
    
    # Handle mock preview
    if mock_exists and mock_path != 'Not found':
        if mock_is_folder:
            # For folders, show iframe to editor
            mock_preview = f'''
            <div class="syft-folder-editor">
                <div style="margin-bottom: 8px; font-size: 12px; color: #6b7280;">📁 Folder contents (editable):</div>
                <iframe src="http://localhost:8004/editor?path={mock_path}" 
                        style="width: 100%; height: 400px; border: 1px solid #e5e7eb; border-radius: 6px;">
                </iframe>
            </div>
            '''
        else:
            # For files, show text preview
            try:
                with open(mock_path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    mock_preview = html.escape(content)
                    if len(content) == 500:
                        mock_preview += '...'
            except:
                mock_preview = 'Unable to read file content'
    
    # Handle private preview
    if private_exists and private_path != 'Not found':
        if private_is_folder:
            # For folders, show iframe to editor
            private_preview = f'''
            <div class="syft-folder-editor">
                <div style="margin-bottom: 8px; font-size: 12px; color: #6b7280;">📁 Folder contents (editable):</div>
                <iframe src="http://localhost:8004/editor?path={private_path}" 
                        style="width: 100%; height: 400px; border: 1px solid #e5e7eb; border-radius: 6px;">
                </iframe>
            </div>
            '''
        else:
            # For files, show text preview
            try:
                with open(private_path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    private_preview = html.escape(content)
                    if len(content) == 500:
                        private_preview += '...'
            except:
                private_preview = 'Unable to read file content'
    
    # Generate HTML
    return f'''
    <style>
        .syft-static-viewer {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f9fafb;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }}
        
        .syft-widget-header {{
            background: #f3f4f6;
            padding: 16px 20px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .syft-widget-title {{
            font-size: 18px;
            font-weight: 600;
            color: #111827;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .syft-uid-badge {{
            font-size: 11px;
            font-family: monospace;
            background: #e5e7eb;
            padding: 2px 6px;
            border-radius: 4px;
            color: #6b7280;
        }}
        
        .syft-view-only {{
            font-size: 11px;
            color: #6b7280;
            padding: 4px 8px;
            background: #f3f4f6;
            border-radius: 4px;
        }}
        
        .syft-tabs {{
            display: flex;
            background: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
            overflow-x: auto;
        }}
        
        .syft-tab {{
            padding: 12px 24px;
            font-size: 14px;
            color: #111827;
            font-weight: 500;
            white-space: nowrap;
            position: relative;
            background: none;
            border: none;
            cursor: default;
        }}
        
        .syft-tab::after {{
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 2px;
            background: #3b82f6;
        }}
        
        .syft-content {{
            background: white;
        }}
        
        .syft-tab-content {{
            padding: 24px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .syft-tab-content:last-child {{
            border-bottom: none;
        }}
        
        .syft-section-title {{
            font-size: 16px;
            font-weight: 500;
            color: #111827;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .syft-form-group {{
            margin-bottom: 20px;
        }}
        
        .syft-form-label {{
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }}
        
        .syft-form-input {{
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            background: #f9fafb;
            color: #374151;
            font-family: inherit;
        }}
        
        .syft-info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }}
        
        .syft-info-item {{
            background: #f9fafb;
            padding: 12px 16px;
            border-radius: 6px;
        }}
        
        .syft-info-label {{
            font-size: 11px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}
        
        .syft-info-value {{
            font-size: 14px;
            color: #111827;
            font-family: monospace;
        }}
        
        .syft-file-section {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        
        .syft-file-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}
        
        .syft-file-title {{
            font-size: 16px;
            font-weight: 500;
            color: #111827;
        }}
        
        .syft-file-status {{
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        .syft-file-status.available {{
            background: #dcfce7;
            color: #065f46;
        }}
        
        .syft-file-status.not-found {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .syft-file-info {{
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 12px;
            font-family: monospace;
        }}
        
        .syft-file-preview {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 12px;
            font-family: monospace;
            font-size: 12px;
            line-height: 1.5;
            color: #374151;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-all;
        }}
        
        .syft-permissions-section {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        
        .syft-permissions-title {{
            font-size: 16px;
            font-weight: 500;
            color: #111827;
            margin-bottom: 16px;
        }}
        
        .syft-permission-group {{
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .syft-permission-group:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        
        .syft-permission-label {{
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 8px;
        }}
        
        .syft-email-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .syft-email-tag {{
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            background: #dbeafe;
            color: #1e40af;
            border-radius: 4px;
            font-size: 13px;
        }}
        
        .syft-email-tag.public {{
            background: #dcfce7;
            color: #065f46;
        }}
        
        .syft-metadata-item {{
            display: flex;
            padding: 8px 0;
            border-bottom: 1px solid #f3f4f6;
        }}
        
        .syft-metadata-item:last-child {{
            border-bottom: none;
        }}
        
        .syft-metadata-key {{
            flex: 0 0 200px;
            font-weight: 500;
            color: #374151;
            font-size: 14px;
        }}
        
        .syft-metadata-value {{
            flex: 1;
            color: #6b7280;
            font-family: monospace;
            font-size: 13px;
            word-break: break-all;
        }}
    </style>
    
    <div class="syft-static-viewer">
        <div class="syft-widget-header">
            <div class="syft-widget-title">
                <span>{html.escape(name)}</span>
                <span class="syft-uid-badge">{uid[:8]}...</span>
            </div>
            <span class="syft-view-only">📄 View-only mode</span>
        </div>
        
        <div class="syft-tabs">
            <div class="syft-tab">Overview</div>
            <div class="syft-tab">Files</div>
            <div class="syft-tab">Permissions</div>
            <div class="syft-tab">Metadata</div>
        </div>
        
        <div class="syft-content">
            <!-- Overview Tab Content -->
            <div class="syft-tab-content">
                <h3 class="syft-section-title">Overview</h3>
                
                <div class="syft-form-group">
                    <label class="syft-form-label">Name</label>
                    <input type="text" class="syft-form-input" value="{html.escape(name)}" readonly>
                </div>
                
                <div class="syft-form-group">
                    <label class="syft-form-label">Description</label>
                    <textarea class="syft-form-input" readonly>{html.escape(description)}</textarea>
                </div>
                
                <div class="syft-info-grid">
                    <div class="syft-info-item">
                        <div class="syft-info-label">UID</div>
                        <div class="syft-info-value">{uid}</div>
                    </div>
                    <div class="syft-info-item">
                        <div class="syft-info-label">Created</div>
                        <div class="syft-info-value">{created_at}</div>
                    </div>
                    <div class="syft-info-item">
                        <div class="syft-info-label">Updated</div>
                        <div class="syft-info-value">{updated_at}</div>
                    </div>
                    <div class="syft-info-item">
                        <div class="syft-info-label">File Type</div>
                        <div class="syft-info-value">{file_type}</div>
                    </div>
                    <div class="syft-info-item">
                        <div class="syft-info-label">Owner</div>
                        <div class="syft-info-value">{html.escape(owner_email)}</div>
                    </div>
                    <div class="syft-info-item">
                        <div class="syft-info-label">Object Type</div>
                        <div class="syft-info-value">{object_type}</div>
                    </div>
                </div>
                
                {f'''
                <div class="syft-form-group">
                    <label class="syft-form-label">Mock Note</label>
                    <textarea class="syft-form-input" readonly>{html.escape(mock_note)}</textarea>
                </div>
                ''' if mock_note else ''}
            </div>
            
            <!-- Files Tab Content -->
            <div class="syft-tab-content">
                <h3 class="syft-section-title">Files</h3>
                
                <div class="syft-file-section">
                    <div class="syft-file-header">
                        <h4 class="syft-file-title">🔍 Mock {"Folder" if mock_is_folder else "File"}</h4>
                        <span class="syft-file-status {"available" if mock_exists else "not-found"}">
                            {"✓ Available" if mock_exists else "✗ Not Found"}
                        </span>
                    </div>
                    <div class="syft-file-info">Path: {html.escape(str(mock_path))}</div>
                    {mock_preview if mock_preview else ''}
                </div>
                
                <div class="syft-file-section">
                    <div class="syft-file-header">
                        <h4 class="syft-file-title">🔐 Private {"Folder" if private_is_folder else "File"}</h4>
                        <span class="syft-file-status {"available" if private_exists else "not-found"}">
                            {"✓ Available" if private_exists else "✗ Not Found"}
                        </span>
                    </div>
                    <div class="syft-file-info">Path: {html.escape(str(private_path))}</div>
                    {private_preview if private_preview else ''}
                </div>
                
                <div class="syft-file-section">
                    <div class="syft-file-header">
                        <h4 class="syft-file-title">📋 Config File (.syftobject.yaml)</h4>
                        <span class="syft-file-status available">✓ Available</span>
                    </div>
                    <div class="syft-file-info">Path: {html.escape(str(syftobject_path))}</div>
                </div>
            </div>
            
            <!-- Permissions Tab Content -->
            <div class="syft-tab-content">
                <h3 class="syft-section-title">Permissions</h3>
                
                {render_permissions_section("Discovery Permissions", "Who can discover this object exists", 
                                          SyftObjectConfigAccessor(syft_obj).get_read_permissions())}
                
                <div class="syft-permissions-section">
                    <h4 class="syft-permissions-title">Mock File Permissions</h4>
                    <div class="syft-permission-group">
                        <div class="syft-permission-label">Read Access</div>
                        <div class="syft-email-list">
                            {render_permission_tags(MockAccessor(syft_obj.mock_url, syft_obj).get_read_permissions())}
                        </div>
                    </div>
                    <div class="syft-permission-group">
                        <div class="syft-permission-label">Write Access</div>
                        <div class="syft-email-list">
                            {render_permission_tags(MockAccessor(syft_obj.mock_url, syft_obj).get_write_permissions())}
                        </div>
                    </div>
                </div>
                
                <div class="syft-permissions-section">
                    <h4 class="syft-permissions-title">Private File Permissions</h4>
                    <div class="syft-permission-group">
                        <div class="syft-permission-label">Read Access</div>
                        <div class="syft-email-list">
                            {render_permission_tags(PrivateAccessor(syft_obj.private_url, syft_obj).get_read_permissions())}
                        </div>
                    </div>
                    <div class="syft-permission-group">
                        <div class="syft-permission-label">Write Access</div>
                        <div class="syft-email-list">
                            {render_permission_tags(PrivateAccessor(syft_obj.private_url, syft_obj).get_write_permissions())}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Metadata Tab Content -->
            <div class="syft-tab-content">
                <h3 class="syft-section-title">Metadata</h3>
                
                <div class="syft-permissions-section">
                    <h4 class="syft-permissions-title">System Metadata</h4>
                    <div class="syft-metadata-item">
                        <div class="syft-metadata-key">Object Type</div>
                        <div class="syft-metadata-value">{syft_obj.object_type}</div>
                    </div>
                    <div class="syft-metadata-item">
                        <div class="syft-metadata-key">Owner Email</div>
                        <div class="syft-metadata-value">{html.escape(owner_email)}</div>
                    </div>
                    {f'''
                    <div class="syft-metadata-item">
                        <div class="syft-metadata-key">Mock Note</div>
                        <div class="syft-metadata-value">{html.escape(mock_note)}</div>
                    </div>
                    ''' if mock_note else ''}
                </div>
                
                {render_custom_metadata(syft_obj)}
            </div>
        </div>
    </div>
    '''


def render_permissions_section(title: str, description: str, permissions: list) -> str:
    """Render a permissions section"""
    return f'''
    <div class="syft-permissions-section">
        <h4 class="syft-permissions-title">{title}</h4>
        <div class="syft-permission-group">
            <div class="syft-permission-label">{description}</div>
            <div class="syft-email-list">
                {render_permission_tags(permissions)}
            </div>
        </div>
    </div>
    '''


def render_permission_tags(permissions: list) -> str:
    """Render permission email tags"""
    if not permissions:
        return '<span class="syft-email-tag">None</span>'
    
    tags = []
    for perm in permissions:
        if perm in ['public', '*']:
            tags.append('<span class="syft-email-tag public">Public</span>')
        else:
            tags.append(f'<span class="syft-email-tag">{html.escape(perm)}</span>')
    
    return ' '.join(tags)


def render_custom_metadata(syft_obj: 'SyftObject') -> str:
    """Render custom metadata section"""
    # Filter out system fields
    system_fields = {'_file_operations', '_folder_paths', 'owner_email', 'email', 'mock_note', 'admin_permissions'}
    custom_metadata = {k: v for k, v in syft_obj.metadata.items() if k not in system_fields}
    
    if not custom_metadata:
        return ''
    
    items = []
    for key, value in custom_metadata.items():
        # Convert value to string representation
        if isinstance(value, (dict, list)):
            import json
            value_str = json.dumps(value, indent=2)
        else:
            value_str = str(value)
        
        items.append(f'''
        <div class="syft-metadata-item">
            <div class="syft-metadata-key">{html.escape(key)}</div>
            <div class="syft-metadata-value">{html.escape(value_str)}</div>
        </div>
        ''')
    
    return f'''
    <div class="syft-permissions-section">
        <h4 class="syft-permissions-title">Custom Metadata</h4>
        {''.join(items)}
    </div>
    '''