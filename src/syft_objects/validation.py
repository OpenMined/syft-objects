"""Validation utilities for ensuring mock and real file compatibility."""

import json
import pickle
from pathlib import Path
from typing import Optional

import pandas as pd


class MockRealValidationError(ValueError):
    """Raised when mock and real files are incompatible."""
    
    def __init__(self, message: str, file_type: Optional[str] = None, suggestion: Optional[str] = None):
        self.file_type = file_type
        self.suggestion = suggestion
        
        full_message = f"Mock/Real Validation Error: {message}"
        if suggestion:
            full_message += f"\n\nSuggestion: {suggestion}"
        full_message += "\n\nTo skip validation, use: create_object(..., skip_validation=True)"
        
        super().__init__(full_message)


def check_csv_compatibility(mock_path: Path, real_path: Path) -> None:
    """Check if CSV files have compatible column structure."""
    try:
        mock_df = pd.read_csv(mock_path, nrows=1)
        real_df = pd.read_csv(real_path, nrows=1)
        
        mock_cols = list(mock_df.columns)
        real_cols = list(real_df.columns)
        
        if mock_cols != real_cols:
            missing = set(real_cols) - set(mock_cols)
            extra = set(mock_cols) - set(real_cols)
            
            error_msg = f"CSV column mismatch between mock and real files"
            if missing:
                error_msg += f"\n  Missing in mock: {missing}"
            if extra:
                error_msg += f"\n  Extra in mock: {extra}"
                
            raise MockRealValidationError(
                error_msg,
                file_type="CSV",
                suggestion="Ensure your mock CSV has the same column names as the real CSV"
            )
    except pd.errors.EmptyDataError:
        raise MockRealValidationError(
            "One or both CSV files are empty",
            file_type="CSV",
            suggestion="Provide at least header rows in both files"
        )
    except Exception as e:
        if isinstance(e, MockRealValidationError):
            raise
        raise MockRealValidationError(
            f"Failed to read CSV files: {str(e)}",
            file_type="CSV",
            suggestion="Ensure both files are valid CSV format"
        )


def check_json_compatibility(mock_path: Path, real_path: Path) -> None:
    """Check if JSON files have compatible structure."""
    try:
        with open(mock_path) as f:
            mock_data = json.load(f)
        with open(real_path) as f:
            real_data = json.load(f)
            
        # Check if both are same type (dict, list, etc)
        if type(mock_data) != type(real_data):
            raise MockRealValidationError(
                f"JSON type mismatch: mock is {type(mock_data).__name__}, "
                f"real is {type(real_data).__name__}",
                file_type="JSON",
                suggestion="Ensure both files have the same JSON structure type (dict, list, etc.)"
            )
            
        # For dicts, check top-level keys
        if isinstance(real_data, dict):
            mock_keys = set(mock_data.keys())
            real_keys = set(real_data.keys())
            
            if mock_keys != real_keys:
                missing = real_keys - mock_keys
                extra = mock_keys - real_keys
                
                error_msg = "JSON key mismatch between mock and real files"
                if missing:
                    error_msg += f"\n  Missing in mock: {missing}"
                if extra:
                    error_msg += f"\n  Extra in mock: {extra}"
                    
                raise MockRealValidationError(
                    error_msg,
                    file_type="JSON",
                    suggestion="Mock JSON should have the same top-level keys as real JSON"
                )
                
    except json.JSONDecodeError as e:
        raise MockRealValidationError(
            f"Invalid JSON format: {str(e)}",
            file_type="JSON", 
            suggestion="Ensure both files contain valid JSON"
        )
    except Exception as e:
        if isinstance(e, MockRealValidationError):
            raise
        raise MockRealValidationError(
            f"Failed to read JSON files: {str(e)}",
            file_type="JSON"
        )


def check_dataframe_compatibility(mock_path: Path, real_path: Path) -> None:
    """For parquet/pickle files containing DataFrames."""
    try:
        # Load based on extension
        if str(mock_path).endswith('.parquet'):
            mock_df = pd.read_parquet(mock_path)
            real_df = pd.read_parquet(real_path)
        else:  # pickle
            with open(mock_path, 'rb') as f:
                mock_df = pickle.load(f)
            with open(real_path, 'rb') as f:
                real_df = pickle.load(f)
                
        # Check if both are DataFrames
        if not isinstance(mock_df, pd.DataFrame) or not isinstance(real_df, pd.DataFrame):
            raise MockRealValidationError(
                "Files must both contain pandas DataFrames",
                file_type="DataFrame",
                suggestion="Ensure both files contain DataFrame objects"
            )
            
        # Check columns
        mock_cols = list(mock_df.columns)
        real_cols = list(real_df.columns)
        
        if mock_cols != real_cols:
            missing = set(real_cols) - set(mock_cols)
            extra = set(mock_cols) - set(real_cols)
            
            error_msg = "DataFrame column mismatch"
            if missing:
                error_msg += f"\n  Missing in mock: {missing}"
            if extra:
                error_msg += f"\n  Extra in mock: {extra}"
                
            raise MockRealValidationError(
                error_msg,
                file_type="DataFrame",
                suggestion="Mock DataFrame should have the same columns as the real DataFrame"
            )
            
        # Check dtypes (warning only)
        dtype_mismatches = []
        for col in mock_cols:
            if mock_df[col].dtype != real_df[col].dtype:
                dtype_mismatches.append(
                    f"{col}: mock={mock_df[col].dtype}, real={real_df[col].dtype}"
                )
        
        if dtype_mismatches:
            # This is a warning, not an error
            print(f"Warning: Column dtype differences:\n  " + "\n  ".join(dtype_mismatches))
            
    except Exception as e:
        if isinstance(e, MockRealValidationError):
            raise
        raise MockRealValidationError(
            f"Failed to load DataFrame files: {str(e)}",
            file_type="DataFrame",
            suggestion="Ensure files are valid parquet/pickle format containing DataFrames"
        )


# Registry of validators by file extension
VALIDATORS = {
    '.csv': check_csv_compatibility,
    '.json': check_json_compatibility,
    '.parquet': check_dataframe_compatibility,
    '.pkl': check_dataframe_compatibility,
    '.pickle': check_dataframe_compatibility,
}


def validate_mock_real_compatibility(mock_path: Path, real_path: Path, skip_validation: bool = False) -> None:
    """Validate that mock and real files are compatible.
    
    Args:
        mock_path: Path to mock file
        real_path: Path to real file
        skip_validation: If True, skip all validation
        
    Raises:
        MockRealValidationError: If files are incompatible
    """
    if skip_validation:
        return
        
    # Convert to Path objects if needed
    mock_path = Path(mock_path)
    real_path = Path(real_path)
    
    # Check file extensions match (basic validation)
    mock_ext = mock_path.suffix.lower()
    real_ext = real_path.suffix.lower()
    
    if mock_ext != real_ext:
        raise MockRealValidationError(
            f"File extensions don't match: mock has '{mock_ext}', real has '{real_ext}'",
            suggestion="Ensure mock and real files have the same file extension"
        )
    
    # Run type-specific validation if available
    if real_ext in VALIDATORS:
        VALIDATORS[real_ext](mock_path, real_path)