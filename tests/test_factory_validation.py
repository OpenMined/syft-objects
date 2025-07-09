"""Tests for validation integration in factory.py."""

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from syft_objects import create_object
from syft_objects._validation import MockRealValidationError


class TestFactoryValidation:
    """Test validation integration in the create_object factory function."""
    
    def test_create_object_with_matching_content(self):
        """Test that create_object works with matching mock and real content."""
        obj = create_object(
            name="test",
            mock_contents="test content",
            private_contents="test content"
        )
        assert obj.get_name() == "test"
    
    def test_create_object_with_skip_validation(self, tmp_path):
        """Test that skip_validation=True bypasses all checks."""
        # Create mismatched CSV files
        mock_df = pd.DataFrame({'col1': [1]})
        real_df = pd.DataFrame({'col2': [2]})
        
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.csv"
        
        mock_df.to_csv(mock_path, index=False)
        real_df.to_csv(real_path, index=False)
        
        # Should not raise despite column mismatch
        obj = create_object(
            name="test",
            mock_file=str(mock_path),
            private_file=str(real_path),
            skip_validation=True
        )
        assert obj.get_name() == "test"
    
    def test_create_object_csv_validation_error(self, tmp_path):
        """Test that CSV validation errors are raised properly."""
        # Create mismatched CSV files
        mock_df = pd.DataFrame({'col1': [1], 'col2': [2]})
        real_df = pd.DataFrame({'col1': [1], 'col3': [3]})
        
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.csv"
        
        mock_df.to_csv(mock_path, index=False)
        real_df.to_csv(real_path, index=False)
        
        with pytest.raises(MockRealValidationError) as exc_info:
            create_object(
                name="test",
                mock_file=str(mock_path),
                private_file=str(real_path)
            )
        
        assert "CSV column mismatch" in str(exc_info.value)
        assert "Missing in mock: {'col3'}" in str(exc_info.value)
    
    def test_create_object_json_validation_error(self, tmp_path):
        """Test that JSON validation errors are raised properly."""
        mock_path = tmp_path / "mock.json"
        real_path = tmp_path / "real.json"
        
        mock_path.write_text(json.dumps({"key1": "value"}))
        real_path.write_text(json.dumps({"key2": "value"}))
        
        with pytest.raises(MockRealValidationError) as exc_info:
            create_object(
                name="test",
                mock_file=str(mock_path),
                private_file=str(real_path)
            )
        
        assert "JSON key mismatch" in str(exc_info.value)
    
    def test_create_object_auto_generated_mock_no_validation(self):
        """Test that auto-generated mock files don't trigger validation."""
        # When mock is auto-generated, validation shouldn't fail
        obj = create_object(
            name="test",
            private_contents="private data"
            # mock will be auto-generated
        )
        assert obj.get_name() == "test"
    
    def test_create_object_folder_no_validation(self, tmp_path):
        """Test that folder objects skip validation."""
        mock_folder = tmp_path / "mock_folder"
        real_folder = tmp_path / "real_folder"
        
        mock_folder.mkdir()
        real_folder.mkdir()
        
        # Create different files in each folder
        (mock_folder / "file1.txt").write_text("mock")
        (real_folder / "file2.txt").write_text("real")
        
        # Should not raise - folders skip validation
        obj = create_object(
            name="test_folder",
            mock_folder=str(mock_folder),
            private_folder=str(real_folder)
        )
        assert obj.get_name() == "test_folder"
    
    def test_create_object_extension_mismatch_error(self, tmp_path):
        """Test that extension mismatches are caught."""
        mock_path = tmp_path / "mock.txt"
        real_path = tmp_path / "real.csv"
        
        mock_path.write_text("mock content")
        real_path.write_text("col1\nvalue1")
        
        with pytest.raises(MockRealValidationError) as exc_info:
            create_object(
                name="test",
                mock_file=str(mock_path),
                private_file=str(real_path)
            )
        
        assert "File extensions don't match" in str(exc_info.value)
    
    def test_create_object_cleanup_on_validation_error(self, tmp_path):
        """Test that temporary files are cleaned up on validation error."""
        # Track tmp directory before
        tmp_dir = Path("tmp")
        tmp_dir.mkdir(exist_ok=True)
        files_before = set(tmp_dir.iterdir())
        
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.csv"
        
        # Create mismatched CSV files
        pd.DataFrame({'col1': [1]}).to_csv(mock_path, index=False)
        pd.DataFrame({'col2': [2]}).to_csv(real_path, index=False)
        
        try:
            create_object(
                name="test",
                mock_file=str(mock_path),
                private_file=str(real_path)
            )
        except MockRealValidationError:
            pass
        
        # Check that no new files remain in tmp
        files_after = set(tmp_dir.iterdir())
        new_files = files_after - files_before
        
        # Filter out any .syftobject.yaml files that might be expected
        unexpected_files = [f for f in new_files if not str(f).endswith('.syftobject.yaml')]
        assert len(unexpected_files) == 0, f"Unexpected files not cleaned up: {unexpected_files}"
    
    def test_create_object_parquet_validation(self, tmp_path):
        """Test that parquet DataFrame validation works."""
        mock_df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        real_df = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})
        
        mock_path = tmp_path / "mock.parquet"
        real_path = tmp_path / "real.parquet"
        
        mock_df.to_parquet(mock_path)
        real_df.to_parquet(real_path)
        
        with pytest.raises(MockRealValidationError) as exc_info:
            create_object(
                name="test_df",
                mock_file=str(mock_path),
                private_file=str(real_path)
            )
        
        assert "DataFrame column mismatch" in str(exc_info.value)
        assert "Missing in mock: {'C'}" in str(exc_info.value)
        assert "Extra in mock: {'B'}" in str(exc_info.value)