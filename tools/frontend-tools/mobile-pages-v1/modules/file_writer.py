"""
File Writer with validation and warning headers for generated files.
Integrates with shared utilities as specified in Phase 2 plan.
"""

from pathlib import Path
from typing import Optional
import os
import shutil
import sys
from datetime import datetime

# Add shared utilities to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from file_utils import write_file_with_warning, add_warning_header
from import_utils import smart_add_import


class FileWriter:
    """Handles file writing with validation and safety checks."""
    
    def __init__(self, logger=None):
        self.backup_dir = None
        self.logger = logger
    
    def write_file(self, file_path: Path, content: str, generator_name: str = "TemplateBasedGenerator", 
                  source_file: str = "/tools/frontend-tools/mobile-pages-v2/main.py") -> None:
        """
        Write content to file with warning header using shared utilities.
        
        Args:
            file_path: Target file path
            content: Content to write
            generator_name: Name of the generator creating the file
            source_file: Source file path for reference
        """
        # Backup existing file if it exists
        backup_path = self._backup_existing_file(file_path)
        
        try:
            # Validate content before writing
            if not self._validate_file_content(content):
                raise ValueError(f"Invalid content for file: {file_path}")
            
            # Use shared utility to write file with warning header
            write_file_with_warning(file_path, content, generator_name, source_file)
            
            if self.logger:
                self.logger.verbose(f"Created: {file_path}")
            else:
                print(f"  ✅ Created: {file_path}")
            
        except Exception as e:
            # Restore backup if something went wrong
            if backup_path and backup_path.exists():
                shutil.move(str(backup_path), str(file_path))
                if self.logger:
                    self.logger.warning(f"Error occurred, restored backup: {file_path}")
                else:
                    print(f"  ⚠️  Error occurred, restored backup: {file_path}")
            raise e
    
    def add_import(self, file_path: Path, module: str, import_name: str) -> None:
        """
        Add an import to an existing file using smart import utility.
        
        Args:
            file_path: Path to the file to modify
            module: Module to import from
            import_name: Name to import
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Cannot add import to non-existent file: {file_path}")
        
        # Read current content
        current_content = file_path.read_text(encoding='utf-8')
        
        # Add import using shared utility
        updated_content = smart_add_import(current_content, module, import_name)
        
        # Write back if changed
        if updated_content != current_content:
            # Backup first
            backup_path = self._backup_existing_file(file_path)
            
            try:
                file_path.write_text(updated_content, encoding='utf-8')
                print(f"  📥 Added import: {import_name} from {module} to {file_path}")
            except Exception as e:
                # Restore backup on error
                if backup_path and backup_path.exists():
                    shutil.move(str(backup_path), str(file_path))
                raise e
    
    def _backup_existing_file(self, file_path: Path) -> Optional[Path]:
        """Create backup of existing file."""
        if not file_path.exists():
            return None
        
        # Create backup directory if needed
        if self.backup_dir is None:
            self.backup_dir = file_path.parent / ".generator_backups"
            self.backup_dir.mkdir(exist_ok=True)
        
        # Create backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(str(file_path), str(backup_path))
        return backup_path
    
    def _validate_file_content(self, content: str) -> bool:
        """Validate file content before writing."""
        # Basic validation checks
        if not content or content.strip() == "":
            return False
        
        # Check for common issues
        if "{{" in content and "}}" in content:
            # Warn about potential unsubstituted template variables
            print(f"  ⚠️  Warning: Content contains template variables that may not have been substituted")
        
        return True
    
    def create_directory(self, dir_path: Path) -> None:
        """Create directory with proper error handling."""
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  📁 Created directory: {dir_path}")
        except Exception as e:
            raise OSError(f"Failed to create directory {dir_path}: {e}")
    
    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists."""
        return file_path.exists()
    
    def backup_file(self, file_path: Path) -> Optional[Path]:
        """Create backup of a file."""
        return self._backup_existing_file(file_path)
    
    def restore_backup(self, original_path: Path, backup_path: Path) -> bool:
        """Restore file from backup."""
        try:
            if backup_path.exists():
                shutil.move(str(backup_path), str(original_path))
                return True
            return False
        except Exception:
            return False
    
    def cleanup_backups(self, max_backups: int = 10) -> None:
        """Clean up old backup files, keeping only the most recent."""
        if not self.backup_dir or not self.backup_dir.exists():
            return
        
        # Get all backup files sorted by modification time
        backup_files = sorted(
            self.backup_dir.glob("*.backup_*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        # Remove excess backups
        for backup_file in backup_files[max_backups:]:
            try:
                backup_file.unlink()
                print(f"  🗑️  Cleaned up old backup: {backup_file.name}")
            except Exception:
                pass  # Ignore cleanup errors