"""Tests for auto-installation functionality."""

import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from syft_objects.auto_install import (
    get_syftbox_apps_path,
    is_syftbox_app_installed,
    clone_syftbox_app,
    ensure_syftbox_app_installed
)


class TestAutoInstall:
    """Test cases for auto-installation functionality."""

    def test_get_syftbox_apps_path_exists(self):
        """Test getting SyftBox apps path when SyftBox exists."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            syftbox_path = tmp_path / "SyftBox"
            syftbox_path.mkdir()
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                result = get_syftbox_apps_path()
                expected = tmp_path / "SyftBox" / "apps"
                assert result == expected

    def test_get_syftbox_apps_path_not_exists(self):
        """Test getting SyftBox apps path when SyftBox doesn't exist."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                result = get_syftbox_apps_path()
                assert result is None

    def test_is_syftbox_app_installed_true(self):
        """Test checking if app is installed when it exists."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            syftbox_path = tmp_path / "SyftBox"
            apps_path = syftbox_path / "apps"
            app_path = apps_path / "syft-objects"
            app_path.mkdir(parents=True)
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                result = is_syftbox_app_installed()
                assert result is True

    def test_is_syftbox_app_installed_false(self):
        """Test checking if app is installed when it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            syftbox_path = tmp_path / "SyftBox"
            syftbox_path.mkdir()
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                result = is_syftbox_app_installed()
                assert result is False

    def test_is_syftbox_app_installed_no_syftbox(self):
        """Test checking if app is installed when SyftBox doesn't exist."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                result = is_syftbox_app_installed()
                assert result is False

    @patch('syft_objects.auto_install.subprocess.run')
    def test_clone_syftbox_app_success(self, mock_run):
        """Test successful cloning of syft-objects app."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            syftbox_path = tmp_path / "SyftBox"
            syftbox_path.mkdir()
            
            # Mock successful git operations
            mock_run.side_effect = [
                MagicMock(returncode=0),  # git --version
                MagicMock(returncode=0, stderr="")  # git clone
            ]
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                with patch('builtins.print'):  # Suppress print output
                    result = clone_syftbox_app()
                    assert result is True

    @patch('syft_objects.auto_install.subprocess.run')
    def test_clone_syftbox_app_git_not_available(self, mock_run):
        """Test cloning when git is not available."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            syftbox_path = tmp_path / "SyftBox"
            syftbox_path.mkdir()
            
            # Mock git not available
            mock_run.side_effect = FileNotFoundError()
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                with patch('builtins.print'):  # Suppress print output
                    result = clone_syftbox_app()
                    assert result is False

    def test_clone_syftbox_app_no_syftbox(self):
        """Test cloning when SyftBox doesn't exist."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            with patch('syft_objects.auto_install.Path.home', return_value=tmp_path):
                with patch('builtins.print'):  # Suppress print output
                    result = clone_syftbox_app()
                    assert result is False

    def test_ensure_syftbox_app_installed_already_exists(self):
        """Test ensure function when app is already installed."""
        with patch('syft_objects.auto_install.is_syftbox_app_installed', return_value=True):
            result = ensure_syftbox_app_installed()
            assert result is True

    def test_ensure_syftbox_app_installed_no_syftbox(self):
        """Test ensure function when SyftBox doesn't exist."""
        with patch('syft_objects.auto_install.is_syftbox_app_installed', return_value=False):
            with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=None):
                result = ensure_syftbox_app_installed()
                assert result is False

    def test_ensure_syftbox_app_installed_needs_installation(self):
        """Test ensure function when app needs to be installed."""
        with patch('syft_objects.auto_install.is_syftbox_app_installed', return_value=False):
            with patch('syft_objects.auto_install.get_syftbox_apps_path', return_value=Path("/fake/apps")):
                with patch('syft_objects.auto_install.clone_syftbox_app', return_value=True):
                    with patch('builtins.print'):  # Suppress print output
                        result = ensure_syftbox_app_installed()
                        assert result is True 