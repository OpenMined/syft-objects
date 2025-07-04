# syft-objects factory - Factory functions for creating SyftObjects

import os
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List
from uuid import uuid4

from .models import SyftObject, utcnow
from .client import get_syftbox_client
from .file_ops import (
    move_file_to_syftbox_location, 
    copy_file_to_syftbox_location,
    generate_syftbox_urls,
    generate_syftobject_url
)


def detect_user_email():
    """Auto-detect the user's email from various sources"""
    email = None
    
    # Try multiple ways to detect logged-in email
    email = os.getenv("SYFTBOX_EMAIL")
    if not email:
        syftbox_client = get_syftbox_client()
        if syftbox_client:
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
    
    return email


def syobj(
    name: Optional[str] = None,
    *,  # Force keyword-only arguments after this
    mock_contents: Optional[str] = None,
    private_contents: Optional[str] = None,
    mock_file: Optional[str] = None,
    private_file: Optional[str] = None,
    discovery_read: Optional[List[str]] = None,
    mock_read: Optional[List[str]] = None,
    mock_write: Optional[List[str]] = None,
    private_read: Optional[List[str]] = None,
    private_write: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    reference_only: Optional[bool] = None
) -> SyftObject:
    """
    🔐 **Share files with explicit mock vs private control** 
    
    Create SyftObjects with fine-grained permission control.
    
    Args:
        reference_only: If True, files are referenced in place without copying to SyftBox.
                       If None, uses metadata.get("reference_only", False).
                       When True, overrides move_files_to_syftbox to False.
    """
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
    use_relative_paths = metadata.get("use_relative_paths", False)
    base_path = metadata.get("base_path", None)
    
    # Handle reference_only flag - can be passed as parameter or in metadata
    if reference_only is None:
        reference_only = metadata.get("reference_only", False)
    
    # If reference_only is True, override move_files_to_syftbox to False
    if reference_only:
        move_files_to_syftbox = False
    
    # Create clean metadata dict for the SyftObject (exclude system settings)
    system_keys = {"description", "save_to", "email", "create_syftbox_permissions", "auto_save", "move_files_to_syftbox", "use_relative_paths", "base_path", "reference_only"}
    clean_metadata = {k: v for k, v in metadata.items() if k not in system_keys}
    
    # === CREATE TEMP DIRECTORY ===
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    # === SYFTBOX CLIENT SETUP ===
    syftbox_client = get_syftbox_client()
    
    # === EMAIL AUTO-DETECTION ===
    if email is None:
        email = detect_user_email()
    
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
    
    # === GENERATE UID FOR UNIQUE FILENAMES ===
    uid = uuid4()
    uid_short = str(uid)[:8]  # Use first 8 characters for readability
    
    # === DETERMINE BASE FILENAME WITH UID ===
    base_filename = f"{name.lower().replace(' ', '_')}_{uid_short}.txt"
    
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
        # Auto-generate mock with matching extension to private file
        if private_file:
            # Match the extension of the private file
            private_ext = Path(private_source_path).suffix
            mock_filename = f"{Path(private_source_path).stem}_mock{private_ext}"
        else:
            # Use default extension
            mock_filename = f"{Path(base_filename).stem}_mock{Path(base_filename).suffix}"
        
        mock_file_path = tmp_dir / mock_filename
        
        if private_contents:
            # Create mock from private content (truncated)
            mock_content = private_contents[:50] + "..." if len(private_contents) > 50 else private_contents
            mock_file_path.write_text(f"[MOCK DATA] {mock_content}")
        else:
            # Generic mock
            mock_file_path.write_text(f"[MOCK DATA] Demo version of {name}")
        
        created_files.append(mock_file_path)
        mock_source_path = mock_file_path
    
    # === PERMISSION HANDLING ===
    final_discovery_read = discovery_read or ["public"]
    final_mock_read = mock_read or ["public"]
    final_mock_write = mock_write or []
    final_private_read = private_read or [email]
    final_private_write = private_write or [email]
    
    # === GENERATE SYFT:// URLS OR USE REFERENCE PATHS ===
    mock_is_public = any(x in ("public", "*") for x in final_mock_read)
    
    # Convert base_path to Path if provided
    base_path_obj = Path(base_path) if base_path else None
    
    if reference_only:
        # Reference-only mode: use original file paths without moving to SyftBox
        final_private_path = str(private_source_path.absolute())
        final_mock_path = str(mock_source_path.absolute())
        private_relative = None
        mock_relative = None
        
        # For reference-only mode, save syftobject in current directory or specified save_to location
        if save_to:
            final_syftobject_path = str(Path(save_to).absolute())
        else:
            syftobj_filename = f"{name.lower().replace(' ', '_').replace('-', '_')}_{uid_short}.syftobject.yaml"
            final_syftobject_path = str(Path.cwd().absolute() / syftobj_filename)
        syftobject_relative = None
    else:
        # Normal mode: generate SyftBox URLs with optional relative paths
        final_private_path, final_mock_path, private_relative, mock_relative = generate_syftbox_urls(
            email, private_filename, syftbox_client, mock_is_public=mock_is_public,
            use_relative_paths=use_relative_paths, base_path=base_path_obj
        )
        
        # Generate syftobject URL
        syftobj_filename = f"{name.lower().replace(' ', '_').replace('-', '_')}_{uid_short}.syftobject.yaml"
        final_syftobject_path, syftobject_relative = generate_syftobject_url(
            email, syftobj_filename, syftbox_client, 
            use_relative_paths=use_relative_paths, base_path=base_path_obj
        )
    
    # === MOVE FILES TO SYFTBOX LOCATIONS ===
    if move_files_to_syftbox and syftbox_client:
        # Handle private file
        if private_file and private_source_path != Path(private_file):
            if move_file_to_syftbox_location(private_source_path, final_private_path, syftbox_client):
                files_moved_to_syftbox.append(f"{private_source_path} → {final_private_path}")
        elif private_file:
            if copy_file_to_syftbox_location(private_source_path, final_private_path, syftbox_client):
                files_moved_to_syftbox.append(f"{private_source_path} → {final_private_path}")
        else:
            if move_file_to_syftbox_location(private_source_path, final_private_path, syftbox_client):
                files_moved_to_syftbox.append(f"{private_source_path} → {final_private_path}")
        
        # Handle mock file
        if mock_file and mock_source_path != Path(mock_file):
            if move_file_to_syftbox_location(mock_source_path, final_mock_path, syftbox_client):
                files_moved_to_syftbox.append(f"{mock_source_path} → {final_mock_path}")
        elif mock_file:
            if copy_file_to_syftbox_location(mock_source_path, final_mock_path, syftbox_client):
                files_moved_to_syftbox.append(f"{mock_source_path} → {final_mock_path}")
        else:
            if move_file_to_syftbox_location(mock_source_path, final_mock_path, syftbox_client):
                files_moved_to_syftbox.append(f"{mock_source_path} → {final_mock_path}")
    
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
        uid=uid,
        private_url=final_private_path,
        mock_url=final_mock_path,
        syftobject=final_syftobject_path,
        name=name,
        description=description,
        updated_at=utcnow(),
        metadata=clean_metadata,
        syftobject_permissions=final_discovery_read,
        mock_permissions=final_mock_read,
        mock_write_permissions=final_mock_write,
        private_permissions=final_private_read,
        private_write_permissions=final_private_write,
        # Add relative path support
        base_path=base_path,
        private_url_relative=private_relative,
        mock_url_relative=mock_relative,
        syftobject_relative=syftobject_relative
    )
    
    # === TRACK FILE OPERATIONS ===
    file_operations = {
        "files_moved_to_syftbox": files_moved_to_syftbox,
        "created_files": [str(f) for f in created_files],
        "syftbox_available": bool(syftbox_client),
        "syftobject_yaml_path": None  # Will be set during save
    }
    clean_metadata["_file_operations"] = file_operations
    
    # === AUTO-SAVE ===
    if auto_save:
        # Determine save location
        if save_to:
            save_path = save_to
        else:
            safe_name = name.lower().replace(" ", "_").replace("-", "_")
            save_path = tmp_dir / f"{safe_name}_{uid_short}.syftobject.yaml"
        
        # Save the syftobject.yaml file
        syft_obj.save_yaml(save_path, create_syftbox_permissions=False, use_relative_paths=use_relative_paths)
        
        # Move .syftobject.yaml file to SyftBox location if available
        final_syftobj_path = save_path
        if move_files_to_syftbox and syftbox_client and not str(save_path).startswith("syft://"):
            syftobj_filename = Path(save_path).name
            syftobj_url = f"syft://{email}/public/objects/{syftobj_filename}"
            
            if move_file_to_syftbox_location(Path(save_path), syftobj_url, syftbox_client):
                files_moved_to_syftbox.append(f"{save_path} → {syftobj_url}")
                
                # Update the final path to the SyftBox location
                from .client import SyftBoxURL, SYFTBOX_AVAILABLE
                if SYFTBOX_AVAILABLE:
                    try:
                        syft_url_obj = SyftBoxURL(syftobj_url)
                        final_syftobj_path = syft_url_obj.to_local_path(datasites_path=syftbox_client.datasites)
                    except:
                        pass
        
        # Track the final syftobject.yaml file path
        clean_metadata["_file_operations"]["syftobject_yaml_path"] = str(final_syftobj_path)
        
        # Update the syft object's metadata
        syft_obj.metadata.update(clean_metadata)
        
        # Create SyftBox permission files in the final location
        if create_syftbox_permissions:
            syft_obj._create_syftbox_permissions(Path(final_syftobj_path))
    
    return syft_obj 