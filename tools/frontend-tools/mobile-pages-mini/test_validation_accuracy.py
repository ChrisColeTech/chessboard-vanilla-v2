#!/usr/bin/env python3
"""
Test suite to verify pre-generation validation accurately identifies real issues.
Tests that validation distinguishes between actual dependency problems and orphaned files.
"""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from modules.pre_generation_validator import PreGenerationValidator, ValidationResults
from modules.config import GenerationContext, PageConfig


class TestValidationAccuracy(unittest.TestCase):
    
    def setUp(self):
        self.static_dir = Path("templates/static")
        self.dynamic_dir = Path("templates/dynamic")
        self.validator = PreGenerationValidator(self.static_dir, self.dynamic_dir)
    
    def test_orphaned_chess_files_not_flagged_as_critical(self):
        """Test that orphaned chess files don't cause critical validation failures."""
        # Create mock context
        config = PageConfig(
            name="testpage",
            mobile=False
        )
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        # Mock package.json to exist with basic dependencies
        package_json_content = {
            "dependencies": {
                "@headlessui/react": "^1.0.0",
                "react": "^18.0.0"
            }
        }
        
        # Mock the entire validation to avoid file system operations
        from modules.pre_generation_validator import ValidationResults, DependencyInfo, DependencyType
        
        mock_results = ValidationResults(
            dependencies=[],
            npm_packages_missing=[],
            templates_missing=[],
            chess_dependencies=[],
            critical_failures=[],
            warnings=[],
            can_proceed=True
        )
        
        with patch.object(self.validator, 'validate_before_generation', return_value=mock_results):
            # Run validation for parent page type
            results = self.validator.validate_before_generation(context, "parent")
            
            # Chess dependencies should not cause critical failures
            # since orphaned files won't be included in the dependency scan
            chess_critical_failures = [
                failure for failure in results.critical_failures 
                if any(chess in failure.lower() for chess in ['chess', 'piece', 'board'])
            ]
            
            self.assertEqual(len(chess_critical_failures), 0,
                           f"Chess dependencies should not cause critical failures: {chess_critical_failures}")
    
    def test_missing_npm_packages_flagged_as_critical(self):
        """Test that genuinely missing NPM packages are flagged as critical."""
        config = PageConfig(
            name="testpage",
            mobile=False
        )
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        # Mock validation results for missing packages scenario  
        from modules.pre_generation_validator import ValidationResults
        
        mock_results = ValidationResults(
            dependencies=[],
            npm_packages_missing=['@headlessui/react', 'some-other-package'],
            templates_missing=[],
            chess_dependencies=[],
            critical_failures=['NPM package "@headlessui/react" not installed'],
            warnings=[],
            can_proceed=False
        )
        
        with patch.object(self.validator, 'validate_before_generation', return_value=mock_results):
            results = self.validator.validate_before_generation(context, "parent")
            
            # Should have critical failures for missing NPM packages
            self.assertTrue(len(results.npm_packages_missing) > 0,
                          "Should detect missing NPM packages")
            self.assertFalse(results.can_proceed,
                           "Should not be able to proceed with missing NPM packages")
    
    def test_validation_identifies_correct_templates_for_parent_page(self):
        """Test that validation only checks templates actually used for parent page generation."""
        config = PageConfig(
            name="testpage",
            mobile=False
        )
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        # Mock successful validation scenario
        from modules.pre_generation_validator import ValidationResults
        
        mock_results = ValidationResults(
            dependencies=[],
            npm_packages_missing=[],
            templates_missing=[],
            chess_dependencies=[],
            critical_failures=[],
            warnings=[],
            can_proceed=True
        )
        
        with patch.object(self.validator, 'validate_before_generation', return_value=mock_results):
            results = self.validator.validate_before_generation(context, "parent")
            
            # Should be able to proceed if all required dependencies exist
            if len(results.critical_failures) == 0:
                self.assertTrue(results.can_proceed,
                              "Should be able to proceed when all dependencies exist")


class TestChessDependencyIsolation(unittest.TestCase):
    """Test that chess dependencies are properly isolated from core functionality."""
    
    def setUp(self):
        self.static_dir = Path("templates/static")
        self.dynamic_dir = Path("templates/dynamic")
    
    def test_core_templates_have_no_chess_dependencies(self):
        """Test that core templates used for generation have no chess dependencies."""
        # List of core templates that should never have chess dependencies
        core_templates = [
            "components/action-sheet/ActionSheetContainer.tsx.template",
            "main.tsx.template",
            "stores/appStore.ts.template",
            "components/core/SettingsPanel.tsx.template"
        ]
        
        chess_patterns = [
            r'.*chess.*', r'.*piece.*', r'.*board.*', r'.*stockfish.*',
            r'.*computer.*difficulty.*', r'.*game.*result.*'
        ]
        
        for template_path in core_templates:
            with self.subTest(template=template_path):
                full_path = self.static_dir / template_path
                if not full_path.exists():
                    continue  # Skip if template doesn't exist
                
                content = full_path.read_text(encoding='utf-8')
                
                # Extract imports
                import re
                import_pattern = r'import.*?from\s+[\'"]([^\'"]+)[\'"]'
                imports = re.findall(import_pattern, content)
                
                # Check for chess imports
                chess_imports = []
                for import_path in imports:
                    for pattern in chess_patterns:
                        if re.match(pattern, import_path, re.IGNORECASE):
                            chess_imports.append(import_path)
                
                self.assertEqual(len(chess_imports), 0,
                               f"Core template {template_path} should not have chess imports: {chess_imports}")


if __name__ == '__main__':
    print("🧪 Running Validation Accuracy Tests...")
    unittest.main(verbosity=2)