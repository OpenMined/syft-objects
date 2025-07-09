#!/usr/bin/env python3
"""
Syft-Queue Integration Example using New Folder Objects

This example demonstrates how syft-queue would use the new folder objects 
functionality in syft-objects to manage job folders with state transitions.

Example workflow:
1. Create a job folder with code and data
2. Submit job as folder object to queue's inbox
3. Move job through states: inbox → approved → running → completed
4. Each state transition moves the entire job folder
"""

import os
import shutil
from pathlib import Path
from uuid import uuid4
from datetime import datetime
import tempfile

# Import the updated syft-objects with folder support
from syft_objects import create_object
from syft_objects.models import SyftObject


def create_sample_job_folder(base_dir: Path, job_name: str) -> Path:
    """Create a sample job folder with typical job contents."""
    job_folder = base_dir / job_name
    job_folder.mkdir(exist_ok=True)
    
    # Create job script
    (job_folder / "run.sh").write_text("""#!/bin/bash
echo "Starting ML training job..."
python train.py --data ./data/train.csv --output ./results/
echo "Job completed successfully!"
""")
    
    # Create Python code
    (job_folder / "train.py").write_text("""
import pandas as pd
import numpy as np
from pathlib import Path

def main():
    print("Loading training data...")
    data_path = Path("./data/train.csv")
    if data_path.exists():
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} training samples")
    
    # Simulate training
    print("Training model...")
    accuracy = np.random.uniform(0.85, 0.95)
    
    # Save results
    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)
    
    with open(results_dir / "metrics.json", "w") as f:
        f.write(f'{{"accuracy": {accuracy:.3f}, "loss": 0.123}}')
    
    print(f"Training completed with accuracy: {accuracy:.3f}")

if __name__ == "__main__":
    main()
""")
    
    # Create data folder
    data_folder = job_folder / "data"
    data_folder.mkdir(exist_ok=True)
    
    # Create sample training data
    (data_folder / "train.csv").write_text("""id,feature1,feature2,label
1,0.1,0.5,0
2,0.3,0.7,1
3,0.2,0.4,0
4,0.8,0.9,1
5,0.6,0.3,1
""")
    
    # Create requirements file
    (job_folder / "requirements.txt").write_text("""pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=1.0.0
""")
    
    # Create job config
    (job_folder / "job_config.yaml").write_text("""
job_name: "{job_name}"
timeout: 3600
resources:
  cpu: 2
  memory: "4GB"
environment:
  python_version: "3.9"
""".format(job_name=job_name))
    
    return job_folder


def create_queue_structure(base_dir: Path) -> dict:
    """Create the queue directory structure for different job states."""
    queue_dir = base_dir / "ml_training_queue"
    
    # Create state directories
    states = ["inbox", "approved", "running", "completed", "failed", "rejected"]
    state_dirs = {}
    
    for state in states:
        state_dir = queue_dir / "jobs" / state
        state_dir.mkdir(parents=True, exist_ok=True)
        state_dirs[state] = state_dir
    
    return state_dirs


class JobManager:
    """
    Example implementation showing how syft-queue would use folder objects
    to manage job state transitions.
    """
    
    def __init__(self, queue_dirs: dict):
        self.queue_dirs = queue_dirs
        self.jobs = {}  # Track job objects by UID
    
    def submit_job(self, job_folder_path: Path, owner_email: str = "data_scientist@company.com") -> SyftObject:
        """
        Submit a job folder as a syft-object to the inbox.
        This demonstrates the new folder object functionality.
        """
        job_uid = str(uuid4())
        job_name = job_folder_path.name
        
        print(f"📁 Submitting job folder: {job_name}")
        
        # Create folder object using the new syft-objects functionality
        job_object = create_object(
            name=f"Job: {job_name}",
            private_folder=str(job_folder_path),  # Use new private_folder parameter
            mock_read=["reviewers", "queue_admin"],  # Reviewers can see job exists
            private_read=[owner_email, "queue_admin"],  # Only owner and admin see real data
            metadata={
                "job_uid": job_uid,
                "job_type": "ml_training",
                "submitted_at": datetime.now().isoformat(),
                "submitted_by": owner_email,
                "status": "inbox",
                "queue_name": "ml_training_queue"
            }
        )
        
        # Store job object
        self.jobs[job_uid] = job_object
        
        print(f"✅ Job submitted with UID: {job_uid}")
        print(f"   - Object type: {job_object.object_type}")
        print(f"   - Private URL: {job_object.private_url}")
        print(f"   - Mock URL: {job_object.mock_url}")
        
        return job_object
    
    def approve_job(self, job_uid: str, approver: str = "reviewer@company.com"):
        """Move job from inbox to approved state."""
        if job_uid not in self.jobs:
            raise ValueError(f"Job {job_uid} not found")
        
        job = self.jobs[job_uid]
        print(f"🔍 Approving job: {job.name}")
        
        # Update job metadata
        job.metadata.update({
            "status": "approved",
            "approved_at": datetime.now().isoformat(),
            "approved_by": approver
        })
        
        print(f"✅ Job approved by {approver}")
        return job
    
    def start_job(self, job_uid: str, runner: str = "worker_node_1"):
        """Move job from approved to running state."""
        if job_uid not in self.jobs:
            raise ValueError(f"Job {job_uid} not found")
        
        job = self.jobs[job_uid]
        print(f"🚀 Starting job: {job.name}")
        
        # Access job folder through the folder accessor
        job_folder = job.private.obj  # This returns a FolderAccessor
        
        print(f"   - Job folder exists: {job_folder.exists()}")
        print(f"   - Job files: {[f.name for f in job_folder.list_files()]}")
        
        # Update job metadata
        job.metadata.update({
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "runner": runner
        })
        
        print(f"✅ Job started on {runner}")
        return job
    
    def complete_job(self, job_uid: str, results_summary: dict = None):
        """Move job from running to completed state."""
        if job_uid not in self.jobs:
            raise ValueError(f"Job {job_uid} not found")
        
        job = self.jobs[job_uid]
        print(f"🎉 Completing job: {job.name}")
        
        # Update job metadata with results
        job.metadata.update({
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "results": results_summary or {"status": "success"}
        })
        
        print(f"✅ Job completed successfully")
        return job
    
    def get_job_status(self, job_uid: str) -> dict:
        """Get current status and details of a job."""
        if job_uid not in self.jobs:
            raise ValueError(f"Job {job_uid} not found")
        
        job = self.jobs[job_uid]
        
        # Access the job folder to get current state
        try:
            job_folder = job.private.obj
            file_count = len(job_folder.list_files())
            folder_size = job_folder.size()
            
            status = {
                "job_uid": job_uid,
                "name": job.name,
                "status": job.metadata.get("status", "unknown"),
                "object_type": job.object_type,
                "folder_exists": job_folder.exists(),
                "file_count": file_count,
                "folder_size_bytes": folder_size,
                "metadata": job.metadata
            }
        except Exception as e:
            status = {
                "job_uid": job_uid,
                "name": job.name,
                "status": job.metadata.get("status", "unknown"),
                "error": str(e),
                "metadata": job.metadata
            }
        
        return status
    
    def list_jobs_by_status(self, status: str) -> list:
        """List all jobs with a specific status."""
        matching_jobs = []
        for job_uid, job in self.jobs.items():
            if job.metadata.get("status") == status:
                matching_jobs.append({
                    "job_uid": job_uid,
                    "name": job.name,
                    "submitted_at": job.metadata.get("submitted_at"),
                    "submitted_by": job.metadata.get("submitted_by")
                })
        return matching_jobs


