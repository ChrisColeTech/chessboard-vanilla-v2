#!/usr/bin/env python3
"""
File Writer
Responsible for writing generated content to files
"""

import logging
from pathlib import Path
from typing import Optional


class FileWriter:
    """Handles file writing operations"""
    
    def __init__(self, output_path: str = "../../backend-v2", dry_run: bool = False):
        self.output_path = Path(output_path)
        self.dry_run = dry_run
        self.logger = logging.getLogger("file_writer")
        
        # Track written files for reporting
        self.written_files = []
    
    def write_file(self, relative_path: str, content: str, force: bool = False) -> bool:
        """Write content to a file"""
        file_path = self.output_path / relative_path
        
        if self.dry_run:
            self.logger.info(f"🔍 [DRY RUN] Would write: {relative_path}")
            return True
        
        try:
            # Check if file exists and we're not forcing
            if file_path.exists() and not force:
                self.logger.warning(f"⚠️ File exists, skipping: {relative_path}")
                return False
            
            # Create directories as needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            file_path.write_text(content, encoding='utf-8')
            
            self.written_files.append(str(file_path))
            self.logger.info(f"📝 Written: {relative_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to write {relative_path}: {e}")
            return False
    
    def ensure_directory(self, relative_path: str) -> bool:
        """Ensure a directory exists"""
        dir_path = self.output_path / relative_path
        
        if self.dry_run:
            self.logger.debug(f"🔍 [DRY RUN] Would create directory: {relative_path}")
            return True
        
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"📁 Created directory: {relative_path}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to create directory {relative_path}: {e}")
            return False
    
    def get_written_files(self) -> list:
        """Get list of files that were written"""
        return self.written_files.copy()
    
    def clear_written_files(self):
        """Clear the list of written files"""
        self.written_files.clear()
    
    def get_stats(self) -> dict:
        """Get writing statistics"""
        return {
            'total_files': len(self.written_files),
            'dry_run': self.dry_run,
            'output_path': str(self.output_path)
        }


class FilePathHelper:
    """Helper for generating consistent file paths"""
    
    @staticmethod
    def to_camel_case(snake_str: str) -> str:
        """Convert snake_case to camelCase"""
        components = snake_str.replace('-', '_').split('_')
        return components[0] + ''.join(word.capitalize() for word in components[1:])
    
    @staticmethod
    def to_pascal_case(snake_str: str) -> str:
        """Convert snake_case to PascalCase"""
        components = snake_str.replace('-', '_').split('_')
        return ''.join(word.capitalize() for word in components)
    
    @staticmethod
    def to_kebab_case(input_str: str) -> str:
        """Convert snake_case or camelCase to kebab-case"""
        # Handle camelCase to kebab-case
        import re
        # Insert hyphens before uppercase letters (for camelCase)
        s1 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', input_str)
        # Replace underscores with hyphens (for snake_case)
        s2 = s1.replace('_', '-')
        return s2.lower()
    
    @staticmethod
    def get_model_path(entity: str) -> str:
        """Get path for model file"""
        return f"src/models/{entity}.ts"
    
    @staticmethod
    def get_service_path(entity_lower: str) -> str:
        """Get path for service file"""
        return f"src/services/{entity_lower}Service.ts"
    
    @staticmethod
    def get_routes_path(entities: str) -> str:
        """Get path for routes file using camelCase"""
        filename = FilePathHelper.to_camel_case(entities)
        return f"src/routes/{filename}.ts"
    
    @staticmethod
    def get_infrastructure_paths() -> dict:
        """Get paths for infrastructure files"""
        return {
            'database': 'src/utils/database.ts',
            'auth_middleware': 'src/middleware/auth.ts',
            'validation_middleware': 'src/middleware/validation.ts',
            'app': 'src/app.ts'
        }