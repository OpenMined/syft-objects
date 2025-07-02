"""
FastAPI backend for syft-objects with SyftBox integration
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path as PathLib

from fastapi import FastAPI, Depends, HTTPException, Body, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from loguru import logger

try:
    from syft_objects import objects, ObjectsCollection
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
    title="Syft Objects API",
    description="Manage and view syft objects from the distributed file system",
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


@app.get("/api/objects")
async def get_objects(
    search: Optional[str] = None,
    email_filter: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """Get syft objects with optional filtering and pagination."""
    if not objects:
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
        
        # Convert to list for pagination
        all_objects = collection.to_list()
        total_count = len(all_objects)
        
        # Apply pagination
        start_idx = offset
        end_idx = start_idx + limit if limit else len(all_objects)
        paginated_objects = all_objects[start_idx:end_idx]
        
        # Convert objects to dict format
        objects_data = []
        for i, obj in enumerate(paginated_objects, start=offset):
            # Extract email from private URL
            email = "unknown@example.com"
            try:
                if obj.private.startswith("syft://"):
                    parts = obj.private.split("/")
                    if len(parts) >= 3:
                        email = parts[2]
            except:
                pass
            
            obj_data = {
                "index": i,
                "uid": str(obj.uid),
                "name": obj.name or "Unnamed Object",
                "description": obj.description or "",
                "email": email,
                "private_url": obj.private,
                "mock_url": obj.mock,
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
                    "private": obj._check_file_exists(obj.private),
                    "mock": obj._check_file_exists(obj.mock),
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


@app.get("/api/objects/{object_uid}")
async def get_object_details(object_uid: str) -> Dict[str, Any]:
    """Get detailed information about a specific object."""
    if not objects:
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
            if target_obj.private.startswith("syft://"):
                parts = target_obj.private.split("/")
                if len(parts) >= 3:
                    email = parts[2]
        except:
            pass
        
        return {
            "uid": str(target_obj.uid),
            "name": target_obj.name or "Unnamed Object",
            "description": target_obj.description or "",
            "email": email,
            "private_url": target_obj.private,
            "mock_url": target_obj.mock,
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
                "private": target_obj._check_file_exists(target_obj.private),
                "mock": target_obj._check_file_exists(target_obj.mock),
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting object details: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving object details: {str(e)}")


@app.get("/api/objects/refresh")
async def refresh_objects() -> Dict[str, Any]:
    """Refresh the objects collection."""
    if not objects:
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


@app.get("/api/metadata/emails")
async def get_unique_emails() -> Dict[str, Any]:
    """Get list of unique email addresses."""
    if not objects:
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
    if not objects:
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


# Serve the frontend static files
try:
    frontend_build_path = PathLib(__file__).parent.parent / "frontend" / "out"
    if frontend_build_path.exists():
        app.mount("/", StaticFiles(directory=str(frontend_build_path), html=True), name="static")
    else:
        @app.get("/", response_class=HTMLResponse)
        async def root():
            """Serve the frontend application fallback."""
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Syft Objects UI</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <div id="root">
                    <h1>🔐 Syft Objects UI</h1>
                    <p>Loading frontend...</p>
                    <p>Frontend not built yet. Run the build process first.</p>
                    <p>The API is available at <a href="/docs">/docs</a></p>
                </div>
            </body>
            </html>
            """)
except Exception as e:
    logger.warning(f"Could not setup static file serving: {e}")
    
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the frontend application fallback."""
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Syft Objects UI</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <div id="root">
                <h1>🔐 Syft Objects UI</h1>
                <p>Loading frontend...</p>
                <p>Frontend static serving error. The API is available at <a href="/docs">/docs</a></p>
            </div>
        </body>
        </html>
        """)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SYFTBOX_ASSIGNED_PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port) 