"""Test the public API functions"""
import pytest
from unittest.mock import Mock, patch
import syft_objects as syo


class TestPublicAPI:
    """Test the simplified public API"""
    
    def test_public_api_exports(self):
        """Test that only the essential items are exported"""
        public_attrs = [attr for attr in dir(syo) if not attr.startswith('_')]
        # Should only have the 3 essential items (syobj removed)
        expected = {'create_object', 'delete_object', 'objects'}
        assert set(public_attrs) == expected
        
    def test_create_object_works(self):
        """Test that create_object calls the internal syobj function"""
        # Mock the internal syobj function
        with patch('syft_objects.factory.syobj') as mock_syobj:
            mock_syobj.return_value = Mock()
            result = syo.create_object('test', private_contents='data')
            mock_syobj.assert_called_once_with('test', private_contents='data')
            
    def test_delete_object_by_uid(self):
        """Test deleting object by UID"""
        # Create a mock object
        mock_obj = Mock()
        mock_obj.delete.return_value = True
        
        # Create a mock collection that contains our object
        mock_objects = Mock()
        mock_objects.__getitem__ = Mock(return_value=mock_obj)
        mock_objects.refresh = Mock()
        
        with patch('syft_objects.objects', mock_objects):
            result = syo.delete_object('some-uid-string')
            assert result is True
            mock_objects.__getitem__.assert_called_once_with('some-uid-string')
            mock_obj.delete.assert_called_once()
            mock_objects.refresh.assert_called_once()
                
    def test_delete_object_uid_not_found(self):
        """Test delete with non-existent UID"""
        with patch.object(syo.objects, '__getitem__', side_effect=KeyError):
            with pytest.raises(KeyError, match="Object with UID 'bad-uid' not found"):
                syo.delete_object('bad-uid')
                
    def test_delete_object_invalid_type_int(self):
        """Test delete with integer (no longer supported)"""
        with pytest.raises(TypeError, match="UID must be str, not int"):
            syo.delete_object(123)
            
    def test_delete_object_invalid_type_float(self):
        """Test delete with float"""
        with pytest.raises(TypeError, match="UID must be str, not float"):
            syo.delete_object(3.14)
            
    def test_delete_object_failed_deletion(self):
        """Test when deletion fails"""
        # Create a mock object that fails to delete
        mock_obj = Mock()
        mock_obj.delete.return_value = False
        
        # Create a mock collection that contains our object
        mock_objects = Mock()
        mock_objects.__getitem__ = Mock(return_value=mock_obj)
        mock_objects.refresh = Mock()
        
        with patch('syft_objects.objects', mock_objects):
            result = syo.delete_object('some-uid')
            assert result is False
            mock_objects.__getitem__.assert_called_once_with('some-uid')
            mock_obj.delete.assert_called_once()
            # Refresh should NOT be called if deletion failed
            mock_objects.refresh.assert_not_called()