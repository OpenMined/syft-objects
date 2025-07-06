"""Tests for syft_objects.auto_install module"""

import pytest
import subprocess
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import shutil

from syft_objects.auto_install import (
    get_syftbox_apps_path, is_syftbox_app_installed, clone_syftbox_app,
    ensure_server_healthy, _check_health_endpoint, _get_server_port,
    _wait_for_health_endpoint, wait_for_syft_objects_server, start_syftbox_app,
    is_syftbox_running, reinstall_syftbox_app, ensure_syftbox_app_installed
)


class TestAutoInstallModule:
    """Test auto_install module functions"""
    
    def test_get_syftbox_apps_path_exists(self, temp_dir):
        """Test get_syftbox_apps_path when SyftBox exists"""
        syftbox_dir = temp_dir / "SyftBox"
        syftbox_dir.mkdir()
        
        with patch('syft_objects.auto_install.Path.home', return_value=temp_dir):
            result = get_syftbox_apps_path()
            assert result == syftbox_dir / "apps"
    
    def test_get_syftbox_apps_path_not_exists(self, temp_dir):
        """Test get_syftbox_apps_path when SyftBox doesn't exist"""
        with patch('syft_objects.auto_install.Path.home', return_value=temp_dir):
            result = get_syftbox_apps_path()
            assert result is None
    
    def test_is_syftbox_app_installed_not_found(self):
        """Test is_syftbox_app_installed when apps path not found"""
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=None):
            assert is_syftbox_app_installed() is False
    
    def test_is_syftbox_app_installed_exists(self, temp_dir):
        """Test is_syftbox_app_installed when app exists"""
        apps_path = temp_dir / "apps"
        apps_path.mkdir()
        app_dir = apps_path / "syft-objects"
        app_dir.mkdir()
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            assert is_syftbox_app_installed() is True
    
    def test_is_syftbox_app_installed_not_exists(self, temp_dir):
        """Test is_syftbox_app_installed when app doesn't exist"""
        apps_path = temp_dir / "apps"
        apps_path.mkdir()
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            assert is_syftbox_app_installed() is False
    
    def test_clone_syftbox_app_no_syftbox(self):
        """Test clone_syftbox_app when SyftBox not found"""
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=None):
            with patch('builtins.print') as mock_print:
                result = clone_syftbox_app()
                assert result is False
                mock_print.assert_called()
                assert "SyftBox directory not found" in str(mock_print.call_args)
    
    @patch('subprocess.run')
    def test_clone_syftbox_app_success(self, mock_run, temp_dir):
        """Test clone_syftbox_app successful clone"""
        apps_path = temp_dir / "apps"
        
        # Mock git version check
        mock_run.side_effect = [
            Mock(returncode=0),  # git --version
            Mock(returncode=0, stderr="")  # git clone
        ]
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            result = clone_syftbox_app()
            assert result is True
            assert apps_path.exists()
            
            # Check git clone was called with correct args
            clone_call = mock_run.call_args_list[1]
            assert "git" in clone_call[0][0]
            assert "clone" in clone_call[0][0]
            assert "https://github.com/OpenMined/syft-objects.git" in clone_call[0][0]
    
    @patch('subprocess.run')
    def test_clone_syftbox_app_git_not_available(self, mock_run, temp_dir):
        """Test clone_syftbox_app when git not available"""
        apps_path = temp_dir / "apps"
        
        mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "--version"])
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            with patch('builtins.print') as mock_print:
                result = clone_syftbox_app()
                assert result is False
                assert "Git is not available" in str(mock_print.call_args_list)
    
    @patch('subprocess.run')
    def test_clone_syftbox_app_timeout(self, mock_run, temp_dir):
        """Test clone_syftbox_app with timeout"""
        apps_path = temp_dir / "apps"
        
        mock_run.side_effect = [
            Mock(returncode=0),  # git --version
            subprocess.TimeoutExpired(["git", "clone"], 60)  # git clone timeout
        ]
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            with patch('builtins.print') as mock_print:
                result = clone_syftbox_app()
                assert result is False
                assert "Git clone timed out" in str(mock_print.call_args_list)
    
    @patch('subprocess.run')
    def test_clone_syftbox_app_git_error(self, mock_run, temp_dir):
        """Test clone_syftbox_app with git error"""
        apps_path = temp_dir / "apps"
        
        mock_run.side_effect = [
            Mock(returncode=0),  # git --version
            Mock(returncode=1, stderr="fatal: repository not found")  # git clone error
        ]
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            with patch('builtins.print') as mock_print:
                result = clone_syftbox_app()
                assert result is False
                assert "Failed to clone repository" in str(mock_print.call_args_list)
    
    def test_ensure_server_healthy_no_requests(self):
        """Test ensure_server_healthy when requests not available"""
        with patch('syft_objects.auto_install.requests', None):
            with patch('builtins.print') as mock_print:
                result = ensure_server_healthy()
                assert result is False
                assert "requests library not available" in str(mock_print.call_args)
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    def test_ensure_server_healthy_already_healthy(self, mock_check):
        """Test ensure_server_healthy when server already healthy"""
        mock_check.return_value = True
        
        result = ensure_server_healthy()
        assert result is True
        mock_check.assert_called_once()
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    def test_ensure_server_healthy_no_syftbox(self, mock_apps_path, mock_check):
        """Test ensure_server_healthy when SyftBox not found"""
        mock_check.return_value = False
        mock_apps_path.return_value = None
        
        with patch('builtins.print') as mock_print:
            result = ensure_server_healthy()
            assert result is False
            assert "SyftBox not found" in str(mock_print.call_args)
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    def test_ensure_server_healthy_syftbox_not_running(self, mock_running, mock_apps_path, mock_check):
        """Test ensure_server_healthy when SyftBox not running"""
        mock_check.return_value = False
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = False
        
        with patch('builtins.print') as mock_print:
            result = ensure_server_healthy()
            assert result is False
            assert "SyftBox is not running" in str(mock_print.call_args)
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    @patch('syft_objects.auto_install.is_syftbox_app_installed')
    @patch('syft_objects.auto_install.reinstall_syftbox_app')
    @patch('syft_objects.auto_install._wait_for_health_endpoint')
    def test_ensure_server_healthy_reinstall_success(self, mock_wait, mock_reinstall, 
                                                     mock_installed, mock_running, 
                                                     mock_apps_path, mock_check):
        """Test ensure_server_healthy with successful reinstall"""
        mock_check.return_value = False
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = True
        mock_installed.return_value = False
        mock_reinstall.return_value = True
        mock_wait.return_value = True
        
        result = ensure_server_healthy()
        assert result is True
        mock_reinstall.assert_called_once_with(silent=True)
        mock_wait.assert_called_once()
    
    @patch('syft_objects.auto_install.requests')
    def test_check_health_endpoint_success(self, mock_requests):
        """Test _check_health_endpoint successful check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response
        
        with patch('syft_objects.auto_install._get_server_port', return_value=8004):
            result = _check_health_endpoint()
            assert result is True
            mock_requests.get.assert_called_with("http://localhost:8004/health", timeout=1)
    
    @patch('syft_objects.auto_install.requests')
    def test_check_health_endpoint_failure(self, mock_requests):
        """Test _check_health_endpoint with failure"""
        mock_requests.get.side_effect = Exception("Connection error")
        
        with patch('syft_objects.auto_install._get_server_port', return_value=8004):
            result = _check_health_endpoint()
            assert result is False
    
    def test_check_health_endpoint_no_port(self):
        """Test _check_health_endpoint with no port"""
        with patch('syft_objects.auto_install._get_server_port', return_value=None):
            result = _check_health_endpoint()
            assert result is False
    
    def test_get_server_port_from_config(self, temp_dir):
        """Test _get_server_port reading from config"""
        config_dir = temp_dir / ".syftbox"
        config_dir.mkdir()
        config_file = config_dir / "syft_objects.config"
        config_file.write_text("8005")
        
        with patch('syft_objects.auto_install.Path.home', return_value=temp_dir):
            port = _get_server_port()
            assert port == 8005
    
    def test_get_server_port_no_config(self, temp_dir):
        """Test _get_server_port without config"""
        with patch('syft_objects.auto_install.Path.home', return_value=temp_dir):
            port = _get_server_port()
            assert port is None
    
    def test_get_server_port_invalid_config(self, temp_dir):
        """Test _get_server_port with invalid config"""
        config_dir = temp_dir / ".syftbox"
        config_dir.mkdir()
        config_file = config_dir / "syft_objects.config"
        config_file.write_text("invalid")
        
        with patch('syft_objects.auto_install.Path.home', return_value=temp_dir):
            port = _get_server_port()
            assert port is None
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch('syft_objects.auto_install.time.time')
    @patch('syft_objects.auto_install.time.sleep')
    def test_wait_for_health_endpoint_success(self, mock_sleep, mock_time, mock_check):
        """Test _wait_for_health_endpoint successful wait"""
        mock_time.side_effect = [0, 1, 2]  # Simulate time passing
        mock_check.side_effect = [False, True]  # Fails once, then succeeds
        
        result = _wait_for_health_endpoint(5)
        assert result is True
        assert mock_check.call_count == 2
        mock_sleep.assert_called_once_with(0.5)
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch('syft_objects.auto_install.time.time')
    @patch('syft_objects.auto_install.time.sleep')
    @patch('builtins.print')
    def test_wait_for_health_endpoint_timeout(self, mock_print, mock_sleep, mock_time, mock_check):
        """Test _wait_for_health_endpoint timeout"""
        # Simulate 6 minutes passing (beyond 5 minute timeout)
        mock_time.side_effect = [0, 100, 200, 300, 400]
        mock_check.return_value = False
        
        result = _wait_for_health_endpoint(5)
        assert result is False
        assert "timeout after 5 minutes" in str(mock_print.call_args)
    
    def test_wait_for_syft_objects_server_deprecated(self):
        """Test wait_for_syft_objects_server calls ensure_server_healthy"""
        with patch('syft_objects.auto_install.ensure_server_healthy') as mock_ensure:
            mock_ensure.return_value = True
            
            result = wait_for_syft_objects_server(3)
            assert result is True
            mock_ensure.assert_called_once_with(3)
    
    def test_start_syftbox_app_no_run_script(self, temp_dir):
        """Test start_syftbox_app when run.sh doesn't exist"""
        app_path = temp_dir / "app"
        app_path.mkdir()
        
        with patch('builtins.print') as mock_print:
            result = start_syftbox_app(app_path)
            assert result is False
            assert "run.sh not found" in str(mock_print.call_args)
    
    @patch('subprocess.Popen')
    def test_start_syftbox_app_success(self, mock_popen, temp_dir):
        """Test start_syftbox_app successful start"""
        app_path = temp_dir / "app"
        app_path.mkdir()
        run_script = app_path / "run.sh"
        run_script.touch()
        
        result = start_syftbox_app(app_path)
        assert result is True
        
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        assert args[0] == "bash"
        assert str(run_script) in args
    
    @patch('subprocess.Popen')
    def test_start_syftbox_app_exception(self, mock_popen, temp_dir):
        """Test start_syftbox_app with exception"""
        app_path = temp_dir / "app"
        app_path.mkdir()
        run_script = app_path / "run.sh"
        run_script.touch()
        
        mock_popen.side_effect = Exception("Failed to start")
        
        with patch('builtins.print') as mock_print:
            result = start_syftbox_app(app_path)
            assert result is False
            assert "Failed to start syft-objects app" in str(mock_print.call_args)
    
    @patch('syft_objects.client.get_syftbox_client')
    def test_is_syftbox_running_no_client(self, mock_get_client):
        """Test is_syftbox_running when no client"""
        mock_get_client.return_value = None
        
        result = is_syftbox_running()
        assert result is False
    
    @patch('syft_objects.client.get_syftbox_client')
    @patch('syft_objects.auto_install.requests')
    def test_is_syftbox_running_success(self, mock_requests, mock_get_client):
        """Test is_syftbox_running successful check"""
        mock_client = Mock()
        mock_client.config.client_url = "http://localhost:5000"
        mock_get_client.return_value = mock_client
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "go1.19"
        mock_requests.get.return_value = mock_response
        
        result = is_syftbox_running()
        assert result is True
    
    @patch('syft_objects.client.get_syftbox_client')
    @patch('syft_objects.auto_install.requests')
    def test_is_syftbox_running_not_go(self, mock_requests, mock_get_client):
        """Test is_syftbox_running when response not from Go"""
        mock_client = Mock()
        mock_client.config.client_url = "http://localhost:5000"
        mock_get_client.return_value = mock_client
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "not a go app"
        mock_requests.get.return_value = mock_response
        
        result = is_syftbox_running()
        assert result is False
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    def test_reinstall_syftbox_app_no_syftbox(self, mock_apps_path):
        """Test reinstall_syftbox_app when SyftBox not found"""
        mock_apps_path.return_value = None
        
        result = reinstall_syftbox_app(silent=False)
        assert result is False
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    def test_reinstall_syftbox_app_not_running(self, mock_running, mock_apps_path):
        """Test reinstall_syftbox_app when SyftBox not running"""
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = False
        
        result = reinstall_syftbox_app(silent=False)
        assert result is False
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    @patch('syft_objects.auto_install.clone_syftbox_app')
    @patch('shutil.rmtree')
    def test_reinstall_syftbox_app_success(self, mock_rmtree, mock_clone, 
                                           mock_running, mock_apps_path, temp_dir):
        """Test reinstall_syftbox_app successful reinstall"""
        apps_path = temp_dir / "apps"
        apps_path.mkdir()
        app_dir = apps_path / "syft-objects"
        app_dir.mkdir()
        
        mock_apps_path.return_value = apps_path
        mock_running.return_value = True
        mock_clone.return_value = True
        
        result = reinstall_syftbox_app(silent=False)
        assert result is True
        
        mock_rmtree.assert_called_once_with(app_dir)
        mock_clone.assert_called_once()
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    def test_ensure_syftbox_app_installed_no_syftbox(self, mock_apps_path):
        """Test ensure_syftbox_app_installed when SyftBox not found"""
        mock_apps_path.return_value = None
        
        result = ensure_syftbox_app_installed()
        assert result is False
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    def test_ensure_syftbox_app_installed_not_running(self, mock_running, mock_apps_path):
        """Test ensure_syftbox_app_installed when SyftBox not running"""
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = False
        
        with patch('builtins.print') as mock_print:
            result = ensure_syftbox_app_installed(silent=False)
            assert result is False
            assert "SyftBox is not running" in str(mock_print.call_args_list)
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    @patch('syft_objects.auto_install.is_syftbox_app_installed')
    def test_ensure_syftbox_app_installed_already_installed(self, mock_installed, 
                                                            mock_running, mock_apps_path):
        """Test ensure_syftbox_app_installed when already installed"""
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = True
        mock_installed.return_value = True
        
        result = ensure_syftbox_app_installed()
        assert result is True
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    @patch('syft_objects.auto_install.is_syftbox_app_installed')
    @patch('syft_objects.auto_install.clone_syftbox_app')
    def test_ensure_syftbox_app_installed_auto_install(self, mock_clone, mock_installed,
                                                        mock_running, mock_apps_path):
        """Test ensure_syftbox_app_installed with auto-installation"""
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = True
        mock_installed.return_value = False
        mock_clone.return_value = True
        
        with patch('builtins.print') as mock_print:
            result = ensure_syftbox_app_installed(silent=False)
            assert result is True
            assert "SyftBox detected but syft-objects app not found" in str(mock_print.call_args_list)
            assert "installed successfully" in str(mock_print.call_args_list)
    
    def test_ensure_server_healthy_no_requests_at_module_level(self):
        """Test that requests=None is handled properly"""
        # This tests the behavior when requests is None (simulating lines 13-14)
        with patch('syft_objects.auto_install.requests', None):
            with patch('builtins.print') as mock_print:
                result = ensure_server_healthy()
                assert result is False
                assert "requests library not available" in str(mock_print.call_args)
    
    @patch('subprocess.run')
    def test_clone_syftbox_app_git_not_found(self, mock_run, temp_dir):
        """Test clone_syftbox_app when git binary not found (lines 90-92)"""
        apps_path = temp_dir / "apps"
        
        # Mock git --version to raise FileNotFoundError
        mock_run.side_effect = FileNotFoundError("git not found")
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            with patch('builtins.print') as mock_print:
                result = clone_syftbox_app()
                assert result is False
                assert "Git is not installed" in str(mock_print.call_args_list)
    
    @patch('subprocess.run')
    def test_clone_syftbox_app_unexpected_error(self, mock_run, temp_dir):
        """Test clone_syftbox_app with unexpected error (lines 93-95)"""
        apps_path = temp_dir / "apps"
        
        # Mock git --version to raise unexpected exception
        mock_run.side_effect = Exception("Unexpected error occurred")
        
        with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=apps_path):
            with patch('builtins.print') as mock_print:
                result = clone_syftbox_app()
                assert result is False
                assert "Unexpected error during installation" in str(mock_print.call_args_list)
                assert "Unexpected error occurred" in str(mock_print.call_args_list)
    
    @patch('syft_objects.auto_install._check_health_endpoint')
    @patch('syft_objects.auto_install.get_syftbox_apps_path') 
    @patch('syft_objects.auto_install.is_syftbox_running')
    @patch('syft_objects.auto_install.is_syftbox_app_installed')
    @patch('syft_objects.auto_install.reinstall_syftbox_app')
    def test_ensure_server_healthy_reinstall_failure(self, mock_reinstall, mock_installed,
                                                     mock_running, mock_apps_path, mock_check):
        """Test ensure_server_healthy when reinstall fails (lines 135-136)"""
        mock_check.return_value = False
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = True
        mock_installed.return_value = False
        mock_reinstall.return_value = False  # Reinstall fails
        
        with patch('builtins.print') as mock_print:
            result = ensure_server_healthy()
            assert result is False
            assert "Failed to install syft-objects app" in str(mock_print.call_args_list)
    
    def test_get_server_port_exception(self, temp_dir):
        """Test _get_server_port with exception (lines 164-165)"""
        config_dir = temp_dir / ".syftbox"
        config_dir.mkdir()
        config_file = config_dir / "syft_objects.config"
        config_file.write_text("8004")
        
        # Mock Path.home to return temp_dir
        with patch('syft_objects.auto_install.Path.home', return_value=temp_dir):
            # Mock exists to return True but read_text to raise exception
            with patch.object(Path, 'exists', return_value=True):
                with patch.object(Path, 'read_text', side_effect=Exception("Read error")):
                    port = _get_server_port()
                    assert port is None
    
    @patch('syft_objects.client.get_syftbox_client')
    @patch('syft_objects.auto_install.requests')
    def test_is_syftbox_running_request_exception(self, mock_requests, mock_get_client):
        """Test is_syftbox_running with request exception (lines 248-249)"""
        mock_client = Mock()
        mock_client.config.client_url = "http://localhost:5000"
        mock_get_client.return_value = mock_client
        
        # Mock requests.get to raise exception
        mock_requests.get.side_effect = Exception("Connection error")
        
        result = is_syftbox_running()
        assert result is False
    
    @patch('syft_objects.client.get_syftbox_client')
    def test_is_syftbox_running_client_exception(self, mock_get_client):
        """Test is_syftbox_running with client exception (lines 251-252)"""
        # Mock get_syftbox_client to raise exception
        mock_get_client.side_effect = Exception("Client error")
        
        result = is_syftbox_running()
        assert result is False
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    @patch('shutil.rmtree')
    def test_reinstall_syftbox_app_exception(self, mock_rmtree, mock_running, mock_apps_path, temp_dir):
        """Test reinstall_syftbox_app with exception (lines 298-301)"""
        apps_path = temp_dir / "apps"
        apps_path.mkdir()
        app_dir = apps_path / "syft-objects"
        app_dir.mkdir()
        
        mock_apps_path.return_value = apps_path
        mock_running.return_value = True
        mock_rmtree.side_effect = Exception("Permission denied")
        
        with patch('builtins.print') as mock_print:
            result = reinstall_syftbox_app(silent=False)
            assert result is False
            assert "Error during reinstallation" in str(mock_print.call_args_list)
            assert "Permission denied" in str(mock_print.call_args_list)
    
    @patch('syft_objects.auto_install.get_syftbox_apps_path')
    @patch('syft_objects.auto_install.is_syftbox_running')
    @patch('syft_objects.auto_install.is_syftbox_app_installed')
    @patch('syft_objects.auto_install.clone_syftbox_app')
    def test_ensure_syftbox_app_installed_clone_failure(self, mock_clone, mock_installed,
                                                         mock_running, mock_apps_path):
        """Test ensure_syftbox_app_installed when clone fails (line 337)"""
        mock_apps_path.return_value = Path("/apps")
        mock_running.return_value = True
        mock_installed.return_value = False
        mock_clone.return_value = False  # Clone fails
        
        result = ensure_syftbox_app_installed(silent=True)
        assert result is False
    
