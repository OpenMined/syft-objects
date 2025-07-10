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
    if hasattr(target_obj, 'mock') and hasattr(target_obj.mock, 'get_path'):
        mock_path = target_obj.mock.get_path()
    elif hasattr(target_obj, 'mock') and hasattr(target_obj.mock, 'path'):
        mock_path = target_obj.mock.path
    else:
        mock_path = getattr(target_obj, 'mock_path', None)
    
    if hasattr(target_obj, 'private') and hasattr(target_obj.private, 'get_path'):
        private_path = target_obj.private.get_path()
    elif hasattr(target_obj, 'private') and hasattr(target_obj.private, 'path'):
        private_path = target_obj.private.path
    else:
        private_path = getattr(target_obj, 'private_path', None)
    
    if hasattr(target_obj, 'syftobject_config') and hasattr(target_obj.syftobject_config, 'get_path'):
        syftobject_path = target_obj.syftobject_config.get_path()
    elif hasattr(target_obj, 'syftobject_config') and hasattr(target_obj.syftobject_config, 'path'):
        syftobject_path = target_obj.syftobject_config.path
    else:
        syftobject_path = getattr(target_obj, 'syftobject_path', None)
    
    # Check if paths point to folders
    mock_is_folder = False
    private_is_folder = False
    
    if mock_path:
        mock_is_folder = Path(mock_path).is_dir() if Path(mock_path).exists() else False
    
    if private_path:
        private_is_folder = Path(private_path).is_dir() if Path(private_path).exists() else False
    
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
            background: white;
            padding: 0;
            margin: 0;
            color: #374151;
            font-size: 12px;
            line-height: 1.4;
            height: 100vh;
            overflow: hidden;
        }}
        
        .widget-container {{
            background: white;
            border-radius: 0;
            box-shadow: none;
            width: 100%;
            max-width: none;
            margin: 0;
            height: 100%;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}
        
        
        .tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 1px solid #e5e7eb;
            overflow-x: auto;
            justify-content: space-between;
            align-items: center;
        }}
        
        .tabs-left {{
            display: flex;
        }}
        
        .tabs-right {{
            display: flex;
            gap: 6px;
            padding-right: 12px;
        }}
        
        .tab {{
            padding: 6px 16px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 12px;
            color: #6b7280;
            white-space: nowrap;
            transition: all 0.2s;
            position: relative;
            font-weight: 500;
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
            padding: 12px;
            animation: fadeIn 0.3s ease-in-out;
            flex: 1;
            overflow-y: auto;
            min-height: 0;
        }}
        
        /* Files, Permissions, and Metadata tabs should have no left/right padding */
        #files-tab {{
            padding: 0;
        }}
        
        #permissions-tab {{
            padding: 12px 0;
        }}
        
        #metadata-tab {{
            padding: 12px 0;
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
            margin-bottom: 8px;
        }}
        
        .form-label {{
            display: block;
            font-size: 10px;
            font-weight: 600;
            color: #6b7280;
            margin-bottom: 2px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .form-input {{
            width: 100%;
            padding: 4px 8px;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            font-size: 12px;
            transition: all 0.2s;
            font-family: inherit;
            background: white;
        }}
        
        .form-input:focus {{
            outline: none;
            border: 2px solid transparent;
            background-image: linear-gradient(white, white), 
                              linear-gradient(90deg, 
                                rgba(255, 0, 0, 0.3) 0%,
                                rgba(255, 127, 0, 0.3) 14%,
                                rgba(255, 255, 0, 0.3) 28%,
                                rgba(0, 255, 0, 0.3) 42%,
                                rgba(0, 255, 255, 0.3) 56%,
                                rgba(0, 0, 255, 0.3) 70%,
                                rgba(148, 0, 211, 0.3) 84%,
                                rgba(255, 0, 0, 0.3) 100%);
            background-origin: border-box;
            background-clip: padding-box, border-box;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
            animation: rainbowBorder 8s linear infinite;
        }}
        
        @keyframes rainbowBorder {{
            0% {{
                background-image: linear-gradient(white, white), 
                                  linear-gradient(90deg, 
                                    rgba(255, 0, 0, 0.3) 0%,
                                    rgba(255, 127, 0, 0.3) 14%,
                                    rgba(255, 255, 0, 0.3) 28%,
                                    rgba(0, 255, 0, 0.3) 42%,
                                    rgba(0, 255, 255, 0.3) 56%,
                                    rgba(0, 0, 255, 0.3) 70%,
                                    rgba(148, 0, 211, 0.3) 84%,
                                    rgba(255, 0, 0, 0.3) 100%);
            }}
            100% {{
                background-image: linear-gradient(white, white), 
                                  linear-gradient(450deg, 
                                    rgba(255, 0, 0, 0.3) 0%,
                                    rgba(255, 127, 0, 0.3) 14%,
                                    rgba(255, 255, 0, 0.3) 28%,
                                    rgba(0, 255, 0, 0.3) 42%,
                                    rgba(0, 255, 255, 0.3) 56%,
                                    rgba(0, 0, 255, 0.3) 70%,
                                    rgba(148, 0, 211, 0.3) 84%,
                                    rgba(255, 0, 0, 0.3) 100%);
            }}
        }}
        
        .form-input:disabled {{
            background: #f3f4f6;
            color: #9ca3af;
            cursor: not-allowed;
        }}
        
        textarea.form-input {{
            resize: vertical;
            min-height: 32px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 6px;
            margin-bottom: 8px;
        }}
        
        .info-item {{
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid #e5e7eb;
        }}
        
        .info-label {{
            font-size: 10px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 2px;
            line-height: 1.2;
        }}
        
        .info-value {{
            font-size: 12px;
            color: #111827;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-weight: 500;
            line-height: 1.3;
            word-break: break-all;
        }}
        
        .sub-tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 1px solid #e5e7eb;
            overflow-x: auto;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .sub-tab {{
            padding: 6px 12px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 11px;
            color: #6b7280;
            white-space: nowrap;
            transition: all 0.15s;
            position: relative;
            font-weight: 500;
        }}
        
        .sub-tab:hover {{
            color: #374151;
            background: #f3f4f6;
        }}
        
        .sub-tab.active {{
            color: #111827;
            background: white;
            border-bottom: 2px solid #3b82f6;
        }}
        
        .file-tab-content {{
            display: none;
            position: relative;
            flex: 1;
            overflow-y: auto;
            height: 100%;
        }}
        
        .file-tab-content.active {{
            display: block;
        }}
        
        .file-toolbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 10px;
            background: #f8f9fa;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .file-path {{
            font-size: 11px;
            color: #6b7280;
        }}
        
        .file-path code {{
            font-family: 'SF Mono', Monaco, monospace;
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}
        
        .file-iframe-full {{
            width: 100%;
            height: calc(100vh - 54px);
            border: none;
            background: white;
        }}
        
        .file-not-found {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 320px;
            background: #f9fafb;
            border-radius: 8px;
            text-align: center;
            padding: 20px;
        }}
        
        .file-not-found svg {{
            margin-bottom: 16px;
        }}
        
        .file-not-found h3 {{
            color: #374151;
            font-size: 16px;
            margin: 0 0 6px 0;
            font-weight: 600;
        }}
        
        .file-not-found p {{
            color: #6b7280;
            font-size: 12px;
            margin: 0;
            max-width: 400px;
        }}
        
        .btn {{
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 500;
            border: 1px solid transparent;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 3px;
            line-height: 1.4;
        }}
        
        .btn-sm {{
            padding: 3px 8px;
            font-size: 10px;
        }}
        
        /* Primary button - more transparent and airy pastel */
        .btn-primary {{
            background: rgba(147, 197, 253, 0.25);  /* Very light pastel blue */
            color: #3b82f6;
            border-color: rgba(147, 197, 253, 0.4);
            backdrop-filter: blur(4px);
        }}
        
        .btn-primary:hover {{
            background: rgba(147, 197, 253, 0.35);  /* Slightly more opaque on hover */
            border-color: rgba(147, 197, 253, 0.5);
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(147, 197, 253, 0.2);
        }}
        
        /* Secondary button - gray with transparency */
        .btn-secondary {{
            background: rgba(107, 114, 128, 0.05);
            color: #6b7280;
            border-color: rgba(107, 114, 128, 0.1);
        }}
        
        .btn-secondary:hover {{
            background: rgba(107, 114, 128, 0.1);
            border-color: rgba(107, 114, 128, 0.2);
        }}
        
        /* Danger button - red with transparency */
        .btn-danger {{
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            border-color: rgba(239, 68, 68, 0.2);
        }}
        
        .btn-danger:hover {{
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.3);
        }}
        
        /* Additional button colors - consistent neutral style */
        .btn-mint {{
            background: #f3f4f6;
            color: #374151;
        }}
        
        .btn-mint:hover {{
            background: #e5e7eb;
        }}
        
        .btn-peach {{
            background: #f3f4f6;
            color: #374151;
        }}
        
        .btn-peach:hover {{
            background: #e5e7eb;
        }}
        
        .btn-lavender {{
            background: #f3f4f6;
            color: #374151;
        }}
        
        .btn-lavender:hover {{
            background: #e5e7eb;
        }}
        
        .btn-lemon {{
            background: #f3f4f6;
            color: #374151;
        }}
        
        .btn-lemon:hover {{
            background: #e5e7eb;
        }}
        
        .permissions-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 12px;
        }}
        
        .permissions-section {{
            background: #f8f9fa;
            border-radius: 6px;
            padding: 10px 12px;
            border: 1px solid #e5e7eb;
        }}
        
        .permissions-section.full-width {{
            grid-column: 1 / -1;
        }}
        
        .permissions-section.half-width {{
            grid-column: span 1;
        }}
        
        .permissions-title {{
            font-size: 12px;
            font-weight: 600;
            color: #374151;
            margin-bottom: 6px;
        }}
        
        .permission-group {{
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .permission-group:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        
        .permission-label {{
            font-size: 12px;
            font-weight: 600;
            color: #6b7280;
            margin-bottom: 4px;
        }}
        
        .email-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 6px;
            min-height: 24px;
            align-items: center;
        }}
        
        .email-tag {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 6px;
            background: #e0e7ff;
            color: #3730a3;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 500;
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
            gap: 4px;
            margin-top: 2px;
        }}
        
        .add-email input {{
            flex: 1;
            padding: 3px 6px;
            border: 1px solid #d1d5db;
            border-radius: 3px;
            font-size: 11px;
            line-height: 1.3;
            transition: all 0.3s ease;
        }}
        
        .add-email input:focus {{
            outline: none;
            border: 2px solid transparent;
            background-image: linear-gradient(white, white), 
                              linear-gradient(90deg, 
                                rgba(255, 0, 0, 0.3) 0%,
                                rgba(255, 127, 0, 0.3) 14%,
                                rgba(255, 255, 0, 0.3) 28%,
                                rgba(0, 255, 0, 0.3) 42%,
                                rgba(0, 255, 255, 0.3) 56%,
                                rgba(0, 0, 255, 0.3) 70%,
                                rgba(148, 0, 211, 0.3) 84%,
                                rgba(255, 0, 0, 0.3) 100%);
            background-origin: border-box;
            background-clip: padding-box, border-box;
            box-shadow: 0 0 6px rgba(0, 0, 0, 0.05);
            animation: rainbowBorder 8s linear infinite;
        }}
        
        .metadata-editor {{
            background: #f8f9fa;
            border-radius: 0;
            padding: 16px;
            border-top: 1px solid #e5e7eb;
            border-bottom: 1px solid #e5e7eb;
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
            transition: all 0.3s ease;
        }}
        
        .metadata-key:focus {{
            outline: none;
            border: 2px solid transparent;
            background-image: linear-gradient(white, white), 
                              linear-gradient(90deg, 
                                rgba(255, 0, 0, 0.3) 0%,
                                rgba(255, 127, 0, 0.3) 14%,
                                rgba(255, 255, 0, 0.3) 28%,
                                rgba(0, 255, 0, 0.3) 42%,
                                rgba(0, 255, 255, 0.3) 56%,
                                rgba(0, 0, 255, 0.3) 70%,
                                rgba(148, 0, 211, 0.3) 84%,
                                rgba(255, 0, 0, 0.3) 100%);
            background-origin: border-box;
            background-clip: padding-box, border-box;
            box-shadow: 0 0 6px rgba(0, 0, 0, 0.05);
            animation: rainbowBorder 8s linear infinite;
        }}
        
        .metadata-value {{
            flex: 1;
            padding: 6px 10px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 13px;
            font-family: monospace;
            transition: all 0.3s ease;
        }}
        
        .metadata-value:focus {{
            outline: none;
            border: 2px solid transparent;
            background-image: linear-gradient(white, white), 
                              linear-gradient(90deg, 
                                rgba(255, 0, 0, 0.3) 0%,
                                rgba(255, 127, 0, 0.3) 14%,
                                rgba(255, 255, 0, 0.3) 28%,
                                rgba(0, 255, 0, 0.3) 42%,
                                rgba(0, 255, 255, 0.3) 56%,
                                rgba(0, 0, 255, 0.3) 70%,
                                rgba(148, 0, 211, 0.3) 84%,
                                rgba(255, 0, 0, 0.3) 100%);
            background-origin: border-box;
            background-clip: padding-box, border-box;
            box-shadow: 0 0 6px rgba(0, 0, 0, 0.05);
            animation: rainbowBorder 8s linear infinite;
        }}
        
        .metadata-remove {{
            padding: 4px 10px;
            background: #fecaca;
            color: #7f1d1d;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
        }}
        
        .metadata-remove:hover {{
            background: #fca5a5;
        }}
        
        .add-metadata {{
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }}
        
        
        .danger-zone {{
            margin-top: 12px;
            padding: 8px 10px;
            border: 1px solid rgba(254, 202, 202, 0.5);
            border-radius: 6px;
            background: rgba(254, 242, 242, 0.3);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }}
        
        .danger-zone-header {{
            flex: 1;
        }}
        
        .danger-zone-title {{
            font-size: 11px;
            font-weight: 500;
            color: #ef4444;
            margin: 0;
            opacity: 0.8;
        }}
        
        .danger-zone-description {{
            font-size: 10px;
            color: #dc2626;
            margin: 0;
            opacity: 0.7;
        }}
        
        .status-message {{
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            margin-bottom: 12px;
            display: none;
        }}
        
        .status-success {{
            color: #065f46;
            border: 1px solid #bbf7d0;
            animation: rainbowPastel 3s ease-in-out;
        }}
        
        @keyframes rainbowPastel {{
            0% {{ background: #ffcccc; border-color: #ffb3b3; }} /* Pastel Pink */
            14% {{ background: #ffd9b3; border-color: #ffc299; }} /* Pastel Orange */
            28% {{ background: #ffffcc; border-color: #ffffb3; }} /* Pastel Yellow */
            42% {{ background: #ccffcc; border-color: #b3ffb3; }} /* Pastel Green */
            57% {{ background: #ccffff; border-color: #b3ffff; }} /* Pastel Cyan */
            71% {{ background: #ccccff; border-color: #b3b3ff; }} /* Pastel Blue */
            85% {{ background: #ffccff; border-color: #ffb3ff; }} /* Pastel Purple */
            100% {{ background: #dcfce7; border-color: #bbf7d0; }} /* Final teal */
        }}
        
        .status-error {{
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }}
        
        .loading {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid #f3f4f6;
            border-top-color: #3b82f6;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        @media (max-width: 768px) {{
            .permissions-grid {{
                grid-template-columns: 1fr;
            }}
            
            .permissions-section.half-width {{
                grid-column: 1 / -1;
            }}
        }}
    </style>
</head>
<body>
    <div class="widget-container">
        <div class="tabs">
            <div class="tabs-left">
                <button class="tab active" onclick="switchTab('overview')">Overview</button>
                <button class="tab" onclick="switchTab('files')">Files</button>
                <button class="tab" onclick="switchTab('permissions')">Permissions</button>
            </div>
            <div class="tabs-right">
                <button class="btn btn-secondary" onclick="openInNewTab()" title="Open in new tab">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/>
                    </svg>
                    Open
                </button>
                <button class="btn btn-secondary" onclick="refreshObject()" title="Refresh">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>
                    </svg>
                </button>
                <button id="save-overview-btn" class="btn btn-primary" onclick="saveOverview()">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"/>
                    </svg>
                    Save
                </button>
                <button id="save-permissions-btn" class="btn btn-primary" style="display: none;" onclick="savePermissions()">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z"/>
                    </svg>
                    Save Permissions
                </button>
            </div>
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
            
            <div class="form-group">
                <label class="form-label">Mock Note</label>
                <textarea id="mock-note-input" class="form-input" placeholder="Describe what makes this mock data different from the real data..."></textarea>
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
            
            <div class="danger-zone">
                <div class="danger-zone-header">
                    <h4 class="danger-zone-title">Danger Zone</h4>
                    <p class="danger-zone-description">This action cannot be undone</p>
                </div>
                <button class="btn btn-danger btn-sm" onclick="deleteObject()">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6h14zM10 11v6M14 11v6"/>
                    </svg>
                    Delete
                </button>
            </div>
        </div>
        
        <!-- Files Tab -->
        <div id="files-tab" class="tab-content">
            <div class="sub-tabs">
                <button class="sub-tab active" onclick="switchFileTab('mock')">Mock {'Folder' if mock_is_folder else 'File'}</button>
                <button class="sub-tab" onclick="switchFileTab('private')">Private {'Folder' if private_is_folder else 'File'}</button>
                <button class="sub-tab" onclick="switchFileTab('config')">Config (.syftobject.yaml)</button>
            </div>
            
            <!-- Mock File Sub-Tab -->
            <div id="file-mock" class="file-tab-content active">
                {f'<iframe id="mock-iframe" class="file-iframe-full" src="/editor?path={mock_path}&embedded=true"></iframe>' if mock_path else 
                 '''<div class="file-not-found">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="1.5">
                        <path d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <h3>File Not Found</h3>
                    <p>This file doesn't exist locally or you don't have permission to access it.</p>
                </div>'''}
            </div>
            
            <!-- Private File Sub-Tab -->
            <div id="file-private" class="file-tab-content">
                {f'<iframe id="private-iframe" class="file-iframe-full" src="/editor?path={private_path}&embedded=true"></iframe>' if private_path else 
                 '''<div class="file-not-found">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="1.5">
                        <path d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <h3>File Not Found</h3>
                    <p>This file doesn't exist locally or you don't have permission to access it.</p>
                </div>'''}
            </div>
            
            <!-- Config File Sub-Tab -->
            <div id="file-config" class="file-tab-content">
                {f'<iframe id="syftobject-iframe" class="file-iframe-full" src="/editor?path={syftobject_path}&embedded=true"></iframe>' if syftobject_path else 
                 '''<div class="file-not-found">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="1.5">
                        <path d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <h3>File Not Found</h3>
                    <p>This file doesn't exist locally or you don't have permission to access it.</p>
                </div>'''}
            </div>
        </div>
        
        <!-- Permissions Tab -->
        <div id="permissions-tab" class="tab-content">
            <div class="permissions-grid">
                <!-- Discovery Permissions - Full Width -->
                <div class="permissions-section full-width">
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
                
                <!-- Mock and Private Permissions - Side by Side -->
                <div class="permissions-section half-width">
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
                    <div class="permission-group">
                        <div class="permission-label">Admin Access</div>
                        <div id="mock-admin-list" class="email-list"></div>
                        <div class="add-email">
                            <input type="email" id="mock-admin-input" placeholder="Add email address">
                            <button class="btn btn-primary" onclick="addPermission('mock', 'admin')">Add</button>
                        </div>
                    </div>
                </div>
                
                <div class="permissions-section half-width">
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
                    <div class="permission-group">
                        <div class="permission-label">Admin Access</div>
                        <div id="private-admin-list" class="email-list"></div>
                        <div class="add-email">
                            <input type="email" id="private-admin-input" placeholder="Add email address">
                            <button class="btn btn-primary" onclick="addPermission('private', 'admin')">Add</button>
                        </div>
                    </div>
                </div>
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
            
            // Show/hide appropriate save button
            const saveOverviewBtn = document.getElementById('save-overview-btn');
            const savePermBtn = document.getElementById('save-permissions-btn');
            
            if (tabName === 'overview') {{
                saveOverviewBtn.style.display = 'inline-flex';
                savePermBtn.style.display = 'none';
            }} else if (tabName === 'permissions') {{
                saveOverviewBtn.style.display = 'none';
                savePermBtn.style.display = 'inline-flex';
            }} else {{
                saveOverviewBtn.style.display = 'none';
                savePermBtn.style.display = 'none';
            }}
        }}
        
        function switchFileTab(tabName) {{
            // Update sub-tab buttons
            document.querySelectorAll('.sub-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Update sub-tab content
            document.querySelectorAll('.file-tab-content').forEach(content => {{
                content.classList.remove('active');
            }});
            document.getElementById('file-' + tabName).classList.add('active');
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
                
                // File paths are now handled via iframes in the Files tab
                // These elements no longer exist in the HTML
                // document.getElementById('mock-path').textContent = data.paths.mock || 'Not found';
                // document.getElementById('private-path').textContent = data.paths.private || 'Not found';
                // document.getElementById('syftobject-path').textContent = data.paths.syftobject || 'Not found';
                
                // Update permissions - handle both new and old format
                if (data.permissions) {{
                    if (data.permissions.read && Array.isArray(data.permissions.read)) {{
                        // New format: {{read: [], write: [], admin: []}}
                        currentPermissions = {{
                            discovery_permissions: data.permissions.read || [],
                            mock_permissions: {{
                                "read": data.permissions.read || [],
                                "write": data.permissions.write || [],
                                "admin": data.permissions.admin || []
                            }},
                            private_permissions: {{
                                "read": data.permissions.admin || [],  // Admin has private read
                                "write": data.permissions.admin || [],  // Admin has private write
                                "admin": data.permissions.admin || []
                            }}
                        }};
                    }} else {{
                        // Old format - use as is
                        currentPermissions = data.permissions;
                    }}
                }}
                renderPermissions();
                
                // Metadata rendering removed - tab was removed
                
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
            renderPermissionList('syftobject-read-list', currentPermissions.discovery_permissions || []);
            renderPermissionList('mock-read-list', currentPermissions.mock_permissions?.read || []);
            renderPermissionList('mock-write-list', currentPermissions.mock_permissions?.write || []);
            renderPermissionList('mock-admin-list', currentPermissions.mock_permissions?.admin || []);
            renderPermissionList('private-read-list', currentPermissions.private_permissions?.read || []);
            renderPermissionList('private-write-list', currentPermissions.private_permissions?.write || []);
            renderPermissionList('private-admin-list', currentPermissions.private_permissions?.admin || []);
        }}
        
        function renderPermissionList(elementId, emails) {{
            const container = document.getElementById(elementId);
            container.innerHTML = '';
            
            if (!emails || emails.length === 0) {{
                const emptyTag = document.createElement('div');
                emptyTag.className = 'empty-state';
                emptyTag.style.fontSize = '11px';
                emptyTag.style.color = '#9ca3af';
                emptyTag.style.fontStyle = 'italic';
                emptyTag.textContent = 'No permissions set';
                container.appendChild(emptyTag);
            }} else {{
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
        }}
        
        // Metadata rendering function removed - tab was removed
        
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
                if (!currentPermissions.discovery_permissions) currentPermissions.discovery_permissions = [];
                if (!currentPermissions.discovery_permissions.includes(email)) {{
                    currentPermissions.discovery_permissions.push(email);
                }}
            }} else if (fileType === 'mock') {{
                if (!currentPermissions.mock_permissions) currentPermissions.mock_permissions = {{}};
                if (!currentPermissions.mock_permissions[permType]) currentPermissions.mock_permissions[permType] = [];
                if (!currentPermissions.mock_permissions[permType].includes(email)) {{
                    currentPermissions.mock_permissions[permType].push(email);
                }}
            }} else if (fileType === 'private') {{
                if (!currentPermissions.private_permissions) currentPermissions.private_permissions = {{}};
                if (!currentPermissions.private_permissions[permType]) currentPermissions.private_permissions[permType] = [];
                if (!currentPermissions.private_permissions[permType].includes(email)) {{
                    currentPermissions.private_permissions[permType].push(email);
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
                const index = currentPermissions.discovery_permissions?.indexOf(email);
                if (index > -1) {{
                    currentPermissions.discovery_permissions.splice(index, 1);
                }}
            }} else if (fileType === 'mock') {{
                const index = currentPermissions.mock_permissions?.[permType]?.indexOf(email);
                if (index > -1) {{
                    currentPermissions.mock_permissions[permType].splice(index, 1);
                }}
            }} else if (fileType === 'private') {{
                const index = currentPermissions.private_permissions?.[permType]?.indexOf(email);
                if (index > -1) {{
                    currentPermissions.private_permissions[permType].splice(index, 1);
                }}
            }}
            
            // Re-render
            renderPermissions();
        }}
        
        async function savePermissions() {{
            try {{
                // Convert to flat format expected by API
                const updates = {{
                    discovery_read: currentPermissions.discovery_permissions || [],
                    mock_read: currentPermissions.mock_permissions?.read || [],
                    mock_write: currentPermissions.mock_permissions?.write || [],
                    mock_admin: currentPermissions.mock_permissions?.admin || [],
                    private_read: currentPermissions.private_permissions?.read || [],
                    private_write: currentPermissions.private_permissions?.write || [],
                    private_admin: currentPermissions.private_permissions?.admin || []
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
        
        // addMetadata function removed - tab was removed
        
        // updateMetadataValue function removed - tab was removed
        
        // removeMetadata function removed - tab was removed
        
        // saveMetadata function removed - tab was removed
        
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
        
        function openInNewTab() {{
            const currentUrl = window.location.href;
            window.open(currentUrl, '_blank');
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
            }}, 3500);  // Slightly longer to show full animation
        }}
    </script>
</body>
</html>
"""
    
    return html