#!/usr/bin/env python3
"""
Comprehensive test runner for all mobile-pages-v2 phases.
Runs without pytest dependency using simple test discovery.
"""

import sys
import os
import tempfile
import importlib.util
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

def run_simple_tests():
    """Run simple functionality tests for core modules."""
    
    print("🧪 Running Simple Module Tests...")
    
    try:
        # Test Phase 1: Core Infrastructure
        print("\n=== Phase 1: Core Infrastructure ===")
        
        # Test config module
        from config import PageConfig, ProjectCapabilities, GenerationContext, WrapperType
        config = PageConfig(name="TestPage", parent="TestParent", mobile=True)
        assert config.base_name == "Test"
        assert config.page_name == "TestPage"
        assert config.parent_id == "testparent"
        print("✅ Config module working")
        
        # Test template engine basics
        from template_engine import TemplateEngine
        temp_dir = Path(tempfile.mkdtemp())
        templates_root = temp_dir / "templates"
        templates_root.mkdir()
        
        # Create a test template
        test_template = templates_root / "test.template"
        test_template.write_text("Hello {{NAME}}!")
        
        engine = TemplateEngine(templates_root)
        rendered = engine.render_template("test.template", {"NAME": "World"})
        assert "Hello World!" in rendered
        print("✅ TemplateEngine basic functionality")
        
        # Test project detector
        from project_detector import ProjectCapabilityDetector
        detector = ProjectCapabilityDetector(temp_dir)
        capabilities = detector.detect_capabilities()
        assert isinstance(capabilities, ProjectCapabilities)
        print("✅ ProjectCapabilityDetector working")
        
        # Test wrapper selector
        from wrapper_selector import WrapperSelector
        selector = WrapperSelector()
        wrapper_type = selector.select_wrapper_template(config, capabilities)
        assert wrapper_type in [WrapperType.FULL_HOOKS, WrapperType.BASIC_HOOKS, WrapperType.NO_HOOKS, WrapperType.NO_MOBILE]
        print("✅ WrapperSelector working")
        
        # Test file writer basics
        from file_writer import FileWriter
        writer = FileWriter()
        test_file = temp_dir / "test.txt"
        writer.write_file(test_file, "Test content", "TestRunner", __file__)
        assert test_file.exists()
        content = test_file.read_text()
        assert "Test content" in content
        assert "WARNING: GENERATED CODE" in content
        print("✅ FileWriter working")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All simple module tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Simple module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def discover_and_run_unit_tests():
    """Discover and run unit test classes."""
    
    print("\n🧪 Running Unit Test Discovery...")
    
    test_files = [
        'test_template_engine.py',
        'test_project_detector.py', 
        'test_file_writer.py',
        'test_dependency_manager.py',
        'test_child_generator.py',
        'test_wrapper_selector.py',
        'test_variable_generator.py',
        'test_parent_generator.py',
        'test_routing_updater.py',
        'test_validation.py'
    ]
    
    passed_tests = 0
    total_tests = 0
    
    for test_file in test_files:
        test_path = Path('tests') / test_file
        if not test_path.exists():
            print(f"⚠️  Test file not found: {test_file}")
            continue
            
        print(f"\n=== Running {test_file} ===")
        
        try:
            # Load the test module
            spec = importlib.util.spec_from_file_location(
                test_file[:-3], test_path
            )
            test_module = importlib.util.module_from_spec(spec)
            
            # Add to sys.modules to handle imports
            sys.modules[test_file[:-3]] = test_module
            spec.loader.exec_module(test_module)
            
            # Find test classes
            test_classes = []
            for name in dir(test_module):
                obj = getattr(test_module, name)
                if (isinstance(obj, type) and 
                    name.startswith('Test') and 
                    hasattr(obj, 'setup_method')):
                    test_classes.append(obj)
            
            if not test_classes:
                print(f"⚠️  No test classes found in {test_file}")
                continue
            
            # Run tests in each class
            for test_class in test_classes:
                print(f"  Running {test_class.__name__}...")
                
                # Find test methods
                test_methods = [method for method in dir(test_class) 
                              if method.startswith('test_')]
                
                for test_method_name in test_methods:
                    try:
                        # Create test instance
                        test_instance = test_class()
                        
                        # Run setup if exists
                        if hasattr(test_instance, 'setup_method'):
                            test_instance.setup_method()
                        
                        # Run the test method
                        test_method = getattr(test_instance, test_method_name)
                        test_method()
                        
                        # Run teardown if exists  
                        if hasattr(test_instance, 'teardown_method'):
                            test_instance.teardown_method()
                        
                        print(f"    ✅ {test_method_name}")
                        passed_tests += 1
                        
                    except Exception as e:
                        print(f"    ❌ {test_method_name}: {e}")
                    
                    total_tests += 1
                    
        except Exception as e:
            print(f"❌ Failed to load {test_file}: {e}")
    
    print(f"\n📊 Unit Test Results: {passed_tests}/{total_tests} passed")
    return passed_tests, total_tests

