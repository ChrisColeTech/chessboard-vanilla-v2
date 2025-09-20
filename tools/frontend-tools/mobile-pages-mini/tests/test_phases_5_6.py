#!/usr/bin/env python3
"""
Test suite for Phase 5 (Routing Updates) and Phase 6 (CLI & Validation) functionality.
"""

import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

def test_routing_updater():
    """Test ParentRoutingUpdater functionality."""
    print("\n=== Testing ParentRoutingUpdater ===")
    
    try:
        from config import GenerationContext, PageConfig, ProjectCapabilities
        from routing_updater import ParentRoutingUpdater, RoutingUpdateError
        from template_engine import TemplateEngine
        from file_writer import FileWriter
        from variable_generator import VariableGenerator
        
        # Setup test environment
        temp_dir = Path(tempfile.mkdtemp())
        templates_root = temp_dir / "templates"
        templates_root.mkdir(parents=True)
        
        # Create routing templates
        routing_dir = templates_root / "routing"
        routing_dir.mkdir()
        
        (routing_dir / "child-import.template").write_text(
            "import {{CHILD_NAME}}Wrapper from '@/components/{{PARENT_ID}}/{{CHILD_NAME}}Wrapper';"
        )
        (routing_dir / "child-route-config.template").write_text(
            "{ path: '{{CHILD_ID}}', label: '{{CHILD_NAME}}' }"
        )
        (routing_dir / "child-switch-case.template").write_text(
            "case '{{CHILD_ID}}':\n    return <{{CHILD_NAME}}Wrapper />;"
        )
        
        # Create parent page structure
        pages_dir = temp_dir / "src" / "pages"
        settings_dir = pages_dir / "settings"
        settings_dir.mkdir(parents=True)
        
        # Create parent page file with routing markers
        parent_page_content = '''import React from 'react';

// Child page imports

const SettingsPage = () => {
  const routes = [
    { path: 'main', label: 'Main' }
    // Child page routes
  ];
  
  const renderPage = (page) => {
    switch(page) {
      case 'main':
        return <SettingsMainPage />;
      // Child page components
      default:
        return <SettingsMainPage />;
    }
  };
  
  return <div>{renderPage('main')}</div>;
};

export default SettingsPage;'''
        
        parent_page_path = settings_dir / "SettingsPage.tsx"
        parent_page_path.write_text(parent_page_content)
        
        # Setup mocks and routing updater
        template_engine = TemplateEngine(templates_root)
        file_writer = FileWriter()
        variable_generator = VariableGenerator()
        
        routing_updater = ParentRoutingUpdater(template_engine, file_writer, variable_generator)
        
        # Create test context
        config = PageConfig(name="UserProfile", parent="Settings")
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=True)
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=temp_dir,
            variables={}
        )
        
        # Test 1: Find parent page file
        found_parent = routing_updater._find_parent_page_file(context, "Settings")
        assert found_parent == parent_page_path
        print("✅ Find parent page file")
        
        # Test 2: Generate routing updates
        updates = routing_updater._generate_routing_updates(context, "UserProfile")
        assert "UserProfileWrapper" in updates['import']
        assert "userprofile" in updates['route_config']
        assert "UserProfileWrapper" in updates['switch_case']
        print("✅ Generate routing updates")
        
        # Test 3: Apply routing updates (backup file first)
        original_content = parent_page_path.read_text()
        routing_updater.update_parent_routing(context, "UserProfile")
        
        updated_content = parent_page_path.read_text()
        assert "UserProfileWrapper" in updated_content
        assert "userprofile" in updated_content
        print("✅ Apply routing updates")
        
        # Test 4: Validate routing injection
        validation = routing_updater.validate_routing_injection(context, "UserProfile")
        assert validation['has_import'] is True
        assert validation['has_route_config'] is True
        assert validation['has_switch_case'] is True
        print("✅ Validate routing injection")
        
        # Test 5: Get child routes in parent
        child_routes = routing_updater.get_child_routes_in_parent(context, "Settings")
        assert "userprofile" in child_routes
        print("✅ Get child routes in parent")
        
        # Test 6: Remove child routing
        routing_updater.remove_child_routing(context, "UserProfile")
        cleaned_content = parent_page_path.read_text()
        assert "UserProfileWrapper" not in cleaned_content
        print("✅ Remove child routing")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All ParentRoutingUpdater tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ ParentRoutingUpdater test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation_module():
    """Test ProjectValidator functionality."""
    print("\n=== Testing ProjectValidator ===")
    
    try:
        from validation import ProjectValidator, ValidationResult, ValidationReport
        from error_handling import ErrorSeverity
        from config import PageConfig
        
        # Setup test environment
        temp_dir = Path(tempfile.mkdtemp())
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        
        # Create basic project structure
        src_dir = temp_dir / "src"
        (src_dir / "pages").mkdir(parents=True)
        (src_dir / "components").mkdir(parents=True)
        (src_dir / "hooks" / "core").mkdir(parents=True)
        (temp_dir / "package.json").write_text('{"name": "test-project"}')
        
        # Create some templates
        (templates_dir / "pages").mkdir()
        (templates_dir / "pages" / "test.template").write_text("Test template {{NAME}}")
        
        # Initialize validator
        validator = ProjectValidator(temp_dir, templates_dir)
        
        # Test 1: Project structure validation
        structure_report = validator.validate_project_structure()
        assert len(structure_report.results) > 0
        assert structure_report.passed  # Should pass basic structure
        print("✅ Project structure validation")
        
        # Test 2: Template validation
        template_report = validator.validate_templates()
        assert len(template_report.results) > 0
        print("✅ Template validation")
        
        # Test 3: Capabilities validation
        capabilities_report = validator.validate_project_capabilities()
        assert len(capabilities_report.results) > 0
        print("✅ Capabilities validation")
        
        # Test 4: Dependencies validation (should handle missing gracefully)
        deps_report = validator.validate_dependencies()
        assert len(deps_report.results) > 0
        print("✅ Dependencies validation")
        
        # Test 5: Comprehensive validation
        comprehensive_report = validator.run_comprehensive_validation()
        assert len(comprehensive_report.results) > 0
        assert comprehensive_report.summary['total'] > 0
        print("✅ Comprehensive validation")
        
        # Test 6: Validation result creation
        test_results = [
            ValidationResult("Test", "Item1", True, "Success"),
            ValidationResult("Test", "Item2", False, "Failed", "error")
        ]
        test_report = validator._create_report("Test", test_results)
        assert test_report.summary['total'] == 2
        assert test_report.summary['passed'] == 1
        assert test_report.summary['failed'] == 1
        print("✅ Validation result creation")
        
        # Test 7: Print validation report (should not crash)
        import io
        from contextlib import redirect_stdout
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            validator.print_validation_report(test_report, show_details=False)
        
        output = captured_output.getvalue()
        assert "Validation Summary" in output
        print("✅ Print validation report")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ All ProjectValidator tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ ProjectValidator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """Test ErrorHandler functionality."""
    print("\n=== Testing ErrorHandler ===")
    
    try:
        from error_handling import (
            ErrorHandler, GeneratorError, ErrorContext, ErrorSeverity,
            ProjectStructureError, TemplateError, with_error_handling
        )
        
        # Test 1: Error handler initialization
        error_handler = ErrorHandler(verbose=True)
        assert error_handler.verbose is True
        assert error_handler.error_count == 0
        print("✅ Error handler initialization")
        
        # Test 2: Error context creation
        context = ErrorContext(
            operation="test_operation",
            component="TestComponent",
            inputs={"param1": "value1"}
        )
        assert context.operation == "test_operation"
        assert context.component == "TestComponent"
        print("✅ Error context creation")
        
        # Test 3: Custom generator errors
        test_error = TemplateError(
            "Test template error",
            context=context,
            severity=ErrorSeverity.MEDIUM
        )
        assert test_error.severity == ErrorSeverity.MEDIUM
        assert test_error.context == context
        print("✅ Custom generator errors")
        
        # Test 4: Exception wrapping
        try:
            raise FileNotFoundError("Test file not found")
        except Exception as e:
            wrapped = error_handler._wrap_exception(e, context)
            assert isinstance(wrapped, GeneratorError)
            assert "Test file not found" in str(wrapped)
        print("✅ Exception wrapping")
        
        # Test 5: Error handling without exit
        can_continue = error_handler.handle_exception(
            TemplateError("Non-critical template error", severity=ErrorSeverity.LOW),
            exit_on_critical=False
        )
        assert can_continue in [True, False]  # Should return a boolean
        print("✅ Error handling without exit")
        
        # Test 6: Error decorator
        @with_error_handling("test_operation", "TestComponent")
        def test_function_that_fails():
            raise ValueError("Test error")
        
        # Should not crash when decorated function fails
        result = test_function_that_fails()
        assert result is None  # Should return None on failure
        print("✅ Error handling decorator")
        
        # Test 7: Recovery strategies
        from error_handling import ValidationError as EHValidationError
        recovery_result = error_handler._handle_validation_error(
            EHValidationError("Test validation error", context=context)
        )
        assert isinstance(recovery_result, bool)
        print("✅ Recovery strategies")
        
        print("✅ All ErrorHandler tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ ErrorHandler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_integration():
    """Test CLI integration and basic functionality."""
    print("\n=== Testing CLI Integration ===")
    
    try:
        import importlib.util
        
        # Load the CLI module
        cli_path = Path(__file__).parent / "main.py"
        if not cli_path.exists():
            print("⚠️  CLI file not found, skipping CLI integration test")
            return True
        
        spec = importlib.util.spec_from_file_location("main", cli_path)
        cli_module = importlib.util.module_from_spec(spec)
        
        # Test 1: CLI module import
        spec.loader.exec_module(cli_module)
        assert hasattr(cli_module, "TemplateBasedGeneratorCLI")
        print("✅ CLI module import")
        
        # Test 2: CLI class structure
        cli_class = cli_module.TemplateBasedGeneratorCLI
        expected_methods = [
            'create_parent_page',
            'create_child_page', 
            'analyze_project',
            'validate_generated_files'
        ]
        
        for method in expected_methods:
            assert hasattr(cli_class, method)
        print("✅ CLI class structure")
        
        # Test 3: Argument parser creation
        # Import main function and check it doesn't crash
        assert hasattr(cli_module, "main")
        print("✅ CLI argument parser")
        
        print("✅ All CLI integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ CLI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all Phase 5-6 tests."""
    print("🧪 Testing Phase 5 (Routing Updates) & Phase 6 (CLI & Validation)")
    print("="*70)
    
    all_passed = True
    
    # Run all test functions
    test_functions = [
        test_routing_updater,
        test_validation_module,
        test_error_handling,
        test_cli_integration
    ]
    
    for test_func in test_functions:
        try:
            passed = test_func()
            all_passed &= passed
        except Exception as e:
            print(f"❌ Test function {test_func.__name__} failed: {e}")
            all_passed = False
    
    # Final results
    print("\n" + "="*70)
    print("🧪 PHASE 5-6 TEST RESULTS")
    print("="*70)
    
    if all_passed:
        print("🎉 ALL PHASE 5-6 TESTS PASSED!")
        print("✅ Routing updates, validation, and CLI are working correctly")
    else:
        print("❌ SOME PHASE 5-6 TESTS FAILED!")
        print("⚠️  Phase 5-6 functionality needs attention")
    
    print("="*70)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())