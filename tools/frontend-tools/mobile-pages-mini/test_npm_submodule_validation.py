#!/usr/bin/env python3
"""
Test suite to verify NPM package submodule detection works correctly.
Tests the fix for handling imports like 'react-icons/hi' and 'zustand/middleware'.
"""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from modules.pre_generation_validator import PreGenerationValidator
from modules.config import GenerationContext, PageConfig


class TestNPMSubmoduleValidation(unittest.TestCase):
    
    def setUp(self):
        self.static_dir = Path("templates/static")
        self.dynamic_dir = Path("templates/dynamic")
        self.validator = PreGenerationValidator(self.static_dir, self.dynamic_dir)
    
    def test_extract_root_package_name_regular_packages(self):
        """Test root package extraction for regular packages."""
        # Test regular package submodules
        self.assertEqual(
            self.validator._extract_root_package_name("react-icons/hi"),
            "react-icons"
        )
        self.assertEqual(
            self.validator._extract_root_package_name("zustand/middleware"),
            "zustand"
        )
        self.assertEqual(
            self.validator._extract_root_package_name("lodash/pick"),
            "lodash"
        )
        
        # Test packages without submodules
        self.assertEqual(
            self.validator._extract_root_package_name("react"),
            "react"
        )
        self.assertEqual(
            self.validator._extract_root_package_name("zustand"),
            "zustand"
        )
    
    def test_extract_root_package_name_scoped_packages(self):
        """Test root package extraction for scoped packages."""
        # Test scoped packages (should return full name)
        self.assertEqual(
            self.validator._extract_root_package_name("@radix-ui/react-slot"),
            "@radix-ui/react-slot"
        )
        self.assertEqual(
            self.validator._extract_root_package_name("@headlessui/react"),
            "@headlessui/react"
        )
        self.assertEqual(
            self.validator._extract_root_package_name("@types/node"),
            "@types/node"
        )
    
    def test_npm_package_exists_with_submodules(self):
        """Test NPM package detection works with submodules."""
        config = PageConfig(name="testpage", mobile=False)
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        # Mock package.json with parent packages
        package_json_content = {
            "dependencies": {
                "react-icons": "^4.0.0",
                "zustand": "^4.0.0",
                "@headlessui/react": "^1.0.0"
            }
        }
        
        with patch('builtins.open'), \
             patch('json.load', return_value=package_json_content), \
             patch('pathlib.Path.exists', return_value=True):
            
            # Test submodule detection
            self.assertTrue(
                self.validator._check_npm_package_exists("react-icons/hi", context),
                "Should detect react-icons/hi as part of react-icons package"
            )
            self.assertTrue(
                self.validator._check_npm_package_exists("react-icons/vsc", context),
                "Should detect react-icons/vsc as part of react-icons package"
            )
            self.assertTrue(
                self.validator._check_npm_package_exists("zustand/middleware", context),
                "Should detect zustand/middleware as part of zustand package"
            )
            
            # Test scoped packages
            self.assertTrue(
                self.validator._check_npm_package_exists("@headlessui/react", context),
                "Should detect scoped package correctly"
            )
            
            # Test parent packages
            self.assertTrue(
                self.validator._check_npm_package_exists("react-icons", context),
                "Should detect parent package"
            )
            self.assertTrue(
                self.validator._check_npm_package_exists("zustand", context),
                "Should detect parent package"
            )
    
    def test_npm_package_missing_parent(self):
        """Test NPM package detection fails when parent package is missing."""
        config = PageConfig(name="testpage", mobile=False)
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        # Mock package.json without the parent packages
        package_json_content = {
            "dependencies": {
                "react": "^18.0.0"
                # Missing react-icons and zustand
            }
        }
        
        with patch('builtins.open'), \
             patch('json.load', return_value=package_json_content), \
             patch('pathlib.Path.exists', return_value=True):
            
            # Test submodule detection fails when parent missing
            self.assertFalse(
                self.validator._check_npm_package_exists("react-icons/hi", context),
                "Should fail when react-icons parent package is missing"
            )
            self.assertFalse(
                self.validator._check_npm_package_exists("zustand/middleware", context),
                "Should fail when zustand parent package is missing"
            )
    
    def test_npm_package_dev_dependencies(self):
        """Test NPM package detection works with devDependencies."""
        config = PageConfig(name="testpage", mobile=False)
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        # Mock package.json with packages in devDependencies
        package_json_content = {
            "dependencies": {
                "react": "^18.0.0"
            },
            "devDependencies": {
                "react-icons": "^4.0.0",
                "@types/node": "^18.0.0"
            }
        }
        
        with patch('builtins.open'), \
             patch('json.load', return_value=package_json_content), \
             patch('pathlib.Path.exists', return_value=True):
            
            # Test submodule detection in devDependencies
            self.assertTrue(
                self.validator._check_npm_package_exists("react-icons/hi", context),
                "Should detect submodules in devDependencies"
            )
            self.assertTrue(
                self.validator._check_npm_package_exists("@types/node", context),
                "Should detect scoped packages in devDependencies"
            )
    
    def test_npm_package_no_package_json(self):
        """Test NPM package detection fails gracefully when package.json missing."""
        config = PageConfig(name="testpage", mobile=False)
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        with patch('pathlib.Path.exists', return_value=False):
            # Test fails gracefully when package.json doesn't exist
            self.assertFalse(
                self.validator._check_npm_package_exists("react-icons/hi", context),
                "Should return False when package.json doesn't exist"
            )


class TestIntegrationWithRealPackages(unittest.TestCase):
    """Integration tests with common real-world package patterns."""
    
    def setUp(self):
        self.static_dir = Path("templates/static")
        self.dynamic_dir = Path("templates/dynamic")
        self.validator = PreGenerationValidator(self.static_dir, self.dynamic_dir)
    
    def test_common_submodule_patterns(self):
        """Test common real-world submodule import patterns."""
        test_cases = [
            # (import_path, expected_root_package)
            ("react-icons/hi", "react-icons"),
            ("react-icons/vsc", "react-icons"),
            ("react-icons/fa", "react-icons"),
            ("zustand/middleware", "zustand"),
            ("lodash/pick", "lodash"),
            ("lodash/map", "lodash"),
            ("date-fns/format", "date-fns"),
            ("ramda/curry", "ramda"),
            # Scoped packages
            ("@radix-ui/react-slot", "@radix-ui/react-slot"),
            ("@headlessui/react", "@headlessui/react"),
            ("@types/node", "@types/node"),
            ("@babel/core", "@babel/core"),
            ("@babel/preset-env", "@babel/preset-env"),
            # Edge cases
            ("react", "react"),
            ("vue", "vue"),
            ("@vue/core", "@vue/core"),
        ]
        
        for import_path, expected_root in test_cases:
            with self.subTest(import_path=import_path):
                actual_root = self.validator._extract_root_package_name(import_path)
                self.assertEqual(
                    actual_root, expected_root,
                    f"Failed for {import_path}: expected {expected_root}, got {actual_root}"
                )


if __name__ == '__main__':
    print("🧪 Running NPM Submodule Validation Tests...")
    unittest.main(verbosity=2)