"""Test ObjectsCollection widget behavior with server status."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from syft_objects.collections import ObjectsCollection


class TestObjectsCollectionWidget:
    """Test widget display behavior based on server status."""
    
    def test_widget_shows_waiting_ui_when_server_not_ready(self):
        """Test that widget shows waiting UI when server isn't ready."""
        collection = ObjectsCollection()
        collection._server_ready = False
        
        with patch('syft_objects.collections.get_syft_objects_port') as mock_port:
            mock_port.return_value = 8004
            
            html = collection.widget()
            
            # Verify waiting UI elements
            assert "⏳ Waiting for syft-objects server..." in html
            assert "The server is starting up" in html
            assert "checkServer()" in html  # JavaScript polling function
            assert "http://localhost:8004/health" in html
            assert 'id="syft-widget-' not in html  # No active iframe when server not ready
    
    def test_widget_shows_iframe_when_server_ready(self):
        """Test that widget shows iframe when server is ready."""
        collection = ObjectsCollection()
        collection._server_ready = True
        
        with patch('syft_objects.collections.get_syft_objects_url') as mock_url:
            mock_url.return_value = "http://localhost:8004/widget"
            
            html = collection.widget()
            
            # Verify iframe is shown
            assert "<iframe" in html
            assert "http://localhost:8004/widget" in html
            assert "SyftObjects Widget" in html
            assert "⏳ Waiting for syft-objects server..." not in html
    
    def test_widget_auto_retry_javascript(self):
        """Test the auto-retry JavaScript in waiting UI."""
        collection = ObjectsCollection()
        collection._server_ready = False
        
        with patch('syft_objects.collections.get_syft_objects_port') as mock_port:
            with patch('syft_objects.collections.get_syft_objects_url') as mock_url:
                mock_port.return_value = 8004
                mock_url.return_value = "http://localhost:8004/widget"
                
                html = collection.widget()
                
                # Verify JavaScript retry logic
                assert "let attempts = 0;" in html
                assert "const maxAttempts = 60;" in html  # 30 seconds
                assert "setTimeout(checkServer, 500)" in html
                assert "fetch('http://localhost:8004/health'" in html
                assert "Server is ready! Replace with iframe" in html
    
    @patch('syft_objects.collections.ensure_syftbox_app_installed')
    @patch('syft_objects.collections.ensure_server_healthy')
    def test_ensure_server_ready_caching(self, mock_healthy, mock_installed):
        """Test that _ensure_server_ready caches results."""
        collection = ObjectsCollection()
        
        # First call
        mock_installed.return_value = True
        mock_healthy.return_value = True
        collection._ensure_server_ready()
        
        assert collection._server_ready is True
        assert mock_installed.call_count == 1
        assert mock_healthy.call_count == 1
        
        # Second call should skip checks
        collection._ensure_server_ready()
        
        assert mock_installed.call_count == 1  # Not called again
        assert mock_healthy.call_count == 1  # Not called again
    
    @patch('syft_objects.collections.ensure_syftbox_app_installed')
    @patch('syft_objects.collections.ensure_server_healthy')
    def test_ensure_server_ready_handles_not_installed(self, mock_healthy, mock_installed):
        """Test handling when SyftBox app is not installed."""
        collection = ObjectsCollection()
        
        mock_installed.return_value = False
        collection._ensure_server_ready()
        
        assert collection._server_ready is False
        assert mock_healthy.call_count == 0  # Should not check health if not installed
    
    def test_widget_custom_dimensions(self):
        """Test widget with custom width and height."""
        collection = ObjectsCollection()
        collection._server_ready = True
        
        with patch('syft_objects.collections.get_syft_objects_url') as mock_url:
            mock_url.return_value = "http://localhost:8004/widget"
            
            html = collection.widget(width="800px", height="400px")
            
            assert 'width="800px"' in html
            assert 'height="400px"' in html
    
    def test_widget_custom_url(self):
        """Test widget with custom URL."""
        collection = ObjectsCollection()
        collection._server_ready = True
        
        custom_url = "http://localhost:9999/custom-widget"
        html = collection.widget(url=custom_url)
        
        assert custom_url in html
        assert "<iframe" in html