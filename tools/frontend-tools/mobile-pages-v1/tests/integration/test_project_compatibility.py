#!/usr/bin/env python3
"""
Integration tests for project compatibility and migration scenarios.
Tests generator behavior with different project structures and configurations.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../shared'))

def test_legacy_project_compatibility():
    """Test generator behavior with legacy project structures."""
    print("\n=== Testing Legacy Project Compatibility ===")
    
    try:
        from main import TemplateBasedGeneratorCLI
        
        # Setup legacy project structure (no hooks, basic React)
        temp_dir = Path(tempfile.mkdtemp())
        src_dir = temp_dir / "src"
        (src_dir / "pages").mkdir(parents=True)
        (src_dir / "components").mkdir(parents=True)
        (temp_dir / "package.json").write_text('{"name": "legacy-project"}')
        
        # Create some legacy pages without hooks
        dashboard_dir = src_dir / "pages" / "dashboard"
        dashboard_dir.mkdir(parents=True)
        (dashboard_dir / "DashboardPage.jsx").write_text("""
import React from 'react';

export default function DashboardPage() {
  return <div>Legacy Dashboard</div>;
}
        """)
        
        # Initialize CLI
        cli = TemplateBasedGeneratorCLI(str(temp_dir))
        
        # Test 1: Analyze legacy project
        capabilities = cli.project_detector.detect_capabilities()
        
        # Should detect no advanced capabilities
        assert capabilities.has_page_hooks == False, "Should not detect hooks in legacy project"
        assert capabilities.has_mobile_hook == False, "Should not detect mobile hook in legacy project"
        assert len(capabilities.existing_parents) == 1, "Should detect Dashboard parent"
        assert "dashboard" in capabilities.existing_parents, "Should detect dashboard parent"
        
        # Test 2: Generate child page in legacy project (should use no-hooks template)
        cli.create_child_page("Reports", "Dashboard")
        
        # Verify wrapper uses appropriate template (no hooks)
        wrapper_path = src_dir / "components" / "dashboard" / "ReportsWrapper.tsx"
        assert wrapper_path.exists(), "Wrapper should be created for legacy project"
        
        wrapper_content = wrapper_path.read_text()
        assert "usePageInstructions" not in wrapper_content, "Should not use hooks in legacy project"
        assert "usePageActions" not in wrapper_content, "Should not use hooks in legacy project"
        
        print("✅ Legacy project compatibility")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Legacy project compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mixed_capability_project():
    """Test generator behavior with projects that have some but not all capabilities."""
    print("\n=== Testing Mixed Capability Project ===")
    
    try:
        from main import TemplateBasedGeneratorCLI
        
        # Setup project with only page hooks, no mobile hook
        temp_dir = Path(tempfile.mkdtemp())
        src_dir = temp_dir / "src"
        (src_dir / "pages").mkdir(parents=True)
        (src_dir / "components").mkdir(parents=True)
        (src_dir / "hooks" / "core").mkdir(parents=True)
        (temp_dir / "package.json").write_text('{"name": "mixed-project"}')
        
        # Create page hooks but not mobile hook
        core_hooks = src_dir / "hooks" / "core"
        (core_hooks / "usePageInstructions.ts").write_text("export const usePageInstructions = () => {};")
        (core_hooks / "usePageActions.ts").write_text("export const usePageActions = () => {};")
        # Deliberately omit useIsMobile.ts
        
        # Initialize CLI
        cli = TemplateBasedGeneratorCLI(str(temp_dir))
        
        # Test capability detection
        capabilities = cli.project_detector.detect_capabilities()
        assert capabilities.has_page_hooks == True, "Should detect page hooks"
        assert capabilities.has_mobile_hook == False, "Should not detect mobile hook"
        
        # Create parent page
        cli.create_parent_page("Settings")
        
        # Create child page
        cli.create_child_page("UserProfile", "Settings")
        
        # Verify wrapper uses basic hooks template (has page hooks but no mobile)
        wrapper_path = src_dir / "components" / "settings" / "UserProfileWrapper.tsx"
        assert wrapper_path.exists(), "Wrapper should be created"
        
        wrapper_content = wrapper_path.read_text()
        assert "usePageInstructions" in wrapper_content, "Should use page hooks"
        assert "usePageActions" in wrapper_content, "Should use page hooks"
        assert "useIsMobile" not in wrapper_content, "Should not use mobile hook when not available"
        
        print("✅ Mixed capability project")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Mixed capability project test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_existing_project_structure_preservation():
    """Test that generator preserves existing project structure and files."""
    print("\n=== Testing Existing Project Structure Preservation ===")
    
    try:
        from main import TemplateBasedGeneratorCLI
        
        # Setup project with existing structure
        temp_dir = Path(tempfile.mkdtemp())
        src_dir = temp_dir / "src"
        (src_dir / "pages").mkdir(parents=True)
        (src_dir / "components").mkdir(parents=True)
        (src_dir / "hooks" / "core").mkdir(parents=True)
        (temp_dir / "package.json").write_text('{"name": "existing-project"}')
        
        # Create existing files with custom content
        settings_dir = src_dir / "pages" / "settings"
        settings_dir.mkdir(parents=True)
        
        existing_file = settings_dir / "SettingsPage.tsx"
        original_content = """import React from 'react';
