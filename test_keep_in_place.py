#!/usr/bin/env python3
"""
Test script demonstrating the new keep_files_in_place functionality
"""

from syft_objects import syobj
from pathlib import Path

def main():
    print("🔄 Testing keep_files_in_place functionality...")
    
    # ===========================================
    # Test 1: Regular behavior (copies files)
    # ===========================================
    print("\n1. Testing regular behavior (files copied to SyftBox)...")
    
    csv_file = Path("tmp/sales_data.csv")
    if csv_file.exists():
        regular_obj = syobj(
            name="Regular Sales Data",
            private_file=str(csv_file),
            keep_files_in_place=False,  # Default behavior
            private_read=["sales@company.com"],
            mock_read=["public"],
            metadata={"auto_save": True}
        )
        print(f"✅ Created regular object: {regular_obj.uid}")
        print(f"   Private URL: {regular_obj.private_url}")
        print(f"   Private Path: {regular_obj.private_path}")
        print(f"   File exists: {Path(regular_obj.private_path).exists() if regular_obj.private_path else 'No path'}")
        print(f"   Original file still exists: {csv_file.exists()}")
        print(f"   Metadata has keep_files_in_place: {regular_obj.metadata.get('_keep_files_in_place', False)}")
    else:
        print("❌ CSV file not found - skipping regular test")
    
    print("\n" + "="*60)
    
    # ===========================================
    # Test 2: Keep files in place (no copying)
    # ===========================================
    print("\n2. Testing keep_files_in_place=True...")
    
    html_file = Path("widget_test.html")
    if html_file.exists():
        keep_in_place_obj = syobj(
            name="Widget Test (In Place)",
            private_file=str(html_file),
            keep_files_in_place=True,  # NEW: Don't copy files
            private_read=["developer@company.com"],
            mock_read=["public"],
            metadata={"auto_save": True}
        )
        print(f"✅ Created keep-in-place object: {keep_in_place_obj.uid}")
        print(f"   Private URL: {keep_in_place_obj.private_url}")
        print(f"   Private Path: {keep_in_place_obj.private_path}")
        print(f"   File exists at resolved path: {Path(keep_in_place_obj.private_path).exists() if keep_in_place_obj.private_path else 'No path'}")
        print(f"   Original file still exists: {html_file.exists()}")
        print(f"   Original file path: {html_file.absolute()}")
        print(f"   Resolved path matches original: {keep_in_place_obj.private_path == str(html_file.absolute())}")
        print(f"   Metadata has keep_files_in_place: {keep_in_place_obj.metadata.get('_keep_files_in_place', False)}")
        print(f"   Original file paths stored: {keep_in_place_obj.metadata.get('_original_file_paths', {})}")
    else:
        print("❌ HTML file not found - skipping keep-in-place test")
    
    print("\n" + "="*60)
    
    # ===========================================
    # Test 3: Both files specified, kept in place
    # ===========================================
    print("\n3. Testing both private and mock files kept in place...")
    
    config_file = Path("tmp/config.json")
    config_mock_file = Path("tmp/config_mock.json")
    
    if config_file.exists() and config_mock_file.exists():
        both_files_obj = syobj(
            name="Config Files (Both In Place)",
            private_file=str(config_file),
            mock_file=str(config_mock_file),
            keep_files_in_place=True,
            private_read=["admin@company.com"],
            mock_read=["public"],
            metadata={"auto_save": True}
        )
        print(f"✅ Created both-files-in-place object: {both_files_obj.uid}")
        print(f"   Private URL: {both_files_obj.private_url}")
        print(f"   Mock URL: {both_files_obj.mock_url}")
        print(f"   Private Path: {both_files_obj.private_path}")
        print(f"   Mock Path: {both_files_obj.mock_path}")
        print(f"   Private file exists: {Path(both_files_obj.private_path).exists() if both_files_obj.private_path else 'No path'}")
        print(f"   Mock file exists: {Path(both_files_obj.mock_path).exists() if both_files_obj.mock_path else 'No path'}")
        print(f"   Original private still exists: {config_file.exists()}")
        print(f"   Original mock still exists: {config_mock_file.exists()}")
        print(f"   Private path matches original: {both_files_obj.private_path == str(config_file.absolute())}")
        print(f"   Mock path matches original: {both_files_obj.mock_path == str(config_mock_file.absolute())}")
        print(f"   Original paths: {both_files_obj.metadata.get('_original_file_paths', {})}")
    else:
        print("❌ Config files not found - skipping both-files test")
    
    print("\n" + "="*60)
    
    # ===========================================
    # Test 4: Test file access methods
    # ===========================================
    print("\n4. Testing file access methods...")
    
    sample_file = Path("tmp/sample.txt")
    if sample_file.exists():
        access_test_obj = syobj(
            name="Access Test (In Place)",
            private_file=str(sample_file),
            keep_files_in_place=True,
            private_read=["test@company.com"],
            mock_read=["public"],
            metadata={"auto_save": True}
        )
        
        print(f"✅ Created access test object: {access_test_obj.uid}")
        
        # Test different access methods
        print(f"   .private_url: {access_test_obj.private_url}")
        print(f"   .private_path: {access_test_obj.private_path}")
        
        try:
            # Test DataAccessor
            print(f"   .private.url: {access_test_obj.private.url}")
            print(f"   .private.path: {access_test_obj.private.path}")
            
            # Test file reading
            try:
                with access_test_obj.private.file as f:
                    content = f.read()[:50]  # First 50 chars
                print(f"   File content (first 50 chars): {repr(content)}")
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
                
        except Exception as e:
            print(f"   ❌ Error accessing private data: {e}")
    else:
        print("❌ Sample file not found - skipping access test")
    
    print("\n🎉 Keep-in-place testing complete!")
    print("\n💡 Key Benefits:")
    print("   ✅ Files stay in original locations")
    print("   ✅ No disk space duplication")
    print("   ✅ Python API works normally")
    print("   ✅ UI can still display and serve files")
    print("\n⚠️  Limitations:")
    print("   ❌ No cross-user SyftBox sharing")
    print("   ❌ Limited permission system")
    print("   ❌ Files must remain accessible at original paths")


if __name__ == "__main__":
    main() 