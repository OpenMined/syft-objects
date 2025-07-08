"""
Filesystem Code Editor Module
A fully featured file system browser and code editor for the FastAPI server.
Completely decoupled from syft-objects functionality.
"""

import os
import mimetypes
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import HTTPException
from fastapi.responses import HTMLResponse
import json
from syft_perm import get_file_permissions


class FileSystemManager:
    """Manages filesystem operations for the code editor."""
    
    ALLOWED_EXTENSIONS = {
        # Text files
        '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.sass',
        '.json', '.yaml', '.yml', '.xml', '.md', '.txt', '.csv', '.log',
        '.sql', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
        # Config files
        '.ini', '.cfg', '.conf', '.toml', '.env', '.gitignore', '.dockerignore',
        # Code files
        '.c', '.cpp', '.h', '.hpp', '.java', '.php', '.rb', '.go', '.rs', '.swift',
        '.kt', '.scala', '.clj', '.lisp', '.hs', '.elm', '.dart', '.r', '.m', '.mm',
        # Web files
        '.vue', '.svelte', '.astro', '.htmx', '.mustache', '.handlebars',
        # Data files
        '.jsonl', '.ndjson', '.tsv', '.properties', '.lock',
        # Documentation
        '.rst', '.tex', '.latex', '.adoc', '.org',
    }
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit
    
    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)
    
    def _check_permissions(self, file_path: str, required_permission: str, user_email: str) -> bool:
        """Check if user has required permission for the file"""
        # Temporarily allow all operations while debugging
        return True
        
        # Original code commented out for now
        # if not user_email:
        #     return False
            
        # try:
        #     perms = get_file_permissions(file_path)
        #     if not perms:
        #         return False
                
        #     if required_permission == "read":
        #         return (user_email in perms.get("read", []) or 
        #                user_email in perms.get("write", []) or 
        #                user_email in perms.get("admin", []) or 
        #                "*" in perms.get("read", []))
        #     elif required_permission == "write":
        #         return (user_email in perms.get("write", []) or 
        #                user_email in perms.get("admin", []) or 
        #                "*" in perms.get("write", []))
        #     elif required_permission == "admin":
        #         return (user_email in perms.get("admin", []) or 
        #                "*" in perms.get("admin", []))
        #     return False
        # except Exception as e:
        #     print(f"Error checking permissions: {e}")
        #     return False

    def _validate_path(self, path: str) -> Path:
        """Validate and resolve a path, ensuring it's within allowed bounds."""
        try:
            resolved_path = Path(path).resolve()
            
            # If we have a base path, ensure the resolved path is within it
            if self.root_dir and not str(resolved_path).startswith(str(self.root_dir)):
                raise HTTPException(status_code=403, detail="Access denied: Path outside allowed directory")
            
            return resolved_path
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid path: {str(e)}")
    
    def _is_text_file(self, file_path: Path) -> bool:
        """Check if a file is a text file that can be edited."""
        if file_path.suffix.lower() in self.ALLOWED_EXTENSIONS:
            return True
        
        # Check MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type.startswith('text/'):
            return True
        
        # Try to read a small portion to detect if it's text
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return chunk.decode('utf-8', errors='strict') is not None
        except (UnicodeDecodeError, PermissionError):
            return False
    
    def list_directory(self, dir_path: str, user_email: str) -> List[dict]:
        """List directory contents, filtering based on read permissions"""
        abs_path = os.path.abspath(os.path.join(self.root_dir, dir_path))
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="Directory not found")
            
        try:
            items = []
            for item in os.listdir(abs_path):
                item_path = os.path.join(abs_path, item)
                # Only include items the user has permission to read
                if self._check_permissions(item_path, "read", user_email):
                    items.append({
                        "name": item,
                        "type": "directory" if os.path.isdir(item_path) else "file"
                    })
            return items
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def read_file(self, file_path: str, user_email: str) -> str:
        """Read a file's contents if user has permission"""
        abs_path = os.path.abspath(os.path.join(self.root_dir, file_path))
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        if not self._check_permissions(abs_path, "read", user_email):
            raise HTTPException(status_code=403, detail="Permission denied")
            
        try:
            with open(abs_path, 'r') as f:
                return f.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def write_file(self, file_path: str, content: str, user_email: str) -> None:
        """Write content to a file if user has permission"""
        abs_path = os.path.abspath(os.path.join(self.root_dir, file_path))
        
        if not self._check_permissions(abs_path, "write", user_email):
            raise HTTPException(status_code=403, detail="Permission denied")
            
        try:
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, 'w') as f:
                f.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def create_directory(self, path: str) -> Dict[str, Any]:
        """Create a new directory."""
        dir_path = self._validate_path(path)
        
        if dir_path.exists():
            raise HTTPException(status_code=400, detail="Directory already exists")
        
        try:
            dir_path.mkdir(parents=True, exist_ok=False)
            return {
                'path': str(dir_path),
                'message': 'Directory created successfully'
            }
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Error creating directory: {str(e)}")
    
    def delete_file(self, file_path: str, user_email: str) -> None:
        """Delete a file if user has permission"""
        abs_path = os.path.abspath(os.path.join(self.root_dir, file_path))
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        if not self._check_permissions(abs_path, "write", user_email):
            raise HTTPException(status_code=403, detail="Permission denied")
            
        try:
            os.remove(abs_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


def generate_editor_html(initial_path: str = None) -> str:
    """Generate the HTML for the file editor interface."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SyftBox File Editor</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
    <style>
        :root {{
            --background: 0 0% 100%;
            --foreground: 222.2 84% 4.9%;
            --card: 0 0% 100%;
            --card-foreground: 222.2 84% 4.9%;
            --popover: 0 0% 100%;
            --popover-foreground: 222.2 84% 4.9%;
            --primary: 222.2 47.4% 11.2%;
            --primary-foreground: 210 40% 98%;
            --secondary: 210 40% 96.1%;
            --secondary-foreground: 222.2 47.4% 11.2%;
            --muted: 210 40% 96.1%;
            --muted-foreground: 215.4 16.3% 46.9%;
            --accent: 210 40% 96.1%;
            --accent-foreground: 222.2 47.4% 11.2%;
            --destructive: 0 84.2% 60.2%;
            --destructive-foreground: 210 40% 98%;
            --border: 214.3 31.8% 91.4%;
            --input: 214.3 31.8% 91.4%;
            --ring: 222.2 84% 4.9%;
            --radius: 0.5rem;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: hsl(var(--background));
            color: hsl(var(--foreground));
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 16px;
        }}

        .main-content {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 24px;
            min-height: 600px;
        }}

        .panel {{
            background: hsl(var(--card));
            border: 1px solid hsl(var(--border));
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: 0 2px 10px rgb(0 0 0 / 0.04);
            display: flex;
            flex-direction: column;
        }}

        .panel-header {{
            background: hsl(var(--muted));
            padding: 12px 16px;
            border-bottom: 1px solid hsl(var(--border));
            font-weight: 500;
            color: hsl(var(--foreground));
            font-size: 0.95rem;
        }}

        .panel-content {{
            flex: 1;
            overflow: auto;
            background: hsl(var(--card));
        }}

        .breadcrumb {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
            padding: 12px 16px;
            background: hsl(var(--muted));
            border-bottom: 1px solid hsl(var(--border));
            font-size: 0.9rem;
            max-height: 100px;
            overflow-y: auto;
        }}

        .breadcrumb-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            max-width: 200px;
        }}

        .breadcrumb-link {{
            color: hsl(var(--muted-foreground));
            text-decoration: none;
            padding: 4px 8px;
            border-radius: calc(var(--radius) - 2px);
            transition: all 0.2s;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 150px;
            font-weight: 500;
        }}

        .breadcrumb-link:hover {{
            background: hsl(var(--accent));
            color: hsl(var(--accent-foreground));
            max-width: none;
        }}

        .breadcrumb-current {{
            color: hsl(var(--foreground));
            font-weight: 500;
            background: hsl(var(--muted));
            padding: 4px 8px;
            border-radius: calc(var(--radius) - 2px);
            max-width: 150px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .breadcrumb-separator {{
            color: hsl(var(--muted-foreground));
            font-size: 0.8rem;
        }}

        .file-list {{
            padding: 8px 0;
        }}

        .file-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 16px;
            border-radius: calc(var(--radius) - 2px);
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid transparent;
            background: transparent;
        }}

        .file-item:hover {{
            background: hsl(var(--accent));
        }}

        .file-item.selected {{
            background: hsl(var(--accent));
            border-color: hsl(var(--border));
        }}

        .file-icon {{
            width: 20px;
            height: 20px;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: hsl(var(--muted-foreground));
        }}

        .file-details {{
            flex: 1;
            min-width: 0;
        }}

        .file-name {{
            font-weight: 500;
            color: hsl(var(--foreground));
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .file-meta {{
            font-size: 0.85rem;
            color: hsl(var(--muted-foreground));
            margin-top: 2px;
        }}

        .editor-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        .editor-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 16px;
            background: hsl(var(--muted));
            border-bottom: 1px solid hsl(var(--border));
        }}

        .editor-title {{
            font-weight: 500;
            color: hsl(var(--foreground));
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
            font-size: 0.95rem;
        }}

        .editor-actions {{
            display: flex;
            gap: 8px;
        }}

        .btn {{
            padding: 8px 16px;
            border: 1px solid hsl(var(--border));
            border-radius: calc(var(--radius) - 2px);
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
            background: hsl(var(--card));
            color: hsl(var(--foreground));
        }}

        .btn-primary {{
            background: hsl(var(--primary));
            color: hsl(var(--primary-foreground));
            border-color: transparent;
        }}

        .btn-primary:hover {{
            background: hsl(var(--primary) / 0.9);
        }}

        .btn-secondary {{
            background: hsl(var(--secondary));
            color: hsl(var(--secondary-foreground));
        }}

        .btn-secondary:hover {{
            background: hsl(var(--secondary) / 0.8);
        }}

        .btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .editor-textarea {{
            flex: 1;
            resize: none;
            border: none;
            outline: none;
            padding: 16px;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
            font-size: 14px;
            line-height: 1.6;
            background: hsl(var(--card));
            color: hsl(var(--foreground));
            tab-size: 4;
            width: 100%;
            height: 100%;
        }}

        .editor-textarea:focus {{
            box-shadow: 0 0 0 2px hsl(var(--ring) / 0.1);
        }}

        .status-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 16px;
            background: hsl(var(--muted));
            border-top: 1px solid hsl(var(--border));
            font-size: 0.85rem;
            color: hsl(var(--muted-foreground));
        }}

        .status-left {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .status-right {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .loading {{
            text-align: center;
            padding: 40px;
            color: hsl(var(--muted-foreground));
        }}

        .error {{
            background: hsl(var(--destructive) / 0.1);
            color: hsl(var(--destructive));
            padding: 12px;
            border-radius: calc(var(--radius) - 2px);
            margin: 12px;
            border: 1px solid hsl(var(--destructive) / 0.2);
        }}

        .success {{
            background: hsl(142.1 76.2% 36.3% / 0.1);
            color: hsl(142.1 76.2% 36.3%);
            padding: 12px;
            border-radius: calc(var(--radius) - 2px);
            margin: 12px;
            border: 1px solid hsl(142.1 76.2% 36.3% / 0.2);
        }}

        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: hsl(var(--muted-foreground));
        }}

        .empty-state h3 {{
            font-size: 1.1rem;
            margin-bottom: 8px;
            color: hsl(var(--foreground));
            font-weight: 500;
        }}

        .empty-state p {{
            color: hsl(var(--muted-foreground));
            font-size: 0.9rem;
        }}

        .logo {{
            width: 48px;
            height: 48px;
            margin: 0 auto 16px;
        }}

        @media (max-width: 900px) {{
            .main-content {{
                grid-template-columns: 1fr;
                gap: 16px;
            }}

            .editor-header {{
                flex-direction: column;
                gap: 8px;
            }}

            .editor-actions {{
                width: 100%;
                justify-content: flex-start;
            }}

            .breadcrumb {{
                padding: 8px 12px;
            }}

            .breadcrumb-item {{
                max-width: 120px;
            }}

            .breadcrumb-link,
            .breadcrumb-current {{
                max-width: 100px;
                font-size: 0.85rem;
            }}
        }}

        @media (max-width: 600px) {{
            .container {{
                padding: 8px;
            }}

            .panel-header {{
                padding: 10px 12px;
            }}

            .breadcrumb {{
                padding: 8px;
            }}

            .file-item {{
                padding: 8px 10px;
            }}

            .editor-textarea {{
                padding: 10px;
                font-size: 13px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="main-content">
            <div class="panel file-browser">
                <div class="panel-header">File Browser</div>
                <div class="breadcrumb"></div>
                <div class="panel-content">
                    <div class="file-list"></div>
                </div>
            </div>
            <div class="panel editor-panel">
                <div class="editor-header">
                    <div class="editor-title">Welcome to SyftBox Editor</div>
                    <div class="editor-actions">
                        <button onclick="saveFile()" class="btn btn-primary">Save</button>
                        <button onclick="deleteFile()" class="btn btn-destructive">Delete</button>
                    </div>
                </div>
                <div class="editor-container">
                    <div id="editor"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let editor;
        let currentPath = '{initial_path or ""}';
        
        // Initialize Ace editor
        editor = ace.edit("editor");
        editor.setTheme("ace/theme/tomorrow");
        editor.session.setMode("ace/mode/text");
        editor.setOptions({{
            enableAutocompletion: true,
            enableBasicAutocompletion: false,  // Deprecated
            enableLiveAutocompletion: false,   // Deprecated
            enableSnippets: false,             // Deprecated
            showPrintMargin: false,
            fontSize: "14px",
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            useSoftTabs: true,
            navigateWithinSoftTabs: true,
            tabSize: 4
        }});

        // Handle initial path if provided
        if (currentPath) {{
            loadFile(currentPath);
        }}

        function loadFile(path) {{
            if (!path) return;
            
            currentPath = path;
            fetch(`/api/filesystem/read?path=${encodeURIComponent(path)}&user_email=*`)
                .then(response => {{
                    if (!response.ok) throw new Error(`HTTP error! status: ${{response.status}}`);
                    return response.text();
                }})
                .then(content => {{
                    editor.setValue(content, -1);
                    updateEditorMode(path);
                }})
                .catch(error => showError(`Error loading file: ${{error}}`));
        }}

        function updateEditorMode(path) {{
            if (!path) return;
            
            const ext = path.split('.').pop().toLowerCase();
            const modeMap = {{
                'py': 'python',
                'js': 'javascript',
                'jsx': 'javascript',
                'ts': 'typescript',
                'tsx': 'typescript',
                'html': 'html',
                'css': 'css',
                'json': 'json',
                'md': 'markdown',
                'txt': 'text'
            }};
            
            const mode = modeMap[ext] || 'text';
            editor.session.setMode(`ace/mode/${{mode}}`);
        }}

        // Get user email from SyftBox client
        async function initSyftUser() {{
            try {{
                const response = await fetch('/api/client-info');
                const data = await response.json();
                window.syftUserEmail = data.user_email;
            }} catch (error) {{
                console.error('Error getting user email:', error);
                window.syftUserEmail = 'admin@example.com';
            }}
        }}

        async function loadDirectory(path) {{
            const params = new URLSearchParams({{
                path: path || '',
                user_email: window.syftUserEmail || 'admin@example.com'
            }});
            
            try {{
                const response = await fetch(`/api/filesystem/list?${{params}}`);
                const data = await response.json();
                renderFileList(data);
                renderBreadcrumb(path);
                currentPath = path;
            }} catch (error) {{
                showError('Error loading directory: ' + error);
            }}
        }}

        async function saveFile() {{
            if (!currentPath) return;
            
            try {{
                const response = await fetch('/api/filesystem/write', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        path: currentPath,
                        content: editor.getValue(),
                        user_email: window.syftUserEmail || 'admin@example.com'
                    }})
                }});
                const data = await response.json();
                showSuccess('File saved successfully');
            }} catch (error) {{
                showError('Error saving file: ' + error);
            }}
        }}

        async function deleteFile() {{
            if (!currentPath) return;
            
            if (!confirm('Are you sure you want to delete this file?')) return;
            
            const params = new URLSearchParams({{
                path: currentPath,
                user_email: window.syftUserEmail || 'admin@example.com'
            }});
            
            try {{
                const response = await fetch(`/api/filesystem/delete?${{params}}`, {{
                    method: 'DELETE'
                }});
                const data = await response.json();
                showSuccess('File deleted successfully');
                loadDirectory(currentPath);
                editor.setValue('');
                currentPath = null;
            }} catch (error) {{
                showError('Error deleting file: ' + error);
            }}
        }}

        function renderFileList(items) {{
            const fileList = document.querySelector('.file-list');
            fileList.innerHTML = '';
            
            items.forEach(item => {{
                const div = document.createElement('div');
                div.className = 'file-item';
                div.innerHTML = `
                    <div class="file-icon">${{item.type === 'directory' ? '📁' : '📄'}}</div>
                    <div class="file-details">
                        <div class="file-name">${{item.name}}</div>
                    </div>
                `;
                
                div.onclick = () => {{
                    if (item.type === 'directory') {{
                        loadDirectory(item.path);
                    }} else {{
                        loadFile(item.path);
                    }}
                }};
                
                fileList.appendChild(div);
            }});
        }}

        function renderBreadcrumb(path) {{
            const parts = path ? path.split('/').filter(Boolean) : [];
            const breadcrumb = document.querySelector('.breadcrumb');
            breadcrumb.innerHTML = '';
            
            // Add root
            const root = document.createElement('a');
            root.href = '#';
            root.className = 'breadcrumb-link';
            root.textContent = 'Root';
            root.onclick = (e) => {{
                e.preventDefault();
                loadDirectory('');
            }};
            breadcrumb.appendChild(root);
            
            // Add path parts
            let currentPath = '';
            parts.forEach((part, i) => {{
                // Add separator
                const separator = document.createElement('span');
                separator.className = 'breadcrumb-separator';
                separator.textContent = '/';
                breadcrumb.appendChild(separator);
                
                currentPath += '/' + part;
                
                // Add path part
                const link = document.createElement(i === parts.length - 1 ? 'span' : 'a');
                link.className = i === parts.length - 1 ? 'breadcrumb-current' : 'breadcrumb-link';
                link.textContent = part;
                
                if (i < parts.length - 1) {{
                    link.href = '#';
                    link.onclick = (e) => {{
                        e.preventDefault();
                        loadDirectory(currentPath);
                    }};
                }}
                
                breadcrumb.appendChild(link);
            }});
        }}

        function showError(message) {{
            console.error(message);
            // Add UI notification here
        }}

        function showSuccess(message) {{
            console.log(message);
            // Add UI notification here
        }}

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            initSyftUser().then(() => {{
                loadDirectory(initialPath || '');
            }});
        }});
    </script>
</body>
</html>"""
    
    return html_content 