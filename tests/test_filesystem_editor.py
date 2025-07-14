"""Tests for filesystem editor functionality"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from backend.filesystem_editor import generate_editor_html, FileSystemManager
from fastapi import HTTPException


class TestFileSystemEditor:
    """Test filesystem editor with file-specific path support"""
    
    def test_generate_editor_html_with_directory_path(self):
        """Test that generate_editor_html works with directory paths"""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=False):
            
            html = generate_editor_html('/some/directory')
            
            # Check that it's not in file-only mode
            assert 'this.isInitialFile = false' in html
            assert "this.currentPath = '/some/directory'" in html
            assert 'this.initialFilePath = null' in html
    
    def test_generate_editor_html_with_file_path(self):
        """Test that generate_editor_html detects file paths correctly"""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=True), \
             patch('pathlib.Path.parent', new_callable=lambda: Mock(return_value=Path('/some'))):
            
            html = generate_editor_html('/some/file.py')
            
            # Check that it's in file-only mode
            assert 'this.isInitialFile = true' in html
            assert "this.currentPath = '/some'" in html
            assert 'this.initialFilePath = `/some/file.py`' in html
            assert 'this.fileOnlyMode = this.isInitialFile' in html
    
    def test_generate_editor_html_with_nonexistent_path(self):
        """Test that generate_editor_html handles non-existent paths"""
        with patch('pathlib.Path.exists', return_value=False):
            html = generate_editor_html('/nonexistent/path')
            
            # Should default to directory mode
            assert 'this.isInitialFile = false' in html
            assert "this.currentPath = '/nonexistent/path'" in html
    
    def test_generate_editor_html_includes_toggle_button(self):
        """Test that the toggle explorer button is included"""
        html = generate_editor_html()
        
        # Check for toggle button
        assert 'toggleExplorerBtn' in html
        assert 'Toggle File Explorer' in html
        assert 'toggleFileOnlyMode' in html
    
    def test_generate_editor_html_includes_file_only_styles(self):
        """Test that file-only mode CSS is included"""
        html = generate_editor_html()
        
        # Check for file-only mode CSS
        assert '.file-only-mode' in html
        assert 'grid-template-columns: 1fr' in html
        assert '.file-only-mode .panel:first-child' in html
    
    def test_file_system_manager_text_file_detection(self):
        """Test FileSystemManager can detect text files"""
        manager = FileSystemManager()
        
        # Test with allowed extensions
        assert manager._is_text_file(Path('test.py')) == True
        assert manager._is_text_file(Path('test.js')) == True
        assert manager._is_text_file(Path('test.md')) == True
        
        # Test with non-text extensions
        assert manager._is_text_file(Path('test.jpg')) == False
        assert manager._is_text_file(Path('test.exe')) == False
    
    def test_file_system_manager_path_validation(self):
        """Test FileSystemManager path validation"""
        manager = FileSystemManager()
        
        # Test valid path
        with patch('pathlib.Path.resolve') as mock_resolve:
            mock_resolve.return_value = Path('/valid/path')
            result = manager._validate_path('/valid/path')
            assert result == Path('/valid/path')
        
        # Test with base path restriction
        manager_restricted = FileSystemManager(base_path='/allowed')
        with patch('pathlib.Path.resolve') as mock_resolve:
            mock_resolve.return_value = Path('/not/allowed/path')
            with pytest.raises(HTTPException) as exc_info:
                manager_restricted._validate_path('/not/allowed/path')
            assert exc_info.value.status_code == 403