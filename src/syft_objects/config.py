# syft-objects config - Configuration management for syft-objects

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class SyftObjectsConfig:
    """Configuration management for syft-objects"""
    
    def __init__(self):
        self._config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from various sources in priority order"""
        config = {
            # Default configuration
            "suggest_mock_notes": True,
            "mock_note_timeout": 2.0,
            "mock_note_sensitivity": "ask",  # always|ask|never
            "auto_analyze_mock": True,
        }
        
        # Try to load from ~/.syftbox/syft-objects.yaml
        config_path = Path.home() / ".syftbox" / "syft-objects.yaml"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    user_config = yaml.safe_load(f) or {}
                    config.update(user_config)
            except Exception:
                pass
        
        # Override with environment variables
        env_mapping = {
            "SYFT_OBJECTS_SUGGEST_NOTES": ("suggest_mock_notes", lambda x: x.lower() == "true"),
            "SYFT_OBJECTS_NOTE_TIMEOUT": ("mock_note_timeout", float),
            "SYFT_OBJECTS_NOTE_SENSITIVITY": ("mock_note_sensitivity", str),
            "SYFT_OBJECTS_AUTO_ANALYZE": ("auto_analyze_mock", lambda x: x.lower() == "true"),
        }
        
        for env_var, (config_key, converter) in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    config[config_key] = converter(value)
                except Exception:
                    pass
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value (runtime only, not persisted)"""
        self._config[key] = value
    
    @property
    def suggest_mock_notes(self) -> bool:
        """Whether to suggest mock notes"""
        return self.get("suggest_mock_notes", True)
    
    @suggest_mock_notes.setter
    def suggest_mock_notes(self, value: bool) -> None:
        self.set("suggest_mock_notes", value)
    
    @property
    def mock_note_timeout(self) -> float:
        """Timeout in seconds for mock note suggestions"""
        return self.get("mock_note_timeout", 2.0)
    
    @property
    def mock_note_sensitivity(self) -> str:
        """Sensitivity level for mock note suggestions: always|suggest|never"""
        return self.get("mock_note_sensitivity", "suggest")
    
    @mock_note_sensitivity.setter
    def mock_note_sensitivity(self, value: str) -> None:
        self.set("mock_note_sensitivity", value)
    
    @property
    def auto_analyze_mock(self) -> bool:
        """Whether to automatically analyze mock files"""
        return self.get("auto_analyze_mock", True)


# Global config instance
config = SyftObjectsConfig()