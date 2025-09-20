"""
Tests for the File Writer module.
"""

import pytest
from pathlib import Path
import tempfile
import os
import sys
from datetime import datetime

# Add the modules directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from file_writer import FileWriter


class TestFileWriter:
    """Test cases for FileWriter class."""
    
    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_root = Path(self.temp_dir)
        self.writer = FileWriter()
    
    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_write_file_creates_new_file(self):
        """Test writing content to a new file."""
        test_file = self.test_root / "test.tsx"
        content = 'export const TestComponent = () => <div>Hello</div>;'
        
        self.writer.write_file(test_file, content)
        
        assert test_file.exists()
        file_content = test_file.read_text()
        assert content in file_content
        assert "WARNING: This file is auto-generated" in file_content
    
    def test_write_file_creates_parent_directories(self):
        """Test that parent directories are created if they don't exist."""
        nested_file = self.test_root / "deep" / "nested" / "path" / "test.tsx"
        content = 'export const TestComponent = () => <div>Hello</div>;'
        
        self.writer.write_file(nested_file, content)
        
        assert nested_file.exists()
        assert nested_file.parent.exists()
    
    def test_write_file_creates_backup_of_existing(self):
        """Test that existing files are backed up before overwriting."""
        test_file = self.test_root / "existing.tsx"
        original_content = "Original content"
        new_content = "New content"
        
        # Create original file
        test_file.write_text(original_content)
        
        # Write new content
        self.writer.write_file(test_file, new_content)
        
        # Check that backup was created
        backup_dir = self.test_root / ".generator_backups"
        assert backup_dir.exists()
        
        backup_files = list(backup_dir.glob("existing.tsx.backup_*"))
        assert len(backup_files) == 1
        
        # Check backup contains original content
        backup_content = backup_files[0].read_text()
        assert original_content == backup_content
    
    def test_warning_header_typescript_format(self):
        """Test that TypeScript files get proper comment format using shared utilities."""
        test_file = self.test_root / "test.tsx"
        content = 'export const TestComponent = () => <div>Hello</div>;'
        
        self.writer.write_file(test_file, content, "TestGenerator", "/test/path")
        
        file_content = test_file.read_text()
        # Shared utility uses /* */ format for TypeScript
        assert file_content.startswith("/*")
        assert "WARNING: GENERATED CODE - DO NOT MODIFY" in file_content
        assert "TestGenerator" in file_content
        assert "/test/path" in file_content
    
    def test_shared_utility_integration(self):
        """Test that shared utilities are properly used."""
        test_file = self.test_root / "test.tsx"
        content = 'export const TestComponent = () => <div>Hello</div>;'
        
        self.writer.write_file(test_file, content, "TestGenerator", "/test/path")
        
        file_content = test_file.read_text()
        # Verify shared utility warning format is used
        assert "WARNING: GENERATED CODE - DO NOT MODIFY" in file_content
        assert content in file_content
    
    def test_validate_file_content_empty(self):
        """Test validation rejects empty content."""
        assert not self.writer._validate_file_content("")
        assert not self.writer._validate_file_content("   ")
        assert not self.writer._validate_file_content(None)
    
    def test_validate_file_content_valid(self):
        """Test validation accepts valid content."""
        assert self.writer._validate_file_content("export const Component = () => <div/>;")
        assert self.writer._validate_file_content("// Comment\nconst x = 1;")
    
    def test_validate_file_content_template_variables(self):
        """Test validation warns about unsubstituted template variables."""
        content = "export const {{COMPONENT_NAME}} = () => <div>{{CONTENT}}</div>;"
        
        # Should return True but print warning
        assert self.writer._validate_file_content(content)
    
    def test_create_directory(self):
        """Test directory creation."""
        new_dir = self.test_root / "new" / "directory"
        
        self.writer.create_directory(new_dir)
        
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_file_exists(self):
        """Test file existence check."""
        existing_file = self.test_root / "existing.txt"
        non_existing = self.test_root / "missing.txt"
        
        existing_file.write_text("content")
        
        assert self.writer.file_exists(existing_file)
        assert not self.writer.file_exists(non_existing)
    
    def test_backup_and_restore(self):
        """Test manual backup and restore functionality."""
        original_file = self.test_root / "original.txt"
        original_content = "Original content"
        
        original_file.write_text(original_content)
        
        # Create backup
        backup_path = self.writer.backup_file(original_file)
        
        assert backup_path is not None
        assert backup_path.exists()
        assert backup_path.read_text() == original_content
        
        # Modify original
        original_file.write_text("Modified content")
        
        # Restore from backup
        success = self.writer.restore_backup(original_file, backup_path)
        
        assert success
        assert original_file.read_text() == original_content
        assert not backup_path.exists()  # Should be moved, not copied
    
    def test_cleanup_backups(self):
        """Test backup cleanup functionality."""
        # Create multiple backup files
        backup_dir = self.test_root / ".generator_backups"
        backup_dir.mkdir()
        self.writer.backup_dir = backup_dir
        
        # Create test backup files with different timestamps
        for i in range(15):
            backup_file = backup_dir / f"test{i}.txt.backup_20240101_10{i:02d}00"
            backup_file.write_text(f"backup {i}")
        
        # Cleanup keeping only 5 most recent
        self.writer.cleanup_backups(max_backups=5)
        
        remaining_backups = list(backup_dir.glob("*.backup_*"))
        assert len(remaining_backups) == 5
        
        # Check that the most recent ones were kept
        backup_names = [f.name for f in remaining_backups]
        assert "test14.txt.backup_20240101_101400" in backup_names
        assert "test0.txt.backup_20240101_100000" not in backup_names
    
    def test_write_file_rollback_on_error(self):
        """Test that backup is restored if write fails."""
        test_file = self.test_root / "test.txt"
        original_content = "Original content"
        
        # Create original file
        test_file.write_text(original_content)
        
        # Mock validation to fail
        original_validate = self.writer._validate_file_content
        self.writer._validate_file_content = lambda x: False
        
        try:
            with pytest.raises(ValueError):
                self.writer.write_file(test_file, "New content")
            
            # File should be restored to original
            assert test_file.read_text() == original_content
        finally:
            # Restore original validation
            self.writer._validate_file_content = original_validate
    
    def test_backup_nonexistent_file(self):
        """Test backing up a file that doesn't exist."""
        non_existent = self.test_root / "missing.txt"
        
        backup_path = self.writer.backup_file(non_existent)
        
        assert backup_path is None
    
    def test_add_import_to_existing_file(self):
        """Test adding import to existing TypeScript file using shared utilities."""
        test_file = self.test_root / "test.tsx"
        initial_content = '''import React from 'react';

export const TestComponent = () => <div>Hello</div>;'''
        
        test_file.write_text(initial_content)
        
        # Add new import
        self.writer.add_import(test_file, './hooks/useTest', 'useTest')
        
        updated_content = test_file.read_text()
        assert 'import { useTest } from \'./hooks/useTest\'' in updated_content
        assert 'import React from \'react\'' in updated_content
        assert 'export const TestComponent' in updated_content
    
    def test_add_import_avoids_duplicates(self):
        """Test that adding duplicate imports doesn't create duplicates."""
        test_file = self.test_root / "test.tsx"
        initial_content = '''import React from 'react';
import { useState } from 'react';

export const TestComponent = () => <div>Hello</div>;'''
        
        test_file.write_text(initial_content)
        
        # Try to add existing import
        self.writer.add_import(test_file, 'react', 'useState')
        
        updated_content = test_file.read_text()
        # Should not duplicate
        assert updated_content.count('useState') == 1
        assert updated_content.count('from \'react\'') == 2  # React and { useState }
    
    def test_add_import_to_nonexistent_file_fails(self):
        """Test that adding import to non-existent file raises error."""
        non_existent = self.test_root / "missing.tsx"
        
        with pytest.raises(FileNotFoundError):
            self.writer.add_import(non_existent, './test', 'TestImport')