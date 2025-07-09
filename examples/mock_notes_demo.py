#!/usr/bin/env python3
"""
Demo of the mock notes feature in syft-objects

This shows how mock notes help users understand the characteristics
of mock data without revealing private information.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.syft_objects import create_object
from src.syft_objects.config import config


def demo_manual_mock_note():
    """Example 1: Manually setting a mock note"""
    print("\n=== Example 1: Manual Mock Note ===")
    
    # Create an object with a manual mock note
    obj = create_object(
        "user_analytics",
        private_contents="user_id,timestamp,action,value\n" + "\n".join(
            f"{i},2024-01-{i%30+1:02d},{['click','view','purchase'][i%3]},{i*10}"
            for i in range(10000)
        ),
        mock_contents="user_id,timestamp,action,value\n1,2024-01-01,click,10\n2,2024-01-01,view,20\n3,2024-01-02,purchase,30",
        mock_note="3 sample rows for testing (anonymized)"
    )
    
    print(f"Created object: {obj.get_name()}")
    print(f"Mock note: {obj.mock.get_note()}")
    

def demo_automatic_suggestion():
    """Example 2: Automatic mock note suggestion (safe)"""
    print("\n=== Example 2: Automatic Safe Analysis ===")
    
    # Temporarily disable suggestions to avoid prompts in demo
    original = config.suggest_mock_notes
    config.suggest_mock_notes = True
    config.mock_note_sensitivity = "never"  # Only safe analysis
    
    try:
        # Create CSV with automatic analysis
        obj = create_object(
            "sales_data",
            mock_contents="product,price,quantity\nWidget A,10.99,5\nWidget B,20.50,3\n"
        )
        
        print(f"Created object: {obj.get_name()}")
        print(f"Auto-detected mock note: {obj.mock.get_note()}")
        
    finally:
        config.suggest_mock_notes = original


def demo_mock_note_api():
    """Example 3: Using the mock note API"""
    print("\n=== Example 3: Mock Note API ===")
    
    # Create object without note
    obj = create_object(
        "model_weights",
        mock_contents='{"layers": 10, "parameters": null, "architecture": "transformer"}',
        private_contents='{"layers": 10, "parameters": [1.23, 4.56, ...], "architecture": "transformer"}'
    )
    
    # Add note later
    obj.mock.set_note("Model architecture only (no weights)")
    
    print(f"Created object: {obj.get_name()}")
    print(f"Mock note set via API: {obj.mock.get_note()}")


def demo_synthetic_data():
    """Example 4: Synthetic data with privacy guarantees"""
    print("\n=== Example 4: Synthetic Data with Privacy ===")
    
    obj = create_object(
        "patient_records",
        mock_contents="age,condition,treatment\n45,diabetes,metformin\n52,hypertension,lisinopril",
        private_contents="[PRIVATE MEDICAL DATA]",
        mock_note="Synthetic data (ε=2.0 differential privacy)"
    )
    
    print(f"Created object: {obj.get_name()}")
    print(f"Mock note: {obj.mock.get_note()}")
    print("This clearly indicates the mock data is synthetic with privacy guarantees")


def demo_configuration():
    """Example 5: Configuration options"""
    print("\n=== Example 5: Configuration Options ===")
    
    print(f"Current settings:")
    print(f"  - Suggest mock notes: {config.suggest_mock_notes}")
    print(f"  - Timeout: {config.mock_note_timeout}s")
    print(f"  - Sensitivity: {config.mock_note_sensitivity}")
    
    print("\nYou can configure these via:")
    print("  - Environment variables: SYFT_OBJECTS_SUGGEST_NOTES=false")
    print("  - Config file: ~/.syftbox/syft-objects.yaml")
    print("  - Runtime: config.suggest_mock_notes = False")


if __name__ == "__main__":
    print("Mock Notes Feature Demo")
    print("=" * 50)
    
    # Run all demos
    demo_manual_mock_note()
    demo_automatic_suggestion()
    demo_mock_note_api()
    demo_synthetic_data()
    demo_configuration()
    
    print("\n" + "=" * 50)
    print("Mock notes help users understand mock data characteristics")
    print("without revealing private information!")