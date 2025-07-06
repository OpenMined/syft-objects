"""Tests for syft_objects.factory module"""

import pytest
import os
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from uuid import UUID
import yaml

from syft_objects.factory import detect_user_email, syobj
from syft_objects.models import SyftObject


class TestDetectUserEmail:
    """Test detect_user_email function"""
    
    def test_detect_from_env(self):
        """Test email detection from environment variable"""
        with patch.dict(os.environ, {'SYFTBOX_EMAIL': 'env@example.com'}):
            email = detect_user_email()
            assert email == "env@example.com"
    
    @patch('syft_objects.factory.get_syftbox_client')
    def test_detect_from_client(self, mock_get_client):
        """Test email detection from SyftBox client"""
        mock_client = Mock()
        mock_client.email = "client@example.com"
        mock_get_client.return_value = mock_client
        
        with patch.dict(os.environ, {}, clear=True):
            email = detect_user_email()
            assert email == "client@example.com"
    
    def test_detect_from_config_file(self, temp_dir):
        """Test email detection from SyftBox config file"""
        # Create config file
        config_dir = temp_dir / ".syftbox"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text("email: config@example.com\n")
        
        with patch('syft_objects.factory.Path.home', return_value=temp_dir):
            with patch('syft_objects.factory.get_syftbox_client', return_value=None):
                with patch.dict(os.environ, {}, clear=True):
                    email = detect_user_email()
                    assert email == "config@example.com"
    
    @patch('subprocess.run')
    def test_detect_from_git(self, mock_run):
        """Test email detection from git config"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="git@example.com\n"
        )
        
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            with patch('syft_objects.factory.Path.home', return_value=Path("/nonexistent")):
                with patch.dict(os.environ, {}, clear=True):
                    email = detect_user_email()
                    assert email == "git@example.com"
    
    def test_detect_fallback(self):
        """Test email detection fallback"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            with patch('syft_objects.factory.Path.home', return_value=Path("/nonexistent")):
                with patch('subprocess.run', side_effect=Exception("No git")):
                    with patch.dict(os.environ, {}, clear=True):
                        email = detect_user_email()
                        assert email == "user@example.com"


