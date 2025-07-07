#!/usr/bin/env python3
"""Test the clean API wrapper"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import syft_objects as so

def test_clean_api():
    """Test that the clean API hides Pydantic complexity"""
    
    print("Testing clean API wrapper...")
    print("-" * 50)
    
    # Create an object
    obj = so.create_object(
        name="test_clean_api",
        mock_contents="This is mock data",
        private_contents="This is private data"
    )
    
    print(f"Created object: {obj}")
    print(f"Type: {type(obj)}")
    
    # Test basic properties
    print(f"\nBasic properties:")
    print(f"  name: {obj.name}")
    print(f"  uid: {obj.uid}")
    print(f"  type: {obj.type}")
    print(f"  description: {obj.description}")
    
    # Test data access
    print(f"\nData access:")
    print(f"  mock data: {obj.mock.obj}")
    print(f"  private data: {obj.private.obj}")
    
    # Test permissions
    print(f"\nPermissions:")
    for perm_type, emails in obj.permissions.items():
        print(f"  {perm_type}: {emails}")
    
    # Test URLs
    print(f"\nURLs:")
    for url_type, url in obj.urls.items():
        print(f"  {url_type}: {url}")
    
    # Test info method
    print(f"\nInfo method:")
    info = obj.info()
    print(f"  Keys: {list(info.keys())}")
    
    # Check what's in dir()
    print(f"\nClean API dir() output:")
    attrs = [a for a in dir(obj) if not a.startswith('_')]
    print(f"  Public attributes ({len(attrs)}): {attrs}")
    
    # Compare to raw object
    raw_obj = obj._raw()
    raw_attrs = [a for a in dir(raw_obj) if not a.startswith('_') and not a.startswith('model_') and 'pydantic' not in a]
    print(f"\nRaw object has {len(dir(raw_obj))} total attributes")
    print(f"Clean object has {len(dir(obj))} total attributes")
    
    print("\n✅ Clean API test complete!")
    
    # Cleanup
    obj.delete()

if __name__ == "__main__":
    test_clean_api()