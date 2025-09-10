#!/usr/bin/env python3
"""
Configuration module for backend generators
Centralized path and configuration management
"""

import os
from pathlib import Path

def get_backend_path() -> str:
    """
    Get the backend path from environment or use intelligent defaults
    """
    # First check environment variable
    if env_path := os.getenv('BACKEND_PATH'):
        return env_path
    
    # Find project root by looking for package.json or .git
    current = Path(__file__).parent
    while current != current.parent:
        if (current / '.git').exists() or (current / 'package.json').exists():
            # Found project root, look for backend-v2
            backend_v2 = current / 'backend-v2'
            if backend_v2.exists():
                return str(backend_v2)
            # Fallback to backend
            backend = current / 'backend'
            if backend.exists():
                return str(backend)
            break
        current = current.parent
    
    # Last resort fallback
    return str(Path(__file__).parent.parent.parent / 'backend-v2')

# Default backend path
DEFAULT_BACKEND_PATH = get_backend_path()

class GeneratorConfig:
    """Configuration settings for all generators"""
    
    def __init__(self, backend_path: str = None):
        self.backend_path = backend_path or DEFAULT_BACKEND_PATH
        self.backup_enabled = False  # Disable backup by default
        self.verbose = False
        self.dry_run = False
    
    def get_path(self) -> Path:
        """Get backend path as Path object"""
        return Path(self.backend_path)