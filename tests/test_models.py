"""Tests for syft_objects.models module"""

import pytest
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4
from unittest.mock import Mock, patch, MagicMock
import yaml

from syft_objects.models import SyftObject, utcnow, DataAccessor


class TestUtcNow:
    """Test utcnow utility function"""
    
    def test_utcnow_returns_datetime(self):
        """Test that utcnow returns a datetime object"""
        result = utcnow()
        assert isinstance(result, datetime)
        assert result.tzinfo == timezone.utc


class TestSyftObject:
    """Test SyftObject model"""
    
    def test_minimal_creation(self):
        """Test creating SyftObject with minimal required fields"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        assert obj.private_url == "syft://test@example.com/private/test.txt"
        assert obj.mock_url == "syft://test@example.com/public/test.txt"
        assert obj.syftobject == "syft://test@example.com/public/test.syftobject.yaml"
        assert isinstance(obj.uid, UUID)
        assert isinstance(obj.created_at, datetime)
        assert obj.syftobject_permissions == ["public"]
        assert obj.mock_permissions == ["public"]
        assert obj.mock_write_permissions == []
        assert obj.private_permissions == []
        assert obj.private_write_permissions == []
    
    def test_full_creation(self):
        """Test creating SyftObject with all fields"""
        uid = uuid4()
        now = datetime.now(timezone.utc)
        obj = SyftObject(
            uid=uid,
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml",
            created_at=now,
            syftobject_permissions=["test@example.com"],
            mock_permissions=["public"],
            mock_write_permissions=["test@example.com"],
            private_permissions=["test@example.com"],
            private_write_permissions=["test@example.com"],
            name="Test Object",
            description="Test Description",
            updated_at=now,
            metadata={"key": "value"}
        )
        assert obj.uid == uid
        assert obj.created_at == now
        assert obj.name == "Test Object"
        assert obj.description == "Test Description"
        assert obj.metadata == {"key": "value"}
    
    def test_alias_fields(self):
        """Test that field aliases work (private/mock)"""
        obj = SyftObject(
            private="syft://test@example.com/private/test.txt",
            mock="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        assert obj.private_url == "syft://test@example.com/private/test.txt"
        assert obj.mock_url == "syft://test@example.com/public/test.txt"
    
    def test_file_extension_validation_matching(self):
        """Test that matching file extensions pass validation"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        assert obj is not None
    
    def test_file_extension_validation_mismatched(self):
        """Test that mismatched file extensions fail validation"""
        with pytest.raises(ValueError, match="Mock and private files must have matching extensions"):
            SyftObject(
                private_url="syft://test@example.com/private/test.txt",
                mock_url="syft://test@example.com/public/test.csv",
                syftobject="syft://test@example.com/public/test.syftobject.yaml"
            )
    
    def test_file_extension_validation_no_extension(self):
        """Test that files without extensions pass validation"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test",
            mock_url="syft://test@example.com/public/test",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        assert obj is not None
    
    def test_file_extension_validation_one_has_extension(self):
        """Test that validation passes when only one file has extension"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        assert obj is not None
    
    def test_data_accessor_properties(self):
        """Test private and mock data accessor properties"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        assert isinstance(obj.private, DataAccessor)
        assert obj.private.syft_url == "syft://test@example.com/private/test.txt"
        assert obj.private.parent_object == obj
        
        assert isinstance(obj.mock, DataAccessor)
        assert obj.mock.syft_url == "syft://test@example.com/public/test.txt"
        assert obj.mock.parent_object == obj
    
    @patch('syft_objects.models.get_syftbox_client')
    @patch('syft_objects.models.extract_local_path_from_syft_url')
    def test_private_path_property(self, mock_extract, mock_client):
        """Test private_path property"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        # Test with SyftBox client available
        mock_client.return_value = Mock()
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.absolute.return_value = Path("/path/to/test.txt")
        mock_extract.return_value = mock_path
        
        assert obj.private_path == "/path/to/test.txt"
        
        # Test fallback to tmp directory
        mock_extract.return_value = None
        with patch('syft_objects.models.Path') as mock_path_cls:
            mock_tmp_path = Mock()
            mock_tmp_path.exists.return_value = True
            mock_tmp_path.absolute.return_value = Path("/tmp/test.txt")
            mock_path_cls.return_value = mock_tmp_path
            
            assert obj.private_path == "/tmp/test.txt"
    
    @patch('syft_objects.models.get_syftbox_client')
    @patch('syft_objects.models.extract_local_path_from_syft_url')
    def test_mock_path_property(self, mock_extract, mock_client):
        """Test mock_path property"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        mock_client.return_value = Mock()
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.absolute.return_value = Path("/path/to/test.txt")
        mock_extract.return_value = mock_path
        
        assert obj.mock_path == "/path/to/test.txt"
    
    def test_syftobject_path_property(self):
        """Test syftobject_path property"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        with patch('syft_objects.models.get_syftbox_client') as mock_client:
            with patch('syft_objects.models.extract_local_path_from_syft_url') as mock_extract:
                mock_client.return_value = Mock()
                mock_path = Mock()
                mock_path.exists.return_value = True
                mock_path.absolute.return_value = Path("/path/to/test.syftobject.yaml")
                mock_extract.return_value = mock_path
                
                assert obj.syftobject_path == "/path/to/test.syftobject.yaml"
        
        # Test fallback to metadata
        obj.syftobject = ""
        obj.metadata = {"_file_operations": {"syftobject_yaml_path": "/metadata/path.yaml"}}
        assert obj.syftobject_path == "/metadata/path.yaml"
    
    def test_file_type_property(self):
        """Test file_type property extracts correct extensions"""
        test_cases = [
            ("test.txt", "test.txt", ".txt"),
            ("test.csv", "test.csv", ".csv"),
            ("test.json", "test_mock.json", ".json"),
            ("test", "test", ""),
            (".hidden", ".hidden", ""),
            ("test.tar.gz", "test.tar.gz", ".gz"),
        ]
        
        for private_file, mock_file, expected_ext in test_cases:
            obj = SyftObject(
                private_url=f"syft://test@example.com/private/{private_file}",
                mock_url=f"syft://test@example.com/public/{mock_file}",
                syftobject="syft://test@example.com/public/test.syftobject.yaml"
            )
            assert obj.file_type == expected_ext
    
    @patch('syft_objects.models.create_html_display')
    def test_repr_html(self, mock_create_html):
        """Test _repr_html_ method"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        mock_create_html.return_value = "<div>HTML Display</div>"
        result = obj._repr_html_()
        assert result == "<div>HTML Display</div>"
        mock_create_html.assert_called_once_with(obj)
    
    @patch('syft_objects.models.get_syftbox_client')
    @patch('syft_objects.models.extract_local_path_from_syft_url')
    def test_check_file_exists(self, mock_extract, mock_client):
        """Test _check_file_exists method"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        # Test with existing file
        mock_client.return_value = Mock()
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_extract.return_value = mock_path
        
        assert obj._check_file_exists("syft://test@example.com/private/test.txt") is True
        
        # Test with non-existing file
        mock_path.exists.return_value = False
        assert obj._check_file_exists("syft://test@example.com/private/test.txt") is False
        
        # Test exception handling
        mock_client.side_effect = Exception("Error")
        assert obj._check_file_exists("syft://test@example.com/private/test.txt") is False
    
    def test_get_file_preview_text_file(self, temp_dir):
        """Test _get_file_preview with text file"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        # Create test file
        test_file = temp_dir / "test.txt"
        test_content = "Hello World!\nThis is a test file."
        test_file.write_text(test_content)
        
        preview = obj._get_file_preview(str(test_file))
        assert preview == test_content
        
        # Test truncation
        long_content = "x" * 2000
        test_file.write_text(long_content)
        preview = obj._get_file_preview(str(test_file), max_chars=100)
        assert preview.startswith("x" * 100)
        assert "truncated" in preview
    
    def test_get_file_preview_binary_file(self, temp_dir):
        """Test _get_file_preview with binary file"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.bin",
            mock_url="syft://test@example.com/public/test.bin",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        # Create binary file
        test_file = temp_dir / "test.bin"
        test_file.write_bytes(b'\x00\x01\x02\x03\x04')
        
        preview = obj._get_file_preview(str(test_file))
        assert "Binary file" in preview
        assert "test.bin" in preview
        assert "5 bytes" in preview
    
    def test_get_file_preview_missing_file(self):
        """Test _get_file_preview with missing file"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        preview = obj._get_file_preview("/nonexistent/file.txt")
        assert "File not found" in preview
    
    def test_save_yaml(self, temp_dir):
        """Test save_yaml method"""
        obj = SyftObject(
            uid=uuid4(),
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml",
            name="Test Object",
            metadata={"key": "value"}
        )
        
        # Test saving to file
        file_path = temp_dir / "test.yaml"
        
        with patch.object(obj, '_create_syftbox_permissions') as mock_perms:
            obj.save_yaml(file_path)
            
            # Check file was created with correct extension
            expected_path = temp_dir / "test.syftobject.yaml"
            assert expected_path.exists()
            
            # Check content
            with open(expected_path, 'r') as f:
                data = yaml.safe_load(f)
            
            assert data['name'] == "Test Object"
            assert data['private_url'] == "syft://test@example.com/private/test.txt"
            assert data['metadata'] == {"key": "value"}
            
            # Check permissions were called
            mock_perms.assert_called_once_with(expected_path)
    
    def test_save_yaml_without_permissions(self, temp_dir):
        """Test save_yaml without creating permissions"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        file_path = temp_dir / "test.yaml"
        
        with patch.object(obj, '_create_syftbox_permissions') as mock_perms:
            obj.save_yaml(file_path, create_syftbox_permissions=False)
            mock_perms.assert_not_called()
    
    def test_load_yaml(self, temp_dir, sample_yaml_content):
        """Test load_yaml class method"""
        # Save sample YAML
        file_path = temp_dir / "test.syftobject.yaml"
        file_path.write_text(sample_yaml_content)
        
        # Load object
        obj = SyftObject.load_yaml(file_path)
        
        assert obj.name == "test_object"
        assert obj.uid == UUID("12345678-1234-5678-1234-567812345678")
        assert obj.private_url == "syft://test@example.com/private/objects/test.txt"
        assert obj.metadata == {"key": "value"}
    
    def test_load_yaml_wrong_extension(self, temp_dir):
        """Test load_yaml with wrong file extension"""
        file_path = temp_dir / "test.yaml"
        file_path.write_text("name: test")
        
        with pytest.raises(ValueError, match="File must have .syftobject.yaml extension"):
            SyftObject.load_yaml(file_path)
    
    @patch('syft_objects.models.set_file_permissions_wrapper')
    def test_create_syftbox_permissions(self, mock_set_perms):
        """Test _create_syftbox_permissions method"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml",
            syftobject_permissions=["public"],
            mock_permissions=["public"],
            mock_write_permissions=["test@example.com"],
            private_permissions=["test@example.com"],
            private_write_permissions=["test@example.com"]
        )
        
        syftobject_path = Path("/path/to/test.syftobject.yaml")
        obj._create_syftbox_permissions(syftobject_path)
        
        # Check all three permission calls were made
        assert mock_set_perms.call_count == 3
        
        # Check syftobject permissions
        mock_set_perms.assert_any_call(
            str(syftobject_path),
            ["public"]
        )
        
        # Check mock permissions
        mock_set_perms.assert_any_call(
            "syft://test@example.com/public/test.txt",
            ["public"],
            ["test@example.com"]
        )
        
        # Check private permissions
        mock_set_perms.assert_any_call(
            "syft://test@example.com/private/test.txt",
            ["test@example.com"],
            ["test@example.com"]
        )
    
    @patch('syft_objects.models.set_file_permissions_wrapper')
    def test_set_permissions_mock(self, mock_set_perms):
        """Test set_permissions for mock file"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        obj.set_permissions("mock", read=["new@example.com"], write=["writer@example.com"])
        
        assert obj.mock_permissions == ["new@example.com"]
        assert obj.mock_write_permissions == ["writer@example.com"]
        
        mock_set_perms.assert_called_once_with(
            "syft://test@example.com/public/test.txt",
            ["new@example.com"],
            ["writer@example.com"]
        )
    
    @patch('syft_objects.models.set_file_permissions_wrapper')
    def test_set_permissions_private(self, mock_set_perms):
        """Test set_permissions for private file"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        obj.set_permissions("private", read=["new@example.com"])
        
        assert obj.private_permissions == ["new@example.com"]
        
        mock_set_perms.assert_called_once_with(
            "syft://test@example.com/private/test.txt",
            ["new@example.com"],
            []  # write permissions unchanged
        )
    
    @patch('syft_objects.models.set_file_permissions_wrapper')
    def test_set_permissions_syftobject(self, mock_set_perms):
        """Test set_permissions for syftobject file"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        obj.set_permissions("syftobject", read=["new@example.com"])
        
        assert obj.syftobject_permissions == ["new@example.com"]
        
        mock_set_perms.assert_called_once_with(
            "syft://test@example.com/public/test.syftobject.yaml",
            ["new@example.com"]
        )
    
    def test_set_permissions_invalid_type(self):
        """Test set_permissions with invalid file type"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        with pytest.raises(ValueError, match="Invalid file_type"):
            obj.set_permissions("invalid", read=["test@example.com"])
    
    def test_model_dump_serialization(self):
        """Test model serialization with datetime and UUID"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/test.txt",
            mock_url="syft://test@example.com/public/test.txt",
            syftobject="syft://test@example.com/public/test.syftobject.yaml"
        )
        
        data = obj.model_dump(mode='json')
        
        # Check UUID is serialized as string
        assert isinstance(data['uid'], str)
        
        # Check datetime is serialized as string
        assert isinstance(data['created_at'], str)