def run_integration_tests():
    """Run integration tests that test multiple modules together."""
    
    print("\n🧪 Running Integration Tests...")
    
    try:
        # Test complete generation context creation
        from config import GenerationContext, PageConfig, ProjectCapabilities
        from pathlib import Path
        import tempfile
        
        temp_dir = Path(tempfile.mkdtemp())
        config = PageConfig(name="TestChild", parent="TestParent", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        context = GenerationContext(
            frontend_root=temp_dir,
            config=config,
            capabilities=capabilities,
            variables={}
        )
        
        # Test that all directory properties work
        assert context.pages_dir == temp_dir / "src" / "pages"
        assert context.components_dir == temp_dir / "src" / "components"
        assert context.hooks_dir == temp_dir / "src" / "hooks"
        print("✅ GenerationContext integration")
        
        # Test template engine + wrapper selector integration
        from template_engine import TemplateEngine
        from wrapper_selector import WrapperSelector
        
        templates_root = temp_dir / "templates"
        templates_root.mkdir(parents=True)
        
        engine = TemplateEngine(templates_root)
        selector = WrapperSelector()
        
        wrapper_type = selector.select_wrapper_template(config, capabilities)
        requirements = selector.get_wrapper_requirements(wrapper_type)
        
        assert isinstance(requirements, dict)
        assert 'requires_page_hooks' in requirements
        print("✅ TemplateEngine + WrapperSelector integration")
        
        # Test file writer + shared utilities integration
        from file_writer import FileWriter
        
        writer = FileWriter()
        test_file = temp_dir / "integration_test.tsx"
        
        # Test TypeScript file generation with shared utilities
        content = 'export const TestComponent = () => <div>Hello</div>;'
        writer.write_file(test_file, content, "IntegrationTest", __file__)
        
        generated_content = test_file.read_text()
        assert "WARNING: GENERATED CODE - DO NOT MODIFY" in generated_content
        assert content in generated_content
        print("✅ FileWriter + SharedUtilities integration")
        
        # Test smart import functionality
        import_test_file = temp_dir / "import_test.tsx"
        import_content = '''import React from 'react';

export const TestComponent = () => <div>Hello</div>;'''
        
        import_test_file.write_text(import_content)
        writer.add_import(import_test_file, './hooks/useTest', 'useTest')
        
        updated_content = import_test_file.read_text()
        assert 'useTest' in updated_content
        print("✅ Smart import integration")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive test suite."""
    
    print("🧪 Mobile Pages V2 - Comprehensive Test Suite")
    print("="*60)
    
    all_passed = True
    
    # Run simple module tests
    simple_passed = run_simple_tests()
    all_passed &= simple_passed
    
    # Run unit test discovery
    passed_count, total_count = discover_and_run_unit_tests()
    unit_tests_passed = (passed_count == total_count) if total_count > 0 else True
    all_passed &= unit_tests_passed
    
    # Run integration tests
    integration_passed = run_integration_tests()
    all_passed &= integration_passed
    
    # Final results
    print("\n" + "="*60)
    print("🧪 FINAL TEST RESULTS")
    print("="*60)
    print(f"Simple Module Tests: {'✅ PASS' if simple_passed else '❌ FAIL'}")
    print(f"Unit Tests: {'✅ PASS' if unit_tests_passed else '❌ FAIL'} ({passed_count}/{total_count})")
    print(f"Integration Tests: {'✅ PASS' if integration_passed else '❌ FAIL'}")
    print("="*60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Mobile Pages V2 implementation is working correctly")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️  Implementation needs attention")
    
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())