"""Tests for mock/real file validation."""

import json
import pickle
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from syft_objects.validation import (
    MockRealValidationError,
    check_csv_compatibility,
    check_json_compatibility,
    check_dataframe_compatibility,
    validate_mock_real_compatibility,
)


class TestMockRealValidationError:
    """Test the custom validation error class."""
    
    def test_error_message_basic(self):
        """Test basic error message formatting."""
        error = MockRealValidationError("Basic error")
        assert "Mock/Real Validation Error: Basic error" in str(error)
        assert "To skip validation, use: create_object(..., skip_validation=True)" in str(error)
    
    def test_error_message_with_suggestion(self):
        """Test error message with suggestion."""
        error = MockRealValidationError(
            "Column mismatch",
            file_type="CSV",
            suggestion="Check your columns"
        )
        assert "Mock/Real Validation Error: Column mismatch" in str(error)
        assert "Suggestion: Check your columns" in str(error)
        assert "To skip validation, use: create_object(..., skip_validation=True)" in str(error)
    
    def test_error_attributes(self):
        """Test error attributes are stored correctly."""
        error = MockRealValidationError(
            "Test error",
            file_type="JSON",
            suggestion="Fix the JSON"
        )
        assert error.file_type == "JSON"
        assert error.suggestion == "Fix the JSON"


class TestCSVCompatibility:
    """Test CSV file compatibility validation."""
    
    def test_matching_csv_files(self, tmp_path):
        """Test that matching CSV files pass validation."""
        # Create matching CSV files
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.csv"
        
        df.to_csv(mock_path, index=False)
        df.to_csv(real_path, index=False)
        
        # Should not raise
        check_csv_compatibility(mock_path, real_path)
    
    def test_column_mismatch(self, tmp_path):
        """Test that mismatched columns raise error."""
        mock_df = pd.DataFrame({'col1': [1], 'col2': ['a']})
        real_df = pd.DataFrame({'col1': [1], 'col3': ['b']})
        
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.csv"
        
        mock_df.to_csv(mock_path, index=False)
        real_df.to_csv(real_path, index=False)
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_csv_compatibility(mock_path, real_path)
        
        error = exc_info.value
        assert "CSV column mismatch" in str(error)
        assert "Missing in mock: {'col3'}" in str(error)
        assert "Extra in mock: {'col2'}" in str(error)
    
    def test_empty_csv_files(self, tmp_path):
        """Test that empty CSV files raise appropriate error."""
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.csv"
        
        mock_path.write_text("")
        real_path.write_text("")
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_csv_compatibility(mock_path, real_path)
        
        assert "One or both CSV files are empty" in str(exc_info.value)
    
    def test_invalid_csv_file(self, tmp_path):
        """Test that invalid CSV files raise appropriate error."""
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.notcsv"  # Wrong extension to trigger read error
        
        mock_path.write_text("col1,col2\n1,2")
        real_path.write_text("")  # Empty file
        
        # Rename to .csv after writing to bypass extension check in validate_mock_real_compatibility
        real_csv_path = tmp_path / "real.csv"
        real_path.rename(real_csv_path)
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_csv_compatibility(mock_path, real_csv_path)
        
        # Should get empty file error
        assert "One or both CSV files are empty" in str(exc_info.value)


