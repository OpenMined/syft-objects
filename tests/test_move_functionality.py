"""Tests for the move_path functionality in accessors"""

import pytest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, patch

from syft_objects import create_object
from syft_objects.clean_api import MockAccessor, PrivateAccessor, SyftObjectConfigAccessor


class TestMovePathFunctionality:
    """Test the move_path methods on all accessors"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock SyftBox client"""
        client = Mock()
        client.email = "test@example.com"
        client.datasites = Path("/mock/datasites")
        return client
    
    def test_mock_accessor_move_path_with_syft_url(self, temp_dir, mock_client):
        """Test moving mock file with syft:// URL"""
        # Create test object
        mock_file = temp_dir / "mock.txt"
        mock_file.write_text("mock data")
        
        with patch('syft_objects.client.get_syftbox_client', return_value=mock_client):
            with patch('syft_objects.client.extract_local_path_from_syft_url') as mock_extract:
                with patch('syft_objects.file_ops.move_object_to_syftbox_location') as mock_move:
                    # Setup mocks
                    mock_extract.return_value = mock_file
                    mock_move.return_value = True
                    
                    # Create object
                    obj = create_object(
                        name="Test Object",
                        mock_file=str(mock_file),
                        private_contents="private"
                    )
                    
                    # Test move
                    new_url = "syft://test@example.com/public/objects/new_mock.txt"
                    result = obj.mock.move_path(new_url)
                    
                    assert result is True
                    mock_move.assert_called_once()
                    assert obj._CleanSyftObject__obj.mock_url == new_url
    
    def test_private_accessor_move_path_with_local_path(self, temp_dir, mock_client):
        """Test moving private file with local path"""
        # Create test object
        private_file = temp_dir / "private.txt"
        private_file.write_text("private data")
        
        with patch('syft_objects.client.get_syftbox_client', return_value=mock_client):
            with patch('syft_objects.client.extract_local_path_from_syft_url') as mock_extract:
                with patch('syft_objects.file_ops.move_object_to_syftbox_location') as mock_move:
                    # Setup mocks
                    mock_extract.return_value = private_file
                    mock_move.return_value = True
                    
                    # Create object
                    obj = create_object(
                        name="Test Object",
                        mock_contents="mock",
                        private_file=str(private_file)
                    )
                    
                    # Test move with local path
                    result = obj.private.move_path("new_private.txt")
                    
                    assert result is True
                    mock_move.assert_called_once()
                    # Check the URL was constructed correctly
                    call_args = mock_move.call_args[0]
                    # The email is extracted from the object's current URL, not the mock client
                    assert call_args[1].endswith("/private/objects/new_private.txt")
    
    def test_syftobject_config_move_path_ensures_extension(self, temp_dir, mock_client):
        """Test moving syftobject config ensures .syftobject.yaml extension"""
        with patch('syft_objects.client.get_syftbox_client', return_value=mock_client):
            with patch('syft_objects.client.extract_local_path_from_syft_url') as mock_extract:
                with patch('syft_objects.file_ops.move_object_to_syftbox_location') as mock_move:
                    # Setup mocks
                    yaml_file = temp_dir / "obj.syftobject.yaml"
                    yaml_file.touch()  # Create the file
                    mock_extract.return_value = yaml_file
                    mock_move.return_value = True
                    
                    # Create object
                    obj = create_object(
                        name="Test Object",
                        mock_contents="mock",
                        private_contents="private"
                    )
                    
                    # Test move without extension
                    result = obj.syftobject_config.move_path("new_object")
                    
                    assert result is True
                    mock_move.assert_called_once()
                    # Check the URL was constructed with proper extension
                    call_args = mock_move.call_args[0]
                    assert call_args[1].endswith("new_object.syftobject.yaml")
    
    def test_move_path_handles_missing_file(self, temp_dir, mock_client):
        """Test move_path returns False when file doesn't exist"""
        with patch('syft_objects.clean_api.get_syftbox_client', return_value=mock_client):
            with patch('syft_objects.clean_api.extract_local_path_from_syft_url') as mock_extract:
                # File doesn't exist
                mock_extract.return_value = temp_dir / "nonexistent.txt"
                
                obj = create_object(
                    name="Test Object",
                    mock_contents="mock",
                    private_contents="private"
                )
                
                # All accessors should return False
                assert obj.mock.move_path("new_path") is False
                assert obj.private.move_path("new_path") is False
                assert obj.syftobject_config.move_path("new_path") is False
    
    def test_move_path_handles_exceptions(self, temp_dir):
        """Test move_path returns False on exceptions"""
        with patch('syft_objects.client.get_syftbox_client', side_effect=Exception("Test error")):
            obj = create_object(
                name="Test Object",
                mock_contents="mock",
                private_contents="private"
            )
            
            # All accessors should return False
            assert obj.mock.move_path("new_path") is False
            assert obj.private.move_path("new_path") is False
            assert obj.syftobject_config.move_path("new_path") is False