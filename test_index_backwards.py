#!/usr/bin/env python3
"""Test to check if indices are backwards in the main widget"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import syft_objects as so

def test_index_backwards():
    """Test if indices in the widget are backwards"""
    
    print("Testing if indices are backwards...")
    print("-" * 50)
    
    # First, let's see how many objects we have
    total = len(so.objects)
    print(f"Total objects in collection: {total}")
    
    # Check first and last objects
    if total > 0:
        first_obj = so.objects[0]
        last_obj = so.objects[-1]
        
        print(f"\nso.objects[0]:")
        print(f"  Name: {first_obj.name}")
        print(f"  Created: {first_obj.created_at}")
        
        print(f"\nso.objects[-1]:")  
        print(f"  Name: {last_obj.name}")
        print(f"  Created: {last_obj.created_at}")
        
        # Check if dates are in expected order
        if first_obj.created_at and last_obj.created_at:
            if first_obj.created_at < last_obj.created_at:
                print("\n✓ Objects are sorted correctly (oldest first)")
            else:
                print("\n✗ Objects appear to be sorted newest first!")
                
        # Let's also check a few more indices to see the pattern
        print(f"\nChecking indices around the reported issue (index 0 showing as #{total-1}):")
        indices_to_check = [0, 1, 2, total-3, total-2, total-1]
        
        for idx in indices_to_check:
            if 0 <= idx < total:
                obj = so.objects[idx]
                print(f"  so.objects[{idx}] = {obj.name} (created {obj.created_at})")
                
    # Now let's check what the widget shows
    print("\nTo verify the widget display:")
    print("1. In Jupyter, run: so.objects")
    print("2. Check what object is shown in row #0")
    print("3. Compare with so.objects[0] - they should match")
    print(f"4. If row #0 shows '{so.objects[-1].name if total > 0 else 'N/A'}', then indices are backwards")

if __name__ == "__main__":
    test_index_backwards()