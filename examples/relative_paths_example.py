"""Example demonstrating relative path support in syft-objects

This example shows how to create portable SyftObjects that use relative paths,
making them easy to move or share while maintaining file references.
"""

from pathlib import Path
import shutil
from syft_objects import syobj, SyftObject


def main():
    print("=== SyftObjects Relative Path Example ===\n")
    
    # 1. Create a project directory structure
    print("1. Creating project directory structure...")
    project_dir = Path("my_ml_project")
    (project_dir / "data" / "private").mkdir(parents=True, exist_ok=True)
    (project_dir / "data" / "public").mkdir(parents=True, exist_ok=True)
    (project_dir / "metadata").mkdir(parents=True, exist_ok=True)
    
    # 2. Create some data files
    print("2. Creating data files...")
    private_data_path = project_dir / "data" / "private" / "training_data.csv"
    private_data_path.write_text("id,feature1,feature2,label\n1,0.5,1.2,1\n2,0.7,1.5,0")
    
    mock_data_path = project_dir / "data" / "public" / "training_data_mock.csv"
    mock_data_path.write_text("id,feature1,feature2,label\n1,0.1,0.2,1\n2,0.3,0.4,0")
    
    # 3. Create a SyftObject with relative paths
    print("\n3. Creating SyftObject with relative paths...")
    dataset = syobj(
        "ML Training Dataset",
        private_file=str(private_data_path),
        mock_file=str(mock_data_path),
        metadata={
            "description": "Training dataset for ML model",
            "use_relative_paths": True,
            "base_path": str(project_dir),
            "save_to": str(project_dir / "metadata" / "training_dataset.syftobject.yaml"),
            "move_files_to_syftbox": False,  # Keep files in place
            "version": "1.0",
            "columns": ["id", "feature1", "feature2", "label"]
        }
    )
    
    print(f"   Created object: {dataset.name}")
    print(f"   Base path: {dataset.base_path}")
    print(f"   Private relative: {dataset.private_url_relative}")
    print(f"   Mock relative: {dataset.mock_url_relative}")
    
    # 4. Demonstrate portability - move the entire project
    print("\n4. Testing portability - moving project to new location...")
    moved_project = Path("shared_projects") / "ml_project_v2"
    moved_project.parent.mkdir(exist_ok=True)
    
    if moved_project.exists():
        shutil.rmtree(moved_project)
    shutil.move(str(project_dir), str(moved_project))
    
    # 5. Load the object from its new location
    print("\n5. Loading object from new location...")
    loaded_dataset = SyftObject.load_yaml(
        moved_project / "metadata" / "training_dataset.syftobject.yaml"
    )
    
    print(f"   Loaded object: {loaded_dataset.name}")
    print(f"   Auto-detected base path: {loaded_dataset.base_path}")
    print(f"   Private file found at: {loaded_dataset.private_path}")
    print(f"   Mock file found at: {loaded_dataset.mock_path}")
    
    # 6. Access the data
    print("\n6. Accessing data through the object...")
    print(f"   Private data preview: {loaded_dataset.private.obj[:50]}...")
    print(f"   Mock data preview: {loaded_dataset.mock.obj[:50]}...")
    
    # 7. Create a new object in the moved location
    print("\n7. Creating new object in moved location...")
    new_data_path = moved_project / "data" / "private" / "validation_data.csv"
    new_data_path.write_text("id,feature1,feature2,label\n3,0.6,1.3,1\n4,0.8,1.6,0")
    
    validation_dataset = syobj(
        "ML Validation Dataset",
        private_contents="Validation data (private)",
        mock_contents="Validation data (mock)",
        metadata={
            "use_relative_paths": True,
            "base_path": str(moved_project),
            "save_to": str(moved_project / "metadata" / "validation_dataset.syftobject.yaml"),
            "move_files_to_syftbox": False
        }
    )
    
    print(f"   Created: {validation_dataset.name}")
    
    # 8. Show how to handle mixed environments
    print("\n8. Demonstrating fallback resolution...")
    # Even if we change directory, objects can still find their files
    import os
    original_cwd = os.getcwd()
    os.chdir("/tmp")
    
    # Object still works due to path resolution
    print(f"   Changed to directory: {os.getcwd()}")
    print(f"   Private file still accessible: {Path(loaded_dataset.private_path).exists()}")
    
    os.chdir(original_cwd)
    
    print("\n=== Example Complete ===")
    print("\nKey benefits of relative paths:")
    print("- Projects remain portable (can be moved/copied)")
    print("- Easier collaboration (relative to project root)")
    print("- Automatic fallback to absolute paths if needed")
    print("- Works seamlessly with existing syft:// URLs")


if __name__ == "__main__":
    main()