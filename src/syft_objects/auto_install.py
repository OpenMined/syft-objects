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
        return False
        
    timeout_seconds = timeout_minutes * 60
    start_time = time.time()
    waiting_message_shown = False
    
    while time.time() - start_time < timeout_seconds:
        try:
            # Read port from config file
            config_file = Path.home() / ".syftbox" / "syft_objects.config"
            
            if config_file.exists():
                port_str = config_file.read_text().strip()
                if port_str.isdigit():
                    port = int(port_str)
                    
                    # Try to connect to the server health endpoint (fast check)
                    try:
                        response = requests.get(f"http://localhost:{port}/health", timeout=1)
                        if response.status_code == 200:
                            # Only show success message if we had to wait
                            if waiting_message_shown:
                                print(f"✅ Server ready at localhost:{port}")
                            return True
                    except requests.exceptions.RequestException:
                        # Server not ready yet - show waiting message only after first failure
                        if not waiting_message_shown:
                            print("⏳ Starting server...")
                            waiting_message_shown = True
            
            # Wait a bit before checking again
            time.sleep(0.2)
            
        except Exception:
            time.sleep(1)
    
    if waiting_message_shown:
        print(f"⏰ Server startup timeout after {timeout_minutes} minutes")
    return False


def start_syftbox_app(app_path: Path) -> bool:
    """Start the syft-objects app in SyftBox.
    
    Args:
        app_path: Path to the syft-objects app directory
        
    Returns:
        True if app started successfully
    """
    run_script = app_path / "run.sh"
    if not run_script.exists():
        print(f"❌ run.sh not found in {app_path}")
        return False
    
    try:
        print("🚀 Starting syft-objects server...")
        # Start the server in the background
        subprocess.Popen(
            ["bash", str(run_script)],
            cwd=str(app_path),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception as e:
        print(f"❌ Failed to start syft-objects app: {e}")
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


def ensure_syftbox_app_installed(silent=True) -> bool:
    """Ensure syft-objects app is installed in SyftBox (but don't auto-start server).
    
    This function only ensures the app is INSTALLED, not running.
    The server should be started manually by running './run.sh' to avoid recursive loops.
    This prevents the import->start server->import->start server cycle.
    
    Args:
        silent: If True, only print messages for installation actions
        
    Returns:
        True if app is installed and available
    """
    # Check if SyftBox exists
    apps_path = get_syftbox_apps_path()
    if not apps_path:
        # SyftBox not found - this is normal for users not using SyftBox
        return False
    
    # Require SyftBox to be running
    if not is_syftbox_running():
        if not silent:
            print("❌ SyftBox is not running. Please start SyftBox before using syft-objects.")
            print("    Make sure SyftBox is installed and running, then try again.")
        return False
    
    app_installed = is_syftbox_app_installed()
    
    # If app is not installed, clone it (but don't start it)
    if not app_installed:
        if not silent:
            print("SyftBox detected but syft-objects app not found. Attempting auto-installation...")
        if not clone_syftbox_app():
            return False
        
        if not silent:
            print("✅ Syft-objects app installed successfully")
            print("📝 To start the server, run './run.sh' from the app directory")
        return True
    
    else:
        # App is already installed - that's all we need for import
        return True


if __name__ == "__main__":
    # Allow running this module directly for testing
    if ensure_syftbox_app_installed():
        print("syft-objects app is available in SyftBox")
    else:
        print("syft-objects app is not available") 