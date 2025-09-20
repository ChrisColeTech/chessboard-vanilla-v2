"""
Tests for the Dependency Manager module.
"""

import pytest
from pathlib import Path
import tempfile
import os
import sys
from unittest.mock import Mock, patch

# Add the modules directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from dependency_manager import DependencyManager
from config import GenerationContext, PageConfig, ProjectCapabilities
from template_engine import TemplateEngine
from file_writer import FileWriter


class TestDependencyManager:
    """Test cases for DependencyManager class."""
    
    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create basic directory structure
        self.src_dir = self.frontend_root / "src"
        self.hooks_dir = self.src_dir / "hooks" / "core"
        self.components_ui_dir = self.src_dir / "components" / "ui"
        
        self.hooks_dir.mkdir(parents=True)
        self.components_ui_dir.mkdir(parents=True)
        
        # Mock dependencies
        self.mock_template_engine = Mock(spec=TemplateEngine)
        self.mock_file_writer = Mock(spec=FileWriter)
        
        self.dependency_manager = DependencyManager(
            self.mock_template_engine,
            self.mock_file_writer
        )
        
        # Create test context
        self.config = PageConfig(name="TestPage")
        self.capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        self.context = GenerationContext(
            frontend_root=self.frontend_root,
            config=self.config,
            capabilities=self.capabilities,
            variables={}
        )
    
    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_ensure_use_page_data_hook_creates_when_missing(self):
        """Test creating usePageData hook when it doesn't exist."""
        self.mock_template_engine.render_template.return_value = "// Hook content"
        
        self.dependency_manager.ensure_use_page_data_hook(self.context)
        
        # Verify template was rendered
        self.mock_template_engine.render_template.assert_called_once_with(
            'dependencies/use-page-data-hook.ts.template',
            {
                'GENERATOR_NAME': 'DependencyManager',
                'SOURCE_FILE': '/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py'
            }
        )
        
        # Verify file was written
        expected_path = self.hooks_dir / "usePageData.ts"
        self.mock_file_writer.write_file.assert_called_once_with(
            expected_path,
            "// Hook content",
            "DependencyManager",
            "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
        )
    
    def test_ensure_use_page_data_hook_skips_when_exists(self):
        """Test skipping usePageData hook creation when it exists."""
        # Create existing hook file
        hook_path = self.hooks_dir / "usePageData.ts"
        hook_path.write_text("// Existing hook")
        
        self.dependency_manager.ensure_use_page_data_hook(self.context)
        
        # Should not call template engine or file writer
        self.mock_template_engine.render_template.assert_not_called()
        self.mock_file_writer.write_file.assert_not_called()
    
    def test_ensure_data_table_component_creates_when_missing(self):
        """Test creating DataTable component when it doesn't exist."""
        self.mock_template_engine.render_template.return_value = "// Component content"
        
        self.dependency_manager.ensure_data_table_component(self.context)
        
        # Verify template was rendered
        self.mock_template_engine.render_template.assert_called_once_with(
            'dependencies/data-table-component.tsx.template',
            {
                'GENERATOR_NAME': 'DependencyManager',
                'SOURCE_FILE': '/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py'
            }
        )
        
        # Verify file was written
        expected_path = self.components_ui_dir / "DataTable.tsx"
        self.mock_file_writer.write_file.assert_called_once_with(
            expected_path,
            "// Component content",
            "DependencyManager",
            "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
        )
    
    def test_ensure_data_table_component_skips_when_exists(self):
        """Test skipping DataTable component creation when it exists."""
        # Create existing component file
        component_path = self.components_ui_dir / "DataTable.tsx"
        component_path.write_text("// Existing component")
        
        self.dependency_manager.ensure_data_table_component(self.context)
        
        # Should not call template engine or file writer
        self.mock_template_engine.render_template.assert_not_called()
        self.mock_file_writer.write_file.assert_not_called()
    
    def test_ensure_all_dependencies_creates_missing(self):
        """Test that ensure_all_dependencies creates missing dependencies."""
        self.mock_template_engine.render_template.return_value = "// Content"
        
        # Context has no data table capability
        assert not self.context.capabilities.has_data_table
        
        self.dependency_manager.ensure_all_dependencies(self.context)
        
        # Should call both dependency creation methods
        assert self.mock_template_engine.render_template.call_count == 2
        assert self.mock_file_writer.write_file.call_count == 2
    
    def test_ensure_all_dependencies_skips_existing_data_table(self):
        """Test that ensure_all_dependencies skips existing DataTable."""
        # Set capability to have data table
        self.context.capabilities.has_data_table = True
        
        # Create existing usePageData hook so it's skipped
        hook_path = self.hooks_dir / "usePageData.ts"
        hook_path.write_text("// Existing hook")
        
        self.dependency_manager.ensure_all_dependencies(self.context)
        
        # Should not create any dependencies
        self.mock_template_engine.render_template.assert_not_called()
        self.mock_file_writer.write_file.assert_not_called()
    
    @patch('subprocess.run')
    def test_regenerate_index_files_success(self, mock_run):
        """Test successful index file regeneration."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stderr = ""
        
        self.dependency_manager.regenerate_index_files(self.frontend_root)
        
        # Should call subprocess with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        
        assert sys.executable in call_args[0][0]
        assert str(self.frontend_root / "src") in call_args[0][0]
        assert call_args[1]['capture_output'] is True
        assert call_args[1]['text'] is True
    
    @patch('subprocess.run')
    def test_regenerate_index_files_failure(self, mock_run):
        """Test index file regeneration with errors."""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Error message"
        
        # Should not raise exception, just print warning
        self.dependency_manager.regenerate_index_files(self.frontend_root)
        
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_regenerate_index_files_missing_generator(self, mock_run):
        """Test behavior when index generator is missing."""
        # Mock will not be called because file doesn't exist
        self.dependency_manager.regenerate_index_files(self.frontend_root)
        
        # Should not call subprocess if generator doesn't exist
        mock_run.assert_not_called()
    
    def test_validate_dependencies_all_missing(self):
        """Test validation when all dependencies are missing."""
        results = self.dependency_manager.validate_dependencies(self.context)
        
        expected = {
            'usePageData': False,
            'DataTable': False
        }
        assert results == expected
    
    def test_validate_dependencies_all_present(self):
        """Test validation when all dependencies exist."""
        # Create dependency files
        (self.hooks_dir / "usePageData.ts").write_text("// Hook")
        (self.components_ui_dir / "DataTable.tsx").write_text("// Component")
        
        results = self.dependency_manager.validate_dependencies(self.context)
        
        expected = {
            'usePageData': True,
            'DataTable': True
        }
        assert results == expected
    
    def test_validate_dependencies_with_page_hooks(self):
        """Test validation includes page hooks when capability is set."""
        # Set page hooks capability
        self.context.capabilities.has_page_hooks = True
        
        # Create some files
        (self.hooks_dir / "usePageInstructions.ts").write_text("// Hook")
        (self.hooks_dir / "usePageData.ts").write_text("// Hook")
        
        results = self.dependency_manager.validate_dependencies(self.context)
        
        assert 'usePageInstructions' in results
        assert 'usePageActions' in results
        assert results['usePageInstructions'] is True
        assert results['usePageActions'] is False  # Missing
    
    def test_validate_dependencies_with_mobile_hook(self):
        """Test validation includes mobile hook when capability is set."""
        # Set mobile hook capability
        self.context.capabilities.has_mobile_hook = True
        
        # Create mobile hook
        (self.hooks_dir / "useIsMobile.ts").write_text("// Mobile hook")
        
        results = self.dependency_manager.validate_dependencies(self.context)
        
        assert 'useIsMobile' in results
        assert results['useIsMobile'] is True
    
    def test_get_missing_dependencies(self):
        """Test getting list of missing dependencies."""
        # Create only one dependency
        (self.hooks_dir / "usePageData.ts").write_text("// Hook")
        
        missing = self.dependency_manager.get_missing_dependencies(self.context)
        
        assert 'DataTable' in missing
        assert 'usePageData' not in missing
    
    def test_create_missing_directories(self):
        """Test creation of missing project directories."""
        # Remove some directories
        import shutil
        shutil.rmtree(self.hooks_dir)
        
        self.dependency_manager.create_missing_directories(self.context)
        
        # Should call file writer to create directories
        expected_dirs = [
            self.context.pages_dir,
            self.context.components_dir,
            self.context.hooks_dir,
            self.context.actions_dir,
            self.context.instructions_dir,
            self.frontend_root / "src" / "hooks" / "core",
            self.frontend_root / "src" / "components" / "ui"
        ]
        
        # Verify create_directory was called for each directory
        assert self.mock_file_writer.create_directory.call_count == len(expected_dirs)
        
        # Check that the calls included our expected directories
        called_paths = [call[0][0] for call in self.mock_file_writer.create_directory.call_args_list]
        for expected_dir in expected_dirs:
            assert expected_dir in called_paths