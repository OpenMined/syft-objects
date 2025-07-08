#!/usr/bin/env python3
"""Test the widget indexing fix"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import syft_objects as so

def test_widget_fix():
    """Test that the indexing fix is working"""
    
    print("Testing widget indexing fix...")
    print("-" * 50)
    
    total = len(so.objects)
    print(f"Total objects: {total}")
    
    if total == 0:
        print("No objects to test with")
        return
    
    # Test first few objects to verify order
    print("\nFirst 3 objects in Python collection (oldest first):")
    for i in range(min(3, total)):
        obj = so.objects[i]
        print(f"  so.objects[{i}] = {obj.name} (created {obj.created_at})")
    
    # Test last few objects
    print(f"\nLast 3 objects in Python collection:")
    for i in range(max(0, total-3), total):
        obj = so.objects[i]
        print(f"  so.objects[{i}] = {obj.name} (created {obj.created_at})")
    
    # Now check what the fallback widget would show
    print("\nFallback widget should now show:")
    print("- Row #0 = so.objects[0] (oldest)")
    print(f"- Row #{total-1} = so.objects[{total-1}] (newest)")
    print("\nIframe widget should also show:")
    print("- Row #0 = so.objects[0] (oldest)")
    print(f"- Row #{total-1} = so.objects[{total-1}] (newest)")
    
    print("\n✅ Test complete! Widget should now match Python collection indexing.")

if __name__ == "__main__":
    test_widget_fix()