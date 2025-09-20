#!/usr/bin/env python3
"""
Build Issues Reproduction Test Suite
=====================================

This script reproduces each build error found in the TypeScript compilation,
tests the fixes, and validates that all issues are resolved.

Build Errors Found:
1. App.tsx missing children property (AppLayout expects children)
2. Hook import/export casing mismatches (useTestcenterActions vs useTestCenterActions)
3. Hook file casing conflicts (useGameCenterActions.ts vs useGamecenterActions.ts)
4. Component import/export casing mismatches (PlayareaPageWrapper vs PlayAreaPageWrapper)
"""

import subprocess
import sys
import os
from pathlib import Path
import json
import re

class BuildIssuesTester:
    def __init__(self, frontend_root: str):
        self.frontend_root = Path(frontend_root)
        self.src_dir = self.frontend_root / "src"
        
    def run_build_test(self) -> tuple[bool, str]:
        """Run TypeScript build and capture errors."""
        try:
            result = subprocess.run(
                ["npm", "run", "build"], 
                cwd=self.frontend_root,
                capture_output=True, 
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Build timed out after 60 seconds"
        except Exception as e:
            return False, f"Build failed with exception: {e}"

    def test_issue_1_app_children_property(self) -> dict:
        """Test Issue 1: App.tsx missing children property"""
        print("🧪 Testing Issue 1: App.tsx missing children property")
        
        app_tsx = self.src_dir / "App.tsx"
        if not app_tsx.exists():
            return {"status": "FAIL", "error": "App.tsx not found"}
        
        content = app_tsx.read_text()
        
        # Check if AppLayout has children
        has_children_prop = "children" in content and "<AppLayout" in content
        has_page_routing = "selectedTab ===" in content or "switch" in content
        has_placeholder_comment = "Page routing - generated pages will be added here" in content
        
        issues = []
        if not has_children_prop:
            issues.append("AppLayout missing children prop")
        if has_placeholder_comment:
            issues.append("Contains placeholder routing comment instead of actual routing")
        if not has_page_routing:
            issues.append("No page routing logic found")
            
        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "has_children": has_children_prop,
            "has_routing": has_page_routing,
            "has_placeholder": has_placeholder_comment
        }

    def test_issue_2_hook_import_export_casing(self) -> dict:
        """Test Issue 2: Hook import/export casing mismatches"""
        print("🧪 Testing Issue 2: Hook import/export casing mismatches")
        
        action_sheet = self.src_dir / "components/action-sheet/ActionSheetContainer.tsx"
        if not action_sheet.exists():
            return {"status": "FAIL", "error": "ActionSheetContainer.tsx not found"}
        
        content = action_sheet.read_text()
        issues = []
        
        # Check for specific casing mismatches found in build
        if "useTestcenterActions" in content:
            issues.append("Found 'useTestcenterActions' - should be 'useTestCenterActions'")
        if "useGamecenterActions" in content:
            issues.append("Found 'useGamecenterActions' - should be 'useGameCenterActions'")
            
        # Check import paths vs hook names
        import_pattern = r'import\s*{\s*([^}]+)\s*}\s*from\s*["\']([^"\']+)["\']'
        imports = re.findall(import_pattern, content)
        
        for hook_names, import_path in imports:
            if "/hooks/" in import_path:
                hook_list = [h.strip() for h in hook_names.split(',')]
                for hook_name in hook_list:
                    # Check if hook name matches path casing expectations
                    if "testcenter" in import_path.lower() and hook_name == "useTestcenterActions":
                        issues.append(f"Casing mismatch: {hook_name} from {import_path}")
                    if "gamecenter" in import_path.lower() and hook_name == "useGamecenterActions":
                        issues.append(f"Casing mismatch: {hook_name} from {import_path}")
        
        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "imports_found": imports
        }

    def test_issue_3_hook_file_casing_conflicts(self) -> dict:
        """Test Issue 3: Hook file casing conflicts"""
        print("🧪 Testing Issue 3: Hook file casing conflicts")
        
        issues = []
        conflicting_files = []
        
        # Check for conflicting hook files
        hooks_dirs = [
            self.src_dir / "hooks/testcenter",
            self.src_dir / "hooks/gamecenter"
        ]
        
        for hooks_dir in hooks_dirs:
            if hooks_dir.exists():
                files = list(hooks_dir.glob("*.ts"))
                file_names_lower = {}
                
                for file in files:
                    lower_name = file.name.lower()
                    if lower_name in file_names_lower:
                        conflicting_files.append({
                            "file1": str(file_names_lower[lower_name]),
                            "file2": str(file),
                            "conflict": "Case-only difference"
                        })
                        issues.append(f"Conflicting files: {file_names_lower[lower_name]} vs {file}")
                    else:
                        file_names_lower[lower_name] = file
        
        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "conflicting_files": conflicting_files
        }

    def test_issue_4_component_import_export_casing(self) -> dict:
        """Test Issue 4: Component import/export casing mismatches"""
        print("🧪 Testing Issue 4: Component import/export casing mismatches")
        
        gamecenter_page = self.src_dir / "pages/gamecenter/GameCenterPage.tsx"
        if not gamecenter_page.exists():
            return {"status": "FAIL", "error": "GameCenterPage.tsx not found"}
        
        content = gamecenter_page.read_text()
        issues = []
        
        # Check for specific issues found in build
        problematic_imports = [
            "GamecenterPageWrapper",
            "GamecentermainPageWrapper",
            "PlayareaPageWrapper"
        ]
        
        for import_name in problematic_imports:
            if import_name in content:
                issues.append(f"Found problematic import: {import_name}")
        
        # Check if corresponding files exist
        component_dir = self.src_dir / "components/gamecenter"
        if component_dir.exists():
            existing_files = [f.stem for f in component_dir.glob("*.tsx")]
            
            # Check for casing mismatches between imports and files
            import_pattern = r'import\s*{\s*([^}]+)\s*}\s*from\s*["\']([^"\']+)["\']'
            imports = re.findall(import_pattern, content)
            
            for import_names, import_path in imports:
                if "gamecenter" in import_path.lower():
                    import_list = [i.strip() for i in import_names.split(',')]
                    for import_name in import_list:
                        # Check if file exists with different casing
                        expected_file = import_name + "PageWrapper"
                        if expected_file not in existing_files:
                            # Look for case variants
                            lower_variants = [f for f in existing_files if f.lower() == expected_file.lower()]
                            if lower_variants:
                                issues.append(f"Import '{import_name}' doesn't match file '{lower_variants[0]}'")
        
        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues
        }

    def run_comprehensive_test(self) -> dict:
        """Run all tests and generate comprehensive report"""
        print("🚀 Running Build Issues Reproduction Test Suite")
        print("=" * 60)
        
        # First, run build to capture current state
        build_success, build_errors = self.run_build_test()
        
        results = {
            "build_success": build_success,
            "build_errors": build_errors,
            "tests": {}
        }
        
        # Run individual tests
        results["tests"]["issue_1"] = self.test_issue_1_app_children_property()
        results["tests"]["issue_2"] = self.test_issue_2_hook_import_export_casing()
        results["tests"]["issue_3"] = self.test_issue_3_hook_file_casing_conflicts()
        results["tests"]["issue_4"] = self.test_issue_4_component_import_export_casing()
        
        # Summary
        total_tests = len(results["tests"])
        passed_tests = sum(1 for test in results["tests"].values() if test["status"] == "PASS")
        
        results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "all_passed": passed_tests == total_tests
        }
        
        print(f"\n📊 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        print(f"   Build Success: {build_success}")
        
        return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_build_issues.py <frontend_root>")
        sys.exit(1)
    
    frontend_root = sys.argv[1]
    if not Path(frontend_root).exists():
        print(f"Error: Frontend root '{frontend_root}' does not exist")
        sys.exit(1)
    
    tester = BuildIssuesTester(frontend_root)
    results = tester.run_comprehensive_test()
    
    # Save results to JSON for analysis
    results_file = Path(frontend_root) / "build_issues_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Exit with error code if tests failed or build failed
    if not results["summary"]["all_passed"] or not results["build_success"]:
        sys.exit(1)

if __name__ == "__main__":
    main()