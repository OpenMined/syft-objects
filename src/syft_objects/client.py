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
    """Check SyftBox status and store information for startup banner"""
    global _syftbox_status
    _syftbox_status = {
        'available': False,
        'client_connected': False,
        'app_running': False,
        'user_email': None,
        'client_url': None,
        'error': None
    }
    
    try:
        if not SYFTBOX_AVAILABLE:
            _syftbox_status['error'] = "SyftBox not available - install syft-core for full functionality"
            return

        syftbox_client = get_syftbox_client()
        if not syftbox_client:
            _syftbox_status['error'] = "SyftBox client not available - make sure you're logged in"
            return

        _syftbox_status['available'] = True

        # Check 1: Verify SyftBox filesystem is accessible
        try:
            datasites = list(map(lambda x: x.name, syftbox_client.datasites.iterdir()))
            _syftbox_status['client_connected'] = True
            _syftbox_status['user_email'] = syftbox_client.email
        except Exception as e:
            _syftbox_status['error'] = f"SyftBox filesystem not accessible: {e}"
            return

        # Check 2: Verify SyftBox app is running
        try:
            import requests
            response = requests.get(str(syftbox_client.config.client_url), timeout=2)
            if response.status_code == 200 and "go1." in response.text:
                _syftbox_status['app_running'] = True
                _syftbox_status['client_url'] = str(syftbox_client.config.client_url)
        except Exception:
            _syftbox_status['client_url'] = str(syftbox_client.config.client_url)

    except Exception as e:
        _syftbox_status['error'] = f"Could not find SyftBox client: {e}"


def _print_startup_banner():
    """Print a beautiful, polished startup banner for syft-objects"""
    from . import __version__
    
    # Beautiful header
    print("╭─────────────────────────────────────────────────────────────╮")
    print("│                     🔐 SYFT OBJECTS                        │")
    print("│              Distributed Data Discovery & Sharing          │")
    print(f"│                        Version {__version__}                        │")
    print("╰─────────────────────────────────────────────────────────────╯")
    print()
    
    # SyftBox connection status
    if _syftbox_status.get('client_connected'):
        print("🌐 SyftBox Connection:")
        print(f"   ✅ Connected as: {_syftbox_status['user_email']}")
        if _syftbox_status.get('app_running'):
            print(f"   ✅ SyftBox app running")
        else:
            print(f"   ⚠️  SyftBox app not responding")
    elif _syftbox_status.get('error'):
        print("🌐 SyftBox Connection:")
        if "not available" in _syftbox_status['error']:
            print("   ℹ️  SyftBox not installed (optional)")
        else:
            print(f"   ⚠️  {_syftbox_status['error']}")
    
    # Server connection status  
    port = get_syft_objects_port()
    print()
    print("🚀 Syft Objects Server:")
    print(f"   📡 Port: {port}")
    print(f"   🌐 URL: http://localhost:{port}")
    
    print()


# Global variable to store SyftBox status
_syftbox_status = {}


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
    
    # Default fallback port (FastAPI backend)
    return 8004


def get_syft_objects_url(endpoint=""):
    """Get the full URL for syft-objects server endpoints"""
    port = get_syft_objects_port()
    base_url = f"http://localhost:{port}"
    if endpoint:
        return f"{base_url}/{endpoint.lstrip('/')}"
    return base_url


# Initialize SyftBox on module import
_initialize_syftbox() 