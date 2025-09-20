"""
Tests for the Child Page Generator module.
"""

import pytest
from pathlib import Path
import tempfile
import os
import sys
from unittest.mock import Mock, patch, call

# Add the modules directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from child_generator import ChildPageGenerator
from config import GenerationContext, PageConfig, ProjectCapabilities, WrapperType
from template_engine import TemplateEngine
from file_writer import FileWriter
from variable_generator import VariableGenerator
from wrapper_selector import WrapperSelector


class TestChildPageGenerator:
    """Test cases for ChildPageGenerator class."""
    
    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create basic directory structure
        self.src_dir = self.frontend_root / "src"
        self.pages_dir = self.src_dir / "pages"
        self.components_dir = self.src_dir / "components"
        self.actions_dir = self.src_dir / "constants" / "actions" / "pages"
        self.instructions_dir = self.src_dir / "services" / "instructions" / "pages"
        
        # Mock dependencies
        self.mock_template_engine = Mock(spec=TemplateEngine)
        self.mock_file_writer = Mock(spec=FileWriter)
        self.mock_variable_generator = Mock(spec=VariableGenerator)
        self.mock_wrapper_selector = Mock(spec=WrapperSelector)
        
        self.child_generator = ChildPageGenerator(
            self.mock_template_engine,
            self.mock_file_writer,
            self.mock_variable_generator,
            self.mock_wrapper_selector
        )
        
        # Create test context
        self.config = PageConfig(name="TestChild", parent="TestParent")
        self.capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
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
    
    def test_create_child_page_without_parent_fails(self):
        """Test that creating child page without parent raises error."""
        config_no_parent = PageConfig(name="TestChild")
        context_no_parent = GenerationContext(
            frontend_root=self.frontend_root,
            config=config_no_parent,
            capabilities=self.capabilities,
            variables={}
        )
        
        with pytest.raises(ValueError, match="Child pages must specify a parent"):
            self.child_generator.create_child_page(context_no_parent)
    
    def test_create_child_page_basic_flow(self):
        """Test basic child page creation flow."""
        # Setup mocks
        self.mock_variable_generator.generate_child_variables.return_value = {
            'CHILD_NAME': 'TestChildPage',
            'CHILD_ID': 'testchild'
        }
        
        self.mock_template_engine.get_child_templates.return_value = {
            'child_page': 'pages/child-page.tsx.template',
            'child_actions': 'actions/child-actions.ts.template',
            'child_instructions': 'instructions/child-instructions.ts.template'
        }
        
        self.mock_template_engine.render_template.return_value = "// Template content"
        self.mock_wrapper_selector.select_wrapper_template.return_value = WrapperType.FULL_HOOKS
        self.mock_wrapper_selector.validate_wrapper_selection.return_value = []
        self.mock_wrapper_selector.get_wrapper_description.return_value = "Full hooks wrapper"
        self.mock_variable_generator.generate_wrapper_variables.return_value = {'WRAPPER_VAR': 'value'}
        
        # Execute
        self.child_generator.create_child_page(self.context)
        
        # Verify child variable generation was called
        self.mock_variable_generator.generate_child_variables.assert_called_once_with(self.context)
        
        # Verify template engine was called
        self.mock_template_engine.get_child_templates.assert_called_once_with(self.config)
        
        # Verify directories were created
        expected_dirs = [
            self.pages_dir / "testparent",
            self.components_dir / "testparent",
            self.actions_dir,
            self.instructions_dir
        ]
        
        for expected_dir in expected_dirs:
            self.mock_file_writer.create_directory.assert_any_call(expected_dir)
        
        # Verify wrapper selection was called
        self.mock_wrapper_selector.select_wrapper_template.assert_called_once_with(self.config, self.capabilities)
    
    def test_create_child_page_with_mobile_variant(self):
        """Test child page creation with mobile variant."""
        # Setup mobile config
        mobile_config = PageConfig(name="TestChild", parent="TestParent", mobile=True)
        mobile_context = GenerationContext(
            frontend_root=self.frontend_root,
            config=mobile_config,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Setup mocks
        self.mock_variable_generator.generate_child_variables.return_value = {
            'CHILD_NAME': 'TestChildPage',
            'CHILD_ID': 'testchild'
        }
        
        self.mock_template_engine.get_child_templates.return_value = {
            'child_page': 'pages/child-page.tsx.template',
            'mobile_child_page': 'pages/mobile-child-page.tsx.template',
            'child_actions': 'actions/child-actions.ts.template',
            'child_instructions': 'instructions/child-instructions.ts.template'
        }
        
        self.mock_template_engine.render_template.return_value = "// Template content"
        self.mock_wrapper_selector.select_wrapper_template.return_value = WrapperType.FULL_HOOKS
        self.mock_wrapper_selector.validate_wrapper_selection.return_value = []
        self.mock_wrapper_selector.get_wrapper_description.return_value = "Full hooks wrapper"
        self.mock_variable_generator.generate_wrapper_variables.return_value = {'WRAPPER_VAR': 'value'}
        
        # Execute
        self.child_generator.create_child_page(mobile_context)
        
        # Verify mobile template was rendered
        self.mock_template_engine.render_template.assert_any_call(
            'pages/mobile-child-page.tsx.template', 
            {'CHILD_NAME': 'TestChildPage', 'CHILD_ID': 'testchild'}
        )
        
        # Verify mobile file was written
        expected_mobile_path = self.pages_dir / "testparent" / "MobileTestChildPage.tsx"
        self.mock_file_writer.write_file.assert_any_call(
            expected_mobile_path,
            "// Template content",
            "ChildPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
        )
    
    def test_create_child_files_creates_all_components(self):
        """Test that all child files are created correctly."""
        variables = {
            'CHILD_NAME': 'TestChildPage',
            'CHILD_ID': 'testchild'
        }
        
        self.context.variables = variables
        
        # Setup mocks
        self.mock_template_engine.get_child_templates.return_value = {
            'child_page': 'pages/child-page.tsx.template',
            'child_actions': 'actions/child-actions.ts.template',
            'child_instructions': 'instructions/child-instructions.ts.template'
        }
        
        self.mock_template_engine.render_template.return_value = "// Template content"
        
        # Execute private method
        self.child_generator._generate_child_files(self.context)
        
        # Verify all templates were rendered
        expected_calls = [
            call('pages/child-page.tsx.template', variables),
            call('actions/child-actions.ts.template', variables),
            call('instructions/child-instructions.ts.template', variables)
        ]
        self.mock_template_engine.render_template.assert_has_calls(expected_calls, any_order=True)
        
        # Verify all files were written
        expected_files = [
            (self.pages_dir / "testparent" / "TestChildPage.tsx", "ChildPageGenerator"),
            (self.actions_dir / "testchild.ts", "ChildPageGenerator"),
            (self.instructions_dir / "testchild.ts", "ChildPageGenerator")
        ]
        
        for file_path, generator_name in expected_files:
            self.mock_file_writer.write_file.assert_any_call(
                file_path,
                "// Template content",
                generator_name,
                "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
            )
    
    def test_create_adaptive_wrapper_with_validation_warnings(self):
        """Test adaptive wrapper creation with validation warnings."""
        # Setup mocks with validation issues
        self.mock_wrapper_selector.select_wrapper_template.return_value = WrapperType.FULL_HOOKS
        self.mock_wrapper_selector.validate_wrapper_selection.return_value = [
            "Missing mobile hook",
            "Page hooks not configured properly"
        ]
        self.mock_wrapper_selector.get_wrapper_description.return_value = "Full hooks wrapper"
        self.mock_variable_generator.generate_wrapper_variables.return_value = {
            'WRAPPER_VAR': 'value'
        }
        self.mock_template_engine.render_template.return_value = "// Wrapper content"
        
        # Execute
        self.child_generator._create_adaptive_wrapper(self.context)
        
        # Verify validation was performed
        self.mock_wrapper_selector.validate_wrapper_selection.assert_called_once_with(
            WrapperType.FULL_HOOKS, self.config, self.capabilities
        )
        
        # Verify wrapper variables were generated
        self.mock_variable_generator.generate_wrapper_variables.assert_called_once_with(
            self.context, WrapperType.FULL_HOOKS
        )
        
        # Verify wrapper template was rendered with components/ prefix
        self.mock_template_engine.render_template.assert_called_with(
            f"components/{WrapperType.FULL_HOOKS}",
            {'WRAPPER_VAR': 'value'}
        )
        
        # Verify wrapper file was written
        expected_wrapper_path = self.components_dir / "testparent" / "TestChildPageWrapper.tsx"
        self.mock_file_writer.write_file.assert_called_with(
            expected_wrapper_path,
            "// Wrapper content",
            "ChildPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
        )
    
    def test_validate_child_creation_all_files_exist(self):
        """Test validation when all child files exist."""
        # Create mock files
        files_to_create = [
            self.pages_dir / "testparent" / "TestChildPage.tsx",
            self.components_dir / "testparent" / "TestChildPageWrapper.tsx",
            self.actions_dir / "testchild.ts",
            self.instructions_dir / "testchild.ts"
        ]
        
        for file_path in files_to_create:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("// Content")
        
        # Execute validation
        results = self.child_generator.validate_child_creation(self.context)
        
        # Verify all files are reported as existing
        expected_results = {
            'child_page': True,
            'child_wrapper': True,
            'child_actions': True,
            'child_instructions': True
        }
        assert results == expected_results
    
    def test_validate_child_creation_with_mobile_variant(self):
        """Test validation when mobile variant is requested."""
        # Setup mobile config
        mobile_config = PageConfig(name="TestChild", parent="TestParent", mobile=True)
        mobile_context = GenerationContext(
            frontend_root=self.frontend_root,
            config=mobile_config,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Create mock files including mobile variant
        files_to_create = [
            self.pages_dir / "testparent" / "TestChildPage.tsx",
            self.pages_dir / "testparent" / "MobileTestChildPage.tsx",  # Mobile variant
            self.components_dir / "testparent" / "TestChildPageWrapper.tsx",
            self.actions_dir / "testchild.ts",
            self.instructions_dir / "testchild.ts"
        ]
        
        for file_path in files_to_create:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("// Content")
        
        # Execute validation
        results = self.child_generator.validate_child_creation(mobile_context)
        
        # Verify all files including mobile are reported as existing
        expected_results = {
            'child_page': True,
            'mobile_child_page': True,  # Should include mobile variant
            'child_wrapper': True,
            'child_actions': True,
            'child_instructions': True
        }
        assert results == expected_results
    
    def test_validate_child_creation_missing_files(self):
        """Test validation when some files are missing."""
        # Only create some files
        files_to_create = [
            self.pages_dir / "testparent" / "TestChildPage.tsx",
            # Missing wrapper, actions, and instructions
        ]
        
        for file_path in files_to_create:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("// Content")
        
        # Execute validation
        results = self.child_generator.validate_child_creation(self.context)
        
        # Verify missing files are reported as False
        expected_results = {
            'child_page': True,      # Exists
            'child_wrapper': False,  # Missing
            'child_actions': False,  # Missing
            'child_instructions': False  # Missing
        }
        assert results == expected_results
    
    def test_get_created_files_without_mobile(self):
        """Test getting list of files to be created without mobile variant."""
        files = self.child_generator.get_created_files(self.context)
        
        expected_files = [
            self.pages_dir / "testparent" / "TestChildPage.tsx",
            self.components_dir / "testparent" / "TestChildPageWrapper.tsx",
            self.actions_dir / "testchild.ts",
            self.instructions_dir / "testchild.ts"
        ]
        
        assert files == expected_files
    
    def test_get_created_files_with_mobile(self):
        """Test getting list of files to be created with mobile variant."""
        # Setup mobile config
        mobile_config = PageConfig(name="TestChild", parent="TestParent", mobile=True)
        mobile_context = GenerationContext(
            frontend_root=self.frontend_root,
            config=mobile_config,
            capabilities=self.capabilities,
            variables={}
        )
        
        files = self.child_generator.get_created_files(mobile_context)
        
        expected_files = [
            self.pages_dir / "testparent" / "TestChildPage.tsx",
            self.components_dir / "testparent" / "TestChildPageWrapper.tsx",
            self.actions_dir / "testchild.ts",
            self.instructions_dir / "testchild.ts",
            self.pages_dir / "testparent" / "MobileTestChildPage.tsx"  # Mobile variant added
        ]
        
        assert files == expected_files
    
    def test_get_wrapper_description(self):
        """Test getting wrapper description."""
        self.mock_wrapper_selector.select_wrapper_template.return_value = WrapperType.FULL_HOOKS
        self.mock_wrapper_selector.get_wrapper_description.return_value = "Full hooks wrapper"
        
        description = self.child_generator._get_wrapper_description(self.context)
        
        assert description == "Full hooks wrapper"
        self.mock_wrapper_selector.select_wrapper_template.assert_called_once_with(
            self.context.config, self.context.capabilities
        )
        self.mock_wrapper_selector.get_wrapper_description.assert_called_once_with(
            WrapperType.FULL_HOOKS
        )