# syft-objects file_ops - File operations and URL generation utilities

import shutil
from pathlib import Path
from typing import Optional, Tuple

from .client import get_syftbox_client, SyftBoxClient, SyftBoxURL, SYFTBOX_AVAILABLE


def move_file_to_syftbox_location(local_file: Path, syft_url: str, syftbox_client: Optional[SyftBoxClient] = None) -> bool:
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


def copy_file_to_syftbox_location(local_file: Path, syft_url: str, syftbox_client: Optional[SyftBoxClient] = None) -> bool:
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


def generate_syftbox_urls(email: str, filename: str, syftbox_client: Optional[SyftBoxClient] = None, 
                         mock_is_public: bool = True, use_relative_paths: bool = False, 
                         base_path: Optional[Path] = None) -> Tuple[str, str, Optional[str], Optional[str]]:
    """Generate proper syft:// URLs for private and mock files
    
    Args:
        email: User's email address
        filename: Name of the file
        syftbox_client: Optional SyftBox client
        mock_is_public: Whether mock file should be in public directory
        use_relative_paths: Whether to generate relative paths
        base_path: Base path for relative URLs (defaults to current directory)
    
    Returns:
        Tuple of (private_url, mock_url, private_relative, mock_relative)
    """
    private_relative = None
    mock_relative = None
    
    if syftbox_client:
        # Generate URLs that point to actual SyftBox structure
        private_url = f"syft://{email}/private/objects/{filename}"
        # Mock file location depends on permissions
        if mock_is_public:
            mock_url = f"syft://{email}/public/objects/{filename}"
        else:
            mock_url = f"syft://{email}/private/objects/{filename}"
    else:
        # Fallback to generic URLs
        private_url = f"syft://{email}/SyftBox/datasites/{email}/private/objects/{filename}"
        if mock_is_public:
            mock_url = f"syft://{email}/SyftBox/datasites/{email}/public/objects/{filename}"
        else:
            mock_url = f"syft://{email}/SyftBox/datasites/{email}/private/objects/{filename}"
    
    # Generate relative paths if requested
    if use_relative_paths:
        if not base_path:
            base_path = Path.cwd()
        
        # For relative paths, we use a simple structure
        private_relative = f"private/{filename}"
        if mock_is_public:
            mock_relative = f"public/{filename}"
        else:
            mock_relative = f"private/{filename}_mock"
    
    return private_url, mock_url, private_relative, mock_relative


def generate_syftobject_url(email: str, filename: str, syftbox_client: Optional[SyftBoxClient] = None,
                           use_relative_paths: bool = False, base_path: Optional[Path] = None) -> Tuple[str, Optional[str]]:
    """Generate proper syft:// URL for syftobject.yaml file
    
    Args:
        email: User's email address
        filename: Name of the .syftobject.yaml file
        syftbox_client: Optional SyftBox client
        use_relative_paths: Whether to generate relative path
        base_path: Base path for relative URL (defaults to current directory)
    
    Returns:
        Tuple of (syftobject_url, syftobject_relative)
    """
    syftobject_relative = None
    
    if syftbox_client:
        # Generate URL that points to actual SyftBox structure
        syftobject_url = f"syft://{email}/public/objects/{filename}"
    else:
        # Fallback to generic URL
        syftobject_url = f"syft://{email}/SyftBox/datasites/{email}/public/objects/{filename}"
    
    # Generate relative path if requested
    if use_relative_paths:
        syftobject_relative = f"metadata/{filename}"
    
    return syftobject_url, syftobject_relative 