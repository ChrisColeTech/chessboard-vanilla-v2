#!/usr/bin/env python3
"""
Tests for the Hook Integrator module
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.hook_integrator import HookIntegrator


class TestHookIntegrator(unittest.TestCase):
    """Test the Hook Integrator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.frontend_root = self.test_dir / "frontend"
        self.frontend_root.mkdir(parents=True)
        
        # Create hooks directory
        self.hooks_dir = self.frontend_root / "src/hooks"
        self.hooks_dir.mkdir(parents=True)
        
        # Mock file writer
        self.mock_file_writer = Mock()
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_hook_integrator_initialization(self):
        """Test HookIntegrator initialization"""
        # Test with mock file writer
        integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, self.frontend_root)
        self.assertEqual(integrator.file_writer, self.mock_file_writer)
        self.assertEqual(integrator.hooks_dir, self.frontend_root / "src/hooks")
        
        # Should have config integration
        self.assertTrue(hasattr(integrator, 'config_integration'))
    
    def test_hook_integrator_initialization_without_file_writer(self):
        """Test HookIntegrator initialization without explicit file writer"""
        # Should create default file writer
        with patch('modules.hook_integrator.FileWriter') as mock_file_writer_class:
            mock_file_writer_instance = Mock()
            mock_file_writer_class.return_value = mock_file_writer_instance
            
            integrator = HookIntegrator(self.frontend_root)
            
            # Should use default file writer
            mock_file_writer_class.assert_called_once()
            self.assertEqual(integrator.file_writer, mock_file_writer_instance)
    
    def test_hook_integrator_paths(self):
        """Test that HookIntegrator sets up correct paths"""
        integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Should set up correct directory structure
        expected_hooks_dir = self.frontend_root / "src/hooks"
        self.assertEqual(integrator.hooks_dir, expected_hooks_dir)
        
        # Frontend root should be stored correctly
        self.assertEqual(integrator.frontend_root, self.frontend_root)
    
    def test_hook_integrator_with_nonexistent_frontend_root(self):
        """Test HookIntegrator with nonexistent frontend root"""
        nonexistent_root = self.test_dir / "nonexistent"
        
        # Should still initialize without errors
        integrator = HookIntegrator(nonexistent_root, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, nonexistent_root)
        self.assertEqual(integrator.hooks_dir, nonexistent_root / "src/hooks")
    
    def test_hook_integrator_config_integration(self):
        """Test that HookIntegrator properly initializes config integration"""
        with patch('modules.hook_integrator.ConfigIntegration') as mock_config_integration_class:
            mock_config_integration = Mock()
            mock_config_integration_class.return_value = mock_config_integration
            
            integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
            
            # Should create config integration with frontend root
            mock_config_integration_class.assert_called_once_with(self.frontend_root)
            self.assertEqual(integrator.config_integration, mock_config_integration)
    
    def test_hook_integrator_file_writer_dependency(self):
        """Test HookIntegrator dependency on FileWriter"""
        integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Should store the file writer
        self.assertEqual(integrator.file_writer, self.mock_file_writer)
        
        # File writer should be available for use
        self.assertTrue(hasattr(integrator.file_writer, 'write_file'))
    
    def test_hook_integrator_attributes(self):
        """Test that HookIntegrator has expected attributes"""
        integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Should have all required attributes
        self.assertTrue(hasattr(integrator, 'frontend_root'))
        self.assertTrue(hasattr(integrator, 'file_writer'))
        self.assertTrue(hasattr(integrator, 'hooks_dir'))
        self.assertTrue(hasattr(integrator, 'config_integration'))
        
        # Attributes should have correct types
        self.assertIsInstance(integrator.frontend_root, Path)
        self.assertIsInstance(integrator.hooks_dir, Path)
    
    def test_hook_integrator_path_handling(self):
        """Test HookIntegrator path handling"""
        # Test with string path
        string_path = str(self.frontend_root)
        integrator = HookIntegrator(string_path, self.mock_file_writer)
        
        # Should convert to Path object
        self.assertIsInstance(integrator.frontend_root, Path)
        self.assertEqual(str(integrator.frontend_root), string_path)
    
    def test_hook_integrator_directory_structure(self):
        """Test expected directory structure setup"""
        integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Should expect src/hooks structure
        expected_path = self.frontend_root / "src" / "hooks"
        self.assertEqual(integrator.hooks_dir, expected_path)
        
        # Path should be correctly formed
        self.assertTrue(str(integrator.hooks_dir).endswith("src/hooks"))
    
    def test_hook_integrator_methods_existence(self):
        """Test that HookIntegrator has expected methods (interface test)"""
        integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Test that integrator is properly instantiated
        self.assertIsNotNone(integrator)
        
        # Test that it has the basic attributes we expect
        self.assertTrue(hasattr(integrator, 'frontend_root'))
        self.assertTrue(hasattr(integrator, 'file_writer'))
        self.assertTrue(hasattr(integrator, 'hooks_dir'))
        self.assertTrue(hasattr(integrator, 'config_integration'))
    
    def test_hook_integrator_imports(self):
        """Test that HookIntegrator can be imported and has expected dependencies"""
        # Test that the class is properly imported
        self.assertTrue(hasattr(HookIntegrator, '__init__'))
        
        # Test that it expects the right constructor parameters
        import inspect
        sig = inspect.signature(HookIntegrator.__init__)
        params = list(sig.parameters.keys())
        
        # Should have self, frontend_root, and optional file_writer
        self.assertIn('self', params)
        self.assertIn('frontend_root', params)
        self.assertIn('file_writer', params)
    
    def test_hook_integrator_with_different_paths(self):
        """Test HookIntegrator with different path configurations"""
        # Test with nested path
        nested_frontend = self.test_dir / "deep" / "nested" / "frontend"
        integrator = HookIntegrator(nested_frontend, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, nested_frontend)
        self.assertEqual(integrator.hooks_dir, nested_frontend / "src/hooks")
        
        # Test with current directory
        current_dir = Path(".")
        integrator = HookIntegrator(current_dir, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, current_dir)
        self.assertEqual(integrator.hooks_dir, current_dir / "src/hooks")


if __name__ == '__main__':
    unittest.main()