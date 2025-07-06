"""Tests for syft_objects.data_accessor module"""

import pytest
import json
import pickle
import sqlite3
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import pandas as pd
import numpy as np
import yaml

from syft_objects.data_accessor import DataAccessor


class TestDataAccessor:
    """Test DataAccessor class"""
    
    def test_init(self):
        """Test DataAccessor initialization"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        assert accessor._syft_url == "syft://test@example.com/test.txt"
        assert accessor._syft_object == mock_obj
        assert accessor._cached_obj is None
        assert accessor._cached_path is None
    
    def test_url_property(self):
        """Test url property"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        assert accessor.url == "syft://test@example.com/test.txt"
    
    def test_path_property(self):
        """Test path property with caching"""
        mock_obj = Mock()
        mock_obj._get_local_file_path.return_value = "/local/path/test.txt"
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        # First access
        path1 = accessor.path
        assert path1 == "/local/path/test.txt"
        assert mock_obj._get_local_file_path.call_count == 1
        
        # Second access should use cache
        path2 = accessor.path
        assert path2 == "/local/path/test.txt"
        assert mock_obj._get_local_file_path.call_count == 1  # Still 1
    
    def test_file_property_text(self, temp_dir):
        """Test file property with text file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello World")
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        with accessor.file as f:
            content = f.read()
        
        assert content == "Hello World"
    
    def test_file_property_binary(self, temp_dir):
        """Test file property with binary file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.bin"
        test_file.write_bytes(b'\x00\x01\x02\x03')
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.bin", mock_obj)
        
        with accessor.file as f:
            content = f.read()
        
        assert content == b'\x00\x01\x02\x03'
    
    def test_file_property_not_found(self):
        """Test file property when file not found"""
        mock_obj = Mock()
        mock_obj._get_local_file_path.return_value = ""
        
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        with pytest.raises(FileNotFoundError, match="File not found"):
            _ = accessor.file
    
    def test_obj_property_caching(self):
        """Test obj property with caching"""
        mock_obj = Mock()
        mock_obj._get_local_file_path.return_value = "/path/test.txt"
        
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        with patch.object(accessor, '_load_file_content') as mock_load:
            mock_load.return_value = "loaded content"
            
            # First access
            obj1 = accessor.obj
            assert obj1 == "loaded content"
            assert mock_load.call_count == 1
            
            # Second access should use cache
            obj2 = accessor.obj
            assert obj2 == "loaded content"
            assert mock_load.call_count == 1  # Still 1
    
    def test_load_file_content_txt(self, temp_dir):
        """Test loading text file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello World")
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        content = accessor._load_file_content()
        
        assert content == "Hello World"
    
    def test_load_file_content_csv_with_pandas(self, temp_dir):
        """Test loading CSV file with pandas available"""
        mock_obj = Mock()
        test_file = temp_dir / "test.csv"
        test_file.write_text("col1,col2\n1,2\n3,4")
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.csv", mock_obj)
        df = accessor._load_file_content()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ['col1', 'col2']
    
    def test_load_file_content_csv_without_pandas(self, temp_dir):
        """Test loading CSV file without pandas"""
        mock_obj = Mock()
        test_file = temp_dir / "test.csv"
        csv_content = "col1,col2\n1,2\n3,4"
        test_file.write_text(csv_content)
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.csv", mock_obj)
        
        with patch('builtins.__import__', side_effect=ImportError("No pandas")):
            content = accessor._load_file_content()
        
        assert "Warning: pandas not available" in content
        assert csv_content in content
    
    def test_load_file_content_json(self, temp_dir):
        """Test loading JSON file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.json", mock_obj)
        data = accessor._load_file_content()
        
        assert data == test_data
    
    def test_load_file_content_sqlite(self, temp_dir):
        """Test loading SQLite database"""
        mock_obj = Mock()
        test_file = temp_dir / "test.db"
        
        # Create a simple database
        conn = sqlite3.connect(str(test_file))
        conn.execute("CREATE TABLE test (id INTEGER, name TEXT)")
        conn.close()
        
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.db", mock_obj)
        conn = accessor._load_file_content()
        
        assert isinstance(conn, sqlite3.Connection)
        
        # Verify we can query the table
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert ('test',) in tables
        conn.close()
    
    def test_load_file_content_excel(self, temp_dir):
        """Test loading Excel file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.xlsx"
        
        # Create test Excel file
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        df.to_excel(test_file, index=False)
        
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.xlsx", mock_obj)
        loaded_df = accessor._load_file_content()
        
        assert isinstance(loaded_df, pd.DataFrame)
        assert len(loaded_df) == 2
    
    def test_load_file_content_parquet(self, temp_dir):
        """Test loading Parquet file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.parquet"
        
        # Create test Parquet file
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        df.to_parquet(test_file)
        
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.parquet", mock_obj)
        loaded_df = accessor._load_file_content()
        
        assert isinstance(loaded_df, pd.DataFrame)
        assert len(loaded_df) == 2
    
    def test_load_file_content_pickle(self, temp_dir):
        """Test loading pickle file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.pkl"
        
        test_data = {"key": "value", "list": [1, 2, 3]}
        with open(test_file, 'wb') as f:
            pickle.dump(test_data, f)
        
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.pkl", mock_obj)
        loaded_data = accessor._load_file_content()
        
        assert loaded_data == test_data
    
    def test_load_file_content_yaml(self, temp_dir):
        """Test loading YAML file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.yaml"
        test_data = {"key": "value", "list": [1, 2, 3]}
        test_file.write_text(yaml.dump(test_data))
        
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.yaml", mock_obj)
        loaded_data = accessor._load_file_content()
        
        assert loaded_data == test_data
    
    def test_load_file_content_numpy(self, temp_dir):
        """Test loading numpy array"""
        mock_obj = Mock()
        test_file = temp_dir / "test.npy"
        
        arr = np.array([1, 2, 3, 4])
        np.save(test_file, arr)
        
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.npy", mock_obj)
        loaded_arr = accessor._load_file_content()
        
        assert np.array_equal(loaded_arr, arr)
    
    def test_load_file_content_numpy_archive(self, temp_dir):
        """Test loading numpy archive"""
        mock_obj = Mock()
        test_file = temp_dir / "test.npz"
        
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([4, 5, 6])
        np.savez(test_file, a=arr1, b=arr2)
        
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.npz", mock_obj)
        loaded_data = accessor._load_file_content()
        
        assert isinstance(loaded_data, np.lib.npyio.NpzFile)
        assert np.array_equal(loaded_data['a'], arr1)
        assert np.array_equal(loaded_data['b'], arr2)
    
    def test_load_file_content_binary(self, temp_dir):
        """Test loading binary file"""
        mock_obj = Mock()
        test_file = temp_dir / "test.bin"
        test_file.write_bytes(b'\x00\x01\x02\x03')
        mock_obj._get_local_file_path.return_value = str(test_file)
        
        accessor = DataAccessor("syft://test@example.com/test.bin", mock_obj)
        content = accessor._load_file_content()
        
        assert "Binary file: test.bin" in content
        assert "Size: 4 bytes" in content
    
    def test_load_file_content_not_found(self):
        """Test loading non-existent file"""
        mock_obj = Mock()
        mock_obj._get_local_file_path.return_value = ""
        
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        content = accessor._load_file_content()
        
        assert content == "File not found: syft://test@example.com/test.txt"
    
    def test_load_file_content_error(self):
        """Test error handling in file loading"""
        mock_obj = Mock()
        mock_obj._get_local_file_path.side_effect = Exception("Test error")
        
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        content = accessor._load_file_content()
        
        assert "Error loading file: Test error" in content
    
    def test_repr_html_with_dataframe(self):
        """Test _repr_html_ with pandas DataFrame"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.csv", mock_obj)
        
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        accessor._cached_obj = df
        
        html = accessor._repr_html_()
        assert "<table" in html
        assert "col1" in html
        assert "col2" in html
    
    def test_repr_html_with_string(self):
        """Test _repr_html_ with string content"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        accessor._cached_obj = "Hello World"
        
        html = accessor._repr_html_()
        assert "<pre>Hello World</pre>" in html
    
    def test_repr_html_with_long_string(self):
        """Test _repr_html_ with long string (truncation)"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        accessor._cached_obj = "x" * 2000
        
        html = accessor._repr_html_()
        assert "<pre>" in html
        assert "x" * 1000 in html
        assert "..." in html
    
    def test_repr_html_with_dict(self):
        """Test _repr_html_ with dictionary"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.json", mock_obj)
        
        accessor._cached_obj = {"key": "value", "number": 42}
        
        html = accessor._repr_html_()
        assert "<pre>" in html
        assert '"key": "value"' in html
        assert '"number": 42' in html
    
    def test_repr_html_with_sqlite(self, temp_dir):
        """Test _repr_html_ with SQLite connection"""
        mock_obj = Mock()
        test_file = temp_dir / "test.db"
        
        # Create a database with tables
        conn = sqlite3.connect(str(test_file))
        conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        conn.execute("CREATE TABLE posts (id INTEGER, content TEXT)")
        
        accessor = DataAccessor("syft://test@example.com/test.db", mock_obj)
        accessor._cached_obj = conn
        
        html = accessor._repr_html_()
        assert "SQLite Database" in html
        assert "users" in html
        assert "posts" in html
        
        conn.close()
    
    def test_repr_html_with_custom_repr(self):
        """Test _repr_html_ with object that has custom _repr_html_"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        custom_obj = Mock()
        custom_obj._repr_html_ = Mock(return_value="<div>Custom HTML</div>")
        accessor._cached_obj = custom_obj
        
        html = accessor._repr_html_()
        assert html == "<div>Custom HTML</div>"
    
    def test_repr_html_error(self):
        """Test _repr_html_ error handling"""
        mock_obj = Mock()
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        # Force an error by setting obj to something that will fail
        accessor._cached_obj = Mock()
        accessor._cached_obj.__str__ = Mock(side_effect=Exception("Test error"))
        
        html = accessor._repr_html_()
        assert "Error generating HTML representation" in html
        assert "Test error" in html
    
    def test_repr_and_str(self):
        """Test __repr__ and __str__ methods"""
        mock_obj = Mock()
        mock_obj._get_local_file_path.return_value = "/local/path/test.txt"
        accessor = DataAccessor("syft://test@example.com/test.txt", mock_obj)
        
        repr_str = repr(accessor)
        assert "DataAccessor" in repr_str
        assert "syft://test@example.com/test.txt" in repr_str
        assert "/local/path/test.txt" in repr_str
        
        str_str = str(accessor)
        assert str_str == repr_str
    
    @property
    def syft_url(self) -> str:
        """For testing parent_object property"""
        return self._syft_url
    
    @property  
    def parent_object(self):
        """For testing parent_object property"""
        return self._syft_object