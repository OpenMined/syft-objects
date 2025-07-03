#!/usr/bin/env python3
"""
Example demonstrating how to use SingleSyftObjBacked and MultiSyftObjBacked.

These classes provide persistent, file-backed objects with automatic privacy controls
when used with SyftBox.
"""

from pathlib import Path
import tempfile
from syft_objects import SingleSyftObjBacked, MultiSyftObjBacked

def single_backed_example():
    """Example using SingleSyftObjBacked for simple persistent objects."""
    print("🔍 SingleSyftObjBacked Example")
    print("=" * 40)
    
    # Create a simple job-like object
    with tempfile.TemporaryDirectory() as temp_dir:
        job_path = Path(temp_dir) / "my_job"
        job = SingleSyftObjBacked(job_path, "analysis_job_001")
        
        # Set job attributes
        job._set_attribute("status", "pending")
        job._set_attribute("created_by", "researcher@university.edu")
        job._set_attribute("parameters", {
            "model": "bert-base",
            "learning_rate": 0.001,
            "epochs": 10
        })
        
        # Create folders for job files
        input_folder = job._set_folder_attribute("inputs")
        output_folder = job._set_folder_attribute("outputs")
        logs_folder = job._set_folder_attribute("logs")
        
        # Set job description
        job._set_text_file("description", "NLP model training job for sentiment analysis")
        
        # Show current state
        print(f"Job exists: {job.exists()}")
        print(f"Job status: {job._get_attribute('status')}")
        print(f"Job parameters: {job._get_attribute('parameters')}")
        print(f"All attributes: {job._list_attributes()}")
        print(f"Input folder: {input_folder}")
        print(f"Description: {job._get_text_file('description')}")
        
        # Update job status
        job._set_attribute("status", "running")
        job._set_attribute("progress", 0.25)
        
        print(f"Updated status: {job._get_attribute('status')}")
        print(f"Progress: {job._get_attribute('progress')}")
        
        print("✅ SingleSyftObjBacked example completed!\n")

def multi_backed_example():
    """Example using MultiSyftObjBacked for complex objects with multiple concerns."""
    print("🔍 MultiSyftObjBacked Example")
    print("=" * 40)
    
    # Create a Hugging Face API interface
    with tempfile.TemporaryDirectory() as temp_dir:
        api_path = Path(temp_dir) / "hf_interface"
        hf_api = MultiSyftObjBacked(api_path, "huggingface_api")
        
        # Create separate syft-objects for different concerns
        
        # 1. Configuration (public)
        hf_api._create_syft_object("config", {
            "model_name": "bert-base-uncased",
            "api_endpoint": "https://api-inference.huggingface.co",
            "timeout": 30,
            "max_retries": 3
        }, mock_read=["public"])
        
        # 2. Credentials (private)
        hf_api._create_syft_object("credentials", {
            "api_key": "hf_xxxxxxxxxxxxxxxxxxxx",
            "user_token": "secret_user_token"
        }, private_read=["owner@example.com"], mock_read=[])
        
        # 3. Cache (semi-public)
        hf_api._create_syft_object("cache", {
            "last_request": None,
            "cached_results": {},
            "cache_expiry": None
        }, mock_read=["public"])
        
        # 4. Logs (private)
        hf_api._create_syft_object("logs", {
            "requests_count": 0,
            "errors": [],
            "performance_metrics": {}
        })
        
        # Show what we created
        print(f"API interface exists: {hf_api.exists()}")
        print(f"Syft-objects: {hf_api._list_syft_objects()}")
        
        # Access different data
        config = hf_api._get_syft_object_data("config")
        print(f"Config: {config}")
        
        cache = hf_api._get_syft_object_data("cache")
        print(f"Cache: {cache}")
        
        # Update logs (simulate API usage)
        hf_api._set_syft_object_data("logs", {
            "requests_count": 5,
            "errors": [],
            "performance_metrics": {
                "avg_response_time": 0.8,
                "success_rate": 1.0
            }
        })
        
        # Update cache
        hf_api._set_syft_object_data("cache", {
            "last_request": "2024-01-15T10:30:00Z",
            "cached_results": {
                "hello world": {"label": "POSITIVE", "score": 0.9998}
            },
            "cache_expiry": "2024-01-15T11:30:00Z"
        })
        
        # Show updated data
        logs = hf_api._get_syft_object_data("logs")
        updated_cache = hf_api._get_syft_object_data("cache")
        
        print(f"Updated logs: {logs}")
        print(f"Updated cache: {updated_cache}")
        
        print("✅ MultiSyftObjBacked example completed!\n")

if __name__ == "__main__":
    print("🚀 Syft-Objects Backed Objects Examples")
    print("=" * 50)
    print("These examples show how to use backed objects for persistent,")
    print("privacy-aware file storage that works with SyftBox.")
    print()
    
    single_backed_example()
    multi_backed_example()
    
    print("🎉 All examples completed!")
    print()
    print("📝 Key Benefits:")
    print("• Persistent storage across application restarts")
    print("• Automatic privacy controls with syft-objects")
    print("• JSON fallback when SyftBox isn't configured")
    print("• Easy to subclass for domain-specific objects")
    print("• Built-in serialization for complex data types") 