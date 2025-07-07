"""Tests for backend.fast_main module"""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from uuid import uuid4
import json

from fastapi.testclient import TestClient
from backend.fast_main import app


class TestFastAPIEndpoints:
    """Test FastAPI endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    @patch('backend.fast_main.SYFTBOX_AVAILABLE', False)
    def test_status_syftbox_not_available(self, client):
        """Test /api/status when SyftBox not available"""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        
        assert data["app"] == "Syft Objects UI"
        assert data["syftbox"]["status"] == "not_available"
        assert data["components"]["backend"] == "running"
    
    @patch('backend.fast_main.SYFTBOX_AVAILABLE', True)
    @patch('backend.fast_main.get_syftbox_client')
    def test_status_syftbox_connected(self, mock_get_client, client):
        """Test /api/status when SyftBox connected"""
        mock_syftbox = Mock()
        mock_syftbox.email = "test@example.com"
        mock_get_client.return_value = mock_syftbox
        
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        
        assert data["syftbox"]["status"] == "connected"
        assert data["syftbox"]["user_email"] == "test@example.com"
    
    @patch('backend.fast_main.SYFTBOX_AVAILABLE', True)
    @patch('backend.fast_main.get_syftbox_client')
    def test_client_info(self, mock_get_client, client):
        """Test /api/client-info endpoint"""
        mock_syftbox = Mock()
        mock_syftbox.email = "test@example.com"
        mock_get_client.return_value = mock_syftbox
        
        response = client.get("/api/client-info")
        assert response.status_code == 200
        data = response.json()
        
        assert data["user_email"] == "test@example.com"
        assert data["defaults"]["admin_email"] == "test@example.com"
        assert data["defaults"]["permissions"]["private_read"] == "test@example.com"
    
    def test_client_info_no_syftbox(self, client):
        """Test /api/client-info without SyftBox"""
        with patch('backend.fast_main.SYFTBOX_AVAILABLE', False):
            response = client.get("/api/client-info")
            assert response.status_code == 200
            data = response.json()
            
            assert data["user_email"] == "admin@example.com"
    
    @patch('backend.fast_main.objects', None)
    def test_get_objects_not_available(self, client):
        """Test /api/objects when objects not available"""
        response = client.get("/api/objects")
        assert response.status_code == 503
        assert response.json()["detail"] == "Syft objects not available"
    
    @patch('backend.fast_main.objects')
    def test_get_objects_empty(self, mock_objects, client):
        """Test /api/objects with empty collection"""
        mock_collection = Mock()
        mock_collection.to_list.return_value = []
        mock_objects.search.return_value = mock_collection
        mock_objects.filter_by_email.return_value = mock_collection
        mock_objects.to_list.return_value = []
        
        response = client.get("/api/objects")
        assert response.status_code == 200
        data = response.json()
        
        assert data["objects"] == []
        assert data["total_count"] == 0
        assert data["has_more"] is False
    
    @patch('backend.fast_main.objects')
    def test_get_objects_with_data(self, mock_objects, client, sample_syft_object_data):
        """Test /api/objects with objects"""
        mock_obj = Mock()
        mock_obj.uid = uuid4()
        mock_obj.name = "Test Object"
        mock_obj.description = "Test description"
        mock_obj.private_url = "syft://test@example.com/private/test.txt"
        mock_obj.mock_url = "syft://test@example.com/public/test.txt"
        mock_obj.syftobject = "syft://test@example.com/public/test.syftobject.yaml"
        mock_obj.created_at = datetime.now()
        mock_obj.updated_at = datetime.now()
        mock_obj.metadata = {}
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = []
        mock_obj.private_permissions = ["test@example.com"]
        mock_obj.private_write_permissions = ["test@example.com"]
        mock_obj.file_type = ".txt"
        mock_obj._check_file_exists = Mock(return_value=True)
        
        mock_objects.to_list.return_value = [mock_obj]
        
        response = client.get("/api/objects")
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["objects"]) == 1
        obj_data = data["objects"][0]
        assert obj_data["name"] == "Test Object"
        assert obj_data["email"] == "test@example.com"
        assert obj_data["type"] == ".txt"
    
    @patch('backend.fast_main.objects')
    def test_get_objects_with_search(self, mock_objects, client):
        """Test /api/objects with search parameter"""
        mock_collection = Mock()
        mock_collection.to_list.return_value = []
        mock_collection._search_info = "Search results for 'test'"
        mock_objects.search.return_value = mock_collection
        
        response = client.get("/api/objects?search=test")
        assert response.status_code == 200
        data = response.json()
        
        mock_objects.search.assert_called_once_with("test")
        assert data["search_info"] == "Search results for 'test'"
    
    @patch('backend.fast_main.objects')
    def test_get_objects_with_pagination(self, mock_objects, client):
        """Test /api/objects with pagination"""
        # Create 10 mock objects
        mock_objs = []
        for i in range(10):
            obj = Mock()
            obj.uid = uuid4()
            obj.name = f"Object {i}"
            obj.created_at = datetime.now()
            obj.private_url = f"syft://test@example.com/private/obj{i}.txt"
            obj.mock_url = f"syft://test@example.com/public/obj{i}.txt"
            obj.syftobject = f"syft://test@example.com/public/obj{i}.syftobject.yaml"
            obj.updated_at = None
            obj.description = ""
            obj.metadata = {}
            obj.file_type = ".txt"
            obj._check_file_exists = Mock(return_value=True)
            obj.syftobject_permissions = ["public"]
            obj.mock_permissions = ["public"]
            obj.mock_write_permissions = []
            obj.private_permissions = ["test@example.com"]
            obj.private_write_permissions = ["test@example.com"]
            mock_objs.append(obj)
        
        mock_objects.to_list.return_value = mock_objs
        
        response = client.get("/api/objects?limit=5&offset=2")
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["objects"]) == 5
        assert data["total_count"] == 10
        assert data["offset"] == 2
        assert data["limit"] == 5
        assert data["has_more"] is True
    
    @patch('backend.fast_main.objects', None)
    def test_create_object_not_available(self, client):
        """Test POST /api/objects when objects not available"""
        response = client.post("/api/objects", json={
            "name": "Test",
            "description": "Test"
        })
        assert response.status_code == 503
    
    @patch('backend.fast_main.objects')
    @patch('syft_objects.factory.syobj')
    @patch('backend.fast_main.get_syftbox_client')
    def test_create_object_minimal(self, mock_get_client, mock_syobj, mock_objects, client):
        """Test POST /api/objects with minimal data"""
        mock_get_client.return_value = None
        
        mock_obj = Mock()
        mock_obj.uid = uuid4()
        mock_obj.name = "Test Object"
        mock_obj.description = "Test description"
        mock_obj.created_at = datetime.now()
        mock_obj.private_url = "syft://test@example.com/private/test.txt"
        mock_obj.mock_url = "syft://test@example.com/public/test.txt"
        mock_obj.syftobject = "syft://test@example.com/public/test.syftobject.yaml"
        
        mock_syobj.return_value = mock_obj
        
        response = client.post("/api/objects", json={
            "name": "Test Object",
            "description": "Test description"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["object"]["name"] == "Test Object"
        mock_objects.refresh.assert_called_once()
    
    @patch('backend.fast_main.objects')
    @patch('syft_objects.factory.syobj')
    def test_create_object_with_files(self, mock_syobj, mock_objects, client):
        """Test POST /api/objects with file content"""
        mock_obj = Mock()
        mock_obj.uid = uuid4()
        mock_obj.name = "File Object"
        mock_obj.description = ""
        mock_obj.created_at = datetime.now()
        mock_obj.private_url = "syft://test@example.com/private/data.txt"
        mock_obj.mock_url = "syft://test@example.com/public/data_mock.txt"
        mock_obj.syftobject = "syft://test@example.com/public/data.syftobject.yaml"
        
        mock_syobj.return_value = mock_obj
        
        response = client.post("/api/objects", json={
            "name": "File Object",
            "private_file_content": "Private data content",
            "private_filename": "data.txt",
            "mock_file_content": "Mock data content",
            "mock_filename": "data_mock.txt",
            "permissions": {
                "mock_read": ["public"],
                "private_read": ["test@example.com"]
            }
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["object"]["name"] == "File Object"
        
        # Check syobj was called with file paths
        mock_syobj.assert_called_once()
        call_args = mock_syobj.call_args
        assert "private_file" in call_args.kwargs
        assert "mock_file" in call_args.kwargs
    
    @patch('backend.fast_main.objects')
    def test_refresh_objects(self, mock_objects, client):
        """Test GET /api/objects/refresh"""
        mock_objects.__len__.return_value = 5
        
        response = client.get("/api/objects/refresh")
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "Objects collection refreshed"
        assert data["count"] == 5
        mock_objects.refresh.assert_called_once()
    
    @patch('syft_objects.auto_install.reinstall_syftbox_app')
    def test_reinstall_syftbox_app(self, mock_reinstall, client):
        """Test POST /api/syftbox/reinstall"""
        mock_reinstall.return_value = True
        
        response = client.post("/api/syftbox/reinstall")
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "reinstalled successfully" in data["message"]
        mock_reinstall.assert_called_once_with(silent=False)
    
    @patch('backend.fast_main.objects')
    def test_get_object_details(self, mock_objects, client):
        """Test GET /api/objects/{object_uid}"""
        uid = str(uuid4())
        
        mock_obj = Mock()
        mock_obj.uid = uid
        mock_obj.name = "Detail Object"
        mock_obj.description = "Detailed description"
        mock_obj.private_url = "syft://test@example.com/private/detail.txt"
        mock_obj.mock_url = "syft://test@example.com/public/detail.txt"
        mock_obj.syftobject = "syft://test@example.com/public/detail.syftobject.yaml"
        mock_obj.created_at = datetime.now()
        mock_obj.updated_at = datetime.now()
        mock_obj.metadata = {"key": "value"}
        mock_obj.private_path = "/path/to/private.txt"
        mock_obj.mock_path = "/path/to/mock.txt"
        mock_obj.syftobject_path = "/path/to/object.syftobject.yaml"
        mock_obj._get_file_preview = Mock(return_value="File preview content")
        mock_obj._check_file_exists = Mock(return_value=True)
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = []
        mock_obj.private_permissions = ["test@example.com"]
        mock_obj.private_write_permissions = ["test@example.com"]
        
        mock_objects.__iter__ = Mock(return_value=iter([mock_obj]))
        
        response = client.get(f"/api/objects/{uid}")
        assert response.status_code == 200
        data = response.json()
        
        assert data["uid"] == uid
        assert data["name"] == "Detail Object"
        assert data["file_previews"]["private"] == "File preview content"
        assert data["file_previews"]["mock"] == "File preview content"
    
    @patch('backend.fast_main.objects')
    def test_get_object_details_not_found(self, mock_objects, client):
        """Test GET /api/objects/{object_uid} not found"""
        mock_objects.__iter__ = Mock(return_value=iter([]))
        
        response = client.get(f"/api/objects/{uuid4()}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Object not found"
    
    @patch('backend.fast_main.objects')
    def test_get_unique_emails(self, mock_objects, client):
        """Test GET /api/metadata/emails"""
        mock_objects.list_unique_emails.return_value = ["test@example.com", "admin@example.com"]
        
        response = client.get("/api/metadata/emails")
        assert response.status_code == 200
        data = response.json()
        
        assert data["emails"] == ["test@example.com", "admin@example.com"]
        assert data["count"] == 2
    
    @patch('backend.fast_main.objects')
    def test_get_unique_names(self, mock_objects, client):
        """Test GET /api/metadata/names"""
        mock_objects.list_unique_names.return_value = ["Object One", "Object Two"]
        
        response = client.get("/api/metadata/names")
        assert response.status_code == 200
        data = response.json()
        
        assert data["names"] == ["Object One", "Object Two"]
        assert data["count"] == 2
    
    @patch('backend.fast_main.objects')
    def test_get_file_content(self, mock_objects, client, temp_dir):
        """Test GET /api/file"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("File content")
        
        mock_obj = Mock()
        mock_obj.private_url = "syft://test@example.com/private/test.txt"
        mock_obj.private_path = str(test_file)
        
        mock_objects.__iter__ = Mock(return_value=iter([mock_obj]))
        
        response = client.get("/api/file?syft_url=syft://test@example.com/private/test.txt")
        assert response.status_code == 200
        assert response.text == "File content"
    
    @patch('backend.fast_main.objects')
    def test_get_file_content_not_found(self, mock_objects, client):
        """Test GET /api/file not found"""
        mock_objects.__iter__ = Mock(return_value=iter([]))
        
        response = client.get("/api/file?syft_url=syft://test@example.com/private/notfound.txt")
        assert response.status_code == 404
        assert response.json()["detail"] == "File not found"
    
    @patch('backend.fast_main.objects')
    def test_save_file_content(self, mock_objects, client, temp_dir):
        """Test PUT /api/objects/{object_uid}/file/{file_type}"""
        uid = str(uuid4())
        test_file = temp_dir / "test.txt"
        test_file.write_text("Original content")
        
        mock_obj = Mock()
        mock_obj.uid = uid
        mock_obj.private_path = str(test_file)
        
        mock_objects.__iter__ = Mock(return_value=iter([mock_obj]))
        
        response = client.put(
            f"/api/objects/{uid}/file/private",
            content="New content"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "saved successfully" in data["message"]
        assert test_file.read_text() == "New content"
        mock_objects.refresh.assert_called_once()
    
    @patch('backend.fast_main.objects')
    def test_update_permissions(self, mock_objects, client):
        """Test PUT /api/objects/{object_uid}/permissions"""
        uid = str(uuid4())
        
        mock_obj = Mock()
        mock_obj.uid = uid
        mock_obj.syftobject_path = "/path/to/object.syftobject.yaml"
        mock_obj.save_yaml = Mock()
        
        mock_objects.__iter__ = Mock(return_value=iter([mock_obj]))
        
        response = client.put(
            f"/api/objects/{uid}/permissions",
            json={
                "private_read": ["new@example.com"],
                "mock_read": ["public"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "updated successfully" in data["message"]
        assert mock_obj.private_permissions == ["new@example.com"]
        assert mock_obj.mock_permissions == ["public"]
        mock_obj.save_yaml.assert_called()
        mock_objects.refresh.assert_called_once()
    
    @patch('backend.fast_main.objects')
    def test_delete_object(self, mock_objects, client, temp_dir):
        """Test DELETE /api/objects/{object_uid}"""
        uid = str(uuid4())
        
        # Create test files
        private_file = temp_dir / "private.txt"
        private_file.write_text("private")
        mock_file = temp_dir / "mock.txt"
        mock_file.write_text("mock")
        syftobj_file = temp_dir / "obj.syftobject.yaml"
        syftobj_file.write_text("metadata")
        
        mock_obj = Mock()
        mock_obj.uid = uid
        mock_obj.private_path = str(private_file)
        mock_obj.mock_path = str(mock_file)
        mock_obj.syftobject_path = str(syftobj_file)
        # Ensure it's not detected as a folder
        mock_obj.is_folder = False
        mock_obj.object_type = 'file'
        mock_obj.metadata = {}
        
        mock_objects.__iter__ = Mock(return_value=iter([mock_obj]))
        
        response = client.delete(f"/api/objects/{uid}")
        assert response.status_code == 200
        data = response.json()
        
        assert "deleted successfully" in data["message"]
        assert data["deleted_files"] == ["private", "mock", "syftobject"]
        assert not private_file.exists()
        assert not mock_file.exists()
        assert not syftobj_file.exists()
        mock_objects.refresh.assert_called_once()
    
    def test_widget_redirect(self, client):
        """Test /widget redirect"""
        response = client.get("/widget", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/widget/"
    
    def test_widget_page(self, client):
        """Test /widget/ page"""
        # Test the actual widget endpoint behavior
        response = client.get("/widget/")
        # The widget page should return HTML content
        assert response.status_code == 200
        assert "html" in response.text.lower()
    
    @patch('backend.fast_main.PathLib')
    def test_root_page(self, mock_pathlib, client):
        """Test / root page"""
        mock_index_file = Mock()
        mock_index_file.exists.return_value = False
        
        mock_pathlib.return_value.parent.parent.__truediv__.return_value.__truediv__.return_value = mock_index_file
        
        response = client.get("/")
        assert response.status_code == 200
        assert "Syft Objects UI" in response.text
        assert "Frontend not built yet" in response.text