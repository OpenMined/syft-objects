#!/usr/bin/env python3
"""
Example: Using reference_only flag to avoid file copying

This example demonstrates the new reference_only flag that allows creating
syft objects that reference files in place without copying them to SyftBox.
"""

import sys
from pathlib import Path

# Add the source directory to the path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import syft_objects as syo


def main():
    print("🔐 SyftObjects Reference-Only Example")
    print("=" * 50)
    
    # Create a sample data file
    data_file = Path("my_data.txt")
    data_file.write_text("This is my important data that I want to share securely!")
    
    print(f"📄 Created sample file: {data_file.absolute()}")
    
    # Example 1: Normal mode (copies files to SyftBox)
    print("\n1️⃣ Normal mode (files copied to SyftBox):")
    try:
        normal_obj = syo.syobj(
            name="Normal Dataset",
            private_file=str(data_file),
            metadata={"description": "Dataset shared via SyftBox"}
        )
        print(f"   ✅ Private URL: {normal_obj.private_url}")
        print(f"   ✅ Mock URL: {normal_obj.mock_url}")
        print("   📁 Files were copied to SyftBox directories")
    except Exception as e:
        print(f"   ⚠️ SyftBox not configured: {e}")
    
    # Example 2: Reference-only mode (files stay in place)
    print("\n2️⃣ Reference-only mode (files stay in place):")
    try:
        reference_obj = syo.syobj(
            name="Reference Dataset",
            private_file=str(data_file),
            reference_only=True,  # 🔑 Key flag!
            metadata={
                "description": "Dataset referenced in place",
                "save_to": "my_dataset.syftobject.yaml"
            }
        )
        print(f"   ✅ Private URL: {reference_obj.private_url}")
        print(f"   ✅ Mock URL: {reference_obj.mock_url}")
        print(f"   ✅ Metadata file: {reference_obj.syftobject}")
        print("   📌 Original file referenced in place (not copied)")
        
        # Verify the original file is still there
        if data_file.exists():
            print(f"   ✅ Original file still exists: {data_file.absolute()}")
        
    except Exception as e:
        print(f"   ❌ Reference-only failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 3: Using reference_only via metadata
    print("\n3️⃣ Reference-only via metadata:")
    try:
        metadata_obj = syo.syobj(
            name="Metadata Reference Dataset",
            private_file=str(data_file),
            metadata={
                "reference_only": True,  # 🔑 Can also be set in metadata
                "description": "Dataset with reference_only in metadata",
                "save_to": "metadata_dataset.syftobject.yaml"
            }
        )
        print(f"   ✅ Created with reference_only in metadata")
        print(f"   ✅ Private URL: {metadata_obj.private_url}")
        
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n🎉 Examples completed!")
    print("\nKey benefits of reference_only=True:")
    print("  • Files stay in their original location")
    print("  • No unnecessary copying or moving")
    print("  • Perfect for large datasets or files you want to keep in place")
    print("  • Still get all SyftObjects benefits (permissions, metadata, etc.)")
    
    # Cleanup
    data_file.unlink(missing_ok=True)
    Path("my_dataset.syftobject.yaml").unlink(missing_ok=True)
    Path("metadata_dataset.syftobject.yaml").unlink(missing_ok=True)


if __name__ == "__main__":
    main()