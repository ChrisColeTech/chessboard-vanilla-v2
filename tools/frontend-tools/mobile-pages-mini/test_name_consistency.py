#!/usr/bin/env python3
"""
Test to reproduce and verify fix for name consistency issues in file generation.

The issue: When creating child pages with compound words like "ChessBoard",
the generator creates files with one casing but generates imports with different casing,
causing TypeScript compilation errors.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add the shared modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from name_standardizer import NameStandardizer

# Add the modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))
from config import PageConfig
from variable_generator import VariableGenerator

def test_name_consistency_issue():
    """Test to reproduce the name consistency issue."""
    print("🧪 Testing name consistency issue reproduction...")
    
    # Test cases that commonly cause issues
    test_cases = [
        ("ChessBoard", "gamehub"),
        ("ScoreBoard", "gamehub"), 
        ("DataTest", "testsection"),
        ("LayoutTest", "testsection"),
        ("UserProfile", "settings"),
        ("GameRoom", "lobby")
    ]
    
    variable_generator = VariableGenerator()
    
    for child_name, parent_name in test_cases:
        print(f"\n📝 Testing: {child_name} (parent: {parent_name})")
        
        # Create page config as the system would
        child_config = PageConfig(name=child_name, parent=parent_name)
        
        print(f"   Original name: {child_name}")
        print(f"   PageConfig.base_name: {child_config.base_name}")
        print(f"   PageConfig.page_id: {child_config.page_id}")
        
        # Test what the variable generator would produce
        wrapper_name = f"{NameStandardizer.to_pascal_case(child_config.base_name)}PageWrapper"
        import_path_name = f"{NameStandardizer.to_pascal_case(child_config.base_name)}PageWrapper"
        
        print(f"   Generated wrapper_name: {wrapper_name}")
        print(f"   Generated import path: {import_path_name}")
        
        # Expected file name (what actually gets created)
        expected_file_name = f"{child_config.page_name}Wrapper.tsx"  # This would be "ChessBoardPageWrapper.tsx"
        
        print(f"   Expected file name: {expected_file_name}")
        
        # Check if there's a mismatch
        if wrapper_name != expected_file_name.replace('.tsx', ''):
            print(f"   ❌ MISMATCH DETECTED!")
            print(f"      Import expects: {wrapper_name}")
            print(f"      File created as: {expected_file_name.replace('.tsx', '')}")
            return False
        else:
            print(f"   ✅ Names match")
    
    print("\n✅ All test cases passed - no issues detected")
    return True

def test_routing_variables_consistency():
    """Test the specific method that generates routing variables."""
    print("\n🧪 Testing routing variables consistency...")
    
    # Create test configs similar to what we have in our failing case
    test_configs = [
        PageConfig(name="ChessBoard", parent="gamehub"),
        PageConfig(name="ScoreBoard", parent="gamehub")
    ]
    
    variable_generator = VariableGenerator()
    
    # Test the routing variables generation
    routing_vars = variable_generator.generate_routing_variables(test_configs)
    
    print("Generated CHILD_IMPORTS:")
    print(routing_vars['CHILD_IMPORTS'])
    print("\nGenerated CHILD_ROUTING_LOGIC:")
    print(routing_vars['CHILD_ROUTING_LOGIC'])
    
    # Check for consistency
    imports = routing_vars['CHILD_IMPORTS']
    routing = routing_vars['CHILD_ROUTING_LOGIC']
    
    # Extract component names from imports and routing
    import_names = []
    routing_names = []
    
    for line in imports.split('\n'):
        if 'import {' in line and 'PageWrapper' in line:
            # Extract the component name between { and }
            start = line.find('{') + 1
            end = line.find('}')
            if start > 0 and end > start:
                import_names.append(line[start:end].strip())
    
    for line in routing.split('\n'):
        if 'CurrentPageComponent =' in line and 'PageWrapper' in line:
            # Extract the component name after =
            parts = line.split('=')
            if len(parts) > 1:
                routing_names.append(parts[1].strip().rstrip(';'))
    
    print(f"\nImport component names: {import_names}")
    print(f"Routing component names: {routing_names}")
    
    # Check if they match
    mismatches = []
    for imp_name, rout_name in zip(import_names, routing_names):
        if imp_name != rout_name:
            mismatches.append((imp_name, rout_name))
    
    if mismatches:
        print(f"❌ MISMATCHES FOUND: {mismatches}")
        return False
    else:
        print("✅ Import and routing names are consistent")
        return True

def test_actual_file_vs_import_naming():
    """Test the actual file naming vs import naming issue."""
    print("\n🧪 Testing actual file vs import naming...")
    
    # Simulate what happens in the real system
    child_config = PageConfig(name="ChessBoard", parent="gamehub")
    
    print(f"Input name: 'ChessBoard'")
    print(f"PageConfig.base_name: '{child_config.base_name}'")
    print(f"PageConfig.page_name: '{child_config.page_name}'")
    
    # What the file would be named (from child generator)
    actual_file_name = f"{child_config.page_name}Wrapper"  # "ChessBoardPageWrapper"
    
    # What the import would reference (from variable generator)
    import_name = f"{NameStandardizer.to_pascal_case(child_config.base_name)}PageWrapper"
    
    print(f"Actual file name: '{actual_file_name}'")
    print(f"Import references: '{import_name}'")
    
    if actual_file_name == import_name:
        print("✅ File name and import name match")
        return True
    else:
        print("❌ MISMATCH: File name and import name don't match!")
        print(f"   This would cause: 'File name differs only in casing' error")
        return False

if __name__ == "__main__":
    print("🚀 Running name consistency tests...\n")
    
    # Run all tests
    test1_passed = test_name_consistency_issue()
    test2_passed = test_routing_variables_consistency() 
    test3_passed = test_actual_file_vs_import_naming()
    
    print(f"\n📊 Test Results:")
    print(f"   Name consistency test: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   Routing variables test: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"   File vs import naming test: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    
    if all([test1_passed, test2_passed, test3_passed]):
        print("\n🎉 ALL TESTS PASSED - No naming consistency issues detected!")
        sys.exit(0)
    else:
        print("\n💥 TESTS FAILED - Naming consistency issues detected!")
        sys.exit(1)