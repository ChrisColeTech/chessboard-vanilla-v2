#!/usr/bin/env python3
"""
Simple Phase 4 functionality test without pytest dependency.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

def test_wrapper_selector():
    """Test WrapperSelector functionality."""
    try:
        from config import PageConfig, ProjectCapabilities, WrapperType
        from wrapper_selector import WrapperSelector
        
        ws = WrapperSelector()
        
        print("=== Testing WrapperSelector ===")
        
        # Test 1: Full hooks wrapper selection
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=True, has_data_table=True)
        result = ws.select_wrapper_template(config, capabilities)
        assert result == WrapperType.FULL_HOOKS, f"Expected {WrapperType.FULL_HOOKS}, got {result}"
        print("✅ Full hooks wrapper selection")
        
        # Test 2: Basic hooks wrapper selection
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(has_page_hooks=True, has_mobile_hook=False, has_data_table=True)
        result = ws.select_wrapper_template(config, capabilities)
        assert result == WrapperType.BASIC_HOOKS, f"Expected {WrapperType.BASIC_HOOKS}, got {result}"
        print("✅ Basic hooks wrapper selection")
        
        # Test 3: No hooks wrapper selection
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(has_page_hooks=False, has_mobile_hook=False, has_data_table=False)
        result = ws.select_wrapper_template(config, capabilities)
        assert result == WrapperType.NO_HOOKS, f"Expected {WrapperType.NO_HOOKS}, got {result}"
        print("✅ No hooks wrapper selection")
        
        # Test 4: Wrapper validation
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(has_page_hooks=False, has_mobile_hook=False, has_data_table=False)
        wrapper_type = ws.select_wrapper_template(config, capabilities)
        issues = ws.validate_wrapper_selection(wrapper_type, config, capabilities)
        assert len(issues) > 0, "Expected validation issues for invalid config"
        print(f"✅ Validation found {len(issues)} issues (expected)")
        
        # Test 5: All wrapper types available
        all_types = ws.get_all_wrapper_types()
        expected_count = 4  # FULL_HOOKS, BASIC_HOOKS, NO_HOOKS, NO_MOBILE
        assert len(all_types) == expected_count, f"Expected {expected_count} wrapper types, got {len(all_types)}"
        print(f"✅ All {len(all_types)} wrapper types available")
        
        # Test 6: Wrapper descriptions
        for wrapper_type in all_types:
            desc = ws.get_wrapper_description(wrapper_type)
            assert desc != "Unknown wrapper type", f"No description for {wrapper_type}"
            assert len(desc) > 10, f"Description too short for {wrapper_type}: {desc}"
        print("✅ All wrapper types have descriptions")
        
        # Test 7: Recommendations
        capabilities_empty = ProjectCapabilities(has_page_hooks=False, has_mobile_hook=False, has_data_table=False)
        recommendations = ws.recommend_wrapper_upgrades(capabilities_empty)
        assert len(recommendations) == 3, f"Expected 3 recommendations, got {len(recommendations)}"
        print("✅ Upgrade recommendations working")
        
        print("✅ All WrapperSelector tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ WrapperSelector test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_page_config():
    """Test PageConfig functionality."""
    try:
        from config import PageConfig
        
        print("\n=== Testing PageConfig ===")
        
        # Test 1: Name normalization
        config1 = PageConfig(name="TestPage")
        assert config1.base_name == "Test", f"Expected 'Test', got '{config1.base_name}'"
        assert config1.page_name == "TestPage", f"Expected 'TestPage', got '{config1.page_name}'"
        print("✅ Name normalization with Page suffix")
        
        # Test 2: Name without Page suffix
        config2 = PageConfig(name="TestChild")
        assert config2.base_name == "TestChild", f"Expected 'TestChild', got '{config2.base_name}'"
        assert config2.page_name == "TestChildPage", f"Expected 'TestChildPage', got '{config2.page_name}'"
        print("✅ Name normalization without Page suffix")
        
        # Test 3: Parent and child IDs
        config3 = PageConfig(name="ChildTest", parent="ParentTest")
        assert config3.parent_id == "parenttest", f"Expected 'parenttest', got '{config3.parent_id}'"
        assert config3.page_id == "childtest", f"Expected 'childtest', got '{config3.page_id}'"
        print("✅ Parent and child ID generation")
        
        print("✅ All PageConfig tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ PageConfig test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all Phase 4 tests."""
    print("🧪 Running Phase 4 functionality tests...\n")
    
    all_passed = True
    
    # Test PageConfig
    all_passed &= test_page_config()
    
    # Test WrapperSelector  
    all_passed &= test_wrapper_selector()
    
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 All Phase 4 tests PASSED!")
        print("✅ Phase 4 implementation is working correctly")
    else:
        print("❌ Some Phase 4 tests FAILED!")
        print("⚠️  Phase 4 needs attention")
    print(f"{'='*50}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())