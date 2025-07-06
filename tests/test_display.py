"""Tests for syft_objects.display module"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
from uuid import uuid4

from syft_objects.display import (
    create_html_display, create_html_template, render_custom_metadata, 
    render_file_operations
)


class TestDisplayModule:
    """Test display module functions"""
    
    def test_create_html_display_minimal(self):
        """Test create_html_display with minimal SyftObject"""
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
        mock_obj._check_file_exists = Mock(return_value=True)
        mock_obj._get_local_file_path = Mock(return_value="/path/to/file")
        
        html = create_html_display(mock_obj)
        
        assert "Test Object" in html
        assert str(mock_obj.uid)[:8] in html
        assert "syft://test@example.com/mock.txt" in html
        assert "syft://test@example.com/private.txt" in html
        assert "✓ Available" in html
    
    def test_create_html_display_with_metadata(self):
        """Test create_html_display with full metadata"""
        mock_obj = Mock()
        mock_obj.name = "Test Object"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.updated_at = datetime.now(timezone.utc)
        mock_obj.description = "Test description"
        mock_obj.metadata = {
            "_file_operations": {
                "files_moved_to_syftbox": ["file1.txt -> /syftbox/file1.txt"],
                "created_files": ["/tmp/file1.txt"],
                "syftbox_available": True,
                "syftobject_yaml_path": "/path/to/object.syftobject.yaml"
            },
            "custom_key": "custom_value"
        }
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = ["test@example.com"]
        mock_obj.private_permissions = ["test@example.com", "other@example.com"]
        mock_obj.private_write_permissions = []
        mock_obj._check_file_exists = Mock(return_value=False)
        mock_obj._get_local_file_path = Mock(return_value="")
        
        html = create_html_display(mock_obj)
        
        assert "Test description" in html
        assert "⚠ Not accessible" in html
        assert "SyftBox Integration Active" in html
        assert "file1.txt -> /syftbox/file1.txt" in html
        assert "custom_key" in html
        assert "custom_value" in html
        assert "2 users" in html  # Multiple private_permissions
    
    def test_permission_badge_rendering(self):
        """Test different permission badge scenarios"""
        mock_obj = Mock()
        mock_obj.name = "Test"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.updated_at = None
        mock_obj.description = None
        mock_obj.metadata = {}
        mock_obj._check_file_exists = Mock(return_value=True)
        mock_obj._get_local_file_path = Mock(return_value="/path")
        
        # Test different permission scenarios
        test_cases = [
            (["public"], "Public"),
            (["*"], "Public"),
            (["user@example.com"], "user@example.com"),
            (["user1@example.com", "user2@example.com"], "2 users"),
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
        assert "['data', 'test']" in result
    
    def test_render_file_operations_empty(self):
        """Test render_file_operations with no operations"""
        result = render_file_operations([], [], True)
        assert result == ""
    
    def test_render_file_operations_with_moves(self):
        """Test render_file_operations with file moves"""
        files_moved = [
            "test.txt -> /syftbox/datasites/user/test.txt",
            "data.csv -> /syftbox/datasites/user/data.csv"
        ]
        
        result = render_file_operations(files_moved, [], True)
        
        assert "✅" in result
        assert "SyftBox Integration Active" in result
        assert "Moved to SyftBox locations:" in result
        assert "test.txt -> /syftbox/datasites/user/test.txt" in result
        assert "data.csv -> /syftbox/datasites/user/data.csv" in result
    
    def test_render_file_operations_without_syftbox(self):
        """Test render_file_operations when SyftBox not available"""
        created_files = ["/tmp/test.txt", "/tmp/data.csv"]
        
        result = render_file_operations([], created_files, False)
        
        assert "⚠️" in result
        assert "SyftBox Not Available" in result
        assert "Created in tmp/ directory:" in result
        assert "/tmp/test.txt" in result
        assert "/tmp/data.csv" in result
        assert "Install syft-core for SyftBox integration" in result
    
    def test_create_html_template_structure(self):
        """Test that create_html_template generates valid structure"""
        mock_obj = Mock()
        mock_obj.name = "Test"
        mock_obj.uid = uuid4()
        mock_obj.mock_url = "syft://test@example.com/mock.txt"
        mock_obj.private_url = "syft://test@example.com/private.txt"
        mock_obj.created_at = datetime.now(timezone.utc)
        mock_obj.metadata = {}  # Add metadata for the template
        mock_obj.syftobject_permissions = ["public"]
        mock_obj.mock_permissions = ["public"]
        mock_obj.mock_write_permissions = []
        mock_obj.private_permissions = []
        mock_obj.private_write_permissions = []
        
        def permission_badge(users, perm_type="read"):
            return f'<span>{users}</span>'
        
        def file_badge(exists, url, file_type="file"):
            return f'<span>{exists}</span>'
        
        html = create_html_template(
            syft_obj=mock_obj,
            mock_file_exists=True,
            private_file_exists=False,
            mock_info="<div>Mock info</div>",
            private_info="",
            syftobject_yaml_path="/path/to/yaml",
            permission_badge=permission_badge,
            file_badge=file_badge,
            updated_row="",
            description_row="",
            files_moved=[],
            created_files=[],
            syftbox_available=True
        )
        
        # Check for required CSS classes
        assert "syft-object" in html
        assert "syft-header" in html
        assert "syft-title" in html
        assert "syft-uid" in html
        assert "syft-section" in html
        assert "syft-file-card" in html
        assert "syft-permissions" in html
        assert "syft-metadata" in html
        
        # Check for content
        assert "Mock info" in html
        assert "/path/to/yaml" in html
        
    def test_file_exists_checks(self):
        """Test file existence checking in display"""
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
        assert "⚠ Not accessible" in html  # Private file doesn't exist
    
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