import yaml
import os
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from YAML file and environment variables"""
        config_path = Path(__file__).parent.parent / "config" / "config.yml"
        
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        # Override with environment variables if they exist
        self.config['database']['base_path'] = os.getenv(
            'SOM_DB_PATH',
            self.config['database']['base_path']
        )
    
    def get_db_path(self, db_name: str) -> Path:
        """Get the full path to a database file"""
        base_path = Path(self.config['database']['base_path'])
        db_file = self.config['database']['files'].get(db_name)
        
        if not db_file:
            raise ValueError(f"Unknown database: {db_name}")
            
        return base_path / db_file
    
    def get(self, *keys: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation"""
        current = self.config
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, default)
            else:
                return default
        return current