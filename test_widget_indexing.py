#!/usr/bin/env python3
"""Test to understand the widget indexing issue"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import syft_objects as so

def test_widget_indexing():
    """Test to understand widget indexing"""
    
    print("Understanding the widget indexing issue...")
    print("-" * 50)
    
    total = len(so.objects)
    print(f"Total objects: {total} (Python indices: 0 to {total-1})")
    
    # The user says:
    # - "when i select so.objects[0] i get the object from #173"
    # - With 173 objects, there's no #173 in 0-based indexing
    # - So the widget must be showing 1-based indices: #1 to #173
    
    print("\nIf widget shows 1-based indexing (#1 to #173):")
    print("- Widget #1 should correspond to so.objects[0]")
    print("- Widget #173 should correspond to so.objects[172]")
    
    print("\nBut user says so.objects[0] returns what's shown as #173")
    print("This means:")
    print("- Widget #173 = so.objects[0] (oldest object)")
    print("- Widget #1 = so.objects[172] (newest object)")
    print("- So widget is showing objects in REVERSE order with 1-based indexing")
    
    print("\nTo fix this, the widget should show:")
    print("- Row #0 = so.objects[0] (oldest)")
    print("- Row #172 = so.objects[172] (newest)")
    print("- Using 0-based indexing to match Python")
    
    # Show what's currently at key indices
    print(f"\nCurrent objects at key indices:")
    print(f"so.objects[0] = {so.objects[0].name} (oldest)")
    print(f"so.objects[172] = {so.objects[172].name} (newest)")

if __name__ == "__main__":
    test_widget_indexing()