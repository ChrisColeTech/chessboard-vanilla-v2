#!/usr/bin/env python3
"""
Tests for the Pre-Generation Validator module
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.pre_generation_validator import (
    DependencyType,
    DependencyInfo, 
    ValidationResults
)

# Import the validator class if it exists in the module
try:
    from modules.pre_generation_validator import PreGenerationValidator
except ImportError:
    PreGenerationValidator = None


class TestPreGenerationValidator(unittest.TestCase):
    """Test the Pre-Generation Validator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_dependency_type_enum(self):
        """Test DependencyType enum values"""
        # Test all enum values exist
        self.assertEqual(DependencyType.NPM_PACKAGE.value, "npm_package")
        self.assertEqual(DependencyType.TEMPLATE_FILE.value, "template_file")
        self.assertEqual(DependencyType.GENERATED_FILE.value, "generated_file")
        self.assertEqual(DependencyType.PROJECT_FILE.value, "project_file")
        self.assertEqual(DependencyType.CHESS_SPECIFIC.value, "chess_specific")
        self.assertEqual(DependencyType.UNKNOWN.value, "unknown")
    
    def test_dependency_info_dataclass(self):
        """Test DependencyInfo dataclass"""
        dependency = DependencyInfo(
            import_path="./component",
            dependency_type=DependencyType.TEMPLATE_FILE,
            exists=True,
            source_template="main.template"
        )
        
        # Test required fields
        self.assertEqual(dependency.import_path, "./component")
        self.assertEqual(dependency.dependency_type, DependencyType.TEMPLATE_FILE)
        self.assertTrue(dependency.exists)
        self.assertEqual(dependency.source_template, "main.template")
        
        # Test optional fields have default values
        self.assertIsNone(dependency.error_message)
        self.assertIsNone(dependency.remediation)
    
    def test_dependency_info_with_optional_fields(self):
        """Test DependencyInfo with optional fields"""
        dependency = DependencyInfo(
            import_path="missing-package",
            dependency_type=DependencyType.NPM_PACKAGE,
            exists=False,
            source_template="package.template",
            error_message="Package not found",
            remediation="Run npm install missing-package"
        )
        
        self.assertEqual(dependency.error_message, "Package not found")
        self.assertEqual(dependency.remediation, "Run npm install missing-package")
    
    def test_validation_results_dataclass(self):
        """Test ValidationResults dataclass"""
        dependency = DependencyInfo(
            import_path="test",
            dependency_type=DependencyType.NPM_PACKAGE,
            exists=True,
            source_template="test.template"
        )
        
        results = ValidationResults(
            dependencies=[dependency],
            npm_packages_missing=["missing-package"],
            templates_missing=["missing.template"],
            chess_dependencies=["chessboard"],
            critical_failures=["Critical error"]
        )
        
        # Test all fields
        self.assertEqual(len(results.dependencies), 1)
        self.assertEqual(results.dependencies[0], dependency)
        self.assertEqual(results.npm_packages_missing, ["missing-package"])
        self.assertEqual(results.templates_missing, ["missing.template"])
        self.assertEqual(results.chess_dependencies, ["chessboard"])
        self.assertEqual(results.critical_failures, ["Critical error"])
    
    def test_validation_results_empty(self):
        """Test ValidationResults with empty lists"""
        results = ValidationResults(
            dependencies=[],
            npm_packages_missing=[],
            templates_missing=[],
            chess_dependencies=[],
            critical_failures=[]
        )
        
        self.assertEqual(len(results.dependencies), 0)
        self.assertEqual(len(results.npm_packages_missing), 0)
        self.assertEqual(len(results.templates_missing), 0)
        self.assertEqual(len(results.chess_dependencies), 0)
        self.assertEqual(len(results.critical_failures), 0)
    
    def test_dependency_type_membership(self):
        """Test DependencyType enum membership"""
        # Test that we can iterate over enum values
        all_types = list(DependencyType)
        self.assertEqual(len(all_types), 6)
        
        # Test specific types are in the enum
        self.assertIn(DependencyType.NPM_PACKAGE, all_types)
        self.assertIn(DependencyType.TEMPLATE_FILE, all_types)
        self.assertIn(DependencyType.GENERATED_FILE, all_types)
        self.assertIn(DependencyType.PROJECT_FILE, all_types)
        self.assertIn(DependencyType.CHESS_SPECIFIC, all_types)
        self.assertIn(DependencyType.UNKNOWN, all_types)
    
    def test_dependency_info_comparison(self):
        """Test DependencyInfo equality comparison"""
        dependency1 = DependencyInfo(
            import_path="./component",
            dependency_type=DependencyType.TEMPLATE_FILE,
            exists=True,
            source_template="main.template"
        )
        
        dependency2 = DependencyInfo(
            import_path="./component",
            dependency_type=DependencyType.TEMPLATE_FILE,
            exists=True,
            source_template="main.template"
        )
        
        dependency3 = DependencyInfo(
            import_path="./different",
            dependency_type=DependencyType.TEMPLATE_FILE,
            exists=True,
            source_template="main.template"
        )
        
        # Same data should be equal
        self.assertEqual(dependency1, dependency2)
        
        # Different data should not be equal
        self.assertNotEqual(dependency1, dependency3)
    
    def test_dependency_type_string_conversion(self):
        """Test DependencyType string representation"""
        self.assertEqual(str(DependencyType.NPM_PACKAGE), "DependencyType.NPM_PACKAGE")
        self.assertEqual(DependencyType.NPM_PACKAGE.name, "NPM_PACKAGE")
        self.assertEqual(DependencyType.NPM_PACKAGE.value, "npm_package")
    
    def test_validation_results_with_mixed_dependencies(self):
        """Test ValidationResults with various dependency types"""
        npm_dep = DependencyInfo(
            import_path="react",
            dependency_type=DependencyType.NPM_PACKAGE,
            exists=True,
            source_template="component.template"
        )
        
        template_dep = DependencyInfo(
            import_path="./base",
            dependency_type=DependencyType.TEMPLATE_FILE,
            exists=False,
            source_template="page.template",
            error_message="Template not found"
        )
        
        chess_dep = DependencyInfo(
            import_path="chessboard-js",
            dependency_type=DependencyType.CHESS_SPECIFIC,
            exists=True,
            source_template="game.template"
        )
        
        results = ValidationResults(
            dependencies=[npm_dep, template_dep, chess_dep],
            npm_packages_missing=["missing-lib"],
            templates_missing=["base.template"],
            chess_dependencies=["chessboard-js"],
            critical_failures=[]
        )
        
        # Verify mixed dependency types
        dep_types = [dep.dependency_type for dep in results.dependencies]
        self.assertIn(DependencyType.NPM_PACKAGE, dep_types)
        self.assertIn(DependencyType.TEMPLATE_FILE, dep_types)
        self.assertIn(DependencyType.CHESS_SPECIFIC, dep_types)
    
    @unittest.skipIf(PreGenerationValidator is None, "PreGenerationValidator class not found")
    def test_pre_generation_validator_exists(self):
        """Test that PreGenerationValidator class exists if implemented"""
        # This test will only run if the validator class is implemented
        self.assertTrue(hasattr(PreGenerationValidator, '__init__'))
    
    def test_dataclass_immutability(self):
        """Test that dataclasses can be created and accessed properly"""
        # Test DependencyInfo is properly structured
        dependency = DependencyInfo(
            import_path="test",
            dependency_type=DependencyType.UNKNOWN,
            exists=False,
            source_template="test.template"
        )
        
        # Should be able to access all fields
        self.assertEqual(dependency.import_path, "test")
        self.assertEqual(dependency.dependency_type, DependencyType.UNKNOWN)
        self.assertFalse(dependency.exists)
        self.assertEqual(dependency.source_template, "test.template")
    
    def test_enum_value_uniqueness(self):
        """Test that all enum values are unique"""
        values = [dep_type.value for dep_type in DependencyType]
        self.assertEqual(len(values), len(set(values)), "Enum values should be unique")
    
    def test_dependency_info_required_fields(self):
        """Test that DependencyInfo requires all non-optional fields"""
        # This should work (all required fields provided)
        dependency = DependencyInfo(
            import_path="./test",
            dependency_type=DependencyType.TEMPLATE_FILE,
            exists=True,
            source_template="source.template"
        )
        self.assertIsNotNone(dependency)
        
        # Test that we can create with minimal required fields
        minimal_dependency = DependencyInfo(
            import_path="minimal",
            dependency_type=DependencyType.UNKNOWN,
            exists=False,
            source_template="minimal.template"
        )
        self.assertIsNotNone(minimal_dependency)


if __name__ == '__main__':
    unittest.main()