class TestJSONCompatibility:
    """Test JSON file compatibility validation."""
    
    def test_matching_json_dicts(self, tmp_path):
        """Test that matching JSON dictionaries pass validation."""
        data = {"key1": "value1", "key2": 123}
        
        mock_path = tmp_path / "mock.json"
        real_path = tmp_path / "real.json"
        
        mock_path.write_text(json.dumps(data))
        real_path.write_text(json.dumps(data))
        
        # Should not raise
        check_json_compatibility(mock_path, real_path)
    
    def test_type_mismatch(self, tmp_path):
        """Test that different JSON types raise error."""
        mock_path = tmp_path / "mock.json"
        real_path = tmp_path / "real.json"
        
        mock_path.write_text(json.dumps({"key": "value"}))
        real_path.write_text(json.dumps([1, 2, 3]))
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_json_compatibility(mock_path, real_path)
        
        assert "JSON type mismatch" in str(exc_info.value)
        assert "mock is dict" in str(exc_info.value)
        assert "real is list" in str(exc_info.value)
    
    def test_key_mismatch(self, tmp_path):
        """Test that mismatched dictionary keys raise error."""
        mock_data = {"key1": "value1", "key2": "value2"}
        real_data = {"key1": "value1", "key3": "value3"}
        
        mock_path = tmp_path / "mock.json"
        real_path = tmp_path / "real.json"
        
        mock_path.write_text(json.dumps(mock_data))
        real_path.write_text(json.dumps(real_data))
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_json_compatibility(mock_path, real_path)
        
        error = exc_info.value
        assert "JSON key mismatch" in str(error)
        assert "Missing in mock: {'key3'}" in str(error)
        assert "Extra in mock: {'key2'}" in str(error)
    
    def test_json_lists(self, tmp_path):
        """Test that JSON lists pass validation (no key checking)."""
        mock_path = tmp_path / "mock.json"
        real_path = tmp_path / "real.json"
        
        mock_path.write_text(json.dumps([1, 2, 3]))
        real_path.write_text(json.dumps([4, 5, 6]))
        
        # Should not raise - lists don't have keys to check
        check_json_compatibility(mock_path, real_path)
    
    def test_invalid_json(self, tmp_path):
        """Test that invalid JSON raises appropriate error."""
        mock_path = tmp_path / "mock.json"
        real_path = tmp_path / "real.json"
        
        mock_path.write_text('{"valid": "json"}')
        real_path.write_text('not valid json')
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_json_compatibility(mock_path, real_path)
        
        assert "Invalid JSON format" in str(exc_info.value)


class TestDataFrameCompatibility:
    """Test DataFrame (parquet/pickle) compatibility validation."""
    
    def test_matching_parquet_files(self, tmp_path):
        """Test that matching parquet files pass validation."""
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        
        mock_path = tmp_path / "mock.parquet"
        real_path = tmp_path / "real.parquet"
        
        df.to_parquet(mock_path)
        df.to_parquet(real_path)
        
        # Should not raise
        check_dataframe_compatibility(mock_path, real_path)
    
    def test_matching_pickle_files(self, tmp_path):
        """Test that matching pickle DataFrames pass validation."""
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        
        mock_path = tmp_path / "mock.pkl"
        real_path = tmp_path / "real.pkl"
        
        with open(mock_path, 'wb') as f:
            pickle.dump(df, f)
        with open(real_path, 'wb') as f:
            pickle.dump(df, f)
        
        # Should not raise
        check_dataframe_compatibility(mock_path, real_path)
    
    def test_dataframe_column_mismatch(self, tmp_path):
        """Test that mismatched DataFrame columns raise error."""
        mock_df = pd.DataFrame({'col1': [1], 'col2': ['a']})
        real_df = pd.DataFrame({'col1': [1], 'col3': ['b']})
        
        mock_path = tmp_path / "mock.parquet"
        real_path = tmp_path / "real.parquet"
        
        mock_df.to_parquet(mock_path)
        real_df.to_parquet(real_path)
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_dataframe_compatibility(mock_path, real_path)
        
        error = exc_info.value
        assert "DataFrame column mismatch" in str(error)
        assert "Missing in mock: {'col3'}" in str(error)
        assert "Extra in mock: {'col2'}" in str(error)
    
    def test_non_dataframe_pickle(self, tmp_path):
        """Test that non-DataFrame pickle files raise error."""
        mock_path = tmp_path / "mock.pkl"
        real_path = tmp_path / "real.pkl"
        
        with open(mock_path, 'wb') as f:
            pickle.dump({"not": "dataframe"}, f)
        with open(real_path, 'wb') as f:
            pickle.dump([1, 2, 3], f)
        
        with pytest.raises(MockRealValidationError) as exc_info:
            check_dataframe_compatibility(mock_path, real_path)
        
        assert "Files must both contain pandas DataFrames" in str(exc_info.value)
    
    def test_dtype_warning(self, tmp_path, capsys):
        """Test that dtype differences produce warnings but don't fail."""
        mock_df = pd.DataFrame({'col1': [1.0, 2.0]})  # float
        real_df = pd.DataFrame({'col1': [1, 2]})      # int
        
        mock_path = tmp_path / "mock.parquet"
        real_path = tmp_path / "real.parquet"
        
        mock_df.to_parquet(mock_path)
        real_df.to_parquet(real_path)
        
        # Should not raise, but should print warning
        check_dataframe_compatibility(mock_path, real_path)
        
        captured = capsys.readouterr()
        assert "Warning: Column dtype differences" in captured.out


