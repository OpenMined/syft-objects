#!/usr/bin/env python3
"""Test that mock write permissions include admin by default"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from syft_objects import create_object

def test_mock_write_permissions():
    """Test that admin has write access to mock by default"""
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up temporary test environment
        test_dir = Path(temp_dir)
        
        # Create test object with minimal parameters
        obj = create_object(
            name="test_object",
            mock_contents="test mock content",
            private_contents="test private content"
        )
        
        print(f"Created object: {obj.name}")
        print(f"Admin email: {obj.private_permissions[0] if obj.private_permissions else 'None'}")
        print(f"Mock read permissions: {obj.mock_permissions}")
        print(f"Mock write permissions: {obj.mock_write_permissions}")
        print(f"Private read permissions: {obj.private_permissions}")
        print(f"Private write permissions: {obj.private_write_permissions}")
        
        # Check that admin has mock write access
        admin_email = obj.private_permissions[0] if obj.private_permissions else None
        
        # Test 1: Admin should have mock write access
        if admin_email and admin_email in obj.mock_write_permissions:
            print("✅ PASS: Admin has mock write access")
            return True
        else:
            print("❌ FAIL: Admin does not have mock write access")
            return False

if __name__ == "__main__":
    success = test_mock_write_permissions()
    sys.exit(0 if success else 1)