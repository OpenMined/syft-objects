# syft-objects client - SyftBox client utilities and connection management

from typing import Optional
from pathlib import Path
import os


# Global variables for client state
SYFTBOX_AVAILABLE = False
SyftBoxClient = None
SyftBoxURL = None


def _initialize_syftbox():
    """Initialize SyftBox client classes if available"""
    global SYFTBOX_AVAILABLE, SyftBoxClient, SyftBoxURL
    
    try:
        from syft_core import Client as _SyftBoxClient
        from syft_core.url import SyftBoxURL as _SyftBoxURL
        SyftBoxClient = _SyftBoxClient
        SyftBoxURL = _SyftBoxURL
        SYFTBOX_AVAILABLE = True
    except ImportError:
        SyftBoxClient = None
        SyftBoxURL = None
        SYFTBOX_AVAILABLE = False


def get_syftbox_client():
    """Get SyftBox client if available, otherwise return None"""
    if not SYFTBOX_AVAILABLE:
        return None
    try:
        return SyftBoxClient.load()
    except Exception:
        return None


def extract_local_path_from_syft_url(syft_url: str):
    """Extract local path from a syft:// URL if it points to a local SyftBox path"""
    if not SYFTBOX_AVAILABLE:
        return None
    
    try:
        client = SyftBoxClient.load()
        syft_url_obj = SyftBoxURL(syft_url)
        return syft_url_obj.to_local_path(datasites_path=client.datasites)
    except Exception:
        return None


def check_syftbox_status():
    """Check SyftBox status and print diagnostic information"""
    try:
        if not SYFTBOX_AVAILABLE:
            print("❌ SyftBox not available - install syft-core for full functionality")
            return

        syftbox_client = get_syftbox_client()
        if not syftbox_client:
            print("❌ SyftBox client not available - make sure you're logged in")
            return

        # Check 1: Verify SyftBox filesystem is accessible
        try:
            datasites = list(map(lambda x: x.name, syftbox_client.datasites.iterdir()))
            print(f"✅ SyftBox filesystem accessible — logged in as: {syftbox_client.email}")
        except Exception as e:
            print(f"❌ SyftBox filesystem not accessible: {e}")
            print("    Make sure SyftBox is properly installed")

        # Check 2: Verify SyftBox app is running
        try:
            import requests
            response = requests.get(str(syftbox_client.config.client_url), timeout=2)
            if response.status_code == 200 and "go1." in response.text:
                print(f"✅ SyftBox app running at {syftbox_client.config.client_url}")
        except Exception:
            print(f"❌ SyftBox app not running at {syftbox_client.config.client_url}")

    except Exception as e:
        print(f"⚠️  Could not find SyftBox client: {e}")
        print("    Make sure SyftBox is installed and you're logged in")


def get_syft_objects_port():
    """Get the port where syft-objects server is running"""
    # Look for the port in the static config file
    config_file = Path.home() / ".syftbox" / "syft_objects.config"
    
    try:
        if config_file.exists():
            port = config_file.read_text().strip()
            if port.isdigit():
                return int(port)
    except Exception:
        pass
    
    # Default fallback port
    return 8003


def get_syft_objects_url(endpoint=""):
    """Get the full URL for syft-objects server endpoints"""
    port = get_syft_objects_port()
    base_url = f"http://localhost:{port}"
    if endpoint:
        return f"{base_url}/{endpoint.lstrip('/')}"
    return base_url


# Initialize SyftBox on module import
_initialize_syftbox() 