#!/usr/bin/env python3
"""
Tests for the Project Detector module
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.project_detector import ProjectCapabilityDetector, ProjectDetectionError
from modules.config import ProjectCapabilities


class TestProjectCapabilityDetector(unittest.TestCase):
    """Test the Project Capability Detector"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.detector = ProjectCapabilityDetector()
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_detect_react_vite_project(self):
        """Test detection of React + Vite project"""
        # Create package.json with React and Vite
        package_json = {
            "name": "test-chess-app",
            "version": "1.0.0",
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.8.0"
            },
            "devDependencies": {
                "vite": "^4.1.0",
                "@vitejs/plugin-react": "^3.1.0",
                "typescript": "^4.9.3",
                "@types/react": "^18.0.28"
            }
        }
        
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        # Create vite.config.ts
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})"""
        
        with open(self.test_dir / "vite.config.ts", 'w') as f:
            f.write(vite_config)
        
        # Detect capabilities
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        # Verify detected capabilities
        self.assertTrue(capabilities.has_react)
        self.assertTrue(capabilities.has_typescript)
        self.assertTrue(capabilities.has_vite)
        self.assertTrue(capabilities.has_react_router)
        self.assertFalse(capabilities.has_next_js)
        self.assertFalse(capabilities.has_webpack)
    
    def test_detect_typescript_support(self):
        """Test TypeScript detection"""
        # Create tsconfig.json
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler"
            }
        }
        
        with open(self.test_dir / "tsconfig.json", 'w') as f:
            import json
            json.dump(tsconfig, f)
        
        # Create package.json with TypeScript
        package_json = {
            "devDependencies": {
                "typescript": "^4.9.3"
            }
        }
        
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        self.assertTrue(capabilities.has_typescript)
        self.assertFalse(capabilities.has_react)  # No React in this test
    
    def test_detect_styling_capabilities(self):
        """Test detection of styling frameworks"""
        package_json = {
            "dependencies": {
                "react": "^18.2.0"
            },
            "devDependencies": {
                "tailwindcss": "^3.2.0",
                "autoprefixer": "^10.4.14",
                "postcss": "^8.4.21"
            }
        }
        
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        # Create tailwind.config.js
        tailwind_config = """module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}"""
        
        with open(self.test_dir / "tailwind.config.js", 'w') as f:
            f.write(tailwind_config)
        
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        self.assertTrue(capabilities.has_tailwind)
        self.assertTrue(capabilities.has_react)
    
    def test_detect_testing_frameworks(self):
        """Test detection of testing frameworks"""
        package_json = {
            "devDependencies": {
                "vitest": "^0.29.0",
                "@testing-library/react": "^14.0.0",
                "@testing-library/jest-dom": "^5.16.5",
                "jsdom": "^21.1.0"
            }
        }
        
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        self.assertTrue(capabilities.has_vitest)
        self.assertTrue(capabilities.has_testing_library)
    
    def test_detect_mobile_capabilities(self):
        """Test detection of mobile-specific dependencies"""
        package_json = {
            "dependencies": {
                "react": "^18.2.0",
                "react-native-web": "^0.18.12"
            },
            "devDependencies": {
                "@capacitor/core": "^4.7.0",
                "@capacitor/cli": "^4.7.0"
            }
        }
        
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        self.assertTrue(capabilities.has_react_native_web)
        self.assertTrue(capabilities.has_capacitor)
    
    def test_empty_project_detection(self):
        """Test detection on empty project"""
        # Create empty package.json
        package_json = {"name": "empty-project", "version": "1.0.0"}
        
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        # Should detect nothing
        self.assertFalse(capabilities.has_react)
        self.assertFalse(capabilities.has_typescript)
        self.assertFalse(capabilities.has_vite)
        self.assertFalse(capabilities.has_tailwind)
    
    def test_missing_package_json_error(self):
        """Test error handling when package.json is missing"""
        with self.assertRaises(ProjectDetectionError) as context:
            self.detector.detect_project_capabilities(self.test_dir)
        
        self.assertIn("package.json not found", str(context.exception))
    
    def test_invalid_package_json_error(self):
        """Test error handling with invalid package.json"""
        # Create invalid JSON
        with open(self.test_dir / "package.json", 'w') as f:
            f.write("{ invalid json content }")
        
        with self.assertRaises(ProjectDetectionError) as context:
            self.detector.detect_project_capabilities(self.test_dir)
        
        self.assertIn("Invalid package.json", str(context.exception))
    
    def test_detect_chess_specific_dependencies(self):
        """Test detection of chess-specific libraries"""
        package_json = {
            "dependencies": {
                "react": "^18.2.0",
                "chess.js": "^1.0.0",
                "react-chessboard": "^1.5.0"
            }
        }
        
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        self.assertTrue(capabilities.has_react)
        # Note: chess-specific capabilities would need to be added to ProjectCapabilities
        # if we want to detect them specifically
    
    def test_src_directory_detection(self):
        """Test detection of src directory structure"""
        # Create src directory with typical structure
        src_dir = self.test_dir / "src"
        src_dir.mkdir()
        (src_dir / "components").mkdir()
        (src_dir / "pages").mkdir()
        (src_dir / "hooks").mkdir()
        
        # Create some files
        (src_dir / "App.tsx").touch()
        (src_dir / "main.tsx").touch()
        
        package_json = {"name": "test", "dependencies": {"react": "^18.0.0"}}
        with open(self.test_dir / "package.json", 'w') as f:
            import json
            json.dump(package_json, f)
        
        capabilities = self.detector.detect_project_capabilities(self.test_dir)
        
        # Basic detection should work
        self.assertTrue(capabilities.has_react)


if __name__ == '__main__':
    unittest.main()