"""Tests for syft_objects.client module"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import os

import syft_objects.client as client_module
from syft_objects.client import (
    _initialize_syftbox, get_syftbox_client, extract_local_path_from_syft_url,
    check_syftbox_status, _print_startup_banner, get_syft_objects_port,
    get_syft_objects_url
)


class TestClientModule:
    """Test client module functions"""
    
    def test_initialize_syftbox_success(self):
        """Test successful SyftBox initialization"""
        # Reset globals first
        client_module.SYFTBOX_AVAILABLE = False
        client_module.SyftBoxClient = None
        client_module.SyftBoxURL = None
        
        # Create mock module
        mock_syft_core = Mock()
        mock_client_class = Mock()
        mock_url_class = Mock()
        mock_syft_core.Client = mock_client_class
        mock_syft_core.url.SyftBoxURL = mock_url_class
        
        with patch.dict('sys.modules', {'syft_core': mock_syft_core, 'syft_core.url': mock_syft_core.url}):
            _initialize_syftbox()
            
            assert client_module.SYFTBOX_AVAILABLE is True
            assert client_module.SyftBoxClient == mock_client_class
            assert client_module.SyftBoxURL == mock_url_class
    
    def test_initialize_syftbox_import_error(self):
        """Test SyftBox initialization with import error"""
        # Reset globals
        client_module.SYFTBOX_AVAILABLE = False
        client_module.SyftBoxClient = None
        client_module.SyftBoxURL = None
        
        with patch('builtins.__import__', side_effect=ImportError("No syft_core")):
            _initialize_syftbox()
            
            assert client_module.SYFTBOX_AVAILABLE is False
            assert client_module.SyftBoxClient is None
            assert client_module.SyftBoxURL is None
    
    def test_get_syftbox_client_not_available(self):
        """Test get_syftbox_client when SyftBox not available"""
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', False):
            result = get_syftbox_client()
            assert result is None
    
    def test_get_syftbox_client_success(self):
        """Test get_syftbox_client successful load"""
        mock_client = Mock()
        mock_client_class = Mock()
        mock_client_class.load.return_value = mock_client
        
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch.object(client_module, 'SyftBoxClient', mock_client_class):
                result = get_syftbox_client()
                assert result == mock_client
                mock_client_class.load.assert_called_once()
    
    def test_get_syftbox_client_exception(self):
        """Test get_syftbox_client with exception"""
        mock_client_class = Mock()
        mock_client_class.load.side_effect = Exception("Load failed")
        
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch.object(client_module, 'SyftBoxClient', mock_client_class):
                result = get_syftbox_client()
                assert result is None
    
    def test_extract_local_path_from_syft_url_not_available(self):
        """Test extract_local_path_from_syft_url when SyftBox not available"""
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', False):
            result = extract_local_path_from_syft_url("syft://test@example.com/test.txt")
            assert result is None
    
    def test_extract_local_path_from_syft_url_success(self):
        """Test extract_local_path_from_syft_url successful conversion"""
        mock_client = Mock()
        mock_client.datasites = Path("/datasites")
        
        mock_client_class = Mock()
        mock_client_class.load.return_value = mock_client
        
        mock_url_obj = Mock()
        mock_url_obj.to_local_path.return_value = Path("/datasites/test@example.com/test.txt")
        
        mock_url_class = Mock(return_value=mock_url_obj)
        
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch.object(client_module, 'SyftBoxClient', mock_client_class):
                with patch.object(client_module, 'SyftBoxURL', mock_url_class):
                    result = extract_local_path_from_syft_url("syft://test@example.com/test.txt")
                    assert result == Path("/datasites/test@example.com/test.txt")
    
    def test_extract_local_path_from_syft_url_exception(self):
        """Test extract_local_path_from_syft_url with exception"""
        mock_client_class = Mock()
        mock_client_class.load.side_effect = Exception("Failed")
        
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch.object(client_module, 'SyftBoxClient', mock_client_class):
                result = extract_local_path_from_syft_url("syft://test@example.com/test.txt")
                assert result is None
    
    def test_check_syftbox_status_not_available(self):
        """Test check_syftbox_status when SyftBox not available"""
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', False):
            check_syftbox_status()
            
            status = client_module._syftbox_status
            assert status['available'] is False
            assert status['client_connected'] is False
            assert status['app_running'] is False
            assert "not available" in status['error']
    
    def test_check_syftbox_status_no_client(self):
        """Test check_syftbox_status when client not available"""
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch('syft_objects.client.get_syftbox_client', return_value=None):
                check_syftbox_status()
                
                status = client_module._syftbox_status
                assert status['available'] is False
                assert "not available" in status['error']
    
    def test_check_syftbox_status_success(self):
        """Test check_syftbox_status successful"""
        mock_client = Mock()
        mock_client.email = "test@example.com"
        mock_datasites = Mock()
        mock_datasites.iterdir.return_value = [Path("/datasites/test@example.com")]
        mock_client.datasites = mock_datasites
        mock_client.config.client_url = "http://localhost:5000"
        
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch('syft_objects.client.get_syftbox_client', return_value=mock_client):
                with patch('requests.get') as mock_get:
                    mock_response = Mock()
                    mock_response.status_code = 200
                    mock_response.text = "go1.19"
                    mock_get.return_value = mock_response
                    
                    check_syftbox_status()
                    
                    status = client_module._syftbox_status
                    assert status['available'] is True
                    assert status['client_connected'] is True
                    assert status['app_running'] is True
                    assert status['user_email'] == "test@example.com"
                    assert status['client_url'] == "http://localhost:5000"
    
    def test_check_syftbox_status_app_not_running(self):
        """Test check_syftbox_status when app not running"""
        mock_client = Mock()
        mock_client.email = "test@example.com"
        mock_datasites = Mock()
        mock_datasites.iterdir.return_value = [Path("/datasites/test@example.com")]
        mock_client.datasites = mock_datasites
        mock_client.config.client_url = "http://localhost:5000"
        
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch('syft_objects.client.get_syftbox_client', return_value=mock_client):
                with patch('requests.get', side_effect=Exception("Connection refused")):
                    check_syftbox_status()
                    
                    status = client_module._syftbox_status
                    assert status['available'] is True
                    assert status['client_connected'] is True
                    assert status['app_running'] is False
                    assert status['client_url'] == "http://localhost:5000"
    
    def test_print_startup_banner_only_if_needed_no_error(self):
        """Test _print_startup_banner with only_if_needed=True and no errors"""
        client_module._syftbox_status = {
            'available': True,
            'client_connected': True,
            'app_running': True,
            'error': None
        }
        
        with patch('builtins.print') as mock_print:
            _print_startup_banner(only_if_needed=True)
            # Should not print anything
            mock_print.assert_not_called()
    
    def test_print_startup_banner_only_if_needed_with_error(self):
        """Test _print_startup_banner with only_if_needed=True and error"""
        client_module._syftbox_status = {
            'error': 'SyftBox not available'
        }
        
        with patch('builtins.print') as mock_print:
            with patch('syft_objects.client.get_syft_objects_port', return_value=8004):
                _print_startup_banner(only_if_needed=True)
                
                # Should print error message
                assert mock_print.call_count >= 1
                # Extract all printed messages
                printed_messages = []
                for call in mock_print.call_args_list:
                    if call[0]:  # Check if there are positional args
                        printed_messages.append(str(call[0][0]))
                printed = ' '.join(printed_messages)
                assert "Syft Objects" in printed
                assert "8004" in printed
    
    def test_print_startup_banner_explicit_connected(self):
        """Test _print_startup_banner explicit call when connected"""
        client_module._syftbox_status = {
            'client_connected': True,
            'user_email': 'test@example.com',
            'error': None
        }
        
        with patch('builtins.print') as mock_print:
            with patch('syft_objects.client.get_syft_objects_port', return_value=8004):
                _print_startup_banner(only_if_needed=False)
                
                assert mock_print.call_count >= 1
                printed_messages = []
                for call in mock_print.call_args_list:
                    if call[0]:  # Check if there are positional args
                        printed_messages.append(str(call[0][0]))
                printed = ' '.join(printed_messages)
                assert "Connected: test@example.com" in printed
                assert "8004" in printed
    
    def test_print_startup_banner_explicit_local_mode(self):
        """Test _print_startup_banner explicit call in local mode"""
        client_module._syftbox_status = {
            'client_connected': False,
            'error': 'SyftBox not available - install syft-core for full functionality'
        }
        
        with patch('builtins.print') as mock_print:
            with patch('syft_objects.client.get_syft_objects_port', return_value=8004):
                _print_startup_banner(only_if_needed=False)
                
                assert mock_print.call_count >= 1
                printed_messages = []
                for call in mock_print.call_args_list:
                    if call[0]:  # Check if there are positional args
                        printed_messages.append(str(call[0][0]))
                printed = ' '.join(printed_messages)
                assert "Local mode" in printed
                assert "8004" in printed
    
    def test_get_syft_objects_port_from_config(self, temp_dir):
        """Test get_syft_objects_port reading from config file"""
        config_dir = temp_dir / ".syftbox"
        config_dir.mkdir()
        config_file = config_dir / "syft_objects.config"
        config_file.write_text("8005")
        
        with patch('syft_objects.client.Path.home', return_value=temp_dir):
            port = get_syft_objects_port()
            assert port == 8005
    
    def test_get_syft_objects_port_invalid_config(self, temp_dir):
        """Test get_syft_objects_port with invalid config"""
        config_dir = temp_dir / ".syftbox"
        config_dir.mkdir()
        config_file = config_dir / "syft_objects.config"
        config_file.write_text("invalid")
        
        with patch('syft_objects.client.Path.home', return_value=temp_dir):
            port = get_syft_objects_port()
            assert port == 8004  # Default
    
    def test_get_syft_objects_port_no_config(self, temp_dir):
        """Test get_syft_objects_port without config file"""
        with patch('syft_objects.client.Path.home', return_value=temp_dir):
            port = get_syft_objects_port()
            assert port == 8004  # Default
    
    def test_get_syft_objects_port_exception(self):
        """Test get_syft_objects_port with exception in file reading"""
        temp_dir = Path("/tmp/test_syft_port_exception")
        
        # Mock the home directory to point to our temp location
        with patch('syft_objects.client.Path.home', return_value=temp_dir):
            # Mock exists() to return True but read_text() to raise an exception
            with patch.object(Path, 'exists', return_value=True):
                with patch.object(Path, 'read_text', side_effect=Exception("Read error")):
                    port = get_syft_objects_port()
                    assert port == 8004  # Should return default due to exception
    
    def test_get_syft_objects_url_base(self):
        """Test get_syft_objects_url for base URL"""
        with patch('syft_objects.client.get_syft_objects_port', return_value=8005):
            url = get_syft_objects_url()
            assert url == "http://localhost:8005"
    
    def test_get_syft_objects_url_with_endpoint(self):
        """Test get_syft_objects_url with endpoint"""
        with patch('syft_objects.client.get_syft_objects_port', return_value=8005):
            url = get_syft_objects_url("api/objects")
            assert url == "http://localhost:8005/api/objects"
    
    def test_get_syft_objects_url_with_leading_slash(self):
        """Test get_syft_objects_url with leading slash in endpoint"""
        with patch('syft_objects.client.get_syft_objects_port', return_value=8005):
            url = get_syft_objects_url("/api/objects")
            assert url == "http://localhost:8005/api/objects"
    
    def test_module_initialization(self):
        """Test that _initialize_syftbox is called on module import"""
        # This is implicitly tested by importing the module
        # The function should have been called during import
        # We can verify by checking if the globals were set (even if to None/False)
        assert hasattr(client_module, 'SYFTBOX_AVAILABLE')
        assert hasattr(client_module, 'SyftBoxClient')
        assert hasattr(client_module, 'SyftBoxURL')
    
    def test_check_syftbox_status_filesystem_exception(self):
        """Test check_syftbox_status with filesystem access exception (lines 82-84)"""
        mock_client = Mock()
        mock_client.email.side_effect = Exception("Email access error")
        
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch('syft_objects.client.get_syftbox_client', return_value=mock_client):
                check_syftbox_status()
                
                status = client_module._syftbox_status
                assert status['available'] is False
                assert "SyftBox filesystem not accessible" in status['error']
                assert "Email access error" in status['error']
    
    def test_check_syftbox_status_client_exception(self):
        """Test check_syftbox_status with client access exception (lines 96-97)"""
        with patch.object(client_module, 'SYFTBOX_AVAILABLE', True):
            with patch('syft_objects.client.get_syftbox_client', side_effect=Exception("Client load error")):
                check_syftbox_status()
                
                status = client_module._syftbox_status
                assert status['available'] is False
                assert "Could not find SyftBox client" in status['error']
                assert "Client load error" in status['error']
    
    def test_print_startup_banner_explicit_with_error_path(self):
        """Test _print_startup_banner explicit call with error path (lines 116-117)"""
        client_module._syftbox_status = {
            'client_connected': False,
            'error': 'Test error message'
        }
        
        with patch('builtins.print') as mock_print:
            with patch('syft_objects.client.get_syft_objects_port', return_value=8004):
                _print_startup_banner(only_if_needed=False)
                
                # Should print error message on lines 116-117
                print_calls = [str(call) for call in mock_print.call_args_list]
                error_prints = [call for call in print_calls if "Test error message" in call and "localhost:8004" in call]
                assert len(error_prints) >= 1
    
    def test_print_startup_banner_explicit_no_connection(self):
        """Test _print_startup_banner explicit call with no connection (lines 131-132)"""
        client_module._syftbox_status = {
            'client_connected': False,
            'error': None  # No specific error, just not connected
        }
        
        with patch('builtins.print') as mock_print:
            with patch('syft_objects.client.get_syft_objects_port', return_value=8004):
                _print_startup_banner(only_if_needed=False)
                
                # Should print basic server info on lines 131-132
                print_calls = [str(call) for call in mock_print.call_args_list]
                server_prints = [call for call in print_calls if "Server: localhost:8004" in call and "error" not in call.lower()]
                assert len(server_prints) >= 1