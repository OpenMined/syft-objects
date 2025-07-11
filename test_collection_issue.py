import syft_objects as so
import os
import time

# Create a simple test object
print("Creating test object...")
test_obj = so.create_object(
    name="Collection Test Object",
    mock_contents="Mock data for testing",
    private_contents="Private data for testing"
)

print(f"Created object with UID: {test_obj.get_uid()}")

# Wait a moment for filesystem
time.sleep(0.5)

# Check if it's in the collection
print("\nChecking if object is in collection...")
try:
    found = so.objects[test_obj.get_uid()]
    print(f"✅ Object found in collection: {found}")
except KeyError:
    print(f"❌ Object NOT found in collection")

# Force refresh and try again
print("\nForcing collection refresh...")
so.objects.refresh()

print("Checking again after refresh...")
try:
    found = so.objects[test_obj.get_uid()]
    print(f"✅ Object found after refresh: {found}")
except KeyError:
    print(f"❌ Object still NOT found after refresh")

# Check the syftobject file directly
print("\nChecking syftobject file...")
from syft_objects.client import get_syftbox_client
client = get_syftbox_client()
if client:
    # Get the syftobject path from the object
    syftobj_config = test_obj.syftobject_config
    syftobj_path = syftobj_config.get_path() if syftobj_config else None
    
    print(f"Syftobject path: {syftobj_path}")
    if syftobj_path and os.path.exists(syftobj_path):
        print(f"✅ Syftobject file exists")
        
        # Try loading it directly
        from syft_objects.models import SyftObject
        from syft_objects.clean_api import CleanSyftObject
        try:
            direct_obj = SyftObject._load_yaml(syftobj_path)
            clean_obj = CleanSyftObject(direct_obj)
            print(f"✅ Can load object directly: {clean_obj.get_uid()}")
        except Exception as e:
            print(f"❌ Error loading directly: {e}")
    else:
        print(f"❌ Syftobject file not found")