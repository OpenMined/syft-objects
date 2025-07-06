"""Tests for syft_objects.file_ops module"""

import pytest
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from syft_objects.file_ops import (
    move_file_to_syftbox_location, copy_file_to_syftbox_location,
    generate_syftbox_urls, generate_syftobject_url
)


class TestFileOpsModule:
    """Test file_ops module functions"""
    
    @patch('syft_objects.file_ops.SYFTBOX_AVAILABLE', False)
    def test_move_file_no_syftbox(self, temp_dir):
        """Test move_file_to_syftbox_location when SyftBox not available"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        result = move_file_to_syftbox_location(test_file, "syft://test@example.com/test.txt")
        assert result is False
        assert test_file.exists()  # File should not be moved
    
    @patch('syft_objects.file_ops.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.file_ops.SyftBoxURL')
    @patch('shutil.move')
    def test_move_file_success(self, mock_move, mock_url_class, temp_dir):
        """Test move_file_to_syftbox_location successful move"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        
        target_path = temp_dir / "datasites" / "test@example.com" / "private" / "test.txt"
        mock_url_obj = Mock()
        mock_url_obj.to_local_path.return_value = target_path
        mock_url_class.return_value = mock_url_obj
        
        result = move_file_to_syftbox_location(
            test_file, 
            "syft://test@example.com/private/test.txt",
            mock_client
        )
        
        assert result is True
        mock_move.assert_called_once_with(str(test_file), str(target_path))
        mock_url_obj.to_local_path.assert_called_once_with(datasites_path=mock_client.datasites)
    
    @patch('syft_objects.file_ops.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.file_ops.SyftBoxURL')
    @patch('builtins.print')
    def test_move_file_exception(self, mock_print, mock_url_class, temp_dir):
        """Test move_file_to_syftbox_location with exception"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        mock_client = Mock()
        mock_url_class.side_effect = Exception("URL error")
        
        result = move_file_to_syftbox_location(
            test_file,
            "syft://test@example.com/private/test.txt",
            mock_client
        )
        
        assert result is False
        mock_print.assert_called()
        assert "Could not move object" in str(mock_print.call_args)
    
    @patch('syft_objects.file_ops.SYFTBOX_AVAILABLE', False)
    def test_copy_file_no_syftbox(self, temp_dir):
        """Test copy_file_to_syftbox_location when SyftBox not available"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        result = copy_file_to_syftbox_location(test_file, "syft://test@example.com/test.txt")
        assert result is False
    
    @patch('syft_objects.file_ops.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.file_ops.SyftBoxURL')
    @patch('shutil.copy2')
    def test_copy_file_success(self, mock_copy, mock_url_class, temp_dir):
        """Test copy_file_to_syftbox_location successful copy"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        
        target_path = temp_dir / "datasites" / "test@example.com" / "public" / "test.txt"
        mock_url_obj = Mock()
        mock_url_obj.to_local_path.return_value = target_path
        mock_url_class.return_value = mock_url_obj
        
        result = copy_file_to_syftbox_location(
            test_file,
            "syft://test@example.com/public/test.txt",
            mock_client
        )
        
        assert result is True
        mock_copy.assert_called_once_with(str(test_file), str(target_path))
    
    @patch('syft_objects.file_ops.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.file_ops.SyftBoxURL')
    def test_copy_file_creates_directory(self, mock_url_class, temp_dir):
        """Test copy_file_to_syftbox_location creates parent directory"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        
        target_path = temp_dir / "datasites" / "test@example.com" / "new" / "dir" / "test.txt"
        mock_url_obj = Mock()
        mock_url_obj.to_local_path.return_value = target_path
        mock_url_class.return_value = mock_url_obj
        
        with patch('shutil.copy2'):
            result = copy_file_to_syftbox_location(
                test_file,
                "syft://test@example.com/new/dir/test.txt",
                mock_client
            )
        
        assert result is True
        assert target_path.parent.exists()
    
    def test_generate_syftbox_urls_with_client(self):
        """Test generate_syftbox_urls with SyftBox client"""
        mock_client = Mock()
        
        # Test with public mock
        private_url, mock_url = generate_syftbox_urls(
            "test@example.com",
            "data.txt",
            mock_client,
            mock_is_public=True
        )
        
        assert private_url == "syft://test@example.com/private/objects/data.txt"
        assert mock_url == "syft://test@example.com/public/objects/data.txt"
        
        # Test with private mock
        private_url, mock_url = generate_syftbox_urls(
            "test@example.com",
            "data.txt",
            mock_client,
            mock_is_public=False
        )
        
        assert private_url == "syft://test@example.com/private/objects/data.txt"
        assert mock_url == "syft://test@example.com/private/objects/data.txt"
    
    def test_generate_syftbox_urls_without_client(self):
        """Test generate_syftbox_urls without SyftBox client"""
        # Test with public mock
        private_url, mock_url = generate_syftbox_urls(
            "test@example.com",
            "data.txt",
            None,
            mock_is_public=True
        )
        
        assert private_url == "syft://test@example.com/SyftBox/datasites/test@example.com/private/objects/data.txt"
        assert mock_url == "syft://test@example.com/SyftBox/datasites/test@example.com/public/objects/data.txt"
        
        # Test with private mock
        private_url, mock_url = generate_syftbox_urls(
            "test@example.com",
            "data.txt",
            None,
            mock_is_public=False
        )
        
        assert private_url == "syft://test@example.com/SyftBox/datasites/test@example.com/private/objects/data.txt"
        assert mock_url == "syft://test@example.com/SyftBox/datasites/test@example.com/private/objects/data.txt"
    
    def test_generate_syftobject_url_with_client(self):
        """Test generate_syftobject_url with SyftBox client"""
        mock_client = Mock()
        
        url = generate_syftobject_url(
            "test@example.com",
            "object.syftobject.yaml",
            mock_client
        )
        
        assert url == "syft://test@example.com/public/objects/object.syftobject.yaml"
    
    def test_generate_syftobject_url_without_client(self):
        """Test generate_syftobject_url without SyftBox client"""
        url = generate_syftobject_url(
            "test@example.com",
            "object.syftobject.yaml",
            None
        )
        
        assert url == "syft://test@example.com/SyftBox/datasites/test@example.com/public/objects/object.syftobject.yaml"
    
    @patch('syft_objects.file_ops.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.file_ops.SyftBoxURL')
    @patch('shutil.copy2')
    def test_copy_file_exception_handling(self, mock_copy, mock_url_class, temp_dir):
        """Test copy_file_to_syftbox_location exception handling"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        
        target_path = temp_dir / "datasites" / "test@example.com" / "public" / "test.txt"
        mock_url_obj = Mock()
        mock_url_obj.to_local_path.return_value = target_path
        mock_url_class.return_value = mock_url_obj
        
        # Make copy2 raise an exception
        mock_copy.side_effect = Exception("Copy failed")
        
        with patch('builtins.print') as mock_print:
            result = copy_file_to_syftbox_location(
                test_file,
                "syft://test@example.com/public/test.txt",
                mock_client
            )
            
            assert result is False
            mock_print.assert_called_with("Warning: Could not copy object to SyftBox location: Copy failed")