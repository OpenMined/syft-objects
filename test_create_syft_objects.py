#!/usr/bin/env python3
"""
Example script showing how to create SyftObjects with existing files
"""

from syft_objects import syobj
from pathlib import Path
import json

def main():
    print("🔐 Creating SyftObjects with existing files...")
    
    # ===========================================
    # Example 1: Using existing CSV files
    # ===========================================
    print("\n1. Creating SyftObject with existing CSV files...")
    
    # Check if the files exist
    csv_file = Path("tmp/sales_data.csv")
    csv_mock_file = Path("tmp/sales_data_mock.csv")
    
    if csv_file.exists() and csv_mock_file.exists():
        sales_obj = syobj(
            name="Sales Data Q4 2024",
            private_file=str(csv_file),      # Use existing private file
            mock_file=str(csv_mock_file),    # Use existing mock file
            private_read=["sales-team@company.com", "manager@company.com"],
            private_write=["sales-team@company.com"],
            mock_read=["public"],            # Mock data is public
            mock_write=[],                   # No mock write permissions
            metadata={
                "description": "Q4 2024 sales data with public mock version",
                "department": "Sales",
                "quarter": "Q4_2024",
                "file_type": "CSV",
                "auto_save": True
            }
        )
        print(f"✅ Created sales object: {sales_obj.uid}")
        print(f"   Private: {sales_obj.private_url}")
        print(f"   Mock: {sales_obj.mock_url}")
    else:
        print("❌ Sales CSV files not found - skipping")
    
    # ===========================================
    # Example 2: Using existing JSON config files
    # ===========================================
    print("\n2. Creating SyftObject with JSON config files...")
    
    config_file = Path("tmp/config.json")
    config_mock_file = Path("tmp/config_mock.json")
    
    if config_file.exists() and config_mock_file.exists():
        config_obj = syobj(
            name="Application Configuration",
            private_file=str(config_file),
            mock_file=str(config_mock_file),
            private_read=["admin@company.com", "devops@company.com"],
            private_write=["admin@company.com"],
            mock_read=["public"],
            mock_write=[],
            metadata={
                "description": "Application configuration with sanitized mock version",
                "environment": "production",
                "type": "configuration",
                "auto_save": True
            }
        )
        print(f"✅ Created config object: {config_obj.uid}")
        print(f"   Private: {config_obj.private_url}")
        print(f"   Mock: {config_obj.mock_url}")
    else:
        print("❌ Config JSON files not found - skipping")
    
    # ===========================================
    # Example 3: Using HTML file as private, auto-generate mock
    # ===========================================
    print("\n3. Creating SyftObject with HTML file (auto-generated mock)...")
    
    html_file = Path("widget_test.html")
    
    if html_file.exists():
        html_obj = syobj(
            name="Widget Test Page",
            private_file=str(html_file),
            # Note: mock_file is omitted, so it will auto-generate mock content
            private_read=["developer@company.com"],
            private_write=["developer@company.com"],
            mock_read=["public"],
            metadata={
                "description": "HTML widget test page with auto-generated mock",
                "file_type": "HTML",
                "purpose": "testing",
                "auto_save": True
            }
        )
        print(f"✅ Created HTML object: {html_obj.uid}")
        print(f"   Private: {html_obj.private_url}")
        print(f"   Mock: {html_obj.mock_url}")
    else:
        print("❌ HTML file not found - skipping")
    
    # ===========================================
    # Example 4: Using SQLite database files  
    # ===========================================
    print("\n4. Creating SyftObject with SQLite database files...")
    
    db_file = Path("tmp/company_data.sqlite")
    db_mock_file = Path("tmp/company_mock.sqlite")
    
    if db_file.exists() and db_mock_file.exists():
        db_obj = syobj(
            name="Company Database",
            private_file=str(db_file),
            mock_file=str(db_mock_file),
            private_read=["dba@company.com", "analytics@company.com"],
            private_write=["dba@company.com"],
            mock_read=["analytics@company.com", "manager@company.com"],
            mock_write=[],
            metadata={
                "description": "Company database with sample data in mock version",
                "database_type": "SQLite",
                "contains_pii": True,
                "backup_frequency": "daily",
                "auto_save": True
            }
        )
        print(f"✅ Created database object: {db_obj.uid}")
        print(f"   Private: {db_obj.private_url}")
        print(f"   Mock: {db_obj.mock_url}")
    else:
        print("❌ Database files not found - skipping")
    
    # ===========================================
    # Example 5: Using large model files (ZIP)
    # ===========================================
    print("\n5. Creating SyftObject with large model files...")
    
    model_file = Path("tmp/gpt2_private.zip")
    model_mock_file = Path("tmp/gpt2_mock.zip")
    
    if model_file.exists() and model_mock_file.exists():
        model_obj = syobj(
            name="GPT-2 Model",
            private_file=str(model_file),
            mock_file=str(model_mock_file),
            private_read=["ml-team@company.com"],
            private_write=["ml-team@company.com"],
            mock_read=["public"],
            mock_write=[],
            metadata={
                "description": "GPT-2 model with demo version for public access",
                "model_type": "transformer",
                "size": "large",
                "framework": "pytorch",
                "auto_save": True,
                "move_files_to_syftbox": True  # This will move to SyftBox if available
            }
        )
        print(f"✅ Created model object: {model_obj.uid}")
        print(f"   Private: {model_obj.private_url}")
        print(f"   Mock: {model_obj.mock_url}")
        print(f"   Metadata: {model_obj.metadata}")
    else:
        print("❌ Model files not found - skipping")
    
    # ===========================================
    # Example 6: Using only private file, no mock
    # ===========================================
    print("\n6. Creating SyftObject with only private file (auto-generated mock)...")
    
    sample_file = Path("tmp/sample.txt")
    
    if sample_file.exists():
        private_only_obj = syobj(
            name="Private Sample Data",
            private_file=str(sample_file),
            # No mock_file specified - will auto-generate
            private_read=["owner@company.com"],
            private_write=["owner@company.com"],
            mock_read=["public"],  # Auto-generated mock will be public
            metadata={
                "description": "Private sample data with auto-generated public mock",
                "sensitivity": "high",
                "auto_save": True
            }
        )
        print(f"✅ Created private-only object: {private_only_obj.uid}")
        print(f"   Private: {private_only_obj.private_url}")
        print(f"   Mock: {private_only_obj.mock_url}")
    else:
        print("❌ Sample file not found - skipping")
    
    # ===========================================
    # Example 7: Advanced permissions and metadata
    # ===========================================
    print("\n7. Creating SyftObject with advanced permissions...")
    
    test_file = Path("tmp/test.json")
    test_mock = Path("tmp/test_mock.json")
    
    if test_file.exists() and test_mock.exists():
        advanced_obj = syobj(
            name="Advanced Test Data",
            private_file=str(test_file),
            mock_file=str(test_mock),
            # Granular permissions
            private_read=["admin@company.com", "analyst@company.com"],
            private_write=["admin@company.com"],
            mock_read=["public"],
            mock_write=["contributor@company.com"],
            syftobject_permissions=["public"],  # Metadata is discoverable
            metadata={
                "description": "Test data with granular permission control",
                "classification": "internal",
                "retention_period": "1_year",
                "owner": "admin@company.com",
                "created_by": "automated_system",
                "tags": ["test", "demo", "permissions"],
                "auto_save": True,
                "email": "admin@company.com",  # Specify owner email
                "create_syftbox_permissions": True  # Create SyftBox permission files
            }
        )
        print(f"✅ Created advanced object: {advanced_obj.uid}")
        print(f"   Private: {advanced_obj.private_url}")
        print(f"   Mock: {advanced_obj.mock_url}")
        print(f"   Permissions: {advanced_obj.private_permissions}")
    else:
        print("❌ Test files not found - skipping")
    
    print("\n🎉 Done! Check the syft-objects UI to see your created objects.")
    print("💡 Tip: Use 'from syft_objects import objects' to access the collection")
    print("💡 Tip: Use 'objects.refresh()' to reload objects from disk")


if __name__ == "__main__":
    main() 