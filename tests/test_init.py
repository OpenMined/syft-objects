"""Tests for syft_objects.__init__ module"""

import pytest
from unittest.mock import patch, Mock
import syft_objects


def test_version():
    """Test version is defined"""
    assert syft_objects.__version__ == "0.6.13"


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


def test_module_initialization():
    """Test module initialization calls"""
    # Just verify that the module can be imported and has expected attributes
    import syft_objects
    
    # Check that expected attributes exist
    assert hasattr(syft_objects, '__version__')
    assert hasattr(syft_objects, 'objects')
    assert hasattr(syft_objects, 'SyftObject')
    assert hasattr(syft_objects, 'ObjectsCollection')


def test_syftobject_class():
    """Test SyftObject class is available"""
    from uuid import uuid4
    uid = uuid4()
    obj = syft_objects.SyftObject(
        name="test",
        uid=uid,
        private_url="syft://test@example.com/private/test.txt",
        mock_url="syft://test@example.com/public/test.txt",
        syftobject="syft://test@example.com/public/test.syftobject.yaml"
    )
    assert obj.name == "test"
    assert obj.uid == uid


def test_data_accessor_class():
    """Test DataAccessor class is available"""
    mock_obj = Mock()
    accessor = syft_objects.DataAccessor("syft://test@example.com/test.txt", mock_obj)
    assert accessor._syft_url == "syft://test@example.com/test.txt"
    assert accessor._syft_object == mock_obj


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


def test_get_syft_objects_port(temp_dir):
    """Test get_syft_objects_port function"""
    # Test with config file
    config_dir = temp_dir / ".syftbox"
    config_dir.mkdir()
    config_file = config_dir / "syft_objects.config"
    config_file.write_text("8005")
    
    with patch('syft_objects.client.Path.home', return_value=temp_dir):
        port = syft_objects.get_syft_objects_port()
        assert port == 8005
    
    # Test without config file
    config_file.unlink()
    with patch('syft_objects.client.Path.home', return_value=temp_dir):
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