"""
Tests for the Template Engine module.
"""

import pytest
from pathlib import Path
import tempfile
import os
import sys

# Add the modules directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from template_engine import TemplateEngine
from config import PageConfig, ProjectCapabilities, WrapperType


class TestTemplateEngine:
    """Test cases for TemplateEngine class."""
    
    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.templates_root = Path(self.temp_dir) / "templates"
        self.templates_root.mkdir(parents=True)
        
        # Create a test template
        self.test_template_path = self.templates_root / "test.template"
        self.test_template_path.write_text("Hello {{NAME}}! Welcome to {{PROJECT}}.")
        
        self.engine = TemplateEngine(self.templates_root)
    
    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_template_success(self):
        """Test successful template loading."""
        content = self.engine.load_template("test.template")
        assert content == "Hello {{NAME}}! Welcome to {{PROJECT}}."
    
    def test_load_template_not_found(self):
        """Test template loading when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            self.engine.load_template("nonexistent.template")
    
    def test_render_template(self):
        """Test template rendering with variable substitution."""
        variables = {
            'NAME': 'John',
            'PROJECT': 'TestProject'
        }
        
        result = self.engine.render_template("test.template", variables)
        assert result == "Hello John! Welcome to TestProject."
    
    def test_render_template_partial_substitution(self):
        """Test template rendering with partial variable substitution."""
        variables = {'NAME': 'Alice'}
        
        result = self.engine.render_template("test.template", variables)
        assert result == "Hello Alice! Welcome to {{PROJECT}}."
    
    def test_select_child_wrapper_template_full_hooks(self):
        """Test wrapper template selection with full hooks and mobile."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=True)
        
        result = self.engine.select_child_wrapper_template(config, capabilities)
        assert result == WrapperType.FULL_HOOKS
    
    def test_select_child_wrapper_template_basic_hooks(self):
        """Test wrapper template selection with page hooks only."""
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=False)
        
        result = self.engine.select_child_wrapper_template(config, capabilities)
        assert result == WrapperType.BASIC_HOOKS
    
    def test_select_child_wrapper_template_no_hooks(self):
        """Test wrapper template selection with no hooks."""
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(has_page_hooks=False, has_mobile_hook=False)
        
        result = self.engine.select_child_wrapper_template(config, capabilities)
        assert result == WrapperType.NO_HOOKS
    
    def test_get_parent_templates(self):
        """Test getting parent template names."""
        templates = self.engine.get_parent_templates()
        
        expected_keys = {'parent_page', 'parent_main', 'parent_actions', 'parent_instructions', 'parent_hook'}
        assert set(templates.keys()) == expected_keys
        assert all(template.endswith('.template') for template in templates.values())
    
    def test_get_child_templates_without_mobile(self):
        """Test getting child template names without mobile variant."""
        config = PageConfig(name="TestPage", mobile=False)
        templates = self.engine.get_child_templates(config)
        
        expected_keys = {'child_page', 'child_actions', 'child_instructions'}
        assert set(templates.keys()) == expected_keys
        assert 'mobile_child_page' not in templates
    
    def test_get_child_templates_with_mobile(self):
        """Test getting child template names with mobile variant."""
        config = PageConfig(name="TestPage", mobile=True)
        templates = self.engine.get_child_templates(config)
        
        expected_keys = {'child_page', 'child_actions', 'child_instructions', 'mobile_child_page'}
        assert set(templates.keys()) == expected_keys
    
    def test_validate_template_exists(self):
        """Test template existence validation."""
        assert self.engine.validate_template_exists("test.template") is True
        assert self.engine.validate_template_exists("nonexistent.template") is False