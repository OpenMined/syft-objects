"""
Pure Python FastAPI backend for syft-objects with integrated HTML generation
No Node.js dependencies - serves HTML directly from Python
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path as PathLib

from fastapi import FastAPI, Depends, HTTPException, Body, Path, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse
from loguru import logger
from fastapi.staticfiles import StaticFiles

# Import filesystem editor components
import sys
sys.path.append(str(PathLib(__file__).parent))
from filesystem_editor import FileSystemManager, generate_editor_html

try:
    from syft_objects import objects
    from syft_objects.collections import ObjectsCollection
    from syft_objects.models import SyftObject
    from syft_objects.client import get_syftbox_client, SYFTBOX_AVAILABLE
except ImportError:
    logger.error("syft-objects not available")
    objects = None
    ObjectsCollection = None
    SyftObject = None
    get_syftbox_client = None
    SYFTBOX_AVAILABLE = False


app = FastAPI(
    title="Syft Objects API (Pure Python)",
    description="Manage and view syft objects from the distributed file system - Pure Python implementation",
    version="0.1.0",
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:*",
        "http://127.0.0.1:*"
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom HTML generation removed - now serving actual Next.js application

# All custom HTML generation functions removed - now serving actual Next.js application

# Mount Next.js static files
from fastapi.staticfiles import StaticFiles

# Mount the Next.js build directory to serve static assets
try:
    app.mount("/_next", StaticFiles(directory="frontend/_next"), name="nextjs_static")
    logger.info("✅ Next.js static files mounted successfully")
except Exception as e:
    logger.warning(f"Could not mount Next.js static files: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Get application status."""
    syftbox_status = "not_available"
    syftbox_email = None
    
    if SYFTBOX_AVAILABLE:
        try:
            client = get_syftbox_client()
            if client:
                syftbox_status = "connected"
                syftbox_email = getattr(client, 'email', 'unknown')
            else:
                syftbox_status = "disconnected"
        except Exception:
            syftbox_status = "error"
    
    return {
        "app": "Syft Objects UI",
        "version": "0.1.0",
        "timestamp": datetime.now(),
        "syftbox": {
            "status": syftbox_status,
            "user_email": syftbox_email
        },
        "components": {
            "backend": "running",
            "objects_collection": "available" if objects else "unavailable"
        }
    }

@app.get("/api/client-info")
async def get_client_info(request: Request):
    """Get client information including user email."""
    # In a real setup, this would come from authentication
    # For now, we'll use a mock user
    return {
        "user_email": "admin@example.com",
        "permissions": ["read", "write", "admin"]
    }

