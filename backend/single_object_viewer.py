"""
Single Object Viewer - HTML/CSS/JS for displaying and editing a single SyftObject
"""

from typing import Dict, Any
import json
from pathlib import Path


def generate_single_object_viewer_html(target_obj: Any, object_uid: str) -> str:
    """Generate HTML for the single object viewer widget."""
    
    # Extract basic info
    name = target_obj.get_name() if hasattr(target_obj, 'get_name') else target_obj.name
    description = target_obj.get_description() if hasattr(target_obj, 'get_description') else target_obj.description
    
    # Get file paths for editor links
    mock_path = target_obj.mock.path if hasattr(target_obj, 'mock') else getattr(target_obj, 'mock_path', None)
    private_path = target_obj.private.path if hasattr(target_obj, 'private') else getattr(target_obj, 'private_path', None)
    syftobject_path = target_obj.syftobject_config.path if hasattr(target_obj, 'syftobject_config') else getattr(target_obj, 'syftobject_path', None)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SyftObject: {name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f9fafb;
            padding: 20px;
            color: #1f2937;
            font-size: 14px;
        }}
        
        .widget-container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            max-width: 1000px;
            margin: 0 auto;
            overflow: hidden;
        }}
        
        .widget-header {{
            background: #f3f4f6;
            padding: 16px 20px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .widget-title {{
            font-size: 18px;
            font-weight: 600;
            color: #111827;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .uid-badge {{
            font-size: 11px;
            font-family: monospace;
            background: #e5e7eb;
            padding: 2px 6px;
            border-radius: 4px;
            color: #6b7280;
        }}
        
        .tabs {{
            display: flex;
            background: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
            overflow-x: auto;
        }}
        
        .tab {{
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 14px;
            color: #6b7280;
            white-space: nowrap;
            transition: all 0.2s;
            position: relative;
        }}
        
        .tab:hover {{
            color: #111827;
            background: #f3f4f6;
        }}
        
        .tab.active {{
            color: #3b82f6;
            font-weight: 500;
        }}
        
        .tab.active::after {{
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 2px;
            background: #3b82f6;
        }}
        
        .tab-content {{
            display: none;
            padding: 24px;
            animation: fadeIn 0.3s ease-in-out;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-label {{
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }}
        
        .form-input {{
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.2s;
            font-family: inherit;
        }}
        
        .form-input:focus {{
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        .form-input:disabled {{
            background: #f3f4f6;
            color: #9ca3af;
            cursor: not-allowed;
        }}
        
        textarea.form-input {{
            resize: vertical;
            min-height: 80px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .info-item {{
            background: #f9fafb;
            padding: 12px 16px;
            border-radius: 6px;
        }}
        
        .info-label {{
            font-size: 11px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}
        
        .info-value {{
            font-size: 14px;
            color: #111827;
            font-family: monospace;
        }}
        
        .file-section {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        
        .file-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}
        
        .file-title {{
            font-size: 16px;
            font-weight: 500;
            color: #111827;
        }}
        
        .file-info {{
            display: flex;
            gap: 16px;
            margin-bottom: 12px;
            font-size: 12px;
            color: #6b7280;
        }}
        
        .file-iframe {{
            width: 100%;
            height: 400px;
            border: none;
            border-radius: 6px;
            background: white;
        }}
        
        .btn {{
            padding: 6px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        
        .btn-primary {{
            background-color: rgba(59, 130, 246, 0.2);
            color: #3b82f6;
            border: none;
        }}
        
        .btn-primary:hover {{
            background-color: rgba(59, 130, 246, 0.3);
        }}
        
        .btn-secondary {{
            background: #e5e7eb;
            color: #374151;
            border: none;
        }}
        
        .btn-secondary:hover {{
            background: #d1d5db;
        }}
        
        .btn-danger {{
            background: rgba(239, 68, 68, 0.2);
            color: #dc2626;
            border: none;
        }}
        
        .btn-danger:hover {{
            background: rgba(239, 68, 68, 0.3);
        }}
        
        .permissions-section {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        
        .permissions-title {{
            font-size: 16px;
            font-weight: 500;
            color: #111827;
            margin-bottom: 16px;
        }}
        
        .permission-group {{
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .permission-group:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        
        .permission-label {{
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 8px;
        }}
        
        .email-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 8px;
        }}
        
        .email-tag {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            background: #dbeafe;
            color: #1e40af;
            border-radius: 4px;
            font-size: 13px;
        }}
        
        .email-tag .remove {{
            cursor: pointer;
            font-size: 16px;
            line-height: 1;
            opacity: 0.7;
            transition: opacity 0.2s;
        }}
        
        .email-tag .remove:hover {{
            opacity: 1;
        }}
        
        .add-email {{
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }}
        
        .add-email input {{
            flex: 1;
            padding: 6px 10px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 13px;
        }}
        
        .metadata-editor {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 20px;
        }}
        
        .metadata-item {{
            display: flex;
            gap: 8px;
            margin-bottom: 8px;
            align-items: flex-start;
        }}
        
        .metadata-key {{
            flex: 0 0 200px;
            padding: 6px 10px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 13px;
            font-family: monospace;
        }}
        
        .metadata-value {{
            flex: 1;
            padding: 6px 10px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 13px;
            font-family: monospace;
        }}
        
        .metadata-remove {{
            padding: 6px 12px;
            background: #fee2e2;
            color: #dc2626;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
        }}
        
        .metadata-remove:hover {{
            background: #fecaca;
        }}
        
        .add-metadata {{
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }}
        
        .action-buttons {{
            display: flex;
            gap: 12px;
            margin-top: 24px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}
        
        .status-message {{
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            margin-bottom: 16px;
            display: none;
        }}
        
        .status-success {{
            background: #dcfce7;
            color: #065f46;
            border: 1px solid #bbf7d0;
        }}
        
        .status-error {{
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }}
        
        .loading {{
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid #f3f4f6;
            border-top-color: #3b82f6;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="widget-container">
        <div class="widget-header">
            <div class="widget-title">
                <span id="object-name">{name}</span>
                <span class="uid-badge">{object_uid[:8]}...</span>
            </div>
            <button class="btn btn-primary" onclick="refreshObject()">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>
                </svg>
                Refresh
            </button>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('overview')">Overview</button>
            <button class="tab" onclick="switchTab('files')">Files</button>
            <button class="tab" onclick="switchTab('permissions')">Permissions</button>
            <button class="tab" onclick="switchTab('metadata')">Metadata</button>
        </div>
        
        <div id="status-message" class="status-message"></div>
        
        <!-- Overview Tab -->
        <div id="overview-tab" class="tab-content active">
            <div class="form-group">
                <label class="form-label">Name</label>
                <input type="text" id="name-input" class="form-input" value="{name}">
            </div>
            
            <div class="form-group">
                <label class="form-label">Description</label>
                <textarea id="description-input" class="form-input">{description or ''}</textarea>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">UID</div>
                    <div class="info-value" id="uid-value">{object_uid}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Created</div>
                    <div class="info-value" id="created-value">Loading...</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Updated</div>
                    <div class="info-value" id="updated-value">Loading...</div>
                </div>
                <div class="info-item">
                    <div class="info-label">File Type</div>
                    <div class="info-value" id="filetype-value">Loading...</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Owner</div>
                    <div class="info-value" id="owner-value">Loading...</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Object Type</div>
                    <div class="info-value" id="object-type-value">Loading...</div>
                </div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Mock Note</label>
                <textarea id="mock-note-input" class="form-input" placeholder="Describe what makes this mock data different from the real data..."></textarea>
            </div>
            
            <div class="action-buttons">
                <button class="btn btn-primary" onclick="saveOverview()">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"/>
                    </svg>
                    Save Changes
                </button>
                <button class="btn btn-danger" onclick="deleteObject()">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6h14zM10 11v6M14 11v6"/>
                    </svg>
                    Delete Object
                </button>
            </div>
        </div>
        
        <!-- Files Tab -->
        <div id="files-tab" class="tab-content">
            <div class="file-section">
                <div class="file-header">
                    <h3 class="file-title">Mock File</h3>
                    <button class="btn btn-secondary" onclick="openInEditor('mock')">
                        Open in Editor
                    </button>
                </div>
                <div class="file-info">
                    <span>Path: <code id="mock-path">{mock_path or 'Not found'}</code></span>
                </div>
                <iframe id="mock-iframe" class="file-iframe" src="/editor?path={mock_path}&embedded=true"></iframe>
            </div>
            
            <div class="file-section">
                <div class="file-header">
                    <h3 class="file-title">Private File</h3>
                    <button class="btn btn-secondary" onclick="openInEditor('private')">
                        Open in Editor
                    </button>
                </div>
                <div class="file-info">
                    <span>Path: <code id="private-path">{private_path or 'Not found'}</code></span>
                </div>
                <iframe id="private-iframe" class="file-iframe" src="/editor?path={private_path}&embedded=true"></iframe>
            </div>
            
            <div class="file-section">
                <div class="file-header">
                    <h3 class="file-title">Config File (.syftobject.yaml)</h3>
                    <button class="btn btn-secondary" onclick="openInEditor('syftobject')">
                        Open in Editor
                    </button>
                </div>
                <div class="file-info">
                    <span>Path: <code id="syftobject-path">{syftobject_path or 'Not found'}</code></span>
                </div>
                <iframe id="syftobject-iframe" class="file-iframe" src="/editor?path={syftobject_path}&embedded=true"></iframe>
            </div>
        </div>
        
        <!-- Permissions Tab -->
        <div id="permissions-tab" class="tab-content">
            <div class="permissions-section">
                <h3 class="permissions-title">Discovery Permissions</h3>
                <div class="permission-group">
                    <div class="permission-label">Who can discover this object exists</div>
                    <div id="syftobject-read-list" class="email-list"></div>
                    <div class="add-email">
                        <input type="email" id="syftobject-read-input" placeholder="Add email address">
                        <button class="btn btn-primary" onclick="addPermission('syftobject', 'read')">Add</button>
                    </div>
                </div>
            </div>
            
            <div class="permissions-section">
                <h3 class="permissions-title">Mock File Permissions</h3>
                <div class="permission-group">
                    <div class="permission-label">Read Access</div>
                    <div id="mock-read-list" class="email-list"></div>
                    <div class="add-email">
                        <input type="email" id="mock-read-input" placeholder="Add email address">
                        <button class="btn btn-primary" onclick="addPermission('mock', 'read')">Add</button>
                    </div>
                </div>
                <div class="permission-group">
                    <div class="permission-label">Write Access</div>
                    <div id="mock-write-list" class="email-list"></div>
                    <div class="add-email">
                        <input type="email" id="mock-write-input" placeholder="Add email address">
                        <button class="btn btn-primary" onclick="addPermission('mock', 'write')">Add</button>
                    </div>
                </div>
            </div>
            
            <div class="permissions-section">
                <h3 class="permissions-title">Private File Permissions</h3>
                <div class="permission-group">
                    <div class="permission-label">Read Access</div>
                    <div id="private-read-list" class="email-list"></div>
                    <div class="add-email">
                        <input type="email" id="private-read-input" placeholder="Add email address">
                        <button class="btn btn-primary" onclick="addPermission('private', 'read')">Add</button>
                    </div>
                </div>
                <div class="permission-group">
                    <div class="permission-label">Write Access</div>
                    <div id="private-write-list" class="email-list"></div>
                    <div class="add-email">
                        <input type="email" id="private-write-input" placeholder="Add email address">
                        <button class="btn btn-primary" onclick="addPermission('private', 'write')">Add</button>
                    </div>
                </div>
            </div>
            
            <div class="action-buttons">
                <button class="btn btn-primary" onclick="savePermissions()">Save Permissions</button>
            </div>
        </div>
        
        <!-- Metadata Tab -->
        <div id="metadata-tab" class="tab-content">
            <div class="metadata-editor">
                <h3 class="permissions-title">Custom Metadata</h3>
                <div id="metadata-list"></div>
                <div class="add-metadata">
                    <input type="text" id="new-metadata-key" class="metadata-key" placeholder="Key">
                    <input type="text" id="new-metadata-value" class="metadata-value" placeholder="Value">
                    <button class="btn btn-primary" onclick="addMetadata()">Add</button>
                </div>
            </div>
            
            <div class="action-buttons">
                <button class="btn btn-primary" onclick="saveMetadata()">Save Metadata</button>
            </div>
        </div>
    </div>
    
    <script>
        const objectUid = '{object_uid}';
        let currentMetadata = {{}};
        let currentPermissions = {{}};
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            loadObjectMetadata();
        }});
        
        function switchTab(tabName) {{
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.remove('active');
            }});
            document.getElementById(tabName + '-tab').classList.add('active');
        }}
        
        async function loadObjectMetadata() {{
            try {{
                const response = await fetch(`/api/object/${{objectUid}}/metadata`);
                if (!response.ok) throw new Error('Failed to load metadata');
                
                const data = await response.json();
                currentMetadata = data;
                
                // Update overview fields
                document.getElementById('name-input').value = data.name || '';
                document.getElementById('description-input').value = data.description || '';
                document.getElementById('mock-note-input').value = data.mock_note || '';
                
                // Update info grid
                document.getElementById('uid-value').textContent = data.uid;
                document.getElementById('created-value').textContent = formatDate(data.created_at);
                document.getElementById('updated-value').textContent = formatDate(data.updated_at);
                document.getElementById('filetype-value').textContent = data.file_type || 'Unknown';
                document.getElementById('owner-value').textContent = data.owner_email || 'Unknown';
                document.getElementById('object-type-value').textContent = data.is_folder ? 'Folder' : 'File';
                
                // Update file paths
                document.getElementById('mock-path').textContent = data.paths.mock || 'Not found';
                document.getElementById('private-path').textContent = data.paths.private || 'Not found';
                document.getElementById('syftobject-path').textContent = data.paths.syftobject || 'Not found';
                
                // Update permissions
                currentPermissions = data.permissions;
                renderPermissions();
                
                // Update metadata
                renderMetadata(data.metadata);
                
            }} catch (error) {{
                showStatus('Error loading object metadata: ' + error.message, 'error');
            }}
        }}
        
        function formatDate(isoString) {{
            if (!isoString) return 'N/A';
            const date = new Date(isoString);
            return date.toLocaleString();
        }}
        
        function renderPermissions() {{
            // Render each permission list
            renderPermissionList('syftobject-read-list', currentPermissions.syftobject?.read || []);
            renderPermissionList('mock-read-list', currentPermissions.mock?.read || []);
            renderPermissionList('mock-write-list', currentPermissions.mock?.write || []);
            renderPermissionList('private-read-list', currentPermissions.private?.read || []);
            renderPermissionList('private-write-list', currentPermissions.private?.write || []);
        }}
        
        function renderPermissionList(elementId, emails) {{
            const container = document.getElementById(elementId);
            container.innerHTML = '';
            
            emails.forEach(email => {{
                const tag = document.createElement('div');
                tag.className = 'email-tag';
                tag.innerHTML = `
                    ${{email}}
                    <span class="remove" onclick="removePermission('${{elementId}}', '${{email}}')">&times;</span>
                `;
                container.appendChild(tag);
            }});
        }}
        
        function renderMetadata(metadata) {{
            const container = document.getElementById('metadata-list');
            container.innerHTML = '';
            
            // Filter out system keys
            const systemKeys = ['owner_email', 'mock_note', '_file_operations', '_folder_paths'];
            
            Object.entries(metadata).forEach(([key, value]) => {{
                if (systemKeys.includes(key)) return;
                
                const item = document.createElement('div');
                item.className = 'metadata-item';
                item.innerHTML = `
                    <input type="text" class="metadata-key" value="${{key}}" readonly>
                    <input type="text" class="metadata-value" value="${{JSON.stringify(value)}}" onblur="updateMetadataValue('${{key}}', this.value)">
                    <button class="metadata-remove" onclick="removeMetadata('${{key}}')">Remove</button>
                `;
                container.appendChild(item);
            }});
        }}
        
        async function updateField(field, value) {{
            try {{
                const updates = {{[field]: value}};
                const response = await fetch(`/api/object/${{objectUid}}/metadata`, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(updates)
                }});
                
                if (!response.ok) throw new Error('Failed to update field');
                
                showStatus(`${{field}} updated successfully`, 'success');
                
                // Update the header if name changed
                if (field === 'name') {{
                    document.getElementById('object-name').textContent = value;
                }}
                
            }} catch (error) {{
                showStatus('Error updating field: ' + error.message, 'error');
            }}
        }}
        
        async function saveOverview() {{
            try {{
                const nameValue = document.getElementById('name-input').value;
                const descriptionValue = document.getElementById('description-input').value;
                const mockNoteValue = document.getElementById('mock-note-input').value;
                
                const updates = {{
                    name: nameValue,
                    description: descriptionValue,
                    mock_note: mockNoteValue
                }};
                
                const response = await fetch(`/api/object/${{objectUid}}/metadata`, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(updates)
                }});
                
                if (!response.ok) throw new Error('Failed to save changes');
                
                showStatus('Overview saved successfully', 'success');
                
                // Update the header if name changed
                document.getElementById('object-name').textContent = nameValue;
                
            }} catch (error) {{
                showStatus('Error saving overview: ' + error.message, 'error');
            }}
        }}
        
        function addPermission(fileType, permType) {{
            const inputId = `${{fileType}}-${{permType}}-input`;
            const input = document.getElementById(inputId);
            const email = input.value.trim();
            
            if (!email) return;
            
            // Update local state
            if (fileType === 'syftobject') {{
                if (!currentPermissions.syftobject) currentPermissions.syftobject = {{}};
                if (!currentPermissions.syftobject.read) currentPermissions.syftobject.read = [];
                if (!currentPermissions.syftobject.read.includes(email)) {{
                    currentPermissions.syftobject.read.push(email);
                }}
            }} else {{
                if (!currentPermissions[fileType]) currentPermissions[fileType] = {{}};
                if (!currentPermissions[fileType][permType]) currentPermissions[fileType][permType] = [];
                if (!currentPermissions[fileType][permType].includes(email)) {{
                    currentPermissions[fileType][permType].push(email);
                }}
            }}
            
            // Re-render
            renderPermissions();
            input.value = '';
        }}
        
        function removePermission(listId, email) {{
            // Parse the list ID to get file type and permission type
            const parts = listId.split('-');
            const fileType = parts[0];
            const permType = parts[1];
            
            // Update local state
            if (fileType === 'syftobject') {{
                const index = currentPermissions.syftobject?.read?.indexOf(email);
                if (index > -1) {{
                    currentPermissions.syftobject.read.splice(index, 1);
                }}
            }} else {{
                const index = currentPermissions[fileType]?.[permType]?.indexOf(email);
                if (index > -1) {{
                    currentPermissions[fileType][permType].splice(index, 1);
                }}
            }}
            
            // Re-render
            renderPermissions();
        }}
        
        async function savePermissions() {{
            try {{
                // Convert to flat format expected by API
                const updates = {{
                    discovery_read: currentPermissions.syftobject?.read || [],
                    mock_read: currentPermissions.mock?.read || [],
                    mock_write: currentPermissions.mock?.write || [],
                    private_read: currentPermissions.private?.read || [],
                    private_write: currentPermissions.private?.write || []
                }};
                
                const response = await fetch(`/api/objects/${{objectUid}}/permissions`, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(updates)
                }});
                
                if (!response.ok) throw new Error('Failed to save permissions');
                
                showStatus('Permissions saved successfully', 'success');
                
            }} catch (error) {{
                showStatus('Error saving permissions: ' + error.message, 'error');
            }}
        }}
        
        function addMetadata() {{
            const keyInput = document.getElementById('new-metadata-key');
            const valueInput = document.getElementById('new-metadata-value');
            
            const key = keyInput.value.trim();
            const value = valueInput.value.trim();
            
            if (!key || !value) return;
            
            // Update local metadata
            currentMetadata.metadata[key] = value;
            
            // Re-render
            renderMetadata(currentMetadata.metadata);
            
            // Clear inputs
            keyInput.value = '';
            valueInput.value = '';
        }}
        
        function updateMetadataValue(key, value) {{
            try {{
                // Try to parse as JSON
                currentMetadata.metadata[key] = JSON.parse(value);
            }} catch {{
                // If not valid JSON, store as string
                currentMetadata.metadata[key] = value;
            }}
        }}
        
        function removeMetadata(key) {{
            delete currentMetadata.metadata[key];
            renderMetadata(currentMetadata.metadata);
        }}
        
        async function saveMetadata() {{
            try {{
                const response = await fetch(`/api/object/${{objectUid}}/metadata`, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{metadata: currentMetadata.metadata}})
                }});
                
                if (!response.ok) throw new Error('Failed to save metadata');
                
                showStatus('Metadata saved successfully', 'success');
                
            }} catch (error) {{
                showStatus('Error saving metadata: ' + error.message, 'error');
            }}
        }}
        
        async function deleteObject() {{
            if (!confirm('Are you sure you want to delete this object? This action cannot be undone.')) {{
                return;
            }}
            
            try {{
                const response = await fetch(`/api/objects/${{objectUid}}`, {{
                    method: 'DELETE'
                }});
                
                if (!response.ok) throw new Error('Failed to delete object');
                
                showStatus('Object deleted successfully', 'success');
                
                // Redirect after a short delay
                setTimeout(() => {{
                    window.location.href = '/';
                }}, 1500);
                
            }} catch (error) {{
                showStatus('Error deleting object: ' + error.message, 'error');
            }}
        }}
        
        function openInEditor(fileType) {{
            let path;
            switch(fileType) {{
                case 'mock':
                    path = currentMetadata.paths.mock;
                    break;
                case 'private':
                    path = currentMetadata.paths.private;
                    break;
                case 'syftobject':
                    path = currentMetadata.paths.syftobject;
                    break;
            }}
            
            if (path) {{
                window.open(`/editor?path=${{encodeURIComponent(path)}}`, '_blank');
            }}
        }}
        
        function refreshObject() {{
            loadObjectMetadata();
            showStatus('Object refreshed', 'success');
        }}
        
        function showStatus(message, type) {{
            const statusEl = document.getElementById('status-message');
            statusEl.textContent = message;
            statusEl.className = `status-message status-${{type}}`;
            statusEl.style.display = 'block';
            
            setTimeout(() => {{
                statusEl.style.display = 'none';
            }}, 3000);
        }}
    </script>
</body>
</html>
"""
    
    return html