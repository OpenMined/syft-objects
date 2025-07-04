"""Test relative path functionality in syft-objects"""

import os
import shutil
import tempfile
from pathlib import Path
import pytest

from syft_objects import syobj, SyftObject
from syft_objects.client import resolve_relative_path, find_syftobject_files


class TestRelativePaths:
    """Test suite for relative path support"""
    
    def setup_method(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
    def teardown_method(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_create_object_with_relative_paths(self):
        """Test creating a SyftObject with relative paths enabled"""
        # Create test directories
        Path("data/private").mkdir(parents=True)
        Path("data/public").mkdir(parents=True)
        Path("metadata").mkdir(parents=True)
        
        # Create object with relative paths
        obj = syobj(
            "test_dataset",
            private_contents="Private data content",
            mock_contents="Mock data content",
            metadata={
                "use_relative_paths": True,
                "base_path": ".",
                "auto_save": True,
                "save_to": "metadata/test_dataset.syftobject.yaml"
            }
        )
        
        # Check that relative paths are set
        assert obj.base_path == "."
        assert obj.private_url_relative is not None
        assert obj.mock_url_relative is not None
        assert obj.syftobject_relative is not None
        
        # Check that files can be resolved
        assert obj.private_path != ""
        assert obj.mock_path != ""
        assert obj.syftobject_path != ""
    
    def test_load_object_with_relative_paths(self):
        """Test loading a SyftObject that uses relative paths"""
        # Create directory structure
        Path("project/data").mkdir(parents=True)
        Path("project/metadata").mkdir(parents=True)
        
        # Create files
        private_file = Path("project/data/private.txt")
        private_file.write_text("Private content")
        
        mock_file = Path("project/data/mock.txt")
        mock_file.write_text("Mock content")
        
        # Create object with relative paths
        obj = syobj(
            "test_object",
            private_file=str(private_file),
            mock_file=str(mock_file),
            metadata={
                "use_relative_paths": True,
                "base_path": "project",
                "auto_save": True,
                "save_to": "project/metadata/test.syftobject.yaml",
                "move_files_to_syftbox": False
            }
        )
        
        # Load the object
        loaded_obj = SyftObject.load_yaml("project/metadata/test.syftobject.yaml")
        
        # Check that base_path was auto-detected
        assert loaded_obj.base_path is not None
        
        # Check that files can be resolved
        assert Path(loaded_obj.private_path).exists()
        assert Path(loaded_obj.mock_path).exists()
    
    def test_object_portability(self):
        """Test that objects with relative paths remain portable"""
        # Create initial structure
        Path("original/data").mkdir(parents=True)
        Path("original/metadata").mkdir(parents=True)
        
        # Create object
        obj = syobj(
            "portable_dataset",
            private_contents="Portable private data",
            mock_contents="Portable mock data",
            metadata={
                "use_relative_paths": True,
                "base_path": "original",
                "auto_save": True,
                "save_to": "original/metadata/portable.syftobject.yaml",
                "move_files_to_syftbox": False
            }
        )
        
        # Move the entire directory
        shutil.move("original", "moved")
        
        # Load from new location
        loaded_obj = SyftObject.load_yaml("moved/metadata/portable.syftobject.yaml")
        
        # Files should still be found via relative paths
        assert Path(loaded_obj.private_path).exists()
        assert Path(loaded_obj.mock_path).exists()
        assert "moved" in loaded_obj.private_path
    
    def test_fallback_resolution(self):
        """Test fallback path resolution when files are moved unexpectedly"""
        # Create object with absolute fallbacks
        obj = syobj(
            "fallback_test",
            private_contents="Test private",
            mock_contents="Test mock",
            metadata={
                "use_relative_paths": True,
                "auto_save": True
            }
        )
        
        # Update fallback paths
        obj._update_relative_paths()
        
        # Check that absolute fallbacks are set
        assert obj.private_url_absolute_fallback is not None
        assert obj.mock_url_absolute_fallback is not None
    
    def test_mixed_path_modes(self):
        """Test objects that mix relative and absolute paths"""
        obj = SyftObject(
            private_url="syft://test@example.com/private/data.csv",
            mock_url="syft://test@example.com/public/data_mock.csv",
            syftobject="syft://test@example.com/public/data.syftobject.yaml",
            base_path=".",
            private_url_relative="local/private.csv",
            mock_url_relative="local/mock.csv"
        )
        
        # Create the relative path files
        Path("local").mkdir(exist_ok=True)
        Path("local/private.csv").write_text("private")
        Path("local/mock.csv").write_text("mock")
        
        # Should resolve to relative paths first
        assert "local" in obj.private_path
        assert "local" in obj.mock_path
    
    def test_path_resolution_helpers(self):
        """Test the path resolution helper functions"""
        # Test resolve_relative_path
        base = Path("base/dir")
        base.mkdir(parents=True)
        
        resolved = resolve_relative_path("base/dir", "../file.txt")
        assert resolved.is_absolute()
        assert "base" in str(resolved.parent)
        
        # Test find_syftobject_files
        Path("search/sub1").mkdir(parents=True)
        Path("search/sub2").mkdir(parents=True)
        
        Path("search/obj1.syftobject.yaml").touch()
        Path("search/sub1/obj2.syftobject.yaml").touch()
        Path("search/sub2/obj3.syftobject.yaml").touch()
        
        found = find_syftobject_files("search")
        assert len(found) == 3
        assert all(f.name.endswith(".syftobject.yaml") for f in found)