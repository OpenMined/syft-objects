"""Tests for syft_objects.display module"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
from uuid import uuid4

from syft_objects.display import (
    create_html_display, create_static_display, render_custom_metadata, 
    render_permissions_section, render_permission_tags
)


class TestDisplayModule:
    """Test display module functions"""
    
    @patch('requests.get')
    def test_create_html_display_minimal(self, mock_get):
        """Test create_html_display with minimal SyftObject"""
        # Mock server not available to get static HTML
        mock_get.side_effect = Exception("Connection error")
        
        mock_obj = Mock()
        mock_obj.name = "Test Object"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.updated_at = None
        mock_obj.description = None
        mock_obj.metadata = {}
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = []
        mock_obj.private_permissions = ["test@example.com"]
        mock_obj.private_write_permissions = ["test@example.com"]
        mock_obj.file_type = "txt"
        mock_obj.is_folder = False
        mock_obj.object_type = "file"
        mock_obj.mock_path = "/path/to/mock.txt"
        mock_obj.private_path = "/path/to/private.txt"
        mock_obj.syftobject_path = "/path/to/config.yaml"
        mock_obj._check_file_exists = Mock(return_value=True)
        mock_obj._get_local_file_path = Mock(return_value="/path/to/file")
        
        html = create_html_display(mock_obj)
        
        assert "Test Object" in html
        assert str(mock_obj.uid)[:8] in html
        assert "✓ Available" in html
    
    @patch('requests.get')
    def test_create_html_display_with_metadata(self, mock_get):
        """Test create_html_display with full metadata"""
        # Mock server not available to get static HTML
        mock_get.side_effect = Exception("Connection error")
        
        mock_obj = Mock()
        mock_obj.name = "Test Object"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.updated_at = datetime.now(timezone.utc)
        mock_obj.description = "Test description"
        mock_obj.metadata = {
            "custom_key": "custom_value"
        }
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = ["test@example.com"]
        mock_obj.private_permissions = ["test@example.com", "other@example.com"]
        mock_obj.private_write_permissions = []
        mock_obj.file_type = "txt"
        mock_obj.is_folder = False
        mock_obj.object_type = "file"
        mock_obj.mock_path = "/path/to/mock.txt"
        mock_obj.private_path = "/path/to/private.txt"
        mock_obj.syftobject_path = "/path/to/config.yaml"
        mock_obj._check_file_exists = Mock(return_value=False)
        mock_obj._get_local_file_path = Mock(return_value="")
        
        html = create_html_display(mock_obj)
        
        assert "Test description" in html
        assert "✗ Not Found" in html  # File not found status
        assert "custom_key" in html
        assert "custom_value" in html
    
    @patch('requests.get')
    def test_permission_badge_rendering(self, mock_get):
        """Test different permission badge scenarios"""
        # Mock server not available to get static HTML
        mock_get.side_effect = Exception("Connection error")
        
        mock_obj = Mock()
        mock_obj.name = "Test"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.updated_at = None
        mock_obj.description = None
        mock_obj.metadata = {}
        mock_obj.file_type = "txt"
        mock_obj.is_folder = False
        mock_obj.object_type = "file"
        mock_obj.mock_path = "/path/to/mock.txt"
        mock_obj.private_path = "/path/to/private.txt"
        mock_obj.syftobject_path = "/path/to/config.yaml"
        mock_obj._check_file_exists = Mock(return_value=True)
        mock_obj._get_local_file_path = Mock(return_value="/path")
        
        # Test different permission scenarios
        test_cases = [
            (["public"], "Public"),
            (["*"], "Public"),
            (["user@example.com"], "user@example.com"),
            (["user1@example.com", "user2@example.com"], "user1@example.com"),  # Check for first user
            ([], "None")
        ]
        
        for permissions, expected_text in test_cases:
            mock_obj.syftobject_permissions = permissions
            mock_obj.mock_permissions = ["public"]
            mock_obj.mock_write_permissions = []
            mock_obj.private_permissions = []
            mock_obj.private_write_permissions = []
            
            html = create_html_display(mock_obj)
            assert expected_text in html
    
    def test_render_custom_metadata_empty(self):
        """Test render_custom_metadata with no custom metadata"""
        mock_obj = Mock()
        mock_obj.metadata = {"_file_operations": {}}
        
        result = render_custom_metadata(mock_obj)
        assert result == ""
    
    def test_render_custom_metadata_with_values(self):
        """Test render_custom_metadata with custom values"""
        mock_obj = Mock()
        mock_obj.metadata = {
            "_file_operations": {},  # System field, should be excluded
            "author": "John Doe",
            "version": "1.0.0",
            "tags": ["data", "test"]
        }
        
        result = render_custom_metadata(mock_obj)
        
        assert "_file_operations" not in result
        assert "author" in result
        assert "John Doe" in result
        assert "version" in result
        assert "1.0.0" in result
        assert "tags" in result
        assert "&quot;data&quot;" in result
        assert "&quot;test&quot;" in result
    
    def test_render_permission_tags_empty(self):
        """Test render_permission_tags with no permissions"""
        result = render_permission_tags([])
        assert 'None' in result
    
    def test_render_permission_tags_with_public(self):
        """Test render_permission_tags with public permissions"""
        result = render_permission_tags(['public'])
        assert 'Public' in result
        assert 'syft-email-tag public' in result
        
        result = render_permission_tags(['*'])
        assert 'Public' in result
        assert 'syft-email-tag public' in result
    
    def test_render_permission_tags_with_emails(self):
        """Test render_permission_tags with email permissions"""
        result = render_permission_tags(['user@example.com'])
        assert 'user@example.com' in result
        assert 'syft-email-tag' in result
        
        result = render_permission_tags(['user1@example.com', 'user2@example.com'])
        assert 'user1@example.com' in result
        assert 'user2@example.com' in result
    
    def test_render_permissions_section(self):
        """Test render_permissions_section"""
        result = render_permissions_section(
            "Test Permissions", 
            "Test description", 
            ["user@example.com"]
        )
        
        assert "Test Permissions" in result
        assert "Test description" in result
        assert "user@example.com" in result
        assert "syft-permissions-section" in result
    
    def test_create_static_display_structure(self):
        """Test that create_static_display generates valid structure"""
        mock_obj = Mock()
        mock_obj.name = "Test"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.updated_at = datetime.now(timezone.utc)
        mock_obj.description = "Test description"
        mock_obj.metadata = {}
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = []
        mock_obj.private_permissions = []
        mock_obj.private_write_permissions = []
        mock_obj.file_type = "txt"
        mock_obj.is_folder = False
        mock_obj.object_type = "file"
        mock_obj.mock_path = "/path/to/mock.txt"
        mock_obj.private_path = "/path/to/private.txt"
        mock_obj.syftobject_path = "/path/to/config.yaml"
        mock_obj._check_file_exists = Mock(return_value=True)
        
        html = create_static_display(mock_obj)
        
        # Check for required CSS classes
        assert "syft-static-viewer" in html
        assert "syft-widget-header" in html
        assert "syft-widget-title" in html
        assert "syft-uid-badge" in html
        assert "syft-tabs" in html
        assert "syft-tab-content" in html
        assert "syft-permissions-section" in html
        assert "syft-file-section" in html
        
        # Check for content
        assert "Test" in html
        assert "Test description" in html
        assert str(mock_obj.uid)[:8] in html
        
    @patch('requests.get')
    def test_file_exists_checks(self, mock_get):
        """Test file existence checking in display"""
        # Mock server not available to get static HTML
        mock_get.side_effect = Exception("Connection error")
        
        mock_obj = Mock()
        mock_obj.name = "Test"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.updated_at = None
        mock_obj.description = None
        mock_obj.metadata = {}
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = []
        mock_obj.private_permissions = []
        mock_obj.private_write_permissions = []
        mock_obj.file_type = "txt"
        mock_obj.is_folder = False
        mock_obj.object_type = "file"
        mock_obj.mock_path = "/path/to/mock.txt"
        mock_obj.private_path = "/path/to/private.txt"
        mock_obj.syftobject_path = "/path/to/config.yaml"
        
        # Mock file existence checks
        check_results = {
            "syft://test@example.com/mock.txt": True,
            "syft://test@example.com/private.txt": False
        }
        mock_obj._check_file_exists = Mock(side_effect=lambda url: check_results.get(url, False))
        mock_obj._get_local_file_path = Mock(return_value="/path/to/file")
        
        html = create_html_display(mock_obj)
        
        # Verify the checks were made
        assert mock_obj._check_file_exists.call_count == 2
        mock_obj._check_file_exists.assert_any_call("syft://test@example.com/mock.txt")
        mock_obj._check_file_exists.assert_any_call("syft://test@example.com/private.txt")
        
        # Check the display shows correct status
        assert "✓ Available" in html  # Mock file exists
        assert "✗ Not Found" in html  # Private file doesn't exist
    
    def test_type_checking_import(self):
        """Test that TYPE_CHECKING import works correctly"""
        from syft_objects import display
        import typing
        
        # Force TYPE_CHECKING to be True to trigger the import
        original_value = typing.TYPE_CHECKING
        try:
            typing.TYPE_CHECKING = True
            # Re-import the module to trigger the TYPE_CHECKING block
            import importlib
            importlib.reload(display)
        finally:
            typing.TYPE_CHECKING = original_value
        
        assert hasattr(display, 'create_html_display')
        assert hasattr(display, 'render_custom_metadata')