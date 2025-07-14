# syft-objects mock analyzer - Smart analysis of mock data characteristics

import os
import json
import csv
from pathlib import Path
from typing import Optional, Tuple, List, Dict
import mimetypes


class MockAnalyzer:
    """Analyzes mock files and suggests appropriate notes"""
    
    # Safe analyses that only look at mock file
    SAFE_ANALYSES = ["empty", "schema_only", "file_type", "mock_only_size"]
    
    # Analyses that compare mock vs private (require consent)
    COMPARISON_ANALYSES = ["size_ratio", "row_ratio", "time_subset", "sampling"]
    
    # Advanced inference (require explicit consent)
    INFERENCE_ANALYSES = ["differential_privacy", "synthetic_detection"]
    
    def __init__(self, sensitivity_level: str = "ask"):
        """
        Initialize analyzer with sensitivity level.
        
        Args:
            sensitivity_level: "always" | "ask" | "never"
        """
        self.sensitivity_level = sensitivity_level
    
    def analyze(
        self, 
        mock_path: Optional[Path] = None,
        private_path: Optional[Path] = None,
        mock_contents: Optional[str] = None,
        private_contents: Optional[str] = None,
        level: str = "safe"
    ) -> Optional[str]:
        """
        Analyze mock data and suggest a note.
        
        Args:
            mock_path: Path to mock file
            private_path: Path to private file  
            mock_contents: Mock file contents (if not saved to file yet)
            private_contents: Private file contents (if not saved to file yet)
            level: "safe" | "comparison" | "inference"
            
        Returns:
            Suggested mock note or None
        """
        suggestions = []
        
        # Always do safe analyses (mock only)
        if level in ["safe", "comparison", "inference"]:
            suggestions.extend(self._safe_analyses(mock_path, mock_contents))
        
        # Do comparison analyses if allowed
        if level in ["comparison", "inference"] and self.sensitivity_level != "never":
            if private_path or private_contents:
                suggestions.extend(self._comparison_analyses(
                    mock_path, private_path, mock_contents, private_contents
                ))
        
        # Do inference analyses if allowed
        if level == "inference" and self.sensitivity_level == "always":
            suggestions.extend(self._inference_analyses(mock_path, mock_contents))
        
        # Return the best suggestion
        return self._select_best_suggestion(suggestions)
    
    def _safe_analyses(
        self, 
        mock_path: Optional[Path],
        mock_contents: Optional[str]
    ) -> List[Tuple[int, str]]:
        """Analyses that only examine the mock file"""
        suggestions = []
        
        # Check if empty
        if mock_contents is not None:
            if not mock_contents or mock_contents.strip() == "":
                suggestions.append((10, "Empty mock file"))
        elif mock_path and mock_path.exists():
            if mock_path.stat().st_size == 0:
                suggestions.append((10, "Empty mock file"))
        
        # Check for schema-only patterns
        if mock_contents:
            if self._is_schema_only(mock_contents):
                suggestions.append((9, "Schema preview"))
            elif "[MOCK DATA]" in mock_contents:
                suggestions.append((8, "Mock placeholder"))
        
        # Analyze file type
        if mock_path:
            ext = mock_path.suffix.lower()
            if ext == ".csv":
                rows = self._count_csv_rows(mock_path, mock_contents)
                if rows > 0:
                    suggestions.append((7, f"{rows} data rows"))
            elif ext == ".json":
                if self._is_json_structure_only(mock_path, mock_contents):
                    suggestions.append((8, "JSON structure"))
            elif ext in [".log", ".txt"]:
                lines = self._count_lines(mock_path, mock_contents)
                if lines > 0:
                    suggestions.append((6, f"{lines} lines"))
        
        return suggestions
    
    def _comparison_analyses(
        self,
        mock_path: Optional[Path],
        private_path: Optional[Path],
        mock_contents: Optional[str],
        private_contents: Optional[str]
    ) -> List[Tuple[int, str]]:
        """Analyses that compare mock vs private data"""
        suggestions = []
        
        # Size comparison
        if mock_path and private_path and mock_path.exists() and private_path.exists():
            mock_size = mock_path.stat().st_size
            private_size = private_path.stat().st_size
            
            if private_size > 0 and mock_size > 0:
                ratio = mock_size / private_size
                percentage = ratio * 100
                
                # Show enough decimal places to avoid showing 0.0% for non-zero data
                if percentage < 0.01:
                    suggestions.append((8, f"{percentage:.3f}% sample by size"))
                elif percentage < 0.1:
                    suggestions.append((8, f"{percentage:.2f}% sample by size"))
                elif percentage < 1:
                    suggestions.append((8, f"{percentage:.1f}% sample by size"))
                elif percentage < 10:
                    suggestions.append((7, f"{percentage:.0f}% sample"))
                else:
                    suggestions.append((6, f"{percentage:.0f}% of size"))
        
        # Row comparison for CSV files
        if mock_path and private_path:
            if mock_path.suffix.lower() == ".csv" and private_path.suffix.lower() == ".csv":
                mock_rows = self._count_csv_rows(mock_path, mock_contents)
                private_rows = self._count_csv_rows(private_path, private_contents)
                
                if mock_rows > 0 and private_rows > 0:
                    if mock_rows < private_rows:
                        if mock_rows <= 1000 and private_rows > 10000:
                            suggestions.append((9, f"First {mock_rows} rows"))
                        else:
                            ratio = mock_rows / private_rows
                            suggestions.append((8, f"{ratio*100:.0f}% of rows"))
        
        return suggestions
    
    def _inference_analyses(
        self,
        mock_path: Optional[Path],
        mock_contents: Optional[str]
    ) -> List[Tuple[int, str]]:
        """Advanced inference analyses"""
        suggestions = []
        
        # Try to detect differential privacy markers
        if mock_contents and "differential_privacy" in mock_contents.lower():
            suggestions.append((10, "Differential privacy synthetic data"))
        
        # Detect synthetic data patterns
        if self._looks_synthetic(mock_path, mock_contents):
            suggestions.append((9, "Synthetic data"))
        
        return suggestions
    
    def _select_best_suggestion(self, suggestions: List[Tuple[int, str]]) -> Optional[str]:
        """Select the best suggestion based on priority scores"""
        if not suggestions:
            return None
        
        # Sort by priority (higher is better)
        suggestions.sort(key=lambda x: x[0], reverse=True)
        return suggestions[0][1]
    
    # Helper methods
    
    def _is_schema_only(self, contents: str) -> bool:
        """Check if content appears to be schema/structure only"""
        schema_indicators = ["<schema>", "SCHEMA", "structure", "template", "example"]
        return any(indicator in contents for indicator in schema_indicators)
    
    def _is_json_structure_only(self, path: Optional[Path], contents: Optional[str]) -> bool:
        """Check if JSON contains only structure with null/empty values"""
        try:
            if contents:
                data = json.loads(contents)
            elif path and path.exists():
                with open(path) as f:
                    data = json.load(f)
            else:
                return False
            
            # Check if all values are None, empty, or placeholder
            def all_empty(obj):
                if isinstance(obj, dict):
                    return all(all_empty(v) for v in obj.values())
                elif isinstance(obj, list):
                    return len(obj) == 0 or all(all_empty(v) for v in obj)
                else:
                    return obj in [None, "", "placeholder", "example", 0, False]
            
            return all_empty(data)
        except:
            return False
    
    def _count_csv_rows(self, path: Optional[Path], contents: Optional[str]) -> int:
        """Count data rows in a CSV file (excluding header)"""
        try:
            if contents:
                lines = contents.strip().split('\n')
                # Subtract 1 for header if there are any lines
                return max(0, len(lines) - 1)
            elif path and path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    row_count = sum(1 for _ in csv.reader(f))
                    # Subtract 1 for header if there are any rows
                    return max(0, row_count - 1)
        except:
            pass
        return 0
    
    def _count_lines(self, path: Optional[Path], contents: Optional[str]) -> int:
        """Count lines in a text file"""
        try:
            if contents:
                return len(contents.strip().split('\n'))
            elif path and path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return sum(1 for _ in f)
        except:
            pass
        return 0
    
    def _looks_synthetic(self, path: Optional[Path], contents: Optional[str]) -> bool:
        """Detect if data looks synthetic"""
        synthetic_markers = [
            "synthetic", "generated", "fake", "sample", "demo",
            "test_data", "mock_data", "example_data"
        ]
        
        if contents:
            content_lower = contents.lower()
            return any(marker in content_lower for marker in synthetic_markers)
        
        if path:
            # Check filename
            name_lower = path.name.lower()
            return any(marker in name_lower for marker in synthetic_markers)
        
        return False


def suggest_mock_note(
    mock_path: Optional[Path] = None,
    private_path: Optional[Path] = None,
    mock_contents: Optional[str] = None,
    private_contents: Optional[str] = None,
    sensitivity: str = "ask"
) -> Optional[str]:
    """
    Convenience function to get a mock note suggestion.
    
    Args:
        mock_path: Path to mock file
        private_path: Path to private file
        mock_contents: Mock file contents
        private_contents: Private file contents  
        sensitivity: "always" | "ask" | "never"
        
    Returns:
        Suggested mock note or None
    """
    analyzer = MockAnalyzer(sensitivity)
    
    # Determine analysis level based on what's provided
    if private_path or private_contents:
        level = "comparison" if sensitivity != "never" else "safe"
    else:
        level = "safe"
    
    return analyzer.analyze(
        mock_path=mock_path,
        private_path=private_path,
        mock_contents=mock_contents,
        private_contents=private_contents,
        level=level
    )