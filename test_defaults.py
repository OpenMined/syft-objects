#!/usr/bin/env python3
"""
Test script to examine the default values in syobj function
"""

from syft_objects import syobj
from pathlib import Path

def main():
    print("🔍 Testing syobj default values...")
    
    # ===========================================
    # Test 1: Minimal call - no parameters
    # ===========================================
    print("\n1. Testing minimal syobj() call (no parameters)...")
    
    minimal_obj = syobj()
    
    print(f"✅ Created minimal object: {minimal_obj.uid}")
    print(f"   Name: {minimal_obj.name}")
    print(f"   Description: {minimal_obj.description}")
    print("")
    print("📋 PERMISSION DEFAULTS:")
    print(f"   Discovery (syftobject_permissions): {minimal_obj.syftobject_permissions}")
    print(f"   Mock Read (mock_permissions): {minimal_obj.mock_permissions}")
    print(f"   Mock Write (mock_write_permissions): {minimal_obj.mock_write_permissions}")
    print(f"   Private Read (private_permissions): {minimal_obj.private_permissions}")
    print(f"   Private Write (private_write_permissions): {minimal_obj.private_write_permissions}")
    print("")
    print("📁 FILE OPERATION DEFAULTS:")
    file_ops = minimal_obj.metadata.get("_file_operations", {})
    print(f"   Auto-save: {file_ops.get('auto_save', 'not set')}")
    print(f"   Move to SyftBox: {file_ops.get('move_files_to_syftbox', 'not set')}")
    print(f"   Create SyftBox permissions: {file_ops.get('create_syftbox_permissions', 'not set')}")
    print(f"   Keep files in place: {file_ops.get('keep_files_in_place', False)}")
    print(f"   SyftBox available: {file_ops.get('syftbox_available', False)}")
    
    print("\n" + "="*60)
    
    # ===========================================
    # Test 2: With existing file
    # ===========================================
    print("\n2. Testing syobj with existing file...")
    
    # Use widget file if it exists
    widget_file = Path("widget_test.html")
    if widget_file.exists():
        file_obj = syobj(private_file=str(widget_file))
        
        print(f"✅ Created file-based object: {file_obj.uid}")
        print(f"   Name: {file_obj.name}")
        print("")
        print("📋 PERMISSION DEFAULTS (with file):")
        print(f"   Discovery: {file_obj.syftobject_permissions}")
        print(f"   Mock Read: {file_obj.mock_permissions}")
        print(f"   Mock Write: {file_obj.mock_write_permissions}")
        print(f"   Private Read: {file_obj.private_permissions}")
        print(f"   Private Write: {file_obj.private_write_permissions}")
    else:
        print("❌ Widget file not found - skipping file test")
    
    print("\n" + "="*60)
    
    # ===========================================
    # Test 3: Explicit custom permissions
    # ===========================================
    print("\n3. Testing syobj with custom permissions...")
    
    custom_obj = syobj(
        name="Custom Permissions Test",
        private_read=["alice@company.com", "bob@company.com"],
        private_write=["alice@company.com"],
        mock_read=["team@company.com"],
        mock_write=["admin@company.com"],
        discovery_read=["public"]  # Note: this maps to syftobject_permissions
    )
    
    print(f"✅ Created custom permissions object: {custom_obj.uid}")
    print("")
    print("📋 CUSTOM PERMISSIONS:")
    print(f"   Discovery: {custom_obj.syftobject_permissions}")
    print(f"   Mock Read: {custom_obj.mock_permissions}")
    print(f"   Mock Write: {custom_obj.mock_write_permissions}")
    print(f"   Private Read: {custom_obj.private_permissions}")
    print(f"   Private Write: {custom_obj.private_write_permissions}")
    
    print("\n" + "="*60)
    
    # ===========================================
    # Analysis: Are the defaults secure?
    # ===========================================
    print("\n🔒 SECURITY ANALYSIS OF DEFAULTS:")
    print("")
    print("✅ GOOD DEFAULTS:")
    print("   • Discovery = ['public'] → Anyone can see the object exists")
    print("   • Mock Read = ['public'] → Demo data is publicly readable")
    print("   • Mock Write = [user_email] → Only creator can modify demo data by default")
    print("   • Private Write = [user_email] → Only creator can modify private data")
    print("")
    print("✅ REASONABLE DEFAULTS:")
    print("   • Private Read = [user_email] → Only creator can read private data")
    print("   • Auto-save = True → Objects are saved automatically")
    print("   • Move to SyftBox = True → Files integrated with sharing system")
    print("   • Keep files in place = False → Uses SyftBox for proper sharing")
    print("   • Smart inference: If permissions are single-user, keeps files in place")
    print("")
    print("⚠️  POTENTIAL CONCERNS:")
    print("   • Mock data is PUBLIC by default - could leak info if not careful")
    print("   • Discovery is PUBLIC - object existence is always visible")
    print("   • Default email detection might fallback to 'user@example.com'")
    print("")
    print("🎯 RECOMMENDATIONS:")
    print("   • Always review mock data before making it public")
    print("   • Explicitly set private_read for sensitive data")
    print("   • Consider setting discovery_read to specific users for secret objects")
    print("   • Test email detection in your environment")
    print("   • New: Single-user workflows now automatically keep files in place for efficiency")
    
    print("\n🎉 Default values analysis complete!")


if __name__ == "__main__":
    main() 