class TestValidateMockRealCompatibility:
    """Test the main validation function."""
    
    def test_skip_validation_flag(self, tmp_path):
        """Test that skip_validation=True skips all checks."""
        mock_path = tmp_path / "mock.txt"
        real_path = tmp_path / "real.csv"  # Different extension!
        
        mock_path.write_text("mock")
        real_path.write_text("real")
        
        # Should not raise despite extension mismatch
        validate_mock_real_compatibility(mock_path, real_path, skip_validation=True)
    
    def test_extension_mismatch(self, tmp_path):
        """Test that mismatched extensions raise error."""
        mock_path = tmp_path / "mock.txt"
        real_path = tmp_path / "real.csv"
        
        mock_path.write_text("mock")
        real_path.write_text("real")
        
        with pytest.raises(MockRealValidationError) as exc_info:
            validate_mock_real_compatibility(mock_path, real_path)
        
        assert "File extensions don't match" in str(exc_info.value)
        assert "mock has '.txt'" in str(exc_info.value)
        assert "real has '.csv'" in str(exc_info.value)
    
    def test_unknown_file_type(self, tmp_path):
        """Test that unknown file types pass basic extension check."""
        mock_path = tmp_path / "mock.xyz"
        real_path = tmp_path / "real.xyz"
        
        mock_path.write_text("mock")
        real_path.write_text("real")
        
        # Should not raise - unknown types just check extensions
        validate_mock_real_compatibility(mock_path, real_path)
    
    def test_csv_validation_called(self, tmp_path):
        """Test that CSV validator is called for .csv files."""
        mock_df = pd.DataFrame({'col1': [1]})
        real_df = pd.DataFrame({'col2': [2]})
        
        mock_path = tmp_path / "mock.csv"
        real_path = tmp_path / "real.csv"
        
        mock_df.to_csv(mock_path, index=False)
        real_df.to_csv(real_path, index=False)
        
        with pytest.raises(MockRealValidationError) as exc_info:
            validate_mock_real_compatibility(mock_path, real_path)
        
        assert "CSV column mismatch" in str(exc_info.value)
    
    def test_json_validation_called(self, tmp_path):
        """Test that JSON validator is called for .json files."""
        mock_path = tmp_path / "mock.json"
        real_path = tmp_path / "real.json"
        
        mock_path.write_text('{"key1": "value"}')
        real_path.write_text('{"key2": "value"}')
        
        with pytest.raises(MockRealValidationError) as exc_info:
            validate_mock_real_compatibility(mock_path, real_path)
        
        assert "JSON key mismatch" in str(exc_info.value)
    
    def test_path_conversion(self, tmp_path):
        """Test that string paths are converted to Path objects."""
        mock_path = str(tmp_path / "mock.txt")
        real_path = str(tmp_path / "real.txt")
        
        Path(mock_path).write_text("mock")
        Path(real_path).write_text("real")
        
        # Should not raise - handles string paths
        validate_mock_real_compatibility(mock_path, real_path)