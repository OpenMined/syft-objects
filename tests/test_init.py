"""Tests for syft_objects.__init__ module"""

import pytest
from unittest.mock import patch, Mock
import syft_objects


def test_version():
    """Test version is defined"""
    assert syft_objects.__version__ == "0.3.7"


def test_exports():
    """Test all expected exports are available"""
    expected_exports = [
        "SyftObject", 
        "DataAccessor",
        "syobj", 
        "objects", 
        "ObjectsCollection",
        "scan_for_syft_objects",
        "load_syft_objects_from_directory",
        "get_syft_objects_port",
        "get_syft_objects_url"
    ]
    
    for export in expected_exports:
        assert hasattr(syft_objects, export)
        assert export in syft_objects.__all__


def test_objects_is_collection_instance():
    """Test that objects is an instance of ObjectsCollection"""
    assert isinstance(syft_objects.objects, syft_objects.ObjectsCollection)


@patch('syft_objects.check_syftbox_status')
@patch('syft_objects.ensure_syftbox_app_installed')
@patch('syft_objects.client._print_startup_banner')
def test_module_initialization(mock_banner, mock_ensure_app, mock_check_status):
    """Test module initialization calls"""
    # Reload module to trigger initialization
    import importlib
    importlib.reload(syft_objects)
    
    # Check that initialization functions were called
    mock_check_status.assert_called_once()
    mock_ensure_app.assert_called_once_with(silent=True)
    mock_banner.assert_called_once_with(only_if_needed=True)


def test_syftobject_class():
    """Test SyftObject class is available"""
    obj = syft_objects.SyftObject(
        name="test",
        uid="123",
        private_url="syft://test@example.com/private/test.txt",
        mock_url="syft://test@example.com/public/test.txt"
    )
    assert obj.name == "test"
    assert obj.uid == "123"


def test_data_accessor_class():
    """Test DataAccessor class is available"""
    with patch('syft_objects.data_accessor.get_syftbox_client') as mock_client:
        mock_client.return_value = Mock()
        accessor = syft_objects.DataAccessor("syft://test@example.com/test.txt")
        assert accessor.syft_url == "syft://test@example.com/test.txt"


def test_syobj_function():
    """Test syobj factory function is available"""
    with patch('syft_objects.factory.SyftObject') as mock_syft_object:
        mock_instance = Mock()
        mock_syft_object.return_value = mock_instance
        
        result = syft_objects.syobj(
            name="test",
            private_contents="private data",
            mock_contents="mock data"
        )
        
        assert result == mock_instance


def test_scan_for_syft_objects():
    """Test scan_for_syft_objects function"""
    with patch('syft_objects.utils.Path') as mock_path:
        mock_path.return_value.rglob.return_value = []
        result = syft_objects.scan_for_syft_objects("/test/path")
        assert result == []


def test_load_syft_objects_from_directory():
    """Test load_syft_objects_from_directory function"""
    with patch('syft_objects.utils.scan_for_syft_objects') as mock_scan:
        mock_scan.return_value = []
        result = syft_objects.load_syft_objects_from_directory("/test/path")
        assert result == []


def test_get_syft_objects_port():
    """Test get_syft_objects_port function"""
    with patch('syft_objects.client.Path') as mock_path:
        # Test with config file
        mock_path.home.return_value = Mock()
        mock_config = Mock()
        mock_config.exists.return_value = True
        mock_config.read_text.return_value = "8005"
        mock_path.home.return_value.__truediv__.return_value.__truediv__.return_value = mock_config
        
        port = syft_objects.get_syft_objects_port()
        assert port == 8005
        
        # Test without config file
        mock_config.exists.return_value = False
        port = syft_objects.get_syft_objects_port()
        assert port == 8004  # default


def test_get_syft_objects_url():
    """Test get_syft_objects_url function"""
    with patch('syft_objects.client.get_syft_objects_port') as mock_port:
        mock_port.return_value = 8004
        
        # Test base URL
        url = syft_objects.get_syft_objects_url()
        assert url == "http://localhost:8004"
        
        # Test with endpoint
        url = syft_objects.get_syft_objects_url("api/objects")
        assert url == "http://localhost:8004/api/objects"
        
        # Test with leading slash
        url = syft_objects.get_syft_objects_url("/api/objects")
        assert url == "http://localhost:8004/api/objects"