class TestSyobj:
    """Test syobj factory function"""
    
    def test_minimal_creation(self):
        """Test syobj with minimal parameters"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            with patch('syft_objects.factory.detect_user_email', return_value="test@example.com"):
                obj = syobj()
                
                assert isinstance(obj, SyftObject)
                assert obj.name.startswith("Auto Object")
                assert "Object" in obj.description and "with explicit" in obj.description
                assert obj.private_permissions == ["test@example.com"]
                assert obj.mock_permissions == ["public"]
    
    def test_with_content_strings(self):
        """Test syobj with content strings"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(
                name="Test Object",
                private_contents="Private data",
                mock_contents="Mock data"
            )
            
            assert obj.name == "Test Object"
            assert "private" in obj.private_url
            assert "public" in obj.mock_url
    
    def test_with_files(self, temp_dir):
        """Test syobj with file paths"""
        # Create test files
        private_file = temp_dir / "private.txt"
        private_file.write_text("Private file content")
        
        mock_file = temp_dir / "mock.txt"
        mock_file.write_text("Mock file content")
        
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(
                name="File Object",
                private_file=str(private_file),
                mock_file=str(mock_file)
            )
            
            assert obj.name == "File Object"
            assert "private" in obj.private_url
            assert "public" in obj.mock_url
    
    def test_file_not_found(self):
        """Test syobj with non-existent file"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            with pytest.raises(FileNotFoundError, match="Private file not found"):
                syobj(private_file="/nonexistent/file.txt")
    
    def test_auto_generate_name_from_content(self):
        """Test automatic name generation from content"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(private_contents="Some test content")
            
            assert obj.name.startswith("Content")
            assert len(obj.name.split()[-1]) == 8  # Hash suffix
    
    def test_auto_generate_name_from_file(self, temp_dir):
        """Test automatic name generation from file"""
        test_file = temp_dir / "my_data_file.csv"
        test_file.write_text("col1,col2\n1,2")
        
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(private_file=str(test_file))
            
            assert obj.name == "My Data File"
    
    def test_permissions_customization(self):
        """Test custom permissions"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(
                name="Custom Perms",
                discovery_read=["user1@example.com"],
                mock_read=["user2@example.com", "user3@example.com"],
                mock_write=["user2@example.com"],
                private_read=["owner@example.com"],
                private_write=["owner@example.com", "admin@example.com"]
            )
            
            assert obj.syftobject_permissions == ["user1@example.com"]
            assert obj.mock_permissions == ["user2@example.com", "user3@example.com"]
            assert obj.mock_write_permissions == ["user2@example.com"]
            assert obj.private_permissions == ["owner@example.com"]
            assert obj.private_write_permissions == ["owner@example.com", "admin@example.com"]
    
    def test_metadata_handling(self):
        """Test metadata processing"""
        metadata = {
            "description": "Custom description",
            "email": "custom@example.com",
            "custom_key": "custom_value",
            "auto_save": False,
            "create_syftbox_permissions": False
        }
        
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(name="Meta Object", metadata=metadata)
            
            assert obj.description == "Custom description"
            assert obj.private_permissions == ["custom@example.com"]
            # System keys should be removed from clean metadata
            assert "auto_save" not in obj.metadata
            assert "create_syftbox_permissions" not in obj.metadata
            assert obj.metadata.get("custom_key") == "custom_value"
    
    @patch('syft_objects.factory.get_syftbox_client')
    @patch('syft_objects.factory.move_file_to_syftbox_location')
    def test_syftbox_file_movement(self, mock_move, mock_get_client, temp_dir):
        """Test file movement to SyftBox locations"""
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        mock_get_client.return_value = mock_client
        mock_move.return_value = True
        
        obj = syobj(
            name="Move Test",
            private_contents="Private data",
            mock_contents="Mock data",
            metadata={"move_files_to_syftbox": True}
        )
        
        # Should have attempted to move files
        assert mock_move.call_count >= 2  # At least private and mock files
        
        # Check file operations were tracked
        file_ops = obj.metadata.get("_file_operations", {})
        assert file_ops.get("syftbox_available") is True
        assert len(file_ops.get("files_moved_to_syftbox", [])) > 0
    
    @patch('syft_objects.factory.get_syftbox_client')
    @patch('syft_objects.factory.copy_file_to_syftbox_location')
    def test_syftbox_file_copy(self, mock_copy, mock_get_client, temp_dir):
        """Test file copying when using existing files"""
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        mock_get_client.return_value = mock_client
        mock_copy.return_value = True
        
        # Create test file
        test_file = temp_dir / "original.txt"
        test_file.write_text("Original content")
        
        obj = syobj(
            name="Copy Test",
            private_file=str(test_file),
            metadata={"move_files_to_syftbox": True}
        )
        
        # Should have copied (not moved) the original file
        mock_copy.assert_called()
        assert test_file.exists()  # Original should still exist
    
    def test_auto_save_disabled(self):
        """Test with auto_save disabled"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            with patch.object(SyftObject, 'save_yaml') as mock_save:
                obj = syobj(
                    name="No Save",
                    metadata={"auto_save": False}
                )
                
                mock_save.assert_not_called()
    
    def test_auto_save_custom_location(self, temp_dir):
        """Test auto_save with custom save location"""
        save_path = temp_dir / "custom" / "location.yaml"
        
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(
                name="Custom Save",
                metadata={"save_to": str(save_path)}
            )
            
            # Should create as .syftobject.yaml
            expected_path = save_path.parent / "location.syftobject.yaml"
            assert expected_path.exists()
    
    def test_mixed_content_and_file(self, temp_dir):
        """Test mixing content string and file"""
        mock_file = temp_dir / "mock.txt"
        mock_file.write_text("Mock from file")
        
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(
                name="Mixed",
                private_contents="Private from string",
                mock_file=str(mock_file)
            )
            
            assert "mixed" in obj.private_url.lower()
            # Check that we have a mock URL with public path
            assert "public" in obj.mock_url
    
    def test_only_mock_content(self):
        """Test with only mock content provided"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(
                name="Mock Only",
                mock_contents="Only mock data"
            )
            
            assert obj.name == "Mock Only"
            # Should auto-generate private content
            assert "private" in obj.private_url
    
    def test_only_private_content(self):
        """Test with only private content provided"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj = syobj(
                name="Private Only",
                private_contents="Only private data"
            )
            
            assert obj.name == "Private Only"
            # Should auto-generate mock content - check that we have a public URL
            assert "public" in obj.mock_url
    
    def test_uid_uniqueness(self):
        """Test that each object gets unique UID"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            obj1 = syobj(name="Object 1")
            obj2 = syobj(name="Object 2")
            
            assert obj1.uid != obj2.uid
            assert isinstance(obj1.uid, UUID)
            assert isinstance(obj2.uid, UUID)
    
    def test_description_auto_generation(self):
        """Test automatic description generation"""
        with patch('syft_objects.factory.get_syftbox_client', return_value=None):
            # With content strings
            obj1 = syobj(
                name="Content Object",
                private_contents="data",
                mock_contents="mock"
            )
            assert "explicit mock and private content" in obj1.description
            
            # With files
            with patch('pathlib.Path.exists', return_value=True):
                obj2 = syobj(
                    name="File Object",
                    private_file="private.txt",
                    mock_file="mock.txt"
                )
                assert "explicit mock and private files" in obj2.description
    
    def test_syftobject_yaml_movement(self, temp_dir):
        """Test .syftobject.yaml file movement to SyftBox"""
        # Skip complex mocking for now - focus on basic functionality
        pass