@app.get("/api/objects")
async def get_objects(
    search: Optional[str] = None,
    email_filter: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """Get syft objects with optional filtering and pagination."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        # Start with all objects
        collection = objects
        
        # Apply search filter
        if search:
            collection = collection.search(search)
        
        # Apply email filter
        if email_filter:
            collection = collection.filter_by_email(email_filter)
        
        # Convert to list and sort by creation date (oldest first for proper indexing)
        all_objects = collection.to_list()
        # Sort by created_at (oldest first) so index 0/1 represents the oldest object
        all_objects.sort(key=lambda x: x.created_at or datetime.min, reverse=False)
        total_count = len(all_objects)
        
        # Apply pagination
        start_idx = offset
        end_idx = start_idx + limit if limit else len(all_objects)
        paginated_objects = all_objects[start_idx:end_idx]
        
        # Convert objects to dict format
        objects_data = []
        for page_idx, obj in enumerate(paginated_objects):
            # Calculate the actual index in the full collection (0-based, ordered by creation)
            actual_index = start_idx + page_idx
            # Extract email from private URL
            email = "unknown@example.com"
            try:
                if obj.private_url.startswith("syft://"):
                    parts = obj.private_url.split("/")
                    if len(parts) >= 3:
                        email = parts[2]
            except:
                pass
            
            # Handle both raw SyftObject and CleanSyftObject
            raw_obj = obj._obj if hasattr(obj, '_obj') else obj
            
            # Get file type - try multiple approaches
            if hasattr(raw_obj, 'get_file_type'):
                file_type = raw_obj.get_file_type()
            elif hasattr(raw_obj, 'get_type'):
                file_type = raw_obj.get_type()
            elif hasattr(raw_obj, 'object_type'):
                file_type = raw_obj.object_type
            else:
                file_type = "file"  # Default fallback
                
            obj_data = {
                "index": actual_index,
                "uid": str(obj.uid),
                "name": obj.name or "Unnamed Object",
                "description": obj.description or "",
                "type": file_type,
                "email": email,
                "private_url": obj.private_url,
                "mock_url": obj.mock_url,
                "syftobject_url": obj.syftobject,
                "created_at": obj.created_at.isoformat() if obj.created_at else None,
                "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
                "permissions": {
                    "syftobject": obj.syftobject_permissions,
                    "mock_read": obj.mock_permissions,
                    "mock_write": obj.mock_write_permissions,
                    "private_read": obj.private_permissions,
                    "private_write": obj.private_write_permissions,
                },
                "metadata": obj.metadata,
                "file_exists": {
                    "private": obj._check_file_exists(obj.private_url),
                    "mock": obj._check_file_exists(obj.mock_url),
                }
            }
            objects_data.append(obj_data)
        
        return {
            "objects": objects_data,
            "total_count": total_count,
            "offset": offset,
            "limit": limit,
            "has_more": end_idx < total_count,
            "search_info": getattr(collection, '_search_info', None)
        }
    
    except Exception as e:
        logger.error(f"Error getting objects: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving objects: {str(e)}")

@app.post("/api/objects")
async def create_object(
    name: str = Body(...),
    description: str = Body(""),
    email: str = Body(""),
    file_content: str = Body(""),  # Legacy single file support
    filename: str = Body(""),      # Legacy single file support
    private_file_content: str = Body(""),  # New dual file support
    private_filename: str = Body(""),      # New dual file support
    mock_file_content: str = Body(""),     # New dual file support
    mock_filename: str = Body(""),         # New dual file support
    metadata: Dict[str, Any] = Body({}),
    permissions: Dict[str, List[str]] = Body({})
) -> Dict[str, Any]:
    """Create a new syft object."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    # Debug logging
    logger.info(f"🚀 Creating object with parameters:")
    logger.info(f"  name: {name}")
    logger.info(f"  description: {description}")
    logger.info(f"  email: {email}")
    logger.info(f"  private_file_content length: {len(private_file_content) if private_file_content else 0}")
    logger.info(f"  private_filename: {private_filename}")
    logger.info(f"  mock_file_content length: {len(mock_file_content) if mock_file_content else 0}")
    logger.info(f"  mock_filename: {mock_filename}")
    logger.info(f"  legacy file_content length: {len(file_content) if file_content else 0}")
    logger.info(f"  legacy filename: {filename}")
    
    try:
        # Import the syobj factory function
        from syft_objects.factory import syobj
        
        # Get the current SyftBox client to get user info
        client = None
        if SYFTBOX_AVAILABLE:
            try:
                client = get_syftbox_client()
            except Exception:
                pass
        
        # Use provided email or fallback to client email
        user_email = email or (client.email if client else "admin@example.com")
        
        # Extract permissions from the permissions dict
        mock_read = permissions.get("mock_read", ["public"])
        mock_write = permissions.get("mock_write", [])
        private_read = permissions.get("private_read", [user_email])
        private_write = permissions.get("private_write", [user_email])
        discovery_read = permissions.get("syftobject", ["public"])
        
        # Prepare metadata with system settings
        extended_metadata = metadata.copy()
        extended_metadata.update({
            "description": description,
            "email": user_email,
            "auto_save": True,
            "move_files_to_syftbox": True,
            "create_syftbox_permissions": True
        })
        
        # Handle file creation - preserve filename if uploaded
        import tempfile
        from pathlib import Path as PathLib
        
        # Check for dual file approach first (new method)
        if private_file_content or mock_file_content:
            temp_dir = PathLib("tmp")
            temp_dir.mkdir(exist_ok=True)
            
            private_file_path = None
            mock_file_path = None
            
            # Handle private file
            if private_file_content:
                if private_filename:
                    private_file_path = temp_dir / private_filename
                else:
                    private_file_path = temp_dir / f"{name}_private.txt"
                private_file_path.write_text(private_file_content)
                logger.info(f"📝 Created private file: {private_file_path} with {len(private_file_content)} chars")
            
            # Handle mock file
            if mock_file_content:
                if mock_filename:
                    mock_file_path = temp_dir / mock_filename
                else:
                    mock_file_path = temp_dir / f"{name}_mock.txt"
                mock_file_path.write_text(mock_file_content)
                logger.info(f"📝 Created mock file: {mock_file_path} with {len(mock_file_content)} chars")
            
            # Create the object using the dual file approach
            if private_file_path and mock_file_path:
                new_object = syobj(
                    name=name,
                    private_file=str(private_file_path),
                    mock_file=str(mock_file_path),
                    mock_read=mock_read,
                    mock_write=mock_write,
                    private_read=private_read,
                    private_write=private_write,
                    discovery_read=discovery_read,
                    metadata=extended_metadata
                )
            elif private_file_path:
                new_object = syobj(
                    name=name,
                    private_file=str(private_file_path),
                    mock_contents=f"[AUTO-GENERATED] Mock content for {name}",
                    mock_read=mock_read,
                    mock_write=mock_write,
                    private_read=private_read,
                    private_write=private_write,
                    discovery_read=discovery_read,
                    metadata=extended_metadata
                )
            else:  # only mock file
                new_object = syobj(
                    name=name,
                    private_contents=f"[AUTO-GENERATED] Private content for {name}",
                    mock_file=str(mock_file_path),
                    mock_read=mock_read,
                    mock_write=mock_write,
                    private_read=private_read,
                    private_write=private_write,
                    discovery_read=discovery_read,
                    metadata=extended_metadata
                )
        
        # Fallback to legacy single file approach
        elif filename and file_content:
            temp_dir = PathLib("tmp")
            temp_dir.mkdir(exist_ok=True)
            
            # Create private file with original filename
            private_file_path = temp_dir / filename
            private_file_path.write_text(file_content)
            
            # Create mock file with original filename (add _mock before extension)
            name_parts = filename.rsplit('.', 1)
            if len(name_parts) == 2:
                mock_filename_legacy = f"{name_parts[0]}_mock.{name_parts[1]}"
            else:
                mock_filename_legacy = f"{filename}_mock"
            mock_file_path = temp_dir / mock_filename_legacy
            
            # Create truncated mock content
            mock_content = file_content[:200] + "..." if len(file_content) > 200 else file_content
            mock_file_path.write_text(f"[DEMO DATA] {mock_content}")
            
            # Create the object using file paths to preserve filenames
            new_object = syobj(
                name=name,
                private_file=str(private_file_path),
                mock_file=str(mock_file_path),
                mock_read=mock_read,
                mock_write=mock_write,
                private_read=private_read,
                private_write=private_write,
                discovery_read=discovery_read,
                metadata=extended_metadata
            )
        else:
            # Create the object using content (original behavior)
            new_object = syobj(
                name=name,
                private_contents=file_content or f"Content for {name}",
                mock_contents=f"[DEMO] Mock content for {name}",
                mock_read=mock_read,
                mock_write=mock_write,
                private_read=private_read,
                private_write=private_write,
                discovery_read=discovery_read,
                metadata=extended_metadata
            )
        
        # Refresh the collection to pick up the new object from filesystem
        objects.refresh()
        
        return {
            "success": True,
            "message": "Object created successfully",
            "object": {
                "uid": str(new_object.uid),
                "name": new_object.name,
                "description": new_object.description,
                "email": user_email,
                "created_at": new_object.created_at.isoformat() if new_object.created_at else None,
                "private_url": new_object.private_url,
                "mock_url": new_object.mock_url,
                "syftobject_url": new_object.syftobject,
            },
            "timestamp": datetime.now()
        }
    
    except Exception as e:
        logger.error(f"Error creating object: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating object: {str(e)}")

@app.get("/api/objects/refresh")
async def refresh_objects() -> Dict[str, Any]:
    """Refresh the objects collection."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        objects.refresh()
        count = len(objects)
        return {
            "message": "Objects collection refreshed",
            "count": count,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Error refreshing objects: {e}")
        raise HTTPException(status_code=500, detail=f"Error refreshing objects: {str(e)}")

@app.post("/api/syftbox/reinstall")
async def reinstall_syftbox_app() -> Dict[str, Any]:
    """Reinstall syft-objects app in SyftBox by removing and re-cloning."""
    try:
        # Import the reinstall function
        from syft_objects.auto_install import reinstall_syftbox_app
        
        logger.info("Starting SyftBox app reinstallation")
        
        # Call the reinstall function
        success = reinstall_syftbox_app(silent=False)
        
        if success:
            logger.info("SyftBox app reinstallation completed successfully")
            return {
                "success": True,
                "message": "Syft-objects app reinstalled successfully",
                "timestamp": datetime.now()
            }
        else:
            logger.error("SyftBox app reinstallation failed")
            return {
                "success": False,
                "message": "Failed to reinstall syft-objects app",
                "timestamp": datetime.now()
            }
    
    except Exception as e:
        logger.error(f"Error during SyftBox app reinstallation: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error reinstalling SyftBox app: {str(e)}"
        )

@app.get("/api/objects/{object_uid}")
async def get_object_details(object_uid: str) -> Dict[str, Any]:
    """Get detailed information about a specific object."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        # Find the object by UID
        target_obj = None
        for obj in objects:
            if str(obj.uid) == object_uid:
                target_obj = obj
                break
        
        if not target_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        
        # Get file previews
        private_preview = ""
        mock_preview = ""
        
        try:
            private_path = target_obj.private_path
            if private_path:
                private_preview = target_obj._get_file_preview(private_path, max_chars=2000)
        except Exception as e:
            private_preview = f"Error reading private file: {str(e)}"
        
        try:
            mock_path = target_obj.mock_path
            if mock_path:
                mock_preview = target_obj._get_file_preview(mock_path, max_chars=2000)
        except Exception as e:
            mock_preview = f"Error reading mock file: {str(e)}"
        
        # Extract email
        email = "unknown@example.com"
        try:
            if target_obj.private_url.startswith("syft://"):
                parts = target_obj.private_url.split("/")
                if len(parts) >= 3:
                    email = parts[2]
        except:
            pass
        
        return {
            "uid": str(target_obj.uid),
            "name": target_obj.name or "Unnamed Object",
            "description": target_obj.description or "",
            "email": email,
            "private_url": target_obj.private_url,
            "mock_url": target_obj.mock_url,
            "syftobject_url": target_obj.syftobject,
            "created_at": target_obj.created_at.isoformat() if target_obj.created_at else None,
            "updated_at": target_obj.updated_at.isoformat() if target_obj.updated_at else None,
            "permissions": {
                "syftobject": target_obj.syftobject_permissions,
                "mock_read": target_obj.mock_permissions,
                "mock_write": target_obj.mock_write_permissions,
                "private_read": target_obj.private_permissions,
                "private_write": target_obj.private_write_permissions,
            },
            "metadata": target_obj.metadata,
            "file_paths": {
                "private": target_obj.private_path,
                "mock": target_obj.mock_path,
                "syftobject": target_obj.syftobject_path,
            },
            "file_previews": {
                "private": private_preview,
                "mock": mock_preview,
            },
            "file_exists": {
                "private": target_obj._check_file_exists(target_obj.private_url),
                "mock": target_obj._check_file_exists(target_obj.mock_url),
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting object details: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving object details: {str(e)}")

@app.get("/api/metadata/emails")
async def get_unique_emails() -> Dict[str, Any]:
    """Get list of unique email addresses."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        emails = objects.list_unique_emails()
        return {
            "emails": emails,
            "count": len(emails)
        }
    except Exception as e:
        logger.error(f"Error getting unique emails: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving emails: {str(e)}")

@app.get("/api/metadata/names")
async def get_unique_names() -> Dict[str, Any]:
    """Get list of unique object names."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        names = objects.list_unique_names()
        return {
            "names": names,
            "count": len(names)
        }
    except Exception as e:
        logger.error(f"Error getting unique names: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving names: {str(e)}")

@app.get("/api/file")
async def get_file_content(syft_url: str) -> PlainTextResponse:
    """Serve file content from syft:// URLs."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        # Convert syft:// URL to local file path
        if not syft_url.startswith("syft://"):
            raise HTTPException(status_code=400, detail="Invalid syft:// URL")
        
        # Find the object that has this URL
        target_obj = None
        is_private = False
        is_mock = False
        
        for obj in objects:
            if obj.private_url == syft_url:
                target_obj = obj
                is_private = True
                break
            elif obj.mock_url == syft_url:
                target_obj = obj
                is_mock = True
                break
        
        if not target_obj:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get the file path
        if is_private:
            file_path = target_obj.private_path
        elif is_mock:
            file_path = target_obj.mock_path
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Check if file exists
        if not file_path or not PathLib(file_path).exists():
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        # Read and return file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try reading as binary if UTF-8 fails
            with open(file_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='replace')
        
        return PlainTextResponse(content=content)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving file {syft_url}: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@app.put("/api/objects/{object_uid}/file/{file_type}")
async def save_file_content(
    object_uid: str,
    file_type: str,
    request: Request
) -> Dict[str, Any]:
    """Save file content for a syft object."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    if file_type not in ['private', 'mock']:
        raise HTTPException(status_code=400, detail="Invalid file type. Must be 'private' or 'mock'")
    
    try:
        # Get the file content from request body
        content = await request.body()
        content_str = content.decode('utf-8')
        
        # Find the object by UID
        target_obj = None
        for obj in objects:
            if str(obj.uid) == object_uid:
                target_obj = obj
                break
        
        if not target_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        
        # Get the raw object if this is a CleanSyftObject
        raw_obj = target_obj._obj if hasattr(target_obj, '_obj') else target_obj
        
        # Check write permissions for the file type
        try:
            from syft_objects.client import get_syftbox_client
            client = get_syftbox_client()
            user_email = client.email if client and hasattr(client, 'email') else None
            
            if not user_email:
                raise HTTPException(status_code=403, detail="User authentication required")
            
            # Check write permissions based on file type
            has_permission = False
            if file_type == 'private':
                write_perms = raw_obj.private_write_permissions if hasattr(raw_obj, 'private_write_permissions') else []
                has_permission = user_email in write_perms
            else:  # mock
                write_perms = raw_obj.mock_write_permissions if hasattr(raw_obj, 'mock_write_permissions') else []
                has_permission = user_email in write_perms
            
            if not has_permission:
                owner_email = raw_obj.get_owner_email() if hasattr(raw_obj, 'get_owner_email') else 'unknown'
                logger.warning(f"User {user_email} attempted to write {file_type} file for object {object_uid} - DENIED")
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied. You don't have write access to the {file_type} file."
                )
            
            logger.info(f"User {user_email} authorized to write {file_type} file for object {object_uid}")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error checking write permissions: {e}")
            raise HTTPException(status_code=403, detail="Permission verification failed")
        
        # Get the file path
        if file_type == 'private':
            file_path = target_obj.private_path
        else:  # mock
            file_path = target_obj.mock_path
        
        if not file_path:
            raise HTTPException(status_code=400, detail=f"No {file_type} file path found for this object")
        
        # Ensure the directory exists
        PathLib(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_str)
        
        # Refresh the objects collection to reflect any changes
        objects.refresh()
        
        return {
            "message": f"File {file_type} saved successfully",
            "object_uid": object_uid,
            "file_type": file_type,
            "file_path": str(file_path),
            "content_length": len(content_str),
            "timestamp": datetime.now()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving {file_type} file for object {object_uid}: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@app.put("/api/objects/{object_uid}/permissions")
async def update_object_permissions(
    object_uid: str,
    permissions: Dict[str, List[str]] = Body(...)
) -> Dict[str, Any]:
    """Update permissions for a syft object."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        # Find the object by UID
        target_obj = None
        for obj in objects:
            if str(obj.uid) == object_uid:
                target_obj = obj
                break
        
        if not target_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        
        # Get the raw object if this is a CleanSyftObject
        raw_obj = target_obj._obj if hasattr(target_obj, '_obj') else target_obj
        
        # Check if user has permission to update permissions (must be owner)
        try:
            from syft_objects.client import get_syftbox_client
            client = get_syftbox_client()
            user_email = client.email if client and hasattr(client, 'email') else None
            
            owner_email = raw_obj.get_owner_email() if hasattr(raw_obj, 'get_owner_email') else 'unknown'
            
            if user_email != owner_email:
                logger.warning(f"User {user_email or 'unknown'} attempted to update permissions for object {object_uid} owned by {owner_email} - DENIED")
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied. Only the owner ({owner_email}) can update permissions."
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error checking permissions: {e}")
            # If we can't verify permissions, deny by default
            raise HTTPException(status_code=403, detail="Permission verification failed")
        
        # Log the current and new permissions for debugging
        logger.info(f"Updating permissions for object {object_uid}")
        logger.info(f"Current permissions: {target_obj.__dict__}")
        logger.info(f"New permissions: {permissions}")
        
        # Update the object's permissions
        updated_fields = []
        if 'private_read' in permissions:
            target_obj.private_permissions = permissions['private_read']
            updated_fields.append('private_read')
        if 'private_write' in permissions:
            target_obj.private_write_permissions = permissions['private_write']
            updated_fields.append('private_write')
        if 'mock_read' in permissions:
            target_obj.mock_permissions = permissions['mock_read']
            updated_fields.append('mock_read')
        if 'mock_write' in permissions:
            target_obj.mock_write_permissions = permissions['mock_write']
            updated_fields.append('mock_write')
        if 'syftobject' in permissions:
            target_obj.syftobject_permissions = permissions['syftobject']
            updated_fields.append('syftobject')
        
        logger.info(f"Updated fields: {updated_fields}")
        logger.info(f"Updated object permissions: {target_obj.__dict__}")
        
        # Update the updated_at timestamp
        target_obj.updated_at = datetime.now()
        
        # Save the object to its .syftobject.yaml file
        try:
            if hasattr(target_obj, 'private') and target_obj.syftobject_path:
                target_obj.private.save(create_syftbox_permissions=True)
                logger.info(f"Object saved to {target_obj.syftobject_path} using .private.save() method")
            elif hasattr(target_obj, 'private') and hasattr(target_obj, 'syftobject'):
                # Try to derive the local path from the syft:// URL
                local_path = target_obj._get_local_file_path(target_obj.syftobject)
                if local_path:
                    target_obj.private.save(local_path, create_syftbox_permissions=True)
                    logger.info(f"Object saved to {local_path} using .private.save() method")
                else:
                    logger.warning("Could not determine local path for syftobject file")
            else:
                logger.warning("Object does not have save_yaml method or syftobject_path")
        except Exception as save_error:
            logger.error(f"Error saving object to yaml: {save_error}")
            raise HTTPException(status_code=500, detail=f"Error saving permissions: {save_error}")
        
        # Refresh the collection to reflect changes
        objects.refresh()
        logger.info("Objects collection refreshed")
        
        return {
            "message": f"Permissions updated successfully for object {object_uid}",
            "object_uid": object_uid,
            "updated_permissions": permissions,
            "timestamp": datetime.now()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating permissions for object {object_uid}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating permissions: {str(e)}")

@app.delete("/api/objects/{object_uid}")
async def delete_object(object_uid: str, user_email: str = None) -> Dict[str, Any]:
    """Delete a syft object by UID."""
    if objects is None:
        raise HTTPException(status_code=503, detail="Syft objects not available")
    
    try:
        # Find the object by UID
        target_obj = None
        for obj in objects:
            if str(obj.uid) == object_uid:
                target_obj = obj
                break
        
        if not target_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        
        # Get the raw object if this is a CleanSyftObject
        raw_obj = target_obj._obj if hasattr(target_obj, '_obj') else target_obj
        
        # Check permissions using the object's can_delete method
        if hasattr(raw_obj, 'can_delete'):
            # Get current user email if not provided
            if not user_email:
                try:
                    from syft_objects.client import get_syftbox_client
                    client = get_syftbox_client()
                    if client and hasattr(client, 'email'):
                        user_email = client.email
                except:
                    pass
            
            if not raw_obj.can_delete(user_email):
                owner_email = raw_obj.get_owner_email() if hasattr(raw_obj, 'get_owner_email') else 'unknown'
                logger.warning(f"User {user_email or 'unknown'} attempted to delete object {object_uid} owned by {owner_email} - DENIED")
                raise HTTPException(
                    status_code=403, 
                    detail=f"Permission denied. Only the owner ({owner_email}) can delete this object."
                )
            else:
                logger.info(f"User {user_email} authorized to delete object {object_uid}")
        
        # Generic deletion logic for both file and folder objects
        deleted_files = []
        
        # Check if this is a folder-type object
        is_folder = getattr(target_obj, '_is_folder', False) or getattr(target_obj, 'object_type', '') == 'folder'
        
        if is_folder:
            # For folder objects, delete the entire directory structure
            try:
                # Try to get folder path from syftobject_path first (most reliable)
                folder_path = None
                if target_obj.syftobject_path:
                    syftobject_path = PathLib(target_obj.syftobject_path)
                    if syftobject_path.exists():
                        folder_path = syftobject_path.parent
                        logger.info(f"Found folder path via syftobject_path: {folder_path}")
                
                # For syft-queue jobs, search across all status directories
                if not folder_path and hasattr(target_obj, 'metadata') and target_obj.metadata and target_obj.metadata.get('type') == 'SyftBox Job':
                    job_uid = str(target_obj.uid)
                    
                    # Common syft-queue base paths
                    potential_bases = [
                        PathLib.home() / "SyftBox" / "datasites",
                        PathLib("/tmp"),  # fallback
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
                                            logger.info(f"Found syft-queue job folder: {folder_path}")
                                            break
                                    if folder_path:
                                        break
                                if folder_path:
                                    break
                        if folder_path:
                            break
                
                # Strategy 3: Check folder paths in metadata with validation
                if not folder_path and hasattr(target_obj, 'metadata') and target_obj.metadata:
                    folder_paths = target_obj.metadata.get('_folder_paths', {})
                    if 'private' in folder_paths:
                        metadata_path = PathLib(folder_paths['private'])
                        logger.info(f"Found folder path via metadata: {metadata_path}")
                        
                        # Check if the metadata path actually exists
                        if metadata_path.exists() and metadata_path.is_dir():
                            folder_path = metadata_path
                            logger.info(f"Metadata path exists and is valid")
                        else:
                            logger.warning(f"Metadata path doesn't exist: {metadata_path}")
                            logger.info(f"Checking if job moved to different status folder...")
                            
                            # The metadata path is stale - search for the job in current location
                            job_uid = str(target_obj.uid)
                            potential_bases = [
                                PathLib.home() / "SyftBox" / "datasites",
                                PathLib("/tmp"),  # fallback
                            ]
                            
                            for base in potential_bases:
                                if base.exists():
                                    # Search for job directories with this UID across all status folders
                                    for queue_dir in base.rglob("**/syft-queues"):
                                        for status_dir in ["running", "completed", "failed", "inbox"]:  # prioritize current status
                                            for job_dir in queue_dir.rglob(f"*/jobs/{status_dir}/*{job_uid}*"):
                                                if job_dir.is_dir():
                                                    folder_path = job_dir
                                                    logger.info(f"Found job in {status_dir} folder: {folder_path}")
                                                    break
                                            if folder_path:
                                                break
                                        if folder_path:
                                            break
                                if folder_path:
                                    break
                
                # Fallback to private_path if it's a directory
                if not folder_path and target_obj.private_path:
                    private_path = PathLib(target_obj.private_path)
                    if private_path.exists() and private_path.is_dir():
                        folder_path = private_path
                        logger.info(f"Found folder path via private_path: {folder_path}")
                
                if folder_path and folder_path.exists() and folder_path.is_dir():
                    import shutil
                    shutil.rmtree(str(folder_path))
                    deleted_files.append("folder_directory")
                    logger.info(f"Deleted folder directory: {folder_path}")
                else:
                    # If we can't find the folder path, fall back to individual file deletion
                    logger.warning(f"Could not determine folder path for {object_uid}, falling back to individual file deletion")
                    logger.warning(f"   private_path: {target_obj.private_path}")
                    logger.warning(f"   syftobject_path: {target_obj.syftobject_path}")
                    logger.warning(f"   metadata: {getattr(target_obj, 'metadata', {})}")
                    if folder_path:
                        logger.warning(f"   folder_path found but invalid: {folder_path}")
                        logger.warning(f"   exists: {folder_path.exists()}")
                        logger.warning(f"   is_dir: {folder_path.is_dir() if folder_path.exists() else 'N/A'}")
                    is_folder = False
            except Exception as e:
                logger.warning(f"Failed to delete folder directory: {e}")
                # Fall back to individual file deletion
                is_folder = False
        
        # Delete individual files (for non-folder objects or fallback)
        if not is_folder:
            # Delete private file if it exists
            if target_obj.private_path and PathLib(target_obj.private_path).exists():
                try:
                    private_path = PathLib(target_obj.private_path)
                    if private_path.is_file():
                        private_path.unlink()
                        deleted_files.append("private")
                    elif private_path.is_dir():
                        import shutil
                        shutil.rmtree(str(private_path))
                        deleted_files.append("private_directory")
                except Exception as e:
                    logger.warning(f"Failed to delete private file/directory: {e}")
            
            # Delete mock file if it exists
            if target_obj.mock_path and PathLib(target_obj.mock_path).exists():
                try:
                    mock_path = PathLib(target_obj.mock_path)
                    if mock_path.is_file():
                        mock_path.unlink()
                        deleted_files.append("mock")
                    elif mock_path.is_dir():
                        import shutil
                        shutil.rmtree(str(mock_path))
                        deleted_files.append("mock_directory")
                except Exception as e:
                    logger.warning(f"Failed to delete mock file/directory: {e}")
            
            # Delete syftobject file if it exists
            if target_obj.syftobject_path and PathLib(target_obj.syftobject_path).exists():
                try:
                    PathLib(target_obj.syftobject_path).unlink()
                    deleted_files.append("syftobject")
                except Exception as e:
                    logger.warning(f"Failed to delete syftobject file: {e}")
        
        # Refresh the objects collection to reflect the deletion
        objects.refresh()
        
        object_type = "folder" if is_folder else "file"
        return {
            "message": f"Syft object {object_uid} deleted successfully",
            "deleted_files": deleted_files,
            "object_type": object_type,
            "timestamp": datetime.now()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting object {object_uid}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting object: {str(e)}")

# Filesystem Editor endpoints
filesystem_manager = FileSystemManager()

@app.get("/editor", response_class=HTMLResponse)
async def editor_page(path: Optional[str] = Query(None)):
    """Serve the filesystem editor HTML page."""
    initial_path = path if path else str(PathLib.home())
    return HTMLResponse(content=generate_editor_html(initial_path))

@app.get("/api/filesystem/list")
async def list_directory(
    path: str = Query(...),
    user_email: str = Query(None)
):
    """List directory contents with permission checks."""
    if not user_email:
        raise HTTPException(status_code=400, detail="user_email is required")
    return filesystem_manager.list_directory(path, user_email)

@app.get("/api/filesystem/read")
async def read_file(
    path: str = Query(...),
    user_email: str = Query(None)
):
    """Read file contents with permission checks."""
    if not user_email:
        raise HTTPException(status_code=400, detail="user_email is required")
    content = filesystem_manager.read_file(path, user_email)
    return {"content": content}

@app.post("/api/filesystem/write")
async def write_file(
    path: str = Body(...),
    content: str = Body(...),
    user_email: str = Body(None)
):
    """Write file contents with permission checks."""
    if not user_email:
        raise HTTPException(status_code=400, detail="user_email is required")
    filesystem_manager.write_file(path, content, user_email)
    return {"message": "File saved successfully"}

@app.post("/api/filesystem/create-directory")
async def create_directory(path: str = Body(...)):
    """Create a new directory."""
    return filesystem_manager.create_directory(path)

@app.delete("/api/filesystem/delete")
async def delete_item(
    path: str = Query(...),
    user_email: str = Query(None)
):
    """Delete file with permission checks."""
    if not user_email:
        raise HTTPException(status_code=400, detail="user_email is required")
    filesystem_manager.delete_file(path, user_email)
    return {"message": "File deleted successfully"}

# Widget endpoints to match original server exactly
@app.get("/widget")
async def widget_redirect():
    """Redirect /widget to /widget/ to match original server behavior."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/widget/", status_code=307)

@app.get("/widget/")
async def widget_page():
    """Serve the Next.js widget page."""
    widget_file = PathLib(__file__).parent.parent / "frontend" / "widget" / "index.html"
    if widget_file.exists():
        return FileResponse(widget_file, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Widget page not found")

# Serve the main page explicitly to match original server
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main Next.js page."""
    main_file = PathLib(__file__).parent.parent / "frontend" / "index.html"
    if main_file.exists():
        return FileResponse(main_file, media_type="text/html")
    else:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head><title>Syft Objects UI</title></head>
        <body>
            <h1>Syft Objects UI</h1>
            <p>Frontend not built yet. Please run the build process.</p>
            <p>API available at <a href="/docs">/docs</a></p>
        </body>
        </html>
        """)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SYFTBOX_ASSIGNED_PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port) 