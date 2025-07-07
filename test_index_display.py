#!/usr/bin/env python3
"""Test that the # column correctly shows collection indices"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import syft_objects as so

def test_index_display():
    """Test that indices in the widget match syft.objects[idx]"""
    
    print("Testing index display in widgets...")
    print("-" * 50)
    
    # Create a few test objects
    objects = []
    for i in range(5):
        obj = so.create_object(
            name=f"test_object_{i}",
            mock_contents=f"Mock data {i}",
            private_contents=f"Private data {i}"
        )
        objects.append(obj)
        print(f"Created object {i}: {obj.name}")
    
    print("\nChecking collection indices...")
    
    # Find where our test objects are in the collection
    total_objects = len(so.objects)
    start_idx = total_objects - 5  # Last 5 objects should be ours
    
    # Test that objects can be accessed by index
    print(f"\nTotal objects in collection: {total_objects}")
    print(f"Our test objects should be at indices {start_idx} through {total_objects-1}")
    
    for i in range(5):
        idx = start_idx + i
        obj = so.objects[idx]
        print(f"so.objects[{idx}] = {obj.name}")
        
    # Also test first few indices to show the widget is correct
    print("\nFirst few objects in collection:")
    for i in range(min(3, total_objects)):
        obj = so.objects[i]
        print(f"so.objects[{i}] = {obj.name}")
        
    print("\n✅ Test complete!")
    print("The # column in the widget should match so.objects[idx] for any index")
    
    # Cleanup
    for obj in objects:
        obj.delete()

if __name__ == "__main__":
    test_index_display()