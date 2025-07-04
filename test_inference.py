#!/usr/bin/env python3
"""
Test script to verify the new inference logic for keep_files_in_place 
and the updated mock_write default
"""

from syft_objects import syobj
from pathlib import Path

def main():
    print("🧪 Testing inference logic and mock_write default changes...")
    
    # ===========================================
    # Test 1: Default behavior (should infer keep_files_in_place=True)
    # ===========================================
    print("\n1. Testing default behavior (should infer keep_files_in_place=True)...")
    
    default_obj = syobj(name="Default Test")
    
    print(f"✅ Created object: {default_obj.name}")
    print(f"   Keep files in place: {default_obj.metadata.get('_keep_files_in_place', False)}")
    print(f"   Mock write permissions: {default_obj.mock_write_permissions}")
    
    # ===========================================
    # Test 2: With shared permissions (should NOT infer keep_files_in_place)
    # ===========================================
    print("\n2. Testing with shared permissions (should NOT infer keep_files_in_place)...")
    
    shared_obj = syobj(
        name="Shared Test",
        private_read=["user@example.com", "alice@company.com"],  # Multiple users
        private_write=["user@example.com"]
    )
    
    print(f"✅ Created object: {shared_obj.name}")
    print(f"   Keep files in place: {shared_obj.metadata.get('_keep_files_in_place', False)}")
    print(f"   Private read: {shared_obj.private_permissions}")
    print(f"   Private write: {shared_obj.private_write_permissions}")
    
    # ===========================================
    # Test 3: Explicitly setting keep_files_in_place=False (should override inference)
    # ===========================================
    print("\n3. Testing explicit keep_files_in_place=False (should override inference)...")
    
    explicit_obj = syobj(
        name="Explicit Test",
        keep_files_in_place=False  # Explicitly set to False
    )
    
    print(f"✅ Created object: {explicit_obj.name}")
    print(f"   Keep files in place: {explicit_obj.metadata.get('_keep_files_in_place', False)}")
    print(f"   Mock write permissions: {explicit_obj.mock_write_permissions}")
    
    # ===========================================
    # Test 4: With empty permissions (should infer keep_files_in_place=True)
    # ===========================================
    print("\n4. Testing with empty permissions (should infer keep_files_in_place=True)...")
    
    empty_obj = syobj(
        name="Empty Permissions Test",
        private_read=[],
        private_write=[]
    )
    
    print(f"✅ Created object: {empty_obj.name}")
    print(f"   Keep files in place: {empty_obj.metadata.get('_keep_files_in_place', False)}")
    print(f"   Private read: {empty_obj.private_permissions}")
    print(f"   Private write: {empty_obj.private_write_permissions}")
    
    # ===========================================
    # Test 5: With existing file (should still apply inference)
    # ===========================================
    print("\n5. Testing with existing file (should still apply inference)...")
    
    widget_file = Path("widget_test.html")
    if widget_file.exists():
        file_obj = syobj(
            name="File Test",
            private_file=str(widget_file)
        )
        
        print(f"✅ Created object: {file_obj.name}")
        print(f"   Keep files in place: {file_obj.metadata.get('_keep_files_in_place', False)}")
        print(f"   Private file: {file_obj.private_url}")
        print(f"   Mock write permissions: {file_obj.mock_write_permissions}")
    else:
        print("❌ Widget file not found - skipping file test")
    
    print("\n" + "="*60)
    
    # ===========================================
    # Summary of changes
    # ===========================================
    print("\n📋 SUMMARY OF CHANGES:")
    print("")
    print("✅ mock_write default changed from [] to [user_email]")
    print("✅ keep_files_in_place inference logic added:")
    print("   • If private_read and private_write are both [user_email] or []")
    print("   • AND keep_files_in_place was not explicitly set")
    print("   • THEN keep_files_in_place = True automatically")
    print("")
    print("🎯 This makes single-user workflows more efficient by default!")
    
    print("\n🎉 Testing complete!")


if __name__ == "__main__":
    main() 