# Test mock notes functionality

import pytest
import os
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.syft_objects import create_object
from src.syft_objects.config import config
from src.syft_objects.mock_analyzer import MockAnalyzer, suggest_mock_note


class TestMockNotes:
    """Test the mock notes feature"""
    
    def setup_method(self):
        """Set up test environment"""
        # Save original config
        self.orig_suggest = config.suggest_mock_notes
        self.orig_sensitivity = config.mock_note_sensitivity
        
        # Disable suggestions by default for tests
        config.suggest_mock_notes = False
        config.mock_note_sensitivity = "never"
        
        # Create temp directory
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up after tests"""
        # Restore config
        config.suggest_mock_notes = self.orig_suggest
        config.mock_note_sensitivity = self.orig_sensitivity
        
        # Clean up temp directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_manual_mock_note(self):
        """Test manually setting a mock note"""
        obj = create_object(
            "test_data",
            mock_contents="sample data",
            private_contents="real data " * 100,
            mock_note="10% sample for testing"
        )
        
        # Check note was set
        assert obj.mock.get_note() == "10% sample for testing"
    
    def test_mock_note_api(self):
        """Test get/set mock note through API"""
        obj = create_object(
            "test_data",
            mock_contents="sample",
            private_contents="real data"
        )
        
        # Initially no note
        assert obj.mock.get_note() is None
        
        # Set a note
        obj.mock.set_note("Test dataset")
        assert obj.mock.get_note() == "Test dataset"
        
        # Update note
        obj.mock.set_note("Updated test dataset")
        assert obj.mock.get_note() == "Updated test dataset"
    
    def test_safe_analysis(self):
        """Test safe mock-only analysis"""
        # Empty mock
        note = suggest_mock_note(
            mock_contents="",
            sensitivity="never"
        )
        assert note == "Empty mock file"
        
        # Mock placeholder
        note = suggest_mock_note(
            mock_contents="[MOCK DATA] Demo version",
            sensitivity="never"
        )
        assert note == "Mock placeholder"
    
    def test_csv_analysis(self):
        """Test CSV file analysis"""
        # Create mock CSV
        mock_csv = Path(self.temp_dir) / "mock.csv"
        mock_csv.write_text("col1,col2,col3\n1,2,3\n4,5,6\n")
        
        note = suggest_mock_note(
            mock_path=mock_csv,
            sensitivity="never"
        )
        assert note == "3 rows"
    
    def test_schema_detection(self):
        """Test schema-only detection"""
        note = suggest_mock_note(
            mock_contents='{"data": null, "schema": true}',
            sensitivity="never"
        )
        # Note might be None if no pattern detected
        assert note is None or "schema" in note.lower() or "structure" in note.lower()
    
    def test_comparison_disabled(self):
        """Test that comparison is disabled when sensitivity is 'never'"""
        # Create files
        mock_csv = Path(self.temp_dir) / "mock.csv"
        private_csv = Path(self.temp_dir) / "private.csv"
        
        mock_csv.write_text("col1,col2\n1,2\n")
        private_csv.write_text("col1,col2\n" + "\n".join(f"{i},{i+1}" for i in range(100)))
        
        # With sensitivity=never, should not compare
        note = suggest_mock_note(
            mock_path=mock_csv,
            private_path=private_csv,
            sensitivity="never"
        )
        
        # Should only get mock-only analysis
        assert note == "2 rows"
        assert "%" not in note
        assert "sample" not in note
    
    def test_analyzer_levels(self):
        """Test different analysis levels"""
        analyzer = MockAnalyzer("never")
        
        # Safe analysis only
        note = analyzer.analyze(
            mock_contents="test data",
            private_contents="much more data",
            level="safe"
        )
        assert note is None or "%" not in note
    
    def test_mock_note_in_metadata(self):
        """Test that mock note is stored in metadata"""
        obj = create_object(
            "test",
            mock_contents="mock",
            private_contents="private",
            mock_note="Test note"
        )
        
        # Check it's in metadata
        assert "mock_note" in obj.get_metadata()
        assert obj.get_metadata()["mock_note"] == "Test note"


class TestMockAnalyzer:
    """Test the MockAnalyzer class"""
    
    def test_empty_detection(self):
        """Test empty file detection"""
        analyzer = MockAnalyzer()
        suggestions = analyzer._safe_analyses(None, "")
        
        # Should detect empty
        assert any("Empty" in s[1] for s in suggestions)
    
    def test_csv_row_counting(self):
        """Test CSV row counting"""
        analyzer = MockAnalyzer()
        
        # Test with contents
        rows = analyzer._count_csv_rows(None, "a,b,c\n1,2,3\n4,5,6")
        assert rows == 3
        
        # Test empty
        rows = analyzer._count_csv_rows(None, "")
        assert rows == 0
    
    def test_json_structure_detection(self):
        """Test JSON structure-only detection"""
        analyzer = MockAnalyzer()
        
        # Structure with null values
        assert analyzer._is_json_structure_only(None, '{"a": null, "b": ""}')
        
        # Structure with data
        assert not analyzer._is_json_structure_only(None, '{"a": "data", "b": 123}')
    
    def test_synthetic_detection(self):
        """Test synthetic data detection"""
        analyzer = MockAnalyzer()
        
        # In filename
        mock_path = Path("synthetic_data.csv")
        assert analyzer._looks_synthetic(mock_path, None)
        
        # In content
        assert analyzer._looks_synthetic(None, "This is generated test data")
        assert not analyzer._looks_synthetic(None, "Real production data")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])