def demonstrate_syft_queue_integration():
    """
    Main demonstration of syft-queue integration with folder objects.
    """
    print("🔄 Syft-Queue Integration with Folder Objects Demo")
    print("=" * 60)
    
    # Create temporary workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. Set up queue structure
        print("\n1️⃣ Setting up queue structure...")
        queue_dirs = create_queue_structure(temp_path)
        job_manager = JobManager(queue_dirs)
        
        # 2. Create sample job
        print("\n2️⃣ Creating sample ML training job...")
        job_folder = create_sample_job_folder(temp_path, "ml_model_training_v1")
        
        print(f"   Created job folder: {job_folder}")
        print(f"   Job files: {[f.name for f in job_folder.iterdir()]}")
        
        # 3. Submit job using folder objects
        print("\n3️⃣ Submitting job as folder object...")
        job_object = job_manager.submit_job(job_folder)
        job_uid = job_object.metadata["job_uid"]
        
        # 4. Demonstrate job status tracking
        print("\n4️⃣ Checking job status...")
        status = job_manager.get_job_status(job_uid)
        print(f"   Status: {status['status']}")
        print(f"   Files: {status['file_count']}")
        print(f"   Size: {status['folder_size_bytes']} bytes")
        
        # 5. Approve job
        print("\n5️⃣ Approving job...")
        job_manager.approve_job(job_uid)
        
        # 6. Start job
        print("\n6️⃣ Starting job...")
        job_manager.start_job(job_uid)
        
        # 7. Access job files during execution
        print("\n7️⃣ Accessing job files during execution...")
        job_folder_accessor = job_object.private.obj
        
        # List all files in the job
        print("   Job files:")
        for file_path in job_folder_accessor.list_files():
            print(f"     - {file_path.name}")
        
        # Read specific files
        print("\n   Reading job configuration:")
        try:
            config_content = job_folder_accessor.read_file("job_config.yaml")
            print(f"     Config: {config_content[:100]}...")
        except FileNotFoundError:
            print("     Config file not found")
        
        # 8. Complete job
        print("\n8️⃣ Completing job...")
        results = {
            "accuracy": 0.92,
            "training_time": "45 minutes",
            "model_size": "124 MB"
        }
        job_manager.complete_job(job_uid, results)
        
        # 9. Final status check
        print("\n9️⃣ Final job status...")
        final_status = job_manager.get_job_status(job_uid)
        print(f"   Final status: {final_status['status']}")
        print(f"   Results: {final_status['metadata'].get('results', {})}")
        
        # 10. Demonstrate folder object serialization
        print("\n🔟 Demonstrating job object serialization...")
        yaml_path = temp_path / f"job_{job_uid}.syftobject.yaml"
        job_object.save_yaml(yaml_path, create_syftbox_permissions=False)
        
        # Load it back
        loaded_job = SyftObject.load_yaml(yaml_path)
        print(f"   Loaded job: {loaded_job.name}")
        print(f"   Object type: {loaded_job.object_type}")
        print(f"   Is folder: {loaded_job.is_folder}")
        
        print("\n✅ Syft-Queue integration demonstration completed!")
        print("\n📝 Key Benefits Demonstrated:")
        print("   - Job folders as first-class syft-objects")
        print("   - State transitions preserve entire job context")
        print("   - Mock/real separation for job security")
        print("   - Folder-level permissions and access control")
        print("   - Easy file access within job folders")
        print("   - Serializable job objects with full metadata")


if __name__ == "__main__":
    demonstrate_syft_queue_integration()