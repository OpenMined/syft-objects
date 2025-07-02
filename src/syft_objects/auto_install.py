"""Auto-installation utilities for SyftBox integration."""

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    requests = None


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


def wait_for_syft_objects_server(timeout_minutes: int = 5) -> bool:
    """Wait for syft-objects server to be available.
    
    Repeatedly checks the port config file and tries to connect to the server.
    
    Args:
        timeout_minutes: Maximum time to wait in minutes
        
    Returns:
        True if server becomes available, False if timeout
    """
    if not requests:
        print("❌ Cannot check server availability - requests library not available")
        return False
        
    timeout_seconds = timeout_minutes * 60
    start_time = time.time()
    last_port = None
    
    print("⏳ Waiting for syft-objects server to start... (this might take a minute and only happens the first time)")
    
    while time.time() - start_time < timeout_seconds:
        try:
            # Read port from config file
            config_file = Path.home() / ".syftbox" / "syft_objects.config"
            
            if config_file.exists():
                port_str = config_file.read_text().strip()
                if port_str.isdigit():
                    port = int(port_str)
                    
                    # Only log port changes to avoid spam
                    if port != last_port:
                        print(f"🔍 Found port {port} in config...")
                        last_port = port
                    
                    # Try to connect to the server health endpoint (fast check)
                    try:
                        response = requests.get(f"http://localhost:{port}/health", timeout=1)
                        if response.status_code == 200:
                            print(f"✅ Syft-objects server is now available at http://localhost:{port}")
                            return True
                    except requests.exceptions.RequestException:
                        # Server not ready yet, continue waiting
                        pass
            
            # Wait a bit before checking again
            time.sleep(0.1)
            
        except Exception as e:
            print(f"⚠️  Error while waiting for server: {e}")
            time.sleep(1)
    
    print(f"⏰ Timeout after {timeout_minutes} minutes waiting for syft-objects server")
    return False




def is_syftbox_running() -> bool:
    """Check if SyftBox daemon/app is running.
    
    Returns:
        True if SyftBox is running and accessible
    """
    try:
        # Import here to avoid circular imports
        from .client import get_syftbox_client
        
        syftbox_client = get_syftbox_client()
        if not syftbox_client:
            return False
        
        # Check if SyftBox app is running by trying to access it
        try:
            response = requests.get(str(syftbox_client.config.client_url), timeout=2)
            return response.status_code == 200 and "go1." in response.text
        except Exception:
            return False
            
    except Exception:
        return False


def ensure_syftbox_app_installed() -> bool:
    """Ensure syft-objects app is installed in SyftBox and server is available.
    
    Requires SyftBox to be running before proceeding.
    Checks if the app exists, and if not, attempts to clone it.
    Then waits for the server to be available.
    This function is designed to be called during package import.
    
    Returns:
        True if app is available and server is running
    """
    # Check if SyftBox exists
    apps_path = get_syftbox_apps_path()
    if not apps_path:
        # SyftBox not found - this is normal for users not using SyftBox
        return False
    
    # Require SyftBox to be running
    if not is_syftbox_running():
        print("❌ SyftBox is not running. Please start SyftBox before using syft-objects.")
        print("    Make sure SyftBox is installed and running, then try again.")
        return False
    
    app_installed = is_syftbox_app_installed()
    app_path = apps_path / "syft-objects"
    
    # If app is not installed, clone it
    if not app_installed:
        print("SyftBox detected but syft-objects app not found. Attempting auto-installation...")
        if not clone_syftbox_app():
            return False
        
        # Wait for server to be available
        return wait_for_syft_objects_server()
    
    else:
        # App is installed, check if server is already running
        try:
            config_file = Path.home() / ".syftbox" / "syft_objects.config"
            if config_file.exists():
                port_str = config_file.read_text().strip()
                if port_str.isdigit() and requests:
                    port = int(port_str)
                    try:
                        response = requests.get(f"http://localhost:{port}/health", timeout=1)
                        if response.status_code == 200:
                            # Server is already running
                            return True
                    except requests.exceptions.RequestException:
                        pass
        except Exception:
            pass
        
        # Wait for server to be available
        return wait_for_syft_objects_server()
    
    return True


if __name__ == "__main__":
    # Allow running this module directly for testing
    if ensure_syftbox_app_installed():
        print("syft-objects app is available in SyftBox")
    else:
        print("syft-objects app is not available") 