"""Tests for syft_objects.collections module"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime
from uuid import uuid4

from syft_objects.collections import ObjectsCollection
from syft_objects.models import SyftObject


class TestObjectsCollection:
    """Test ObjectsCollection class"""
    
    def test_init_empty(self):
        """Test ObjectsCollection initialization without objects"""
        collection = ObjectsCollection()
        assert collection._objects == []
        assert collection._search_info is None
        assert collection._cached is False
        assert collection._server_ready is False
    
    def test_init_with_objects(self):
        """Test ObjectsCollection initialization with objects"""
        objects = [Mock(), Mock()]
        search_info = "Search results"
        collection = ObjectsCollection(objects=objects, search_info=search_info)
        
        assert collection._objects == objects
        assert collection._search_info == search_info
        assert collection._cached is True
        assert collection._server_ready is False
    
    @patch('syft_objects.auto_install.ensure_syftbox_app_installed')
    @patch('syft_objects.auto_install.ensure_server_healthy')
    def test_ensure_server_ready_success(self, mock_healthy, mock_install):
        """Test _ensure_server_ready when server is healthy"""
        mock_healthy.return_value = True
        
        collection = ObjectsCollection()
        collection._ensure_server_ready()
        
        mock_install.assert_called_once_with(silent=True)
        mock_healthy.assert_called_once()
        assert collection._server_ready is True
    
    @patch('syft_objects.auto_install.ensure_syftbox_app_installed')
    @patch('syft_objects.auto_install.ensure_server_healthy')
    @patch('builtins.print')
    def test_ensure_server_ready_unhealthy(self, mock_print, mock_healthy, mock_install):
        """Test _ensure_server_ready when server is not healthy"""
        mock_healthy.return_value = False
        
        collection = ObjectsCollection()
        collection._ensure_server_ready()
        
        mock_install.assert_called_once_with(silent=True)
        mock_healthy.assert_called_once()
        assert collection._server_ready is False
        mock_print.assert_called_with("⚠️  Server not available - some features may not work")
    
    @patch('syft_objects.auto_install.ensure_syftbox_app_installed')
    @patch('builtins.print')
    def test_ensure_server_ready_exception(self, mock_print, mock_install):
        """Test _ensure_server_ready with exception"""
        mock_install.side_effect = Exception("Install failed")
        
        collection = ObjectsCollection()
        collection._ensure_server_ready()
        
        assert collection._server_ready is False
        mock_print.assert_called()
        assert "Could not check server status" in str(mock_print.call_args)
    
    def test_get_object_email(self):
        """Test _get_object_email extraction"""
        collection = ObjectsCollection()
        
        # Test valid syft URL
        mock_obj = Mock()
        mock_obj.private_url = "syft://test@example.com/private/objects/test.txt"
        email = collection._get_object_email(mock_obj)
        assert email == "test@example.com"
        
        # Test invalid URL format
        mock_obj.private_url = "invalid://url"
        email = collection._get_object_email(mock_obj)
        assert email == "unknown@example.com"
        
        # Test exception handling
        mock_obj.private_url = Mock(side_effect=Exception("Error"))
        email = collection._get_object_email(mock_obj)
        assert email == "unknown@example.com"
    
    @patch('syft_objects.collections.SYFTBOX_AVAILABLE', False)
    def test_load_objects_syftbox_not_available(self):
        """Test _load_objects when SyftBox not available"""
        collection = ObjectsCollection()
        collection._load_objects()
        assert collection._objects == []
    
    @patch('syft_objects.collections.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.collections.get_syftbox_client')
    def test_load_objects_no_client(self, mock_get_client):
        """Test _load_objects when client is None"""
        mock_get_client.return_value = None
        
        collection = ObjectsCollection()
        collection._load_objects()
        assert collection._objects == []
    
    @patch('syft_objects.collections.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.collections.get_syftbox_client')
    def test_load_objects_success(self, mock_get_client, temp_dir, sample_yaml_content):
        """Test _load_objects successful loading"""
        # Setup mock client
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        mock_get_client.return_value = mock_client
        
        # Create test structure
        datasites_dir = temp_dir / "datasites"
        datasites_dir.mkdir()
        
        # Create datasite for test@example.com
        test_datasite = datasites_dir / "test@example.com"
        test_datasite.mkdir()
        
        # Create public objects directory
        public_objects = test_datasite / "public" / "objects"
        public_objects.mkdir(parents=True)
        
        # Create private objects directory
        private_objects = test_datasite / "private" / "objects"
        private_objects.mkdir(parents=True)
        
        # Create test objects
        public_obj_file = public_objects / "public_test.syftobject.yaml"
        public_obj_file.write_text(sample_yaml_content)
        
        private_obj_file = private_objects / "private_test.syftobject.yaml"
        modified_content = sample_yaml_content.replace("test_object", "private_object")
        private_obj_file.write_text(modified_content)
        
        # Create non-syftobject files (should be ignored)
        (public_objects / "other.yaml").write_text("not a syft object")
        (private_objects / "data.txt").write_text("some data")
        
        collection = ObjectsCollection()
        collection._load_objects()
        
        assert len(collection._objects) == 2
        names = [obj.name for obj in collection._objects]
        assert "test_object" in names
        assert "private_object" in names
    
    @patch('syft_objects.collections.SYFTBOX_AVAILABLE', True)
    @patch('syft_objects.collections.get_syftbox_client')
    def test_load_objects_with_errors(self, mock_get_client, temp_dir):
        """Test _load_objects with loading errors"""
        # Setup mock client
        mock_client = Mock()
        mock_client.datasites = temp_dir / "datasites"
        mock_get_client.return_value = mock_client
        
        # Create test structure
        datasites_dir = temp_dir / "datasites"
        datasites_dir.mkdir()
        test_datasite = datasites_dir / "test@example.com"
        test_datasite.mkdir()
        public_objects = test_datasite / "public" / "objects"
        public_objects.mkdir(parents=True)
        
        # Create invalid syftobject file
        invalid_obj = public_objects / "invalid.syftobject.yaml"
        invalid_obj.write_text("invalid: yaml: [")
        
        collection = ObjectsCollection()
        collection._load_objects()
        
        # Should handle error gracefully
        assert collection._objects == []
    
    def test_refresh(self):
        """Test refresh method"""
        collection = ObjectsCollection()
        
        with patch.object(collection, '_load_objects') as mock_load:
            result = collection.refresh()
            
            mock_load.assert_called_once()
            assert result == collection
    
    def test_ensure_loaded(self):
        """Test _ensure_loaded method"""
        collection = ObjectsCollection()
        
        # Test when not cached
        with patch.object(collection, '_load_objects') as mock_load:
            collection._cached = False
            collection._ensure_loaded()
            mock_load.assert_called_once()
        
        # Test when cached
        with patch.object(collection, '_load_objects') as mock_load:
            collection._cached = True
            collection._ensure_loaded()
            mock_load.assert_not_called()
    
    def test_search(self):
        """Test search method"""
        # Create test objects
        obj1 = Mock()
        obj1.name = "Unique Object One"
        obj1.description = "Description one"
        obj1.created_at = datetime.now()
        obj1.updated_at = datetime.now()
        obj1.metadata = {"key": "value"}
        
        obj2 = Mock()
        obj2.name = "Another Object"
        obj2.description = "Second description"
        obj2.created_at = datetime.now()
        obj2.updated_at = datetime.now()
        obj2.metadata = {"type": "data"}
        
        collection = ObjectsCollection()
        collection._objects = [obj1, obj2]
        collection._cached = True
        
        with patch.object(collection, '_get_object_email', return_value="test@example.com"):
            # Search by name
            result = collection.search("Unique")
            assert len(result._objects) == 1
            assert result._objects[0] == obj1
            assert "Search results for 'unique'" in result._search_info
            
            # Search by description
            result = collection.search("description")
            assert len(result._objects) == 2
            
            # Search by metadata
            result = collection.search("value")
            assert len(result._objects) == 1
            assert result._objects[0] == obj1
            
            # Search with no results
            result = collection.search("nonexistent")
            assert len(result._objects) == 0
    
    def test_search_special_term(self):
        """Test search with special debug term"""
        obj1 = Mock()
        obj1.name = "Test Object"
        obj1.description = ""
        obj1.created_at = None
        obj1.updated_at = None
        obj1.metadata = {}
        
        collection = ObjectsCollection()
        collection._objects = [obj1]
        collection._cached = True
        
        with patch.object(collection, '_get_object_email', return_value="test@example.com"):
            with patch('builtins.print') as mock_print:
                result = collection.search("xyz123notfound")
                
                assert len(result._objects) == 0
                mock_print.assert_any_call("DEBUG: Testing object Test Object - no matches expected")
    
    def test_filter_by_email(self):
        """Test filter_by_email method"""
        obj1 = Mock()
        obj2 = Mock()
        obj3 = Mock()
        
        collection = ObjectsCollection()
        collection._objects = [obj1, obj2, obj3]
        collection._cached = True
        
        def mock_get_email(obj):
            if obj == obj1:
                return "test@example.com"
            elif obj == obj2:
                return "admin@example.com"
            else:
                return "test@demo.com"
        
        with patch.object(collection, '_get_object_email', side_effect=mock_get_email):
            # Filter by partial email
            result = collection.filter_by_email("test")
            assert len(result._objects) == 2
            assert obj1 in result._objects
            assert obj3 in result._objects
            assert "Filtered by email containing 'test'" in result._search_info
            
            # Filter with no matches
            result = collection.filter_by_email("nonexistent")
            assert len(result._objects) == 0
    
    def test_list_unique_emails(self):
        """Test list_unique_emails method"""
        obj1 = Mock()
        obj2 = Mock()
        obj3 = Mock()
        
        collection = ObjectsCollection()
        collection._objects = [obj1, obj2, obj3]
        collection._cached = True
        
        emails = ["test@example.com", "admin@example.com", "test@example.com"]
        with patch.object(collection, '_get_object_email', side_effect=emails):
            result = collection.list_unique_emails()
            
            assert result == ["admin@example.com", "test@example.com"]  # Sorted and unique
    
    def test_list_unique_names(self):
        """Test list_unique_names method"""
        obj1 = Mock()
        obj1.name = "Object One"
        obj2 = Mock()
        obj2.name = "Object Two"
        obj3 = Mock()
        obj3.name = "Object One"  # Duplicate
        obj4 = Mock()
        obj4.name = None  # No name
        
        collection = ObjectsCollection()
        collection._objects = [obj1, obj2, obj3, obj4]
        collection._cached = True
        
        result = collection.list_unique_names()
        assert result == ["Object One", "Object Two"]  # Sorted and unique, None excluded
    
    def test_to_list(self):
        """Test to_list method"""
        objects = [Mock(), Mock()]
        
        # Test with cached collection
        collection = ObjectsCollection(objects=objects)
        result = collection.to_list()
        assert result == objects
        
        # Test with non-cached collection
        collection = ObjectsCollection()
        collection._cached = False
        with patch.object(collection, '_ensure_loaded'):
            result = collection.to_list()
            assert result == []
    
    def test_get_by_indices(self):
        """Test get_by_indices method"""
        obj1 = Mock()
        obj2 = Mock()
        obj3 = Mock()
        
        collection = ObjectsCollection()
        collection._objects = [obj1, obj2, obj3]
        collection._cached = True
        
        # Valid indices
        result = collection.get_by_indices([0, 2])
        assert result == [obj1, obj3]
        
        # Out of range indices are filtered
        result = collection.get_by_indices([1, 5, -1])
        assert result == [obj2]
    
    def test_getitem_integer(self):
        """Test __getitem__ with integer index"""
        obj1 = Mock()
        obj2 = Mock()
        
        collection = ObjectsCollection()
        collection._objects = [obj1, obj2]
        collection._cached = True
        
        assert collection[0] == obj1
        assert collection[1] == obj2
        assert collection[-1] == obj2
    
    def test_getitem_slice(self):
        """Test __getitem__ with slice"""
        objects = [Mock() for _ in range(5)]
        
        collection = ObjectsCollection(objects=objects, search_info="Original")
        
        # Test slice
        result = collection[:3]
        assert isinstance(result, ObjectsCollection)
        assert len(result._objects) == 3
        assert result._search_info == "Original (slice slice(None, 3, None))"
    
    def test_getitem_string_uid(self):
        """Test __getitem__ with string UID"""
        uid1 = str(uuid4())
        uid2 = str(uuid4())
        
        obj1 = Mock(uid=uid1)
        obj2 = Mock(uid=uid2)
        
        collection = ObjectsCollection()
        collection._objects = [obj1, obj2]
        collection._cached = True
        
        # Valid UID
        result = collection[uid1]
        assert result == obj1
        
        # Invalid UID
        with pytest.raises(KeyError, match="Object with UID .* not found"):
            collection["invalid-uid"]
    
    def test_len(self):
        """Test __len__ method"""
        objects = [Mock(), Mock(), Mock()]
        
        # Cached collection
        collection = ObjectsCollection(objects=objects)
        assert len(collection) == 3
        
        # Non-cached collection
        collection = ObjectsCollection()
        collection._cached = False
        with patch.object(collection, '_ensure_loaded'):
            collection._objects = objects
            assert len(collection) == 3
    
    def test_iter(self):
        """Test __iter__ method"""
        objects = [Mock(), Mock()]
        
        collection = ObjectsCollection(objects=objects)
        result = list(collection)
        assert result == objects
    
    def test_str_with_tabulate(self):
        """Test __str__ with tabulate available"""
        obj1 = Mock()
        obj1.name = "Object One"
        obj1.private_url = "syft://test@example.com/private/obj1.txt"
        obj1.mock_url = "syft://test@example.com/public/obj1.txt"
        
        collection = ObjectsCollection([obj1])
        
        with patch.object(collection, '_get_object_email', return_value="test@example.com"):
            result = str(collection)
            
            assert "Object One" in result
            assert "test@example.com" in result
            assert "Private URL" in result
            assert "Mock URL" in result
    
    def test_str_without_tabulate(self):
        """Test __str__ without tabulate"""
        obj1 = Mock()
        obj1.name = "Object One"
        
        collection = ObjectsCollection([obj1])
        
        with patch.object(collection, '_get_object_email', return_value="test@example.com"):
            with patch('builtins.__import__', side_effect=ImportError("No tabulate")):
                result = str(collection)
                
                assert "Available Syft Objects:" in result
                assert "0: Object One (test@example.com)" in result
    
    def test_str_empty(self):
        """Test __str__ with empty collection"""
        collection = ObjectsCollection()
        result = str(collection)
        assert result == "No syft objects available"
    
    def test_repr(self):
        """Test __repr__ method"""
        collection = ObjectsCollection()
        with patch.object(collection, '__str__', return_value="test string"):
            assert repr(collection) == "test string"
    
    def test_help(self):
        """Test help method"""
        collection = ObjectsCollection()
        
        with patch('builtins.print') as mock_print:
            collection.help()
            
            mock_print.assert_called_once()
            help_text = mock_print.call_args[0][0]
            
            assert "Syft Objects Collection Help" in help_text
            assert "import syft_objects as syo" in help_text
            assert "so.objects.search" in help_text
            assert "so.objects.refresh()" in help_text
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch.object(ObjectsCollection, '_ensure_server_ready')
    @patch.object(ObjectsCollection, 'widget')
    def test_repr_html(self, mock_widget, mock_ensure, mock_health_check):
        """Test _repr_html_ method with server available"""
        mock_widget.return_value = "<iframe>test</iframe>"
        mock_health_check.return_value = True  # Server is healthy
        
        collection = ObjectsCollection()
        result = collection._repr_html_()
        
        mock_ensure.assert_called_once()
        mock_widget.assert_called_once()
        assert result == "<iframe>test</iframe>"
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch.object(ObjectsCollection, '_ensure_server_ready')
    @patch.object(ObjectsCollection, '_generate_fallback_widget')
    def test_repr_html_fallback(self, mock_fallback, mock_ensure, mock_health_check):
        """Test _repr_html_ method with server unavailable"""
        mock_fallback.return_value = "<div>fallback widget</div>"
        mock_health_check.return_value = False  # Server is not healthy
        
        collection = ObjectsCollection()
        result = collection._repr_html_()
        
        mock_ensure.assert_called_once()
        mock_fallback.assert_called_once()
        assert result == "<div>fallback widget</div>"
    
    @patch('syft_objects.collections.get_syft_objects_url')
    @patch.object(ObjectsCollection, '_ensure_server_ready')
    def test_widget(self, mock_ensure, mock_get_url):
        """Test widget method"""
        mock_get_url.return_value = "http://localhost:8004/widget"
        
        collection = ObjectsCollection()
        
        # Default parameters
        result = collection.widget()
        mock_ensure.assert_called_once()
        mock_get_url.assert_called_once_with("widget")
        
        assert '<iframe' in result
        assert 'src="http://localhost:8004/widget"' in result
        assert 'width="100%"' in result
        assert 'height="400px"' in result
        
        # Custom parameters
        result = collection.widget(width="800px", height="400px", url="http://custom.url")
        assert 'src="http://custom.url"' in result
        assert 'width="800px"' in result
        assert 'height="400px"' in result
    
    def test_generate_interactive_table_html(self):
        """Test _generate_interactive_table_html method"""
        obj1 = Mock()
        obj1.name = "Test Object"
        obj1.description = "Test description"
        obj1.private_url = "syft://test@example.com/private/test.txt"
        obj1.mock_url = "syft://test@example.com/public/test.txt"
        obj1.created_at = datetime.now()
        obj1.updated_at = datetime.now()
        obj1.metadata = {"key": "value"}
        
        collection = ObjectsCollection([obj1])
        
        with patch.object(collection, '_get_object_email', return_value="test@example.com"):
            html = collection._generate_interactive_table_html(
                title="Test Title",
                count=1,
                search_indicator="",
                container_id="test-container"
            )
            
            # Check structure
            assert '<style>' in html
            assert 'syft-objects-container' in html
            assert 'Test Title' in html
            assert '(1 total)' in html
            assert 'Test Object' in html
            assert 'test@example.com' in html
            assert 'Test description' in html
            
            # Check JavaScript functions
            assert 'filterSyftObjects' in html
            assert 'selectAllSyftObjects' in html
            assert 'generateSyftObjectsCode' in html

    def test_load_objects_exception_handling(self):
        """Test exception handling in _load_objects"""
        # Test datasites.iterdir() exception (line 68-69)
        mock_client = Mock()
        mock_client.datasites.iterdir.side_effect = Exception("Directory error")
        
        with patch('syft_objects.collections.get_syftbox_client', return_value=mock_client):
            with patch('syft_objects.collections.SYFTBOX_AVAILABLE', True):
                collection = ObjectsCollection()
                collection._load_objects()  # Should handle exception gracefully
                assert collection._objects == []

    def test_load_objects_syftobject_load_exception(self):
        """Test exception handling when loading individual SyftObject files (lines 90-91)"""
        mock_client = Mock()
        mock_datasite = Mock()
        mock_datasite.name = "test@example.com"
        mock_client.datasites.iterdir.return_value = [mock_datasite]
        
        # Create a real path structure that will trigger the exception on the right lines
        from pathlib import Path
        from tempfile import TemporaryDirectory
        
        with TemporaryDirectory() as temp_dir:
            # Create the full directory structure
            email_dir = Path(temp_dir) / "test@example.com"
            
            # Create BOTH public and private directories to hit both exception paths
            public_dir = email_dir / "public" / "objects"
            public_dir.mkdir(parents=True)
            private_dir = email_dir / "private" / "objects"
            private_dir.mkdir(parents=True)
            
            # Create YAML files that will exist
            public_yaml = public_dir / "test_public.syftobject.yaml"
            public_yaml.write_text("invalid: yaml: content")
            private_yaml = private_dir / "test_private.syftobject.yaml"
            private_yaml.write_text("invalid: yaml: content")
            
            # Mock the client to return our temp directory as datasites
            mock_client.datasites = Path(temp_dir)
            
            with patch('syft_objects.collections.get_syftbox_client', return_value=mock_client):
                with patch('syft_objects.collections.SYFTBOX_AVAILABLE', True):
                    # Mock SyftObject.load_yaml to raise an exception - this should hit lines 80 and 90
                    with patch('syft_objects.models.SyftObject.load_yaml', side_effect=Exception("YAML load failed")):
                        collection = ObjectsCollection()
                        collection._load_objects()  # Should continue despite YAML load errors
                        # Objects list should be empty due to exceptions - both exceptions get caught

    def test_load_objects_directory_exception(self):
        """Test exception handling for directory access (lines 93-94)"""
        mock_client = Mock()
        mock_datasite = Mock()
        mock_datasite.name = "test@example.com"
        mock_client.datasites.iterdir.return_value = [mock_datasite]
        
        with patch('syft_objects.collections.get_syftbox_client', return_value=mock_client):
            with patch('syft_objects.collections.SYFTBOX_AVAILABLE', True):
                with patch('pathlib.Path.__truediv__', side_effect=Exception("Path error")):
                    collection = ObjectsCollection()
                    collection._load_objects()  # Should continue despite path errors

    def test_load_objects_general_exception(self):
        """Test general exception handling (lines 96-97)"""
        with patch('syft_objects.collections.get_syftbox_client', side_effect=Exception("Client error")):
            collection = ObjectsCollection()
            collection._load_objects()  # Should handle any general exception
            assert collection._objects == []

    def test_iter_ensures_loaded(self):
        """Test __iter__ calls _ensure_loaded when not cached (line 202)"""
        collection = ObjectsCollection()
        collection._cached = False
        collection._objects = []  # Prevent actual loading
        
        with patch.object(collection, '_ensure_loaded') as mock_ensure:
            list(collection)  # Force iteration
            mock_ensure.assert_called()

    def test_type_checking_import(self):
        """Test TYPE_CHECKING import (line 6)"""
        import typing
        from syft_objects import collections
        
        # Force TYPE_CHECKING to be True to trigger the import
        original_value = typing.TYPE_CHECKING
        try:
            typing.TYPE_CHECKING = True
            import importlib
            importlib.reload(collections)
        finally:
            typing.TYPE_CHECKING = original_value
        
        # Verify module still works
        assert hasattr(collections, 'ObjectsCollection')