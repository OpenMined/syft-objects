#!/usr/bin/env python3
"""Debug widget display to understand the indexing issue"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import syft_objects as so

def debug_widget_display():
    """Debug the widget display to understand indexing"""
    
    print("Debugging widget display...")
    print("-" * 50)
    
    total = len(so.objects)
    print(f"Total objects: {total}")
    
    if total < 5:
        print("Need at least 5 objects for meaningful test")
        return
    
    print(f"\nPython collection order (oldest first):")
    for i in range(min(3, total)):
        obj = so.objects[i]
        print(f"  so.objects[{i}] = {obj.name} (created {obj.created_at})")
    
    print(f"\nLast few objects:")
    for i in range(max(0, total-3), total):
        obj = so.objects[i]
        print(f"  so.objects[{i}] = {obj.name} (created {obj.created_at})")
    
    # Check what widget is being used
    from syft_objects.auto_install import _check_health_endpoint
    server_available = _check_health_endpoint()
    
    print(f"\nWidget mode:")
    if server_available:
        print("  Primary widget: iframe (server available)")
        print("  URL: http://localhost:8004/widget/")
        print("  This uses the React frontend")
    else:
        print("  Fallback widget: local HTML (server not available)")
        print("  This uses the Python-generated HTML")
    
    print(f"\nTo test the indexing issue:")
    print("1. Run 'so.objects' in Jupyter to see the widget")
    print("2. Check if you see an index column with numbers")
    print("3. Note which object is shown at index #0")
    print(f"4. Verify that clicking index #0 matches so.objects[0] = {so.objects[0].name}")
    
    # Test slice indexing too
    print(f"\n5. Test sliced collection 'so.objects[3:5]':")
    sliced = so.objects[3:5]
    for i, obj in enumerate(sliced):
        print(f"   sliced[{i}] should show as index #{3+i} = {obj.name}")

if __name__ == "__main__":
    debug_widget_display()