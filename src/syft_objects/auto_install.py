"""Auto-installation utilities for SyftBox integration."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def get_syftbox_apps_path() -> Optional[Path]:
    """Get the SyftBox apps directory path.
    
    Returns:
        Path to SyftBox/apps directory or None if SyftBox not found
    """
    home = Path.home()
    syftbox_path = home / "SyftBox"
    
    if not syftbox_path.exists():
        return None
        
    apps_path = syftbox_path / "apps"
    return apps_path


def is_syftbox_app_installed() -> bool:
    """Check if syft-objects app is installed in SyftBox.
    
    Returns:
        True if syft-objects app directory exists in SyftBox/apps
    """
    apps_path = get_syftbox_apps_path()
    if not apps_path:
        return False
        
    syft_objects_app_path = apps_path / "syft-objects"
    return syft_objects_app_path.exists() and syft_objects_app_path.is_dir()


def clone_syftbox_app() -> bool:
    """Clone the syft-objects repository into SyftBox/apps.
    
    Returns:
        True if successful, False otherwise
    """
    apps_path = get_syftbox_apps_path()
    if not apps_path:
        print("Warning: SyftBox directory not found. Cannot auto-install syft-objects app.", file=sys.stderr)
        return False
    
    # Ensure apps directory exists
    apps_path.mkdir(parents=True, exist_ok=True)
    
    # Repository URL
    repo_url = "https://github.com/OpenMined/syft-objects.git"
    target_path = apps_path / "syft-objects"
    
    try:
        # Check if git is available
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        
        print(f"Installing syft-objects app to SyftBox...")
        print(f"Cloning {repo_url} to {target_path}")
        
        # Clone the repository
        result = subprocess.run(
            ["git", "clone", repo_url, str(target_path)],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        if result.returncode == 0:
            print(f"✅ Successfully installed syft-objects app to {target_path}")
            return True
        else:
            print(f"❌ Failed to clone repository:", file=sys.stderr)
            print(f"Git error: {result.stderr}", file=sys.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Git clone timed out after 60 seconds", file=sys.stderr)
        return False
    except subprocess.CalledProcessError:
        print("❌ Git is not available. Cannot auto-install syft-objects app.", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("❌ Git is not installed. Cannot auto-install syft-objects app.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error during installation: {e}", file=sys.stderr)
        return False


def ensure_syftbox_app_installed() -> bool:
    """Ensure syft-objects app is installed in SyftBox.
    
    Checks if the app exists, and if not, attempts to clone it.
    This function is designed to be called during package import.
    
    Returns:
        True if app is available (was already installed or successfully installed)
    """
    # Quick check - if already installed, return immediately
    if is_syftbox_app_installed():
        return True
    
    # Only attempt installation if SyftBox exists
    apps_path = get_syftbox_apps_path()
    if not apps_path:
        # SyftBox not found - this is normal for users not using SyftBox
        return False
    
    # SyftBox exists but app is missing - attempt to install
    print("SyftBox detected but syft-objects app not found. Attempting auto-installation...")
    return clone_syftbox_app()


if __name__ == "__main__":
    # Allow running this module directly for testing
    if ensure_syftbox_app_installed():
        print("syft-objects app is available in SyftBox")
    else:
        print("syft-objects app is not available") 