import { CustomComponent } from '../custom';

// This is custom content that should be preserved
const SettingsPage = () => {
  return (
    <div>
      <h1>Custom Settings</h1>
      <CustomComponent />
    </div>
  );
};

export default SettingsPage;"""
        
        existing_file.write_text(original_content)
        
        # Create hooks
        core_hooks = src_dir / "hooks" / "core"
        (core_hooks / "usePageInstructions.ts").write_text("export const usePageInstructions = () => {};")
        (core_hooks / "usePageActions.ts").write_text("export const usePageActions = () => {};")
        (core_hooks / "useIsMobile.ts").write_text("export const useIsMobile = () => {};")
        
        # Initialize CLI
        cli = TemplateBasedGeneratorCLI(str(temp_dir))
        
        # Add a child page - this should not overwrite the existing SettingsPage
        cli.create_child_page("UserProfile", "Settings")
        
        # Verify existing file was not overwritten
        preserved_content = existing_file.read_text()
        assert "CustomComponent" in preserved_content, "Existing custom content should be preserved"
        assert "Custom Settings" in preserved_content, "Existing custom content should be preserved"
        
        # But should have routing injection markers added
        assert "UserProfileWrapper" in preserved_content, "Routing should be injected"
        
        # Verify new files were created
        child_file = settings_dir / "UserProfilePage.tsx"
        assert child_file.exists(), "Child page should be created"
        
        wrapper_file = src_dir / "components" / "settings" / "UserProfileWrapper.tsx"
        assert wrapper_file.exists(), "Wrapper should be created"
        
        print("✅ Existing project structure preservation")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Existing project structure preservation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complex_project_hierarchy():
    """Test generator with complex nested project hierarchies.""" 
    print("\n=== Testing Complex Project Hierarchy ===")
    
    try:
        from main import TemplateBasedGeneratorCLI
        
        # Setup complex project structure
        temp_dir = Path(tempfile.mkdtemp())
        src_dir = temp_dir / "src"
        (src_dir / "pages").mkdir(parents=True)
        (src_dir / "components").mkdir(parents=True)
        (src_dir / "hooks" / "core").mkdir(parents=True)
        (temp_dir / "package.json").write_text('{"name": "complex-project"}')
        
        # Create hooks
        core_hooks = src_dir / "hooks" / "core"
        (core_hooks / "usePageInstructions.ts").write_text("export const usePageInstructions = () => {};")
        (core_hooks / "usePageActions.ts").write_text("export const usePageActions = () => {};")
        (core_hooks / "useIsMobile.ts").write_text("export const useIsMobile = () => {};")
        
        # Initialize CLI
        cli = TemplateBasedGeneratorCLI(str(temp_dir))
        
        # Create multiple parent pages
        parents = ["Dashboard", "Settings", "Reports", "Admin"]
        for parent in parents:
            cli.create_parent_page(parent)
        
        # Create multiple children for each parent
        parent_children = {
            "Dashboard": ["Overview", "Analytics", "Metrics"],
            "Settings": ["UserProfile", "Security", "Preferences", "Billing"],  
            "Reports": ["Monthly", "Quarterly", "Annual"],
            "Admin": ["Users", "Permissions", "Audit"]
        }
        
        for parent, children in parent_children.items():
            for child in children:
                cli.create_child_page(child, parent)
        
        # Verify all structure was created correctly
        for parent in parents:
            parent_dir = src_dir / "pages" / parent.lower()
            assert parent_dir.exists(), f"{parent} directory should exist"
            
            parent_file = parent_dir / f"{parent}Page.tsx"
            assert parent_file.exists(), f"{parent} page should exist"
            
            # Verify all children are in parent routing
            parent_content = parent_file.read_text()
            for child in parent_children[parent]:
                assert f"{child}Wrapper" in parent_content, f"{child} should be in {parent} routing"
                assert child.lower() in parent_content, f"{child} route should be in {parent} routing"
        
        # Verify project analysis works with complex structure
        import io
        from contextlib import redirect_stdout
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            cli.analyze_project()
        
        output = captured_output.getvalue()
        
        # Should detect all parents and children
        for parent in parents:
            assert parent in output, f"Should detect {parent} in analysis"
        
        total_children = sum(len(children) for children in parent_children.values())
        assert f"Total Children: {total_children}" in output, f"Should detect {total_children} total children"
        
        print("✅ Complex project hierarchy")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Complex project hierarchy test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation_integration():
    """Test comprehensive validation integration."""
    print("\n=== Testing Validation Integration ===")
    
    try:
        from main import TemplateBasedGeneratorCLI
        from modules.validation import ProjectValidator
        
        # Setup project
        temp_dir = Path(tempfile.mkdtemp())
        templates_dir = Path(__file__).parent.parent.parent / "templates"
        src_dir = temp_dir / "src"
        (src_dir / "pages").mkdir(parents=True)
        (src_dir / "components").mkdir(parents=True)
        (src_dir / "hooks" / "core").mkdir(parents=True)
        (temp_dir / "package.json").write_text('{"name": "validation-test"}')
        
        # Create hooks
        core_hooks = src_dir / "hooks" / "core"
        (core_hooks / "usePageInstructions.ts").write_text("export const usePageInstructions = () => {};")
        (core_hooks / "usePageActions.ts").write_text("export const usePageActions = () => {};")
        (core_hooks / "useIsMobile.ts").write_text("export const useIsMobile = () => {};")
        
        # Initialize validator
        validator = ProjectValidator(temp_dir, templates_dir)
        
        # Test 1: Run comprehensive validation on fresh project
        report = validator.run_comprehensive_validation()
        
        # Should pass basic structure validation
        structure_issues = validator.get_validation_issues(report, "error")
        assert len(structure_issues) == 0, f"Should not have structure errors: {structure_issues}"
        
        # Test 2: Generate pages and validate
        cli = TemplateBasedGeneratorCLI(str(temp_dir))
        cli.create_parent_page("Dashboard")
        cli.create_child_page("Analytics", "Dashboard")
        
        # Run validation again
        report = validator.run_comprehensive_validation()
        
        # Should still pass
        critical_issues = validator.get_validation_issues(report, "error")
        assert len(critical_issues) == 0, f"Should not have critical issues after generation: {critical_issues}"
        
        # Test 3: CLI validation command
        import io
        from contextlib import redirect_stdout
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            cli.validate_generated_files()
        
        output = captured_output.getvalue()
        assert "dependencies are available" in output, "Validation should report dependency status"
        
        print("✅ Validation integration")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Validation integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all project compatibility tests."""
    print("🧪 Running Integration Tests - Project Compatibility")
    print("=" * 70)
    
    all_passed = True
    
    # Run all test functions
    test_functions = [
        test_legacy_project_compatibility,
        test_mixed_capability_project,
        test_existing_project_structure_preservation,
        test_complex_project_hierarchy,
        test_validation_integration
    ]
    
    for test_func in test_functions:
        try:
            passed = test_func()
            all_passed &= passed
        except Exception as e:
            print(f"❌ Test function {test_func.__name__} failed: {e}")
            all_passed = False
    
    # Final results
    print("\n" + "=" * 70)
    print("🧪 PROJECT COMPATIBILITY TEST RESULTS")
    print("=" * 70)
    
    if all_passed:
        print("🎉 ALL PROJECT COMPATIBILITY TESTS PASSED!")
        print("✅ Generator works correctly with various project types")
    else:
        print("❌ SOME PROJECT COMPATIBILITY TESTS FAILED!")
        print("⚠️  Project compatibility needs attention")
    
    print("=" * 70)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())