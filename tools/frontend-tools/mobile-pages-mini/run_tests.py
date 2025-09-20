#!/usr/bin/env python3
"""
Test Runner for mobile-pages-v2 specialized modules.

Runs all unit tests and integration tests for the specialized modules.
"""

import sys
import subprocess
from pathlib import Path


def run_unit_tests():
    """Run all unit tests for specialized modules."""
    print("=" * 60)
    print("🧪 RUNNING UNIT TESTS")
    print("=" * 60)
    
    test_files = [
        "tests/test_action_registry_manager.py",
        "tests/test_container_integrator.py", 
        "tests/test_hook_integrator.py",
        # "tests/test_integration_validator.py",  # When implemented
    ]
    
    all_passed = True
    
    for test_file in test_files:
        test_path = Path(__file__).parent / test_file
        
        if not test_path.exists():
            print(f"⚠️  Test file not found: {test_file}")
            continue
        
        print(f"\n📋 Running: {test_file}")
        print("-" * 40)
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", str(test_path), "-v"
            ], cwd=Path(__file__).parent, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {test_file}: PASSED")
            else:
                print(f"❌ {test_file}: FAILED")
                print(f"STDOUT:\n{result.stdout}")
                print(f"STDERR:\n{result.stderr}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {test_file}: ERROR - {e}")
            all_passed = False
    
    return all_passed


def run_integration_tests():
    """Run integration tests using the orchestrator."""
    print("=" * 60)
    print("🔗 RUNNING INTEGRATION TESTS")
    print("=" * 60)
    
    # Test with the template-tests-v2/base-app project
    test_project = Path(__file__).parent.parent / "template-tests-v2/base-app"
    
    if not test_project.exists():
        print(f"⚠️  Test project not found: {test_project}")
        print("Skipping integration tests")
        return True
    
    orchestrator = Path(__file__).parent / "integration_orchestrator.py"
    
    try:
        result = subprocess.run([
            sys.executable, str(orchestrator), "test", str(test_project)
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Mobile Pages V2 - Specialized Modules Test Suite")
    
    # Run unit tests
    unit_success = run_unit_tests()
    
    # Run integration tests
    integration_success = run_integration_tests()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    print(f"Unit Tests: {'✅ PASSED' if unit_success else '❌ FAILED'}")
    print(f"Integration Tests: {'✅ PASSED' if integration_success else '❌ FAILED'}")
    
    overall_success = unit_success and integration_success
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()