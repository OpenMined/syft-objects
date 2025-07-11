import syft_objects as so
import os

# Enable debug mode
os.environ["DEBUG_SYFT_OBJECTS"] = "1"

# Force refresh the collection
print("Refreshing collection...")
so.objects.refresh()

# Check how many objects are loaded
print(f"\nTotal objects in collection: {len(so.objects)}")

# List all objects
if len(so.objects) > 0:
    print("\nAll objects:")
    for i, obj in enumerate(so.objects):
        print(f"  {i}: {obj.get_name()} - {obj.get_uid()}")
else:
    print("\nNo objects found in collection")

# Check for specific syftobject.yaml files
from syft_objects.client import get_syftbox_client
client = get_syftbox_client()
if client:
    print(f"\nChecking public/objects directory...")
    public_objects = client.datasites / "liamtrask@gmail.com" / "public" / "objects"
    if public_objects.exists():
        yaml_files = list(public_objects.glob("*.syftobject.yaml"))
        print(f"Found {len(yaml_files)} .syftobject.yaml files:")
        for f in yaml_files:
            print(f"  - {f.name}")
    else:
        print("  Directory does not exist")