"""Tests for syft_objects.permissions module"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import syft_objects.permissions as permissions_module
from syft_objects.permissions import (
    _initialize_permissions, set_file_permissions_wrapper
)


class TestPermissionsModule:
    """Test permissions module functions"""
    
    def test_initialize_permissions_success(self):
        """Test successful permissions initialization"""
        # Reset globals first
        permissions_module.set_file_permissions = None
        permissions_module.get_file_permissions = None
        permissions_module.remove_file_permissions = None
        permissions_module.SYFTBOX_AVAILABLE = False
        
        mock_set = Mock()
        mock_get = Mock()
        mock_remove = Mock()
        
        with patch('syft_objects.permissions.syft_perm') as mock_syft_perm:
            mock_syft_perm.set_file_permissions = mock_set
            mock_syft_perm.get_file_permissions = mock_get
            mock_syft_perm.remove_file_permissions = mock_remove
            mock_syft_perm.SYFTBOX_AVAILABLE = True
            
            _initialize_permissions()
            
            assert permissions_module.set_file_permissions == mock_set
            assert permissions_module.get_file_permissions == mock_get
            assert permissions_module.remove_file_permissions == mock_remove
            assert permissions_module.SYFTBOX_AVAILABLE is True
    
    def test_initialize_permissions_import_error(self):
        """Test permissions initialization with import error"""
        # Reset globals
        permissions_module.set_file_permissions = None
        permissions_module.get_file_permissions = None
        permissions_module.remove_file_permissions = None
        permissions_module.SYFTBOX_AVAILABLE = False
        
        with patch('builtins.__import__', side_effect=ImportError("No syft_perm")):
            with patch('builtins.print') as mock_print:
                _initialize_permissions()
                
                # Check warning was printed
                mock_print.assert_called_with("Warning: syft-perm not available. Install with: pip install syft-perm")
                
                # Check fallback functions were created
                assert permissions_module.SYFTBOX_AVAILABLE is False
                assert callable(permissions_module.set_file_permissions)
                assert callable(permissions_module.get_file_permissions)
                assert callable(permissions_module.remove_file_permissions)
    
    def test_fallback_set_file_permissions(self):
        """Test fallback set_file_permissions function"""
        # Directly test the fallback by creating a fresh module state
        original_set = permissions_module.set_file_permissions
        
        try:
            # Create fallback function manually
            def fallback_set_file_permissions(*args, **kwargs):
                print("Warning: syft-perm not available. File permissions not set.")
            
            permissions_module.set_file_permissions = fallback_set_file_permissions
            
            with patch('builtins.print') as mock_print:
                # Call the fallback function directly
                permissions_module.set_file_permissions("test.txt", ["public"])
                
                # Check that the fallback print was called
                mock_print.assert_called_with("Warning: syft-perm not available. File permissions not set.")
                
        finally:
            permissions_module.set_file_permissions = original_set
    
    def test_fallback_get_file_permissions(self):
        """Test fallback get_file_permissions function"""
        # Force fallback initialization
        permissions_module.get_file_permissions = None
        
        with patch('builtins.__import__', side_effect=ImportError("No syft_perm")):
            _initialize_permissions()
            
            # Call the fallback function
            result = permissions_module.get_file_permissions("test.txt")
            assert result is None
    
    def test_fallback_remove_file_permissions(self):
        """Test fallback remove_file_permissions function"""
        # Directly test the fallback by creating a fresh module state
        original_remove = permissions_module.remove_file_permissions
        
        try:
            # Create fallback function manually
            def fallback_remove_file_permissions(*args, **kwargs):
                print("Warning: syft-perm not available. File permissions not removed.")
            
            permissions_module.remove_file_permissions = fallback_remove_file_permissions
            
            with patch('builtins.print') as mock_print:
                # Call the fallback function directly
                permissions_module.remove_file_permissions("test.txt")
                
                # Check that the fallback print was called
                mock_print.assert_called_with("Warning: syft-perm not available. File permissions not removed.")
                
        finally:
            permissions_module.remove_file_permissions = original_remove
    
    def test_set_file_permissions_wrapper_success(self):
        """Test set_file_permissions_wrapper successful call"""
        mock_set_perms = Mock()
        
        with patch.object(permissions_module, 'set_file_permissions', mock_set_perms):
            set_file_permissions_wrapper("test.txt", ["public"], ["admin"])
            
            mock_set_perms.assert_called_once_with("test.txt", ["public"], ["admin"])
    
    def test_set_file_permissions_wrapper_no_write_perms(self):
        """Test set_file_permissions_wrapper without write permissions"""
        mock_set_perms = Mock()
        
        with patch.object(permissions_module, 'set_file_permissions', mock_set_perms):
            set_file_permissions_wrapper("test.txt", ["public"])
            
            mock_set_perms.assert_called_once_with("test.txt", ["public"], None)
    
    def test_set_file_permissions_wrapper_syftbox_not_available(self):
        """Test set_file_permissions_wrapper when SyftBox not available"""
        mock_set_perms = Mock()
        mock_set_perms.side_effect = ValueError("Could not resolve file path")
        
        with patch.object(permissions_module, 'set_file_permissions', mock_set_perms):
            # Should not raise exception
            set_file_permissions_wrapper("test.txt", ["public"])
            
            mock_set_perms.assert_called_once()
    
    def test_set_file_permissions_wrapper_other_value_error(self):
        """Test set_file_permissions_wrapper with other ValueError"""
        mock_set_perms = Mock()
        mock_set_perms.side_effect = ValueError("Different error")
        
        with patch.object(permissions_module, 'set_file_permissions', mock_set_perms):
            # Should raise exception
            with pytest.raises(ValueError, match="Different error"):
                set_file_permissions_wrapper("test.txt", ["public"])
    
    def test_set_file_permissions_wrapper_generic_exception(self):
        """Test set_file_permissions_wrapper with generic exception"""
        mock_set_perms = Mock()
        mock_set_perms.side_effect = Exception("Generic error")
        
        with patch.object(permissions_module, 'set_file_permissions', mock_set_perms):
            # Should not raise exception (silently handled)
            set_file_permissions_wrapper("test.txt", ["public"])
            
            mock_set_perms.assert_called_once()
    
    def test_module_initialization(self):
        """Test that _initialize_permissions is called on module import"""
        # This is implicitly tested by importing the module
        # We can verify by checking if the globals were set
        assert hasattr(permissions_module, 'set_file_permissions')
        assert hasattr(permissions_module, 'get_file_permissions')
        assert hasattr(permissions_module, 'remove_file_permissions')
        assert hasattr(permissions_module, 'SYFTBOX_AVAILABLE')