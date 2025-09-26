#!/usr/bin/env python3
"""
Tests for the Container Integrator module
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

from modules.container_integrator import ContainerIntegrator


class TestContainerIntegrator(unittest.TestCase):
    """Test the Container Integrator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.frontend_root = self.test_dir / "frontend"
        self.frontend_root.mkdir(parents=True)
        
        # Create expected directory structure
        src_dir = self.frontend_root / "src"
        src_dir.mkdir()
        components_dir = src_dir / "components" / "shared"
        components_dir.mkdir(parents=True)
        
        # Create test files
        self.app_tsx = src_dir / "App.tsx"
        self.app_tsx.write_text("// App.tsx content")
        
        self.action_sheet_container = components_dir / "ActionSheetContainer.tsx"
        self.action_sheet_container.write_text("// ActionSheetContainer content")
        
        # Mock file writer
        self.mock_file_writer = Mock()
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_container_integrator_initialization(self):
        """Test ContainerIntegrator initialization"""
        # Test with mock file writer
        integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, self.frontend_root)
        self.assertEqual(integrator.file_writer, self.mock_file_writer)
        
        # Should set up correct file paths
        expected_app_path = self.frontend_root / "src/App.tsx"
        expected_container_path = self.frontend_root / "src/components/shared/ActionSheetContainer.tsx"
        
        self.assertEqual(integrator.app_tsx_path, expected_app_path)
        self.assertEqual(integrator.action_sheet_container_path, expected_container_path)
        
        # Should have config integration
        self.assertTrue(hasattr(integrator, 'config_integration'))
    
    def test_container_integrator_initialization_without_file_writer(self):
        """Test ContainerIntegrator initialization without explicit file writer"""
        # Should create default file writer
        with patch('modules.container_integrator.FileWriter') as mock_file_writer_class:
            mock_file_writer_instance = Mock()
            mock_file_writer_class.return_value = mock_file_writer_instance
            
            integrator = ContainerIntegrator(self.frontend_root)
            
            # Should use default file writer
            mock_file_writer_class.assert_called_once()
            self.assertEqual(integrator.file_writer, mock_file_writer_instance)
    
    def test_container_integrator_file_paths(self):
        """Test that ContainerIntegrator sets up correct file paths"""
        integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Should set up paths for key integration files
        self.assertEqual(integrator.app_tsx_path, self.frontend_root / "src/App.tsx")
        self.assertEqual(
            integrator.action_sheet_container_path, 
            self.frontend_root / "src/components/shared/ActionSheetContainer.tsx"
        )
        
        # All paths should be Path objects
        self.assertIsInstance(integrator.app_tsx_path, Path)
        self.assertIsInstance(integrator.action_sheet_container_path, Path)
    
    def test_container_integrator_with_nonexistent_frontend_root(self):
        """Test ContainerIntegrator with nonexistent frontend root"""
        nonexistent_root = self.test_dir / "nonexistent"
        
        # Should still initialize without errors
        integrator = ContainerIntegrator(nonexistent_root, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, nonexistent_root)
        
        # Paths should still be set up correctly
        self.assertEqual(integrator.app_tsx_path, nonexistent_root / "src/App.tsx")
        self.assertEqual(
            integrator.action_sheet_container_path,
            nonexistent_root / "src/components/shared/ActionSheetContainer.tsx"
        )
    
    def test_container_integrator_config_integration(self):
        """Test that ContainerIntegrator properly initializes config integration"""
        with patch('modules.container_integrator.ConfigIntegration') as mock_config_integration_class:
            mock_config_integration = Mock()
            mock_config_integration_class.return_value = mock_config_integration
            
            integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
            
            # Should create config integration with frontend root
            mock_config_integration_class.assert_called_once_with(self.frontend_root)
            self.assertEqual(integrator.config_integration, mock_config_integration)
    
    def test_container_integrator_file_writer_dependency(self):
        """Test ContainerIntegrator dependency on FileWriter"""
        integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Should store the file writer
        self.assertEqual(integrator.file_writer, self.mock_file_writer)
        
        # File writer should be available for use
        self.assertTrue(hasattr(integrator.file_writer, 'write_file'))
    
    def test_container_integrator_attributes(self):
        """Test that ContainerIntegrator has expected attributes"""
        integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Should have all required attributes
        self.assertTrue(hasattr(integrator, 'frontend_root'))
        self.assertTrue(hasattr(integrator, 'file_writer'))
        self.assertTrue(hasattr(integrator, 'app_tsx_path'))
        self.assertTrue(hasattr(integrator, 'action_sheet_container_path'))
        self.assertTrue(hasattr(integrator, 'config_integration'))
        
        # Attributes should have correct types
        self.assertIsInstance(integrator.frontend_root, Path)
        self.assertIsInstance(integrator.app_tsx_path, Path)
        self.assertIsInstance(integrator.action_sheet_container_path, Path)
    
    def test_container_integrator_path_handling(self):
        """Test ContainerIntegrator path handling"""
        # Test with string path
        string_path = str(self.frontend_root)
        integrator = ContainerIntegrator(string_path, self.mock_file_writer)
        
        # Should convert to Path object
        self.assertIsInstance(integrator.frontend_root, Path)
        self.assertEqual(str(integrator.frontend_root), string_path)
    
    def test_container_integrator_expected_file_structure(self):
        """Test expected file structure paths"""
        integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
        
        # App.tsx should be in src directory
        self.assertTrue(str(integrator.app_tsx_path).endswith("src/App.tsx"))
        
        # ActionSheetContainer should be in components/shared
        self.assertTrue(
            str(integrator.action_sheet_container_path).endswith(
                "src/components/shared/ActionSheetContainer.tsx"
            )
        )
    
    def test_container_integrator_methods_existence(self):
        """Test that ContainerIntegrator has expected methods (interface test)"""
        integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
        
        # Test that integrator is properly instantiated
        self.assertIsNotNone(integrator)
        
        # Test that it has the basic attributes we expect
        self.assertTrue(hasattr(integrator, 'frontend_root'))
        self.assertTrue(hasattr(integrator, 'file_writer'))
        self.assertTrue(hasattr(integrator, 'app_tsx_path'))
        self.assertTrue(hasattr(integrator, 'action_sheet_container_path'))
        self.assertTrue(hasattr(integrator, 'config_integration'))
    
    def test_container_integrator_imports(self):
        """Test that ContainerIntegrator can be imported and has expected dependencies"""
        # Test that the class is properly imported
        self.assertTrue(hasattr(ContainerIntegrator, '__init__'))
        
        # Test that it expects the right constructor parameters
        import inspect
        sig = inspect.signature(ContainerIntegrator.__init__)
        params = list(sig.parameters.keys())
        
        # Should have self, frontend_root, and optional file_writer
        self.assertIn('self', params)
        self.assertIn('frontend_root', params)
        self.assertIn('file_writer', params)
    
    def test_container_integrator_with_different_paths(self):
        """Test ContainerIntegrator with different path configurations"""
        # Test with nested path
        nested_frontend = self.test_dir / "deep" / "nested" / "frontend"
        integrator = ContainerIntegrator(nested_frontend, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, nested_frontend)
        self.assertEqual(integrator.app_tsx_path, nested_frontend / "src/App.tsx")
        self.assertEqual(
            integrator.action_sheet_container_path,
            nested_frontend / "src/components/shared/ActionSheetContainer.tsx"
        )
        
        # Test with current directory
        current_dir = Path(".")
        integrator = ContainerIntegrator(current_dir, self.mock_file_writer)
        
        self.assertEqual(integrator.frontend_root, current_dir)
        self.assertEqual(integrator.app_tsx_path, current_dir / "src/App.tsx")
        self.assertEqual(
            integrator.action_sheet_container_path,
            current_dir / "src/components/shared/ActionSheetContainer.tsx"
        )
    
    def test_container_integrator_file_path_consistency(self):
        """Test that file paths are consistent with React project structure"""
        integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
        
        # All paths should be under the frontend root
        self.assertTrue(integrator.app_tsx_path.is_relative_to(integrator.frontend_root))
        self.assertTrue(integrator.action_sheet_container_path.is_relative_to(integrator.frontend_root))
        
        # Paths should follow expected React structure
        self.assertEqual(integrator.app_tsx_path.name, "App.tsx")
        self.assertEqual(integrator.action_sheet_container_path.name, "ActionSheetContainer.tsx")


if __name__ == '__main__':
    unittest.main()