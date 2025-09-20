#!/usr/bin/env python3
"""
Simple test runner that manually exercises all the test functions without pytest.
"""

import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

def run_template_engine_tests():
    """Run TemplateEngine tests manually."""
    print("\n=== Testing TemplateEngine ===")
    
    try:
        from template_engine import TemplateEngine, TemplateValidationError
        from config import PageConfig, ProjectCapabilities, WrapperType
        
        # Setup test environment
        temp_dir = Path(tempfile.mkdtemp())
        templates_root = temp_dir / "templates"
        templates_root.mkdir(parents=True)
        
        # Create test template
        test_template = templates_root / "test.template"
        test_template.write_text("Hello {{NAME}}! Welcome to {{PROJECT}}.")
        
        engine = TemplateEngine(templates_root)
        
        # Test 1: Template loading
        content = engine.load_template("test.template")
        assert content == "Hello {{NAME}}! Welcome to {{PROJECT}}."
        print("✅ Template loading")
        
        # Test 2: Template rendering
        variables = {'NAME': 'John', 'PROJECT': 'TestProject'}
        result = engine.render_template("test.template", variables)
        assert result == "Hello John! Welcome to TestProject."
        print("✅ Template rendering")
        
        # Test 3: Wrapper template selection
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=True)
        result = engine.select_child_wrapper_template(config, capabilities)
        assert result == WrapperType.FULL_HOOKS
        print("✅ Wrapper template selection")
        
        # Test 4: Template validation
        assert engine.validate_template_exists("test.template") is True
        assert engine.validate_template_exists("nonexistent.template") is False
        print("✅ Template validation")
        
        # Test 5: Template listing
        templates = engine.list_available_templates()
        assert "test.template" in templates
        print("✅ Template listing")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All TemplateEngine tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ TemplateEngine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_project_detector_tests():
    """Run ProjectCapabilityDetector tests manually."""
    print("\n=== Testing ProjectCapabilityDetector ===")
    
    try:
        from project_detector import ProjectCapabilityDetector, ProjectDetectionError
        from config import ProjectCapabilities
        
        # Setup test environment
        temp_dir = Path(tempfile.mkdtemp())
        frontend_root = temp_dir
        src_dir = frontend_root / "src"
        hooks_core_dir = src_dir / "hooks" / "core"
        components_ui_dir = src_dir / "components" / "ui"
        pages_dir = src_dir / "pages"
        
        hooks_core_dir.mkdir(parents=True)
        components_ui_dir.mkdir(parents=True)
        pages_dir.mkdir(parents=True)
        
        detector = ProjectCapabilityDetector(frontend_root)
        
        # Test 1: Detect no capabilities
        capabilities = detector.detect_capabilities()
        assert capabilities.has_page_hooks is False
        assert capabilities.has_mobile_hook is False
        assert capabilities.has_data_table is False
        print("✅ Detect no capabilities")
        
        # Test 2: Detect page hooks
        (hooks_core_dir / "usePageInstructions.ts").write_text("// Hook content")
        (hooks_core_dir / "usePageActions.ts").write_text("// Hook content")
        capabilities = detector.detect_capabilities()
        assert capabilities.has_page_hooks is True
        print("✅ Detect page hooks")
        
        # Test 3: Detect mobile hook
        (hooks_core_dir / "useIsMobile.ts").write_text("// Mobile hook")
        capabilities = detector.detect_capabilities()
        assert capabilities.has_mobile_hook is True
        print("✅ Detect mobile hook")
        
        # Test 4: Detect DataTable
        (components_ui_dir / "DataTable.tsx").write_text("// DataTable component")
        capabilities = detector.detect_capabilities()
        assert capabilities.has_data_table is True
        print("✅ Detect DataTable")
        
        # Test 5: Detect parent pages
        uitests_dir = pages_dir / "uitests"
        uitests_dir.mkdir()
        (uitests_dir / "UitestsPage.tsx").write_text("// Parent page")
        capabilities = detector.detect_capabilities()
        assert "uitests" in capabilities.existing_parents
        print("✅ Detect parent pages")
        
        # Test 6: Parent existence check
        assert detector.check_parent_exists("uitests") is True
        assert detector.check_parent_exists("nonexistent") is False
        print("✅ Parent existence check")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All ProjectCapabilityDetector tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ ProjectCapabilityDetector test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_file_writer_tests():
    """Run FileWriter tests manually."""
    print("\n=== Testing FileWriter ===")
    
    try:
        from file_writer import FileWriter
        
        # Setup test environment
        temp_dir = Path(tempfile.mkdtemp())
        writer = FileWriter()
        
        # Test 1: Write file with warning header
        test_file = temp_dir / "test.tsx"
        content = 'export const TestComponent = () => <div>Hello</div>;'
        writer.write_file(test_file, content, "TestGenerator", "/test/path")
        
        assert test_file.exists()
        file_content = test_file.read_text()
        assert content in file_content
        assert "WARNING: GENERATED CODE - DO NOT MODIFY" in file_content
        print("✅ Write file with warning header")
        
        # Test 2: Create directories
        nested_file = temp_dir / "deep" / "nested" / "path" / "test.tsx"
        writer.write_file(nested_file, content, "TestGenerator", "/test/path")
        assert nested_file.exists()
        print("✅ Create parent directories")
        
        # Test 3: Backup existing files
        original_content = "Original content"
        backup_test_file = temp_dir / "backup_test.txt"
        backup_test_file.write_text(original_content)
        
        writer.write_file(backup_test_file, "New content", "TestGenerator", "/test/path")
        
        backup_dir = temp_dir / ".generator_backups"
        assert backup_dir.exists()
        backup_files = list(backup_dir.glob("backup_test.txt.backup_*"))
        assert len(backup_files) == 1
        print("✅ Backup existing files")
        
        # Test 4: Smart import functionality
        import_test_file = temp_dir / "import_test.tsx"
        initial_content = '''import React from 'react';

export const TestComponent = () => <div>Hello</div>;'''
        import_test_file.write_text(initial_content)
        
        writer.add_import(import_test_file, './hooks/useTest', 'useTest')
        updated_content = import_test_file.read_text()
        assert 'useTest' in updated_content
        print("✅ Smart import functionality")
        
        # Test 5: Validation
        assert writer.file_exists(test_file) is True
        assert writer.file_exists(temp_dir / "nonexistent.txt") is False
        print("✅ File validation")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All FileWriter tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ FileWriter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_dependency_manager_tests():
    """Run DependencyManager tests manually."""
    print("\n=== Testing DependencyManager ===")
    
    try:
        from dependency_manager import DependencyManager
        from config import GenerationContext, PageConfig, ProjectCapabilities
        from template_engine import TemplateEngine
        from file_writer import FileWriter
        
        # Setup test environment
        temp_dir = Path(tempfile.mkdtemp())
        frontend_root = temp_dir
        hooks_dir = frontend_root / "src" / "hooks" / "core"
        components_ui_dir = frontend_root / "src" / "components" / "ui"
        hooks_dir.mkdir(parents=True)
        components_ui_dir.mkdir(parents=True)
        
        # Mock dependencies
        mock_template_engine = Mock(spec=TemplateEngine)
        mock_file_writer = Mock(spec=FileWriter)
        mock_template_engine.render_template.return_value = "// Mock content"
        
        dependency_manager = DependencyManager(mock_template_engine, mock_file_writer)
        
        # Create test context
        config = PageConfig(name="TestPage")
        capabilities = ProjectCapabilities(has_page_hooks=False, has_mobile_hook=False, has_data_table=False)
        context = GenerationContext(
            frontend_root=frontend_root,
            config=config,
            capabilities=capabilities,
            variables={}
        )
        
        # Test 1: Ensure usePageData hook when missing
        dependency_manager.ensure_use_page_data_hook(context)
        mock_template_engine.render_template.assert_called_with(
            'dependencies/use-page-data-hook.ts.template',
            {'GENERATOR_NAME': 'DependencyManager', 'SOURCE_FILE': '/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py'}
        )
        print("✅ Create missing usePageData hook")
        
        # Test 2: Ensure DataTable component when missing
        dependency_manager.ensure_data_table_component(context)
        mock_template_engine.render_template.assert_called_with(
            'dependencies/data-table-component.tsx.template',
            {'GENERATOR_NAME': 'DependencyManager', 'SOURCE_FILE': '/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py'}
        )
        print("✅ Create missing DataTable component")
        
        # Test 3: Validation
        validation_results = dependency_manager.validate_dependencies(context)
        assert 'usePageData' in validation_results
        assert 'DataTable' in validation_results
        print("✅ Dependency validation")
        
        # Test 4: Missing dependencies list
        missing = dependency_manager.get_missing_dependencies(context)
        assert 'usePageData' in missing
        assert 'DataTable' in missing
        print("✅ Missing dependencies detection")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All DependencyManager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ DependencyManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_wrapper_selector_tests():
    """Run WrapperSelector tests manually."""
    print("\n=== Testing WrapperSelector ===")
    
    try:
        from wrapper_selector import WrapperSelector
        from config import PageConfig, ProjectCapabilities, WrapperType
        
        selector = WrapperSelector()
        
        # Test 1: Full hooks selection
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=True, has_data_table=True)
        result = selector.select_wrapper_template(config, capabilities)
        assert result == WrapperType.FULL_HOOKS
        print("✅ Full hooks wrapper selection")
        
        # Test 2: Basic hooks selection
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=False, has_data_table=True)
        result = selector.select_wrapper_template(config, capabilities)
        assert result == WrapperType.BASIC_HOOKS
        print("✅ Basic hooks wrapper selection")
        
        # Test 3: No hooks selection
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(has_page_hooks=False, has_mobile_hook=False, has_data_table=False)
        result = selector.select_wrapper_template(config, capabilities)
        assert result == WrapperType.NO_HOOKS
        print("✅ No hooks wrapper selection")
        
        # Test 4: Validation with issues
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(has_page_hooks=False, has_mobile_hook=False, has_data_table=False)
        wrapper_type = selector.select_wrapper_template(config, capabilities)
        issues = selector.validate_wrapper_selection(wrapper_type, config, capabilities)
        assert len(issues) > 0
        print("✅ Wrapper validation with issues")
        
        # Test 5: All wrapper types
        all_types = selector.get_all_wrapper_types()
        assert len(all_types) == 4
        expected_types = [WrapperType.FULL_HOOKS, WrapperType.BASIC_HOOKS, WrapperType.NO_HOOKS, WrapperType.NO_MOBILE]
        for expected_type in expected_types:
            assert expected_type in all_types
        print("✅ All wrapper types available")
        
        # Test 6: Descriptions
        for wrapper_type in all_types:
            desc = selector.get_wrapper_description(wrapper_type)
            assert desc != "Unknown wrapper type"
            assert len(desc) > 10
        print("✅ Wrapper descriptions")
        
        print("✅ All WrapperSelector tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ WrapperSelector test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all manual tests."""
    print("🧪 Manual Test Suite for Mobile Pages V2")
    print("="*60)
    
    all_passed = True
    
    # Run all test modules
    test_functions = [
        run_template_engine_tests,
        run_project_detector_tests, 
        run_file_writer_tests,
        run_dependency_manager_tests,
        run_wrapper_selector_tests
    ]
    
    for test_func in test_functions:
        try:
            passed = test_func()
            all_passed &= passed
        except Exception as e:
            print(f"❌ Test function {test_func.__name__} failed: {e}")
            all_passed = False
    
    # Final results
    print("\n" + "="*60)
    print("🧪 MANUAL TEST RESULTS")
    print("="*60)
    
    if all_passed:
        print("🎉 ALL MANUAL TESTS PASSED!")
        print("✅ All implemented phases are working correctly")
    else:
        print("❌ SOME MANUAL TESTS FAILED!")
        print("⚠️  Some functionality needs attention")
    
    print("="*60)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())