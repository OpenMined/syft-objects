"""Tests for syft_objects.utils module"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from uuid import uuid4

from syft_objects.utils import scan_for_syft_objects, load_syft_objects_from_directory
from syft_objects.models import SyftObject


class TestUtilsModule:
    """Test utils module functions"""
    
    def test_scan_for_syft_objects_directory_not_found(self):
        """Test scan_for_syft_objects with non-existent directory"""
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            scan_for_syft_objects("/non/existent/directory")
    
    def test_scan_for_syft_objects_empty_directory(self, temp_dir):
        """Test scan_for_syft_objects with empty directory"""
        result = scan_for_syft_objects(temp_dir)
        assert result == []
    
    def test_scan_for_syft_objects_recursive(self, temp_dir):
        """Test scan_for_syft_objects with recursive search"""
        # Create test structure
        (temp_dir / "obj1.syftobject.yaml").touch()
        (temp_dir / "obj2.syftobject.yaml").touch()
        (temp_dir / "not_syft.yaml").touch()
        
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "obj3.syftobject.yaml").touch()
        
        subsubdir = subdir / "subsubdir"
        subsubdir.mkdir()
        (subsubdir / "obj4.syftobject.yaml").touch()
        
        # Test recursive search
        result = scan_for_syft_objects(temp_dir, recursive=True)
        result_names = [p.name for p in result]
        
        assert len(result) == 4
        assert "obj1.syftobject.yaml" in result_names
        assert "obj2.syftobject.yaml" in result_names
        assert "obj3.syftobject.yaml" in result_names
        assert "obj4.syftobject.yaml" in result_names
        assert "not_syft.yaml" not in result_names
    
    def test_scan_for_syft_objects_non_recursive(self, temp_dir):
        """Test scan_for_syft_objects without recursive search"""
        # Create test structure
        (temp_dir / "obj1.syftobject.yaml").touch()
        (temp_dir / "obj2.syftobject.yaml").touch()
        
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "obj3.syftobject.yaml").touch()
        
        # Test non-recursive search
        result = scan_for_syft_objects(temp_dir, recursive=False)
        result_names = [p.name for p in result]
        
        assert len(result) == 2
        assert "obj1.syftobject.yaml" in result_names
        assert "obj2.syftobject.yaml" in result_names
        assert "obj3.syftobject.yaml" not in result_names
    
    def test_scan_for_syft_objects_with_path_object(self, temp_dir):
        """Test scan_for_syft_objects with Path object input"""
        (temp_dir / "obj1.syftobject.yaml").touch()
        
        result = scan_for_syft_objects(Path(temp_dir))
        assert len(result) == 1
        assert result[0].name == "obj1.syftobject.yaml"
    
    def test_load_syft_objects_from_directory_empty(self, temp_dir):
        """Test load_syft_objects_from_directory with empty directory"""
        result = load_syft_objects_from_directory(temp_dir)
        assert result == []
    
    def test_load_syft_objects_from_directory_success(self, temp_dir, sample_yaml_content):
        """Test load_syft_objects_from_directory with valid files"""
        # Create test files
        file1 = temp_dir / "obj1.syftobject.yaml"
        file1.write_text(sample_yaml_content)
        
        file2 = temp_dir / "obj2.syftobject.yaml"
        # Modify the content slightly for the second object
        modified_content = sample_yaml_content.replace("test_object", "test_object_2")
        modified_content = modified_content.replace("12345678-1234-5678-1234-567812345678", 
                                                    "87654321-4321-8765-4321-876543218765")
        file2.write_text(modified_content)
        
        # Load objects
        objects = load_syft_objects_from_directory(temp_dir)
        
        assert len(objects) == 2
        assert all(isinstance(obj, SyftObject) for obj in objects)
        assert objects[0].name == "test_object"
        assert objects[1].name == "test_object_2"
    
    def test_load_syft_objects_from_directory_with_errors(self, temp_dir, sample_yaml_content):
        """Test load_syft_objects_from_directory with some invalid files"""
        # Create valid file
        file1 = temp_dir / "valid.syftobject.yaml"
        file1.write_text(sample_yaml_content)
        
        # Create invalid file
        file2 = temp_dir / "invalid.syftobject.yaml"
        file2.write_text("invalid: yaml: content: [")
        
        # Create another valid file
        file3 = temp_dir / "valid2.syftobject.yaml"
        modified_content = sample_yaml_content.replace("test_object", "test_object_2")
        file3.write_text(modified_content)
        
        # Load objects with warning capture
        with patch('builtins.print') as mock_print:
            objects = load_syft_objects_from_directory(temp_dir)
        
        # Should load 2 valid objects
        assert len(objects) == 2
        assert objects[0].name == "test_object"
        assert objects[1].name == "test_object_2"
        
        # Should print warning about invalid file
        mock_print.assert_called()
        warning_text = str(mock_print.call_args_list)
        assert "Warning: Failed to load" in warning_text
        assert "invalid.syftobject.yaml" in warning_text
    
    def test_load_syft_objects_from_directory_recursive(self, temp_dir, sample_yaml_content):
        """Test load_syft_objects_from_directory with recursive search"""
        # Create files in root
        file1 = temp_dir / "obj1.syftobject.yaml"
        file1.write_text(sample_yaml_content)
        
        # Create files in subdirectory
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        file2 = subdir / "obj2.syftobject.yaml"
        modified_content = sample_yaml_content.replace("test_object", "test_object_2")
        file2.write_text(modified_content)
        
        # Test recursive load
        objects = load_syft_objects_from_directory(temp_dir, recursive=True)
        assert len(objects) == 2
        
        # Test non-recursive load
        objects = load_syft_objects_from_directory(temp_dir, recursive=False)
        assert len(objects) == 1
        assert objects[0].name == "test_object"
    
    def test_load_syft_objects_from_directory_nonexistent(self):
        """Test load_syft_objects_from_directory with non-existent directory"""
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            load_syft_objects_from_directory("/non/existent/directory")
    
    def test_load_syft_objects_from_directory_path_object(self, temp_dir, sample_yaml_content):
        """Test load_syft_objects_from_directory with Path object"""
        file1 = temp_dir / "obj1.syftobject.yaml"
        file1.write_text(sample_yaml_content)
        
        objects = load_syft_objects_from_directory(Path(temp_dir))
        assert len(objects) == 1
        assert objects[0].name == "test_object"