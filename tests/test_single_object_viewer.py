"""Tests for single_object_viewer module."""

import pytest
from backend.single_object_viewer import generate_single_object_viewer_html
from unittest.mock import Mock


class TestSingleObjectViewer:
    """Test the single object viewer HTML generation."""
    
    def test_generate_html_no_missing_element_references(self):
        """Test that JavaScript doesn't reference non-existent HTML elements."""
        # Create a mock object with required attributes
        mock_obj = Mock()
        mock_obj.name = "Test Object"
        mock_obj.description = "Test Description"
        
        # Set up mock with path as string attribute
        mock_obj.mock = Mock()
        mock_obj.mock.path = "/test/mock/path"
        mock_obj.mock.get_path = Mock(return_value="/test/mock/path")
        
        mock_obj.private = Mock()
        mock_obj.private.path = "/test/private/path"
        mock_obj.private.get_path = Mock(return_value="/test/private/path")
        
        mock_obj.syftobject_config = Mock()
        mock_obj.syftobject_config.path = "/test/syftobject/path"
        mock_obj.syftobject_config.get_path = Mock(return_value="/test/syftobject/path")
        
        # Generate HTML
        html = generate_single_object_viewer_html(mock_obj, "test-uid-123")
        
        # Check that the problematic element references are commented out
        assert "document.getElementById('mock-path').textContent" not in html or \
               "// document.getElementById('mock-path').textContent" in html
        assert "document.getElementById('private-path').textContent" not in html or \
               "// document.getElementById('private-path').textContent" in html
        assert "document.getElementById('syftobject-path').textContent" not in html or \
               "// document.getElementById('syftobject-path').textContent" in html
        
        # Verify that these element IDs don't exist in the HTML
        assert 'id="mock-path"' not in html
        assert 'id="private-path"' not in html
        assert 'id="syftobject-path"' not in html
    
    def test_generate_html_with_none_paths(self):
        """Test HTML generation when all paths are None."""
        # Create a minimal object that simulates missing paths
        class MinimalObject:
            def get_name(self):
                return "Test Object"
            
            def get_description(self):
                return "Test Description"
            
            # No mock, private, or syftobject_config attributes
            
        mock_obj = MinimalObject()
        
        # Generate HTML - should not raise any errors
        html = generate_single_object_viewer_html(mock_obj, "test-uid-123")
        
        # Basic checks
        assert "Test Object" in html
        assert "test-uid-123" in html
        assert "File Not Found" in html  # Should show file not found messages
        
    def test_generate_html_with_folder_paths(self):
        """Test HTML generation when paths point to folders."""
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create actual directories
            mock_dir = os.path.join(tmpdir, "mock_folder")
            private_dir = os.path.join(tmpdir, "private_folder")
            os.makedirs(mock_dir)
            os.makedirs(private_dir)
            
            # Create mock object with folder paths
            mock_obj = Mock()
            mock_obj.name = "Folder Object"
            mock_obj.description = "Object with folders"
            mock_obj.mock = Mock()
            mock_obj.mock.path = mock_dir
            mock_obj.private = Mock()
            mock_obj.private.path = private_dir
            mock_obj.syftobject_config = Mock()
            mock_obj.syftobject_config.path = "/test/config.yaml"
            
            # Generate HTML
            html = generate_single_object_viewer_html(mock_obj, "folder-uid-123")
            
            # Check that folder indication is present
            assert "Mock Folder" in html
            assert "Private Folder" in html
    
    def test_all_textcontent_elements_exist(self):
        """Test that all elements referenced by textContent in JavaScript exist in HTML."""
        import re
        
        # Create a mock object
        mock_obj = Mock()
        mock_obj.name = "Test Object"
        mock_obj.description = "Test Description"
        mock_obj.mock = None
        mock_obj.private = None
        mock_obj.syftobject_config = None
        
        # Generate HTML
        html = generate_single_object_viewer_html(mock_obj, "test-uid-123")
        
        # Find all getElementById().textContent assignments in JavaScript
        # Skip commented lines
        js_section = html.split('<script>')[1].split('</script>')[0]
        active_lines = [line for line in js_section.split('\n') if not line.strip().startswith('//')]
        active_js = '\n'.join(active_lines)
        
        pattern = r"document\.getElementById\('([^']+)'\)\.textContent"
        element_ids = re.findall(pattern, active_js)
        
        # Check each referenced element exists in HTML
        for element_id in element_ids:
            assert f'id="{element_id}"' in html, f"Element with id='{element_id}' not found in HTML but referenced in JavaScript"