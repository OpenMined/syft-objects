"""Test file-backed SyftObject functionality"""

import pytest
from pathlib import Path
from uuid import UUID
import yaml
import time

from syft_objects.models import SyftObject


class TestFileBacked:
    """Test file-backed storage functionality"""
    
    def test_create_file_backed_object(self, temp_dir):
        """Test creating a file-backed SyftObject"""
        # Create initial data
        obj_data = {
            "uid": "12345678-1234-5678-1234-567812345678",
            "private_url": "syft://test@example.com/private/objects/test.txt",
            "mock_url": "syft://test@example.com/public/objects/test_mock.txt", 
            "syftobject": "syft://test@example.com/public/objects/test.syftobject.yaml",
            "name": "Test Object",
            "description": "A test object",
            "metadata": {"key": "value"}
        }
        
        # Save to YAML
        yaml_path = temp_dir / "test.syftobject.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(obj_data, f)
        
        # Create file-backed object
        obj = SyftObject.from_yaml(yaml_path)
        
        # Verify attributes
        assert str(obj.uid) == "12345678-1234-5678-1234-567812345678"
        assert obj.name == "Test Object"
        assert obj.description == "A test object"
        assert obj.metadata == {"key": "value"}
        assert obj._yaml_path == yaml_path
    
    def test_attribute_sync_to_disk(self, temp_dir):
        """Test that attribute changes sync to disk"""
        # Create initial object
        yaml_path = temp_dir / "test.syftobject.yaml"
        obj = SyftObject(
            uid="12345678-1234-5678-1234-567812345678",
            private_url="syft://test@example.com/private/objects/test.txt",
            mock_url="syft://test@example.com/public/objects/test_mock.txt",
            syftobject="syft://test@example.com/public/objects/test.syftobject.yaml",
            name="Initial Name",
            _yaml_path=yaml_path
        )
        
        # Change attribute
        obj.name = "Updated Name"
        obj.description = "New description"
        # For metadata, we need to reassign the whole dict to trigger sync
        new_metadata = obj.metadata.copy()
        new_metadata["new_key"] = "new_value"
        obj.metadata = new_metadata
        
        # Read yaml file directly
        with open(yaml_path, 'r') as f:
            disk_data = yaml.safe_load(f)
        
        # Verify changes persisted
        assert disk_data["name"] == "Updated Name" 
        assert disk_data["description"] == "New description"
        assert disk_data["metadata"]["new_key"] == "new_value"
    
    def test_refresh_from_disk(self, temp_dir):
        """Test refreshing attributes from disk"""
        # Create initial object
        yaml_path = temp_dir / "test.syftobject.yaml"
        obj = SyftObject(
            uid="12345678-1234-5678-1234-567812345678",
            private_url="syft://test@example.com/private/objects/test.txt",
            mock_url="syft://test@example.com/public/objects/test_mock.txt",
            syftobject="syft://test@example.com/public/objects/test.syftobject.yaml",
            name="Initial Name",
            _yaml_path=yaml_path
        )
        
        # Modify yaml file directly
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        data["name"] = "Externally Modified"
        data["metadata"] = {"external": "change"}
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f)
        
        # Refresh object
        obj.refresh()
        
        # Verify object updated
        assert obj.name == "Externally Modified"
        assert obj.metadata == {"external": "change"}
    
    def test_no_caching(self, temp_dir):
        """Test that there's no caching - each read goes to disk"""
        yaml_path = temp_dir / "test.syftobject.yaml"
        
        # Create two objects pointing to same file
        obj1 = SyftObject(
            uid="12345678-1234-5678-1234-567812345678",
            private_url="syft://test@example.com/private/objects/test.txt",
            mock_url="syft://test@example.com/public/objects/test_mock.txt",
            syftobject="syft://test@example.com/public/objects/test.syftobject.yaml",
            name="Object 1",
            _yaml_path=yaml_path
        )
        
        # Load second object from same file
        obj2 = SyftObject.from_yaml(yaml_path)
        
        # Change in obj1
        obj1.name = "Changed by obj1"
        
        # Obj2 should see the change after refresh
        obj2.refresh()
        assert obj2.name == "Changed by obj1"
    
    def test_save_yaml_updates_path(self, temp_dir):
        """Test that save_yaml updates the internal yaml path"""
        # Create object without yaml path
        obj = SyftObject(
            uid="12345678-1234-5678-1234-567812345678",
            private_url="syft://test@example.com/private/objects/test.txt",
            mock_url="syft://test@example.com/public/objects/test_mock.txt",
            syftobject="syft://test@example.com/public/objects/test.syftobject.yaml",
            name="Test"
        )
        
        # Initially no yaml path
        assert obj._yaml_path is None
        
        # Save to file
        yaml_path = temp_dir / "saved.syftobject.yaml"
        obj.save_yaml(yaml_path, create_syftbox_permissions=False)
        
        # Now has yaml path
        assert obj._yaml_path == yaml_path
        
        # Changes should sync
        obj.name = "Updated after save"
        
        # Verify on disk
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        assert data["name"] == "Updated after save"
    
    def test_permission_updates_sync(self, temp_dir):
        """Test that permission updates sync to disk"""
        yaml_path = temp_dir / "test.syftobject.yaml"
        obj = SyftObject(
            uid="12345678-1234-5678-1234-567812345678",
            private_url="syft://test@example.com/private/objects/test.txt",
            mock_url="syft://test@example.com/public/objects/test_mock.txt",
            syftobject="syft://test@example.com/public/objects/test.syftobject.yaml",
            name="Test",
            _yaml_path=yaml_path
        )
        
        # Update permissions
        obj.mock_permissions = ["user1@example.com", "user2@example.com"]
        obj.private_permissions = ["owner@example.com"]
        
        # Read from disk
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        assert data["mock_permissions"] == ["user1@example.com", "user2@example.com"]
        assert data["private_permissions"] == ["owner@example.com"]