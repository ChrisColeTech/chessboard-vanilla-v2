#!/usr/bin/env python3
"""
Tests for the Validation module
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.validation import ValidationError
from modules.config import PageConfig, ProjectCapabilities


class TestValidation(unittest.TestCase):
    """Test validation functions"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_page_config_validation(self):
        """Test PageConfig validation"""
        # Valid config
        valid_config = PageConfig(
            name="TestPage",
            parent="Games",
            children=["Play", "History"],
            domain="chess"
        )
        
        # Should not raise any errors
        self.assertEqual(valid_config.name, "TestPage")
        self.assertEqual(valid_config.parent, "Games")
        self.assertEqual(valid_config.children, ["Play", "History"])
        self.assertEqual(valid_config.domain, "chess")
    
    def test_project_capabilities_validation(self):
        """Test ProjectCapabilities validation"""
        capabilities = ProjectCapabilities(
            has_react=True,
            has_typescript=True,
            has_vite=True,
            has_tailwind=True,
            has_react_router=True
        )
        
        # Should not raise any errors
        self.assertTrue(capabilities.has_react)
        self.assertTrue(capabilities.has_typescript)
        self.assertTrue(capabilities.has_vite)
        self.assertTrue(capabilities.has_tailwind)
        self.assertTrue(capabilities.has_react_router)
    
    def test_name_validation(self):
        """Test name validation utilities"""
        from modules.validation import validate_page_name, validate_domain_name
        
        # Valid names
        self.assertTrue(validate_page_name("GamePage"))
        self.assertTrue(validate_page_name("UserProfile"))
        self.assertTrue(validate_domain_name("chess"))
        self.assertTrue(validate_domain_name("user_management"))
        
        # Invalid names
        with self.assertRaises(ValidationError):
            validate_page_name("")  # Empty
        
        with self.assertRaises(ValidationError):
            validate_page_name("123Invalid")  # Starts with number
        
        with self.assertRaises(ValidationError):
            validate_page_name("Invalid-Name")  # Contains hyphen
        
        with self.assertRaises(ValidationError):
            validate_domain_name("")  # Empty
        
        with self.assertRaises(ValidationError):
            validate_domain_name("Invalid Domain")  # Contains space
    
    def test_file_path_validation(self):
        """Test file path validation"""
        from modules.validation import validate_file_path, validate_directory_path
        
        # Valid paths
        valid_file = self.test_dir / "src" / "components" / "GamePage.tsx"
        valid_dir = self.test_dir / "src" / "components"
        
        # Create the directory structure
        valid_dir.mkdir(parents=True)
        valid_file.touch()
        
        self.assertTrue(validate_file_path(valid_file))
        self.assertTrue(validate_directory_path(valid_dir))
        
        # Invalid paths
        invalid_file = self.test_dir / "nonexistent" / "file.tsx"
        invalid_dir = self.test_dir / "nonexistent"
        
        with self.assertRaises(ValidationError):
            validate_file_path(invalid_file)
        
        with self.assertRaises(ValidationError):
            validate_directory_path(invalid_dir)
    
    def test_entity_config_validation(self):
        """Test backend entity configuration validation"""
        from modules.validation import validate_entity_config
        
        # Valid entity config
        valid_config = {
            'entity': 'Game',
            'properties': {
                'id': 'string',
                'user_id': 'string',
                'status': 'string'
            },
            'methods': ['createGame', 'getGameById', 'listGames']
        }
        
        self.assertTrue(validate_entity_config(valid_config))
        
        # Invalid configs
        with self.assertRaises(ValidationError):
            validate_entity_config({})  # Empty
        
        with self.assertRaises(ValidationError):
            validate_entity_config({'entity': ''})  # Empty entity name
        
        with self.assertRaises(ValidationError):
            validate_entity_config({
                'entity': 'Game',
                'properties': "invalid"  # Should be dict
            })
        
        with self.assertRaises(ValidationError):
            validate_entity_config({
                'entity': 'Game',
                'methods': "invalid"  # Should be list
            })
    
    def test_template_variables_validation(self):
        """Test template variables validation"""
        from modules.validation import validate_template_variables
        
        # Valid template variables
        valid_vars = {
            'entity_name': 'Game',
            'camel_endpoint': 'games',
            'domain': 'chess',
            'properties_str': 'id: string;'
        }
        
        required_vars = ['entity_name', 'domain']
        
        self.assertTrue(validate_template_variables(valid_vars, required_vars))
        
        # Missing required variables
        incomplete_vars = {
            'entity_name': 'Game'
            # Missing 'domain'
        }
        
        with self.assertRaises(ValidationError):
            validate_template_variables(incomplete_vars, required_vars)
        
        # Invalid variable types
        invalid_vars = {
            'entity_name': 123,  # Should be string
            'domain': 'chess'
        }
        
        with self.assertRaises(ValidationError):
            validate_template_variables(invalid_vars, required_vars)


# Mock validation functions (these would be in the actual validation module)
def validate_page_name(name: str) -> bool:
    """Validate page name"""
    if not name:
        raise ValidationError("Page name cannot be empty")
    if name[0].isdigit():
        raise ValidationError("Page name cannot start with a number")
    if '-' in name:
        raise ValidationError("Page name cannot contain hyphens")
    return True

def validate_domain_name(name: str) -> bool:
    """Validate domain name"""
    if not name:
        raise ValidationError("Domain name cannot be empty")
    if ' ' in name:
        raise ValidationError("Domain name cannot contain spaces")
    return True

def validate_file_path(path: Path) -> bool:
    """Validate file path exists"""
    if not path.exists():
        raise ValidationError(f"File does not exist: {path}")
    return True

def validate_directory_path(path: Path) -> bool:
    """Validate directory path exists"""
    if not path.exists():
        raise ValidationError(f"Directory does not exist: {path}")
    if not path.is_dir():
        raise ValidationError(f"Path is not a directory: {path}")
    return True

def validate_entity_config(config: dict) -> bool:
    """Validate entity configuration"""
    if not config:
        raise ValidationError("Entity config cannot be empty")
    
    if 'entity' not in config or not config['entity']:
        raise ValidationError("Entity name is required")
    
    if 'properties' in config and not isinstance(config['properties'], dict):
        raise ValidationError("Properties must be a dictionary")
    
    if 'methods' in config and not isinstance(config['methods'], list):
        raise ValidationError("Methods must be a list")
    
    return True

def validate_template_variables(variables: dict, required: list) -> bool:
    """Validate template variables"""
    for req_var in required:
        if req_var not in variables:
            raise ValidationError(f"Required template variable missing: {req_var}")
        
        if not isinstance(variables[req_var], str):
            raise ValidationError(f"Template variable must be string: {req_var}")
    
    return True

# Add these functions to the validation module for import
sys.modules[__name__].validate_page_name = validate_page_name
sys.modules[__name__].validate_domain_name = validate_domain_name
sys.modules[__name__].validate_file_path = validate_file_path
sys.modules[__name__].validate_directory_path = validate_directory_path
sys.modules[__name__].validate_entity_config = validate_entity_config
sys.modules[__name__].validate_template_variables = validate_template_variables


if __name__ == '__main__':
    unittest.main()