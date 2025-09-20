#!/usr/bin/env python3
"""
Test suite for the Parent Generator module.
"""

import unittest
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.parent_generator import ParentPageGenerator
from modules.template_engine import TemplateEngine
from modules.file_writer import FileWriter
from modules.variable_generator import VariableGenerator
from modules.dependency_manager import DependencyManager
from modules.config import PageConfig, ProjectCapabilities, GenerationContext


class TestParentPageGenerator(unittest.TestCase):
    """Test cases for ParentPageGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.templates_dir = self.temp_dir / "templates"
        
        # Create required template directories
        self.templates_dir.mkdir(parents=True)
        (self.templates_dir / "pages").mkdir()
        (self.templates_dir / "hooks").mkdir()
        (self.templates_dir / "actions").mkdir()
        (self.templates_dir / "instructions").mkdir()
        
        # Create minimal templates
        self._create_minimal_templates()
        
        # Initialize components
        self.template_engine = TemplateEngine(self.templates_dir)
        self.file_writer = FileWriter()
        self.variable_generator = VariableGenerator()
        self.dependency_manager = DependencyManager(self.template_engine, self.file_writer)
        
        self.generator = ParentPageGenerator(
            self.template_engine,
            self.file_writer,
            self.variable_generator,
            self.dependency_manager
        )
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def _create_minimal_templates(self):
        """Create minimal template files for testing."""
        # Parent page template
        parent_template = self.templates_dir / "pages" / "parent-page.tsx.template"
        parent_template.write_text("""
import React from 'react';

const {{PAGE_NAME}} = () => {
  return <div>{{BASE_NAME}} Parent Page</div>;
};

export default {{PAGE_NAME}};
""".strip())
        
        # Parent main page template
        main_template = self.templates_dir / "pages" / "parent-main-page.tsx.template"
        main_template.write_text("""
import React from 'react';

const {{BASE_NAME}}MainPage = () => {
  return <div>{{BASE_NAME}} Main</div>;
};

export default {{BASE_NAME}}MainPage;
""".strip())
        
        # Parent hook template
        hook_template = self.templates_dir / "hooks" / "parent-actions-hook.ts.template"
        hook_template.write_text("""
export const use{{BASE_NAME}}Actions = () => {
  const navigate = (path: string) => {
    // Navigation logic
  };
  
  return { navigate };
};
""".strip())
        
        # Parent actions template
        actions_template = self.templates_dir / "actions" / "parent-actions.ts.template"
        actions_template.write_text("""
export const {{PARENT_ID}}Actions = [
  { id: 'main', label: 'Main', icon: 'home' }
];
""".strip())
        
        # Parent instructions template
        instructions_template = self.templates_dir / "instructions" / "parent-instructions.ts.template"
        instructions_template.write_text("""
export const {{PARENT_ID}}Instructions = {
  main: 'Welcome to {{BASE_NAME}}'
};
""".strip())
    
    def test_create_parent_page(self):
        """Test complete parent page creation."""
        config = PageConfig(name="SettingsPage")
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        # Create parent page
        self.generator.create_parent_page(context)
        
        # Validate files were created
        validation = self.generator.validate_parent_creation(context)
        
        self.assertTrue(validation['parent_page'], "Parent page should be created")
        self.assertTrue(validation['parent_main'], "Parent main page should be created")
        self.assertTrue(validation['parent_hook'], "Parent hook should be created")
        self.assertTrue(validation['parent_actions'], "Parent actions should be created")
        self.assertTrue(validation['parent_instructions'], "Parent instructions should be created")
    
    def test_parent_file_contents(self):
        """Test that generated parent files contain expected content."""
        config = PageConfig(name="ProfilePage")
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        # Create parent page
        self.generator.create_parent_page(context)
        
        # Check main parent page content
        parent_file = context.pages_dir / config.parent_id / f"{config.page_name}.tsx"
        self.assertTrue(parent_file.exists())
        
        content = parent_file.read_text()
        self.assertIn('ProfilePage', content)
        self.assertIn('Profile Parent Page', content)
        
        # Check main page content
        main_file = context.pages_dir / config.parent_id / f"{config.base_name.capitalize()}MainPage.tsx"
        self.assertTrue(main_file.exists())
        
        main_content = main_file.read_text()
        self.assertIn('ProfileMainPage', content)
        self.assertIn('Profile Main', main_content)
    
    def test_get_created_files_list(self):
        """Test getting list of files that would be created."""
        config = PageConfig(name="TestPage")
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        created_files = self.generator.get_created_files(context)
        
        # Should return list of 5 files
        self.assertEqual(len(created_files), 5)
        
        # Check that all expected files are in the list
        file_names = [f.name for f in created_files]
        self.assertIn('TestPage.tsx', file_names)
        self.assertIn('TestMainPage.tsx', file_names)
        self.assertIn('useTestActions.ts', file_names)
        self.assertIn('test.ts', file_names)  # actions config
    
    def test_validation_with_missing_files(self):
        """Test validation when some files are missing."""
        config = PageConfig(name="TestPage")
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        # Validate before creating any files
        validation = self.generator.validate_parent_creation(context)
        
        # All should be False since no files exist
        for result in validation.values():
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()