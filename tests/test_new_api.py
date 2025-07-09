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
        
        # Test get_permissions returns dict
        perms = obj.get_permissions()
        assert isinstance(perms, dict)
        assert "mock" in perms
        assert "private" in perms
        assert "syftobject" in perms
        
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
        
        obj.update_metadata({"key2": "value2"})
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
    
    def test_both_apis_work(self):
        """Test that both old property access and new getter methods work"""
        obj = create_object(
            name="Test Object",
            metadata={"description": "Test Description"},
            private_contents="Private data",
            mock_contents="Mock data"
        )
        
        # Test that both APIs return the same values
        assert obj.name == obj.get_name()
        assert obj.description == obj.get_description()
        assert str(obj.uid) == obj.get_uid()
        
        # Test setters update the properties
        obj.set_name("New Name")
        assert obj.name == "New Name"
        assert obj.get_name() == "New Name"
        
        obj.set_description("New Description")
        assert obj.description == "New Description"
        assert obj.get_description() == "New Description"
    
    def test_dir_shows_both_apis(self):
        """Test that dir() shows both old and new API"""
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
        
        # Check old API properties are also visible
        assert "name" in attrs
        assert "uid" in attrs
        assert "private_url" in attrs
        assert "mock_url" in attrs