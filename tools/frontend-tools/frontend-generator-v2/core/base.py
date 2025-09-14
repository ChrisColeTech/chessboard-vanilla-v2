"""
Base classes for the scaffolder
"""

from pathlib import Path
from typing import Dict, Any

class BaseScaffolder:
    """Base scaffolder class"""
    
    def __init__(self, output_path: Path):
        self.output_path = output_path
    
    def ensure_dir(self, path: Path):
        """Ensure directory exists"""
        path.mkdir(parents=True, exist_ok=True)
    
    def write_file(self, file_path: Path, content: str):
        """Write content to file"""
        self.ensure_dir(file_path.parent)
        file_path.write_text(content, encoding='utf-8')
        print(f"📝 Created {file_path}")