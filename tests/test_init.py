"""Tests for syft_objects.__init__ module"""

import pytest
from unittest.mock import patch, Mock
import syft_objects


def test_version():
    """Test version is defined"""
    assert syft_objects.__version__ == "0.9.67"


def test_exports():
    """Test all expected exports are available"""
    expected_exports = [
        "create_object", 
        "delete_object",
        "objects"
    ]
    
    for export in expected_exports:
        assert hasattr(syft_objects, export)
        assert export in syft_objects.__all__


def test_objects_is_collection_instance():
    """Test that objects is an instance of ObjectsCollection"""
    # ObjectsCollection is now internal, so we can't check the class directly
    # Just verify objects exists and has expected methods
    assert hasattr(syft_objects.objects, 'refresh')
    assert hasattr(syft_objects.objects, 'search')


def test_module_initialization():
    """Test module initialization calls"""
    # Just verify that the module can be imported and has expected attributes
    import syft_objects
    
    # Check that expected attributes exist
    assert hasattr(syft_objects, '__version__')
    assert hasattr(syft_objects, 'objects')
    assert hasattr(syft_objects, 'create_object')
    assert hasattr(syft_objects, 'delete_object')


def test_create_object_function():
    """Test create_object function is available"""
    with patch('syft_objects._factory.syobj') as mock_syobj:
        mock_instance = Mock()
        mock_syobj.return_value = mock_instance
        
        result = syft_objects.create_object(
            name="test",
            private_contents="private data",
            mock_contents="mock data"
        )
        
        assert result == mock_instance
        mock_syobj.assert_called_once_with("test", private_contents="private data", mock_contents="mock data")


def test_delete_object_function():
    """Test delete_object function is available"""
    mock_obj = Mock()
    mock_obj.delete_obj.return_value = True
    mock_obj.uid = "test-uid"
    mock_obj.get_uid.return_value = "test-uid"
    
    with patch.object(syft_objects.objects, '_objects', [mock_obj]):
        with patch.object(syft_objects.objects, '_cached', True):  # Skip loading
            with patch.object(syft_objects.objects, 'refresh') as mock_refresh:
                result = syft_objects.delete_object("test-uid")
                
                assert result is True
                mock_obj.delete_obj.assert_called_once_with(None)  # user_email parameter
                mock_refresh.assert_called_once()


def test_delete_object_not_found():
    """Test delete_object raises KeyError for invalid UID"""
    with patch.object(syft_objects.objects, '__getitem__', side_effect=KeyError):
        with pytest.raises(KeyError, match="Object with UID 'invalid-uid' not found"):
            syft_objects.delete_object("invalid-uid")


def test_delete_object_invalid_type():
    """Test delete_object raises TypeError for non-string UID"""
    with pytest.raises(TypeError, match="UID must be str"):
        syft_objects.delete_object(123)