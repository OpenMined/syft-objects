"""Integration tests for folder object support"""

import pytest
import shutil
from pathlib import Path
from uuid import UUID

from syft_objects import create_object
from syft_objects.models import SyftObject
from syft_objects.data_accessor import FolderAccessor


@pytest.fixture
def temp_folder(temp_dir):
    """Create a temporary folder with test files"""
    folder = temp_dir / "test_folder"
    folder.mkdir()
    
    # Create test files
    (folder / "run.sh").write_text("#!/bin/bash\necho 'Running job'")
    (folder / "data.csv").write_text("id,value\n1,100\n2,200")
    (folder / "config.json").write_text('{"timeout": 3600, "workers": 4}')
    
    # Create subdirectory
    subdir = folder / "logs"
    subdir.mkdir()
    (subdir / "output.log").write_text("Job started\nJob completed")
    
    return folder


class TestFolderObjects:
    """Test folder object functionality"""
    
    def test_folder_object_creation(self, temp_folder):
        """Test creating a folder SyftObject"""
        obj = create_object(
            name="test_job",
            private_folder=str(temp_folder),
            mock_read=["public"],
            private_read=["owner@example.com"]
        )
        
        assert obj.object_type == "folder"
        assert obj.is_folder
        assert obj.private_url.endswith('/')
        assert obj.mock_url.endswith('/')
        assert isinstance(obj.uid, UUID)
    
    def test_folder_url_validation(self):
        """Test that folder URLs must end with /"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/job123",  # No trailing /
            mock_url="syft://test@example.com/public/job123",
            syftobject="syft://test@example.com/public/job123.syftobject.yaml",
            object_type="folder"
        )
        # After validation, should add trailing /
        assert obj.private_url == "syft://test@example.com/private/job123/"
        assert obj.mock_url == "syft://test@example.com/public/job123/"
    
    def test_file_url_validation(self):
        """Test that file URLs cannot end with /"""
        with pytest.raises(ValueError, match="File URLs cannot end with /"):
            SyftObject(
                private_url="syft://test@example.com/private/test.txt/",
                mock_url="syft://test@example.com/public/test.txt/",
                syftobject="syft://test@example.com/public/test.syftobject.yaml",
                object_type="file"
            )
    
    def test_folder_file_parameter_conflict(self, temp_folder):
        """Test that mixing folder and file params raises error"""
        with pytest.raises(ValueError, match="Cannot mix folder and file parameters"):
            create_object(
                name="test",
                private_folder=str(temp_folder),
                mock_file="some_file.txt"
            )
    
    def test_folder_accessor_functionality(self, temp_folder):
        """Test FolderAccessor methods"""
        accessor = FolderAccessor(temp_folder)
        
        # Test exists
        assert accessor.exists()
        
        # Test list_files
        files = accessor.list_files()
        file_names = [f.name for f in files]
        assert "run.sh" in file_names
        assert "data.csv" in file_names
        assert "config.json" in file_names
        assert "logs" not in file_names  # Should not include directories
        
        # Test list_all_files (recursive)
        all_files = accessor.list_all_files()
        all_file_names = [f.name for f in all_files]
        assert "output.log" in all_file_names
        
        # Test get_file
        config_file = accessor.get_file("config.json")
        assert config_file.exists()
        assert "timeout" in config_file.read_text()
        
        # Test read_file
        data = accessor.read_file("data.csv")
        assert "id,value" in data
        
        # Test size
        total_size = accessor.size()
        assert total_size > 0
        
        # Test file not found
        with pytest.raises(FileNotFoundError):
            accessor.get_file("nonexistent.txt")
    
    def test_data_accessor_returns_folder_accessor(self, temp_folder):
        """Test that DataAccessor returns FolderAccessor for folders"""
        obj = create_object(
            name="test_job",
            private_folder=str(temp_folder)
        )
        
        # Access through DataAccessor
        private_accessor = obj.private.obj
        assert isinstance(private_accessor, FolderAccessor)
        
        mock_accessor = obj.mock.obj
        assert isinstance(mock_accessor, FolderAccessor)
    
    def test_auto_mock_folder_generation(self, temp_folder):
        """Test automatic mock folder generation from private"""
        obj = create_object(
            name="auto_mock_test",
            private_folder=str(temp_folder)
        )
        
        # Mock folder should be auto-generated
        mock_accessor = obj.mock.obj
        assert isinstance(mock_accessor, FolderAccessor)
        
        # Check mock files were created
        mock_files = mock_accessor.list_files()
        mock_file_names = [f.name for f in mock_files]
        assert "run.sh" in mock_file_names
        assert "data.csv" in mock_file_names
        
        # Check mock content
        mock_csv = mock_accessor.read_file("data.csv")
        assert "col1,col2,col3" in mock_csv  # Should have mock data
        assert "100" not in mock_csv  # Should not have real data
    
    def test_folder_with_both_mock_and_private(self, temp_folder):
        """Test creating folder with explicit mock and private"""
        # Create mock folder
        mock_folder = temp_folder.parent / "mock_folder"
        mock_folder.mkdir()
        (mock_folder / "data.csv").write_text("id,value\n1,MOCK\n2,MOCK")
        
        try:
            obj = create_object(
                name="both_folders",
                private_folder=str(temp_folder),
                mock_folder=str(mock_folder)
            )
            
            # Check both accessors work
            private_data = obj.private.obj.read_file("data.csv")
            assert "100" in private_data
            
            mock_data = obj.mock.obj.read_file("data.csv")
            assert "MOCK" in mock_data
            assert "100" not in mock_data
        finally:
            if mock_folder.exists():
                shutil.rmtree(mock_folder)
    
    def test_folder_object_serialization(self, temp_folder):
        """Test saving and loading folder objects"""
        obj = create_object(
            name="serialization_test",
            private_folder=str(temp_folder),
            metadata={"job_type": "analysis"}
        )
        
        # Save to YAML
        yaml_path = temp_folder.parent / "test.syftobject.yaml"
        obj.save_yaml(yaml_path, create_syftbox_permissions=False)
        
        # Load from YAML
        loaded = SyftObject.load_yaml(yaml_path)
        assert loaded.object_type == "folder"
        assert loaded.is_folder
        assert loaded.name == "serialization_test"
        assert loaded.metadata["job_type"] == "analysis"
    
    def test_folder_extension_validation_skipped(self):
        """Test that extension validation is skipped for folders"""
        # This should not raise an error even though URLs don't have extensions
        obj = SyftObject(
            private_url="syft://test@example.com/private/job123/",
            mock_url="syft://test@example.com/public/job456/",
            syftobject="syft://test@example.com/public/job.syftobject.yaml",
            object_type="folder"
        )
        assert obj.file_type == ""  # Folders have no file type
    
    def test_nonexistent_folder_error(self):
        """Test error when folder doesn't exist"""
        with pytest.raises(ValueError, match="Private folder not found"):
            create_object(
                name="test",
                private_folder="/nonexistent/folder"
            )
    
    def test_empty_folder_handling(self, temp_dir):
        """Test handling of empty folders"""
        empty_folder = temp_dir / "empty"
        empty_folder.mkdir()
        
        obj = create_object(
            name="empty_test",
            private_folder=str(empty_folder)
        )
        
        accessor = obj.private.obj
        assert accessor.exists()
        assert len(accessor.list_files()) == 0
        assert accessor.size() == 0