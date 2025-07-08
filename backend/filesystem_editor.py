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
    
    def __init__(self, base_path: str = None):
        """Initialize with optional base path restriction."""
        self.base_path = Path(base_path).resolve() if base_path else None
    
    def _validate_path(self, path: str) -> Path:
        """Validate and resolve a path, ensuring it's within allowed bounds."""
        try:
            resolved_path = Path(path).resolve()
            
            # If we have a base path, ensure the resolved path is within it
            if self.base_path and not str(resolved_path).startswith(str(self.base_path)):
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
    
    def list_directory(self, path: str) -> Dict[str, Any]:
        """List directory contents."""
        dir_path = self._validate_path(path)
        
        if not dir_path.exists():
            raise HTTPException(status_code=404, detail="Directory not found")
        
        if not dir_path.is_dir():
            raise HTTPException(status_code=400, detail="Path is not a directory")
        
        try:
            items = []
            
            for item_path in sorted(dir_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                try:
                    stat = item_path.stat()
                    is_directory = item_path.is_dir()
                    
                    item_info = {
                        'name': item_path.name,
                        'path': str(item_path),
                        'is_directory': is_directory,
                        'size': stat.st_size if not is_directory else None,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'is_editable': not is_directory and self._is_text_file(item_path),
                        'extension': item_path.suffix.lower() if not is_directory else None
                    }
                    items.append(item_info)
                    
                except (PermissionError, OSError):
                    # Skip items we can't access
                    continue
            
            # Get parent directory if not at root
            parent_path = None
            if dir_path.parent != dir_path:
                parent_path = str(dir_path.parent)
            
            return {
                'path': str(dir_path),
                'parent': parent_path,
                'items': items,
                'total_items': len(items)
            }
            
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """Read file contents."""
        file_path = self._validate_path(path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        if file_path.is_dir():
            raise HTTPException(status_code=400, detail="Path is a directory")
        
        if file_path.stat().st_size > self.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large to edit")
        
        if not self._is_text_file(file_path):
            raise HTTPException(status_code=415, detail="File type not supported for editing")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stat = file_path.stat()
            return {
                'path': str(file_path),
                'content': content,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': file_path.suffix.lower(),
                'encoding': 'utf-8'
            }
        except UnicodeDecodeError:
            raise HTTPException(status_code=415, detail="File encoding not supported")
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
    
    def write_file(self, path: str, content: str, create_dirs: bool = False) -> Dict[str, Any]:
        """Write content to a file."""
        file_path = self._validate_path(path)
        
        # Create parent directories if requested
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if parent directory exists
        if not file_path.parent.exists():
            raise HTTPException(status_code=400, detail="Parent directory does not exist")
        
        # Check if we can write to this file type
        if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=415, detail="File type not allowed for editing")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            stat = file_path.stat()
            return {
                'path': str(file_path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'message': 'File saved successfully'
            }
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Error writing file: {str(e)}")
    
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
    
    def delete_item(self, path: str, recursive: bool = False) -> Dict[str, Any]:
        """Delete a file or directory."""
        item_path = self._validate_path(path)
        
        if not item_path.exists():
            raise HTTPException(status_code=404, detail="Item not found")
        
        try:
            if item_path.is_dir():
                if recursive:
                    import shutil
                    shutil.rmtree(item_path)
                else:
                    item_path.rmdir()
            else:
                item_path.unlink()
            
            return {
                'path': str(item_path),
                'message': 'Item deleted successfully'
            }
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")


def generate_editor_html(initial_path: str = None) -> str:
    """Generate the HTML for the filesystem code editor."""
    initial_path = initial_path or str(Path.home())
    
    # Read the box.svg file
    box_svg_path = Path(__file__).parent.parent / 'box.svg'
    try:
        with open(box_svg_path, 'r') as f:
            box_svg = f.read()
    except:
        # Fallback if box.svg is not found
        box_svg = '<div class="logo">S</div>'
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SyftBox File Editor</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
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
            <div class="panel">
                <div class="panel-header">
                    📁 File Explorer
                </div>
                <div class="breadcrumb" id="breadcrumb">
                    <div class="loading">Loading...</div>
                </div>
                <div class="panel-content">
                    <div class="file-list" id="fileList">
                        <div class="loading">Loading files...</div>
                    </div>
                </div>
            </div>
            
            <div class="panel">
                <div class="editor-container">
                    <div class="editor-header">
                        <div class="editor-title" id="editorTitle">No file selected</div>
                        <div class="editor-actions">
                            <button class="btn btn-primary" id="saveBtn" disabled>
                                💾 Save
                            </button>
                            <button class="btn btn-secondary" id="newFileBtn">
                                📄 New File
                            </button>
                            <button class="btn btn-secondary" id="newFolderBtn">
                                📁 New Folder
                            </button>
                        </div>
                    </div>
                    <div class="panel-content">
                        <div class="empty-state" id="emptyState">
                            {box_svg}
                            <h3>Welcome to SyftBox Editor</h3>
                            <p>Select a file from the explorer to start editing</p>
                        </div>
                        <textarea class="editor-textarea" id="editor" style="display: none;" placeholder="Start typing..."></textarea>
                    </div>
                    <div class="status-bar">
                        <div class="status-left">
                            <span id="fileInfo">Ready</span>
                        </div>
                        <div class="status-right">
                            <span id="cursorPosition">Ln 1, Col 1</span>
                            <span id="fileSize">0 bytes</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        class FileSystemEditor {{
            constructor() {{
                this.currentPath = '{initial_path}';
                this.currentFile = null;
                this.isModified = false;
                this.initializeElements();
                this.setupEventListeners();
                this.loadDirectory(this.currentPath);
            }}
            
            initializeElements() {{
                this.fileList = document.getElementById('fileList');
                this.editor = document.getElementById('editor');
                this.saveBtn = document.getElementById('saveBtn');
                this.newFileBtn = document.getElementById('newFileBtn');
                this.newFolderBtn = document.getElementById('newFolderBtn');
                this.editorTitle = document.getElementById('editorTitle');
                this.emptyState = document.getElementById('emptyState');
                this.breadcrumb = document.getElementById('breadcrumb');
                this.fileInfo = document.getElementById('fileInfo');
                this.cursorPosition = document.getElementById('cursorPosition');
                this.fileSize = document.getElementById('fileSize');
            }}
            
            setupEventListeners() {{
                this.saveBtn.addEventListener('click', () => this.saveFile());
                this.newFileBtn.addEventListener('click', () => this.createNewFile());
                this.newFolderBtn.addEventListener('click', () => this.createNewFolder());
                
                this.editor.addEventListener('input', () => {{
                    this.isModified = true;
                    this.updateUI();
                }});
                
                this.editor.addEventListener('keyup', () => this.updateCursorPosition());
                this.editor.addEventListener('click', () => this.updateCursorPosition());
                
                // Auto-save on Ctrl+S
                document.addEventListener('keydown', (e) => {{
                    if (e.ctrlKey && e.key === 's') {{
                        e.preventDefault();
                        if (this.currentFile) {{
                            this.saveFile();
                        }}
                    }}
                }});
            }}
            
            async loadDirectory(path) {{
                try {{
                    const response = await fetch(`/api/filesystem/list?path=${{encodeURIComponent(path)}}`);
                    const data = await response.json();
                    
                    if (!response.ok) {{
                        throw new Error(data.detail || 'Failed to load directory');
                    }}
                    
                    this.currentPath = data.path;
                    this.renderFileList(data.items);
                    this.renderBreadcrumb(data.path, data.parent);
                    
                }} catch (error) {{
                    this.showError('Failed to load directory: ' + error.message);
                }}
            }}
            
            renderFileList(items) {{
                if (items.length === 0) {{
                    this.fileList.innerHTML = `
                        <div class="empty-state">
                            <p>No files found in this directory</p>
                        </div>
                    `;
                    return;
                }}
                
                this.fileList.innerHTML = items.map(item => `
                    <div class="file-item" data-path="${item.path}">
                        <div class="file-icon">
                            ${{item.is_directory ? '📁' : item.is_editable ? '📄' : '📎'}}
                        </div>
                        <div class="file-details">
                            <div class="file-name">${item.name}</div>
                            <div class="file-meta">
                                ${{item.is_directory ? 'Directory' : this.formatSize(item.size)}} • 
                                ${{new Date(item.modified).toLocaleString()}}
                            </div>
                        </div>
                    </div>
                `).join('');
                
                this.fileList.querySelectorAll('.file-item').forEach(item => {{
                    item.addEventListener('click', () => {{
                        const path = item.dataset.path;
                        const isDirectory = item.querySelector('.file-icon').textContent.includes('📁');
                        
                        if (isDirectory) {{
                            this.loadDirectory(path);
                        }} else {{
                            this.loadFile(path);
                        }}
                    }});
                }});
            }}
            
            renderBreadcrumb(path, parent) {{
                const parts = path.split('/').filter(Boolean);
                let currentPath = '';
                
                const breadcrumbItems = parts.map((part, index) => {{
                    currentPath += '/' + part;
                    const isLast = index === parts.length - 1;
                    
                    if (isLast) {{
                        return `<div class="breadcrumb-item">
                            <span class="breadcrumb-current">${part}</span>
                        </div>`;
                    }}
                    
                    return `<div class="breadcrumb-item">
                        <a href="#" class="breadcrumb-link" data-path="${currentPath}">${part}</a>
                        <span class="breadcrumb-separator">›</span>
                    </div>`;
                }});
                
                // Add root
                breadcrumbItems.unshift(`
                    <div class="breadcrumb-item">
                        <a href="#" class="breadcrumb-link" data-path="/">root</a>
                        <span class="breadcrumb-separator">›</span>
                    </div>
                `);
                
                this.breadcrumb.innerHTML = breadcrumbItems.join('');
                
                this.breadcrumb.querySelectorAll('.breadcrumb-link').forEach(link => {{
                    link.addEventListener('click', (e) => {{
                        e.preventDefault();
                        this.loadDirectory(link.dataset.path);
                    }});
                }});
            }}
            
            async loadFile(path) {{
                try {{
                    const response = await fetch(`/api/filesystem/read?path=${{encodeURIComponent(path)}}`);
                    const data = await response.json();
                    
                    if (!response.ok) {{
                        throw new Error(data.detail || 'Failed to load file');
                    }}
                    
                    this.currentFile = data;
                    this.editor.value = data.content;
                    this.isModified = false;
                    this.updateUI();
                    
                    // Show editor
                    this.emptyState.style.display = 'none';
                    this.editor.style.display = 'block';
                    this.editor.focus();
                    
                }} catch (error) {{
                    this.showError('Failed to load file: ' + error.message);
                }}
            }}
            
            async saveFile() {{
                if (!this.currentFile) return;
                
                try {{
                    const response = await fetch('/api/filesystem/write', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            path: this.currentFile.path,
                            content: this.editor.value
                        }})
                    }});
                    
                    const data = await response.json();
                    
                    if (!response.ok) {{
                        throw new Error(data.detail || 'Failed to save file');
                    }}
                    
                    this.isModified = false;
                    this.updateUI();
                    this.showSuccess('File saved successfully');
                    
                }} catch (error) {{
                    this.showError('Failed to save file: ' + error.message);
                }}
            }}
            
            async createNewFile() {{
                const name = prompt('Enter file name:');
                if (!name) return;
                
                const path = `${{this.currentPath}}/${{name}}`;
                
                try {{
                    const response = await fetch('/api/filesystem/write', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            path,
                            content: '',
                            create_dirs: true
                        }})
                    }});
                    
                    const data = await response.json();
                    
                    if (!response.ok) {{
                        throw new Error(data.detail || 'Failed to create file');
                    }}
                    
                    await this.loadDirectory(this.currentPath);
                    await this.loadFile(path);
                    
                }} catch (error) {{
                    this.showError('Failed to create file: ' + error.message);
                }}
            }}
            
            async createNewFolder() {{
                const name = prompt('Enter folder name:');
                if (!name) return;
                
                const path = `${{this.currentPath}}/${{name}}`;
                
                try {{
                    const response = await fetch('/api/filesystem/mkdir', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ path }})
                    }});
                    
                    const data = await response.json();
                    
                    if (!response.ok) {{
                        throw new Error(data.detail || 'Failed to create folder');
                    }}
                    
                    await this.loadDirectory(this.currentPath);
                    
                }} catch (error) {{
                    this.showError('Failed to create folder: ' + error.message);
                }}
            }}
            
            updateUI() {{
                if (this.currentFile) {{
                    this.editorTitle.textContent = this.currentFile.path;
                    this.saveBtn.disabled = !this.isModified;
                    this.fileInfo.textContent = this.isModified ? 'Modified' : 'Saved';
                    this.fileSize.textContent = this.formatSize(this.editor.value.length);
                    this.updateCursorPosition();
                }} else {{
                    this.editorTitle.textContent = 'No file selected';
                    this.saveBtn.disabled = true;
                    this.fileInfo.textContent = 'Ready';
                    this.fileSize.textContent = '0 bytes';
                    this.cursorPosition.textContent = 'Ln 1, Col 1';
                }}
            }}
            
            updateCursorPosition() {{
                const pos = this.editor.selectionStart;
                const lines = this.editor.value.substr(0, pos).split('\n');
                const line = lines.length;
                const col = lines[lines.length - 1].length + 1;
                this.cursorPosition.textContent = `Ln ${{line}}, Col ${{col}}`;
            }}
            
            formatSize(bytes) {{
                if (bytes === 0) return '0 bytes';
                const k = 1024;
                const sizes = ['bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
            }}
            
            showError(message) {{
                const error = document.createElement('div');
                error.className = 'error';
                error.textContent = message;
                this.fileList.insertAdjacentElement('afterbegin', error);
                setTimeout(() => error.remove(), 5000);
            }}
            
            showSuccess(message) {{
                const success = document.createElement('div');
                success.className = 'success';
                success.textContent = message;
                this.fileList.insertAdjacentElement('afterbegin', success);
                setTimeout(() => success.remove(), 3000);
            }}
        }}
        
        new FileSystemEditor();
    </script>
</body>
</html>
"""
    return html_content 