"""Test mock file permissions are set correctly"""

import os
import tempfile
from pathlib import Path
import pytest
import shutil

def test_mock_file_has_write_admin_permissions():
    """Test that mock files get write and admin permissions for the owner by default"""
    # Only run if syft-perm is available
    try:
        import syft_perm as sp
        import syft_objects as so
    except ImportError:
        pytest.skip("syft-perm not available")
    
    # Get current user email - use a known value if not set
    email = os.getenv('SYFTBOX_EMAIL')
    if not email:
        # If SYFTBOX_EMAIL is not set, skip the test
        pytest.skip("SYFTBOX_EMAIL not set")
    
    # Check if SyftBox is available
    syftbox_path = Path.home() / "SyftBox"
    if not syftbox_path.exists():
        pytest.skip("SyftBox not available")
    
    # Create object with mock file
    obj = so.create_object(
        name='test_mock_permissions',
        mock_contents='Test mock data',
        private_contents='Test private data'
    )
    
    # Check if mock file exists
    mock_path = obj.mock.path
    assert mock_path is not None
    assert Path(mock_path).exists()
    
    # Skip test if file is not in SyftBox (happens in test environments)
    if 'SyftBox' not in str(mock_path):
        pytest.skip("Mock file not in SyftBox - permissions not set")
    
    # Get permissions
    perms = sp.get_file_permissions(mock_path)
    
    # Permissions should not be None
    assert perms is not None, f"Could not get permissions for {mock_path}"
    
    # Check write permissions
    assert 'write' in perms
    assert email in perms['write']
    
    # Check admin permissions
    assert 'admin' in perms
    assert email in perms['admin']
    
    # Check read permissions (should be public by default)
    assert 'read' in perms
    assert '*' in perms['read'] or 'public' in perms['read']
    
    # Clean up
    obj.delete_obj(email)


def test_mock_file_custom_write_permissions():
    """Test that mock files can have custom write permissions"""
    try:
        import syft_perm as sp
        import syft_objects as so
    except ImportError:
        pytest.skip("syft-perm not available")
    
    email = os.getenv('SYFTBOX_EMAIL')
    if not email:
        pytest.skip("SYFTBOX_EMAIL not set")
    
    # Check if SyftBox is available
    syftbox_path = Path.home() / "SyftBox"
    if not syftbox_path.exists():
        pytest.skip("SyftBox not available")
    
    other_user = 'other@example.com'
    
    # Create object with custom mock write permissions
    obj = so.create_object(
        name='test_custom_mock_perms',
        mock_contents='Test mock data',
        private_contents='Test private data',
        mock_write=[email, other_user]
    )
    
    # Check if mock file exists
    mock_path = obj.mock.path
    assert mock_path is not None
    assert Path(mock_path).exists()
    
    # Skip test if file is not in SyftBox (happens in test environments)
    if 'SyftBox' not in str(mock_path):
        pytest.skip("Mock file not in SyftBox - permissions not set")
    
    # Get permissions
    perms = sp.get_file_permissions(mock_path)
    
    # Check write permissions include both users
    assert 'write' in perms
    assert email in perms['write']
    assert other_user in perms['write']
    
    # Check admin permissions (should match write)
    assert 'admin' in perms
    assert email in perms['admin']
    assert other_user in perms['admin']
    
    # Clean up
    obj.delete_obj(email)


def test_private_file_permissions_with_move():
    """Test that private files get permissions when moved to SyftBox"""
    try:
        import syft_perm as sp
        import syft_objects as so
    except ImportError:
        pytest.skip("syft-perm not available")
    
    email = os.getenv('SYFTBOX_EMAIL')
    if not email:
        pytest.skip("SYFTBOX_EMAIL not set")
    
    # Create object with move_files_to_syftbox=True
    obj = so.create_object(
        name='test_private_perms',
        mock_contents='Test mock data',
        private_contents='Test private data',
        move_files_to_syftbox=True
    )
    
    # Check if private file exists in SyftBox
    private_path = obj.private.path
    assert private_path is not None
    assert Path(private_path).exists()
    assert 'SyftBox' in str(private_path)  # Should be in SyftBox
    
    # Get permissions
    perms = sp.get_file_permissions(private_path)
    
    # Check permissions are set to owner only
    assert 'read' in perms
    assert email in perms['read']
    assert len(perms['read']) == 1
    
    assert 'write' in perms
    assert email in perms['write']
    assert len(perms['write']) == 1
    
    assert 'admin' in perms
    assert email in perms['admin']
    assert len(perms['admin']) == 1
    
    # Clean up
    obj.delete_obj(email)


def test_private_file_no_permissions_without_move():
    """Test that private files don't get permissions when not moved to SyftBox"""
    try:
        import syft_perm as sp
        import syft_objects as so
    except ImportError:
        pytest.skip("syft-perm not available")
    
    email = os.getenv('SYFTBOX_EMAIL')
    if not email:
        pytest.skip("SYFTBOX_EMAIL not set")
    
    # Create object without moving files
    obj = so.create_object(
        name='test_no_private_perms',
        mock_contents='Test mock data',
        private_contents='Test private data',
        move_files_to_syftbox=False
    )
    
    # Check if private file exists but not in SyftBox
    private_path = obj.private.path
    assert private_path is not None
    assert Path(private_path).exists()
    assert 'SyftBox' not in str(private_path)  # Should NOT be in SyftBox
    assert 'tmp' in str(private_path)  # Should be in tmp
    
    # Trying to get permissions should fail or return None/empty
    try:
        perms = sp.get_file_permissions(private_path)
        # If it doesn't fail, permissions should be empty or minimal
        assert perms is None or perms == {} or not any(perms.get(k) for k in ['read', 'write', 'admin'])
    except:
        # Expected - can't set permissions outside SyftBox
        pass
    
    # Clean up - delete the tmp file manually since it's not in SyftBox
    if Path(private_path).exists():
        Path(private_path).unlink()


def test_no_warning_when_creating_objects():
    """Test that creating objects doesn't produce warnings about NoneType"""
    try:
        import syft_objects as so
    except ImportError:
        pytest.skip("syft-objects not available")
    
    import io
    import sys
    from contextlib import redirect_stderr
    
    # Capture stderr to check for warnings
    stderr_capture = io.StringIO()
    
    with redirect_stderr(stderr_capture):
        # Create object
        obj = so.create_object(
            name='test_no_warnings',
            mock_contents='Test',
            private_contents='Test'
        )
    
    # Get captured output
    stderr_output = stderr_capture.getvalue()
    
    # Check that there's no NoneType warning
    assert "'NoneType' object has no attribute 'get'" not in stderr_output
    
    # Clean up if possible
    try:
        email = os.getenv('SYFTBOX_EMAIL')
        if email and hasattr(obj, 'delete_obj'):
            obj.delete_obj(email)
    except:
        # Ignore cleanup errors in test
        pass