"""Pytest configuration and fixtures for syft-objects tests"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_syftbox_client():
    """Mock SyftBox client for testing"""
    client = Mock()
    client.email = "test@example.com"
    client.datasites = Path("/tmp/test_datasites")
    client.config = Mock()
    client.config.client_url = "http://localhost:5001"
    return client


@pytest.fixture
def mock_syftbox_available(monkeypatch):
    """Mock SyftBox availability"""
    monkeypatch.setattr("syft_objects.client.SYFTBOX_AVAILABLE", True)
    

@pytest.fixture
def sample_syft_object_data():
    """Sample data for creating SyftObject instances"""
    return {
        "name": "test_object",
        "uid": "12345678-1234-5678-1234-567812345678",
        "description": "Test object description",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
        "private_url": "syft://test@example.com/private/objects/test.txt",
        "mock_url": "syft://test@example.com/public/objects/test_mock.txt",
        "syftobject": "syft://test@example.com/public/objects/test.syftobject.yaml",
        "private_permissions": ["test@example.com"],
        "private_write_permissions": ["test@example.com"],
        "mock_permissions": ["public"],
        "mock_write_permissions": ["test@example.com"],
        "syftobject_permissions": ["public"],
        "metadata": {"key": "value"}
    }


@pytest.fixture
def sample_yaml_content():
    """Sample YAML content for SyftObject"""
    return """name: test_object
uid: 12345678-1234-5678-1234-567812345678
description: Test object description
created_at: '2024-01-01T00:00:00'
updated_at: '2024-01-01T00:00:00'
private_url: syft://test@example.com/private/objects/test.txt
mock_url: syft://test@example.com/public/objects/test_mock.txt
syftobject: syft://test@example.com/public/objects/test.syftobject.yaml
private_permissions:
  - test@example.com
private_write_permissions:
  - test@example.com
mock_permissions:
  - public
mock_write_permissions:
  - test@example.com
syftobject_permissions:
  - public
metadata:
  key: value
"""


@pytest.fixture(autouse=True)
def reset_globals():
    """Reset global variables before each test"""
    # Reset client globals
    import syft_objects.client as client_module
    client_module.SYFTBOX_AVAILABLE = False
    client_module.SyftBoxClient = None
    client_module.SyftBoxURL = None
    client_module._syftbox_status = {}
    
    # Reset collections globals
    import syft_objects.collections as collections_module
    # Clear any cached objects
    yield
    # Cleanup after test