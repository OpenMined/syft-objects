"""Tests for the new SyftObject API"""

import pytest
from syft_objects import create_object


class TestNewAPI:
    """Test the new getter/setter API for SyftObject"""
    
    def test_getter_methods(self):
        """Test all getter methods work correctly"""
        obj = create_object(
            name="Test Object",
            metadata={"description": "Test Description"},
            private_contents="Private data",
            mock_contents="Mock data"
        )
        
        # Test getters
        assert obj.get_name() == "Test Object"
        assert obj.get_description() == "Test Description"
        assert isinstance(obj.get_uid(), str)
        assert obj.get_uid() != ""
        assert obj.get_file_type() == "txt"
        
        # Test get_info returns dict
        info = obj.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Test Object"
        assert info["description"] == "Test Description"
        
        # Test explicit permission getters
        read_perms = obj.get_read_permissions()
        write_perms = obj.get_write_permissions()
        admin_perms = obj.get_admin_permissions()
        assert isinstance(read_perms, list)
        assert isinstance(write_perms, list)
        assert isinstance(admin_perms, list)
        
        # Test get_urls returns dict
        urls = obj.get_urls()
        assert isinstance(urls, dict)
        assert "mock" in urls
        assert "private" in urls
        assert "syftobject" in urls
    
    def test_setter_methods(self):
        """Test all setter methods work correctly"""
        obj = create_object(
            name="Original Name",
            metadata={"description": "Original Description"},
            private_contents="Private data",
            mock_contents="Mock data"
        )
        
        # Test setters
        obj.set_name("New Name")
        assert obj.get_name() == "New Name"
        
        obj.set_description("New Description")
        assert obj.get_description() == "New Description"
        
        # Test metadata setters
        obj.set_metadata({"key": "value"})
        assert obj.get_metadata() == {"key": "value"}
        
        # Test merging metadata manually
        current = obj.get_metadata()
        current.update({"key2": "value2"})
        obj.set_metadata(current)
        metadata = obj.get_metadata()
        assert metadata["key"] == "value"
        assert metadata["key2"] == "value2"
    
    def test_accessor_objects(self):
        """Test accessor objects work correctly"""
        obj = create_object(
            name="Test Object",
            private_contents="Private data",
            mock_contents="Mock data"
        )
        
        # Test mock accessor
        assert hasattr(obj, "mock")
        mock_url = obj.mock.get_url()
        assert mock_url.startswith("syft://")
        assert "public" in mock_url
        
        # Test private accessor
        assert hasattr(obj, "private")
        private_url = obj.private.get_url()
        assert private_url.startswith("syft://")
        assert "private" in private_url
        
        # Test syftobject_config accessor
        assert hasattr(obj, "syftobject_config")
        config_url = obj.syftobject_config.get_url()
        assert config_url.startswith("syft://")
        assert ".syftobject.yaml" in config_url
    
    def test_new_api_consistency(self):
        """Test that the new API getter/setter methods work consistently"""
        obj = create_object(
            name="Test Object",
            metadata={"description": "Test Description"},
            private_contents="Private data",
            mock_contents="Mock data"
        )
        
        # Test initial values
        assert obj.get_name() == "Test Object"
        assert obj.get_description() == "Test Description"
        assert isinstance(obj.get_uid(), str)
        
        # Test setters update the values
        obj.set_name("New Name")
        assert obj.get_name() == "New Name"
        
        obj.set_description("New Description")
        assert obj.get_description() == "New Description"
    
    def test_dir_shows_new_api(self):
        """Test that dir() shows the new API methods"""
        obj = create_object(
            name="Test Object",
            private_contents="Private data",
            mock_contents="Mock data"
        )
        
        attrs = dir(obj)
        
        # Check new API methods are visible
        assert "get_name" in attrs
        assert "get_uid" in attrs
        assert "set_name" in attrs
        assert "mock" in attrs
        assert "private" in attrs
        assert "syftobject_config" in attrs
        assert "delete_obj" in attrs
        
        # Check new permission methods are visible
        assert "get_read_permissions" in attrs
        assert "get_write_permissions" in attrs
        assert "get_admin_permissions" in attrs
        assert "set_read_permissions" in attrs
        assert "set_write_permissions" in attrs
        assert "set_admin_permissions" in attrs