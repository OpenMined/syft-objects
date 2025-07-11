"""
Test permission management functionality.
"""

import pytest
from pathlib import Path
import syft_perm as sp

def test_set_get_permissions(tmp_path):
    """Test setting and getting permissions on files and folders"""
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    # Create test folder
    test_folder = tmp_path / "test_folder"
    test_folder.mkdir()
    
    # Test file permissions
    sp.set_permissions(str(test_file), read_users=["user1@example.com"], write_users=["user2@example.com"])
    perms = sp.get_permissions(str(test_file))
    assert perms["read"] == ["user1@example.com"]
    assert perms["write"] == ["user2@example.com"]
    
    # Test folder permissions without subfolders
    sp.set_permissions(str(test_folder), read_users=["user3@example.com"], write_users=["user4@example.com"], including_subfolders=False)
    perms = sp.get_permissions(str(test_folder))
    assert perms["read"] == ["user3@example.com"]
    assert perms["write"] == ["user4@example.com"]
    
    # Test folder permissions with subfolders
    sp.set_permissions(str(test_folder), read_users=["user5@example.com"], write_users=["user6@example.com"], including_subfolders=True)
    perms = sp.get_permissions(str(test_folder))
    assert perms["read"] == ["user5@example.com"]
    assert perms["write"] == ["user6@example.com"]

def test_invalid_path_type():
    """Test that setting permissions on wrong path type raises error"""
    with pytest.raises(ValueError, match="not a directory"):
        sp.set_folder_permissions("nonexistent.txt", read_users=["user@example.com"])
    
    with pytest.raises(ValueError, match="not a file"):
        sp.set_file_permissions("nonexistent/", read_users=["user@example.com"])

def test_public_permissions(tmp_path):
    """Test setting public permissions"""
    test_file = tmp_path / "public.txt"
    test_file.write_text("public content")
    
    sp.set_permissions(str(test_file), read_users=["*"], write_users=["admin@example.com"])
    perms = sp.get_permissions(str(test_file))
    assert perms["read"] == ["*"]
    assert perms["write"] == ["admin@example.com"]

def test_remove_permissions(tmp_path):
    """Test removing permissions"""
    test_file = tmp_path / "removable.txt"
    test_file.write_text("test content")
    
    # Set initial permissions
    sp.set_permissions(str(test_file), read_users=["user@example.com"], write_users=["admin@example.com"])
    
    # Remove permissions
    sp.remove_file_permissions(str(test_file))
    
    # Verify permissions are gone
    perms = sp.get_permissions(str(test_file))
    assert perms is None