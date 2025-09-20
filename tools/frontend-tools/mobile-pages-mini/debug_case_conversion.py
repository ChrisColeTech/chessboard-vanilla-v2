#!/usr/bin/env python3
"""
Debug script to trace where APITester becomes ApiTester in the generation pipeline.
"""

import sys
from pathlib import Path
import tempfile
import os

# Add directories to path so we can import shared modules
parent_dir = Path(__file__).parent.parent.parent
shared_dir = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(shared_dir))

from modules.config import PageConfig
from modules.variable_generator import VariableGenerator
from page_config_manager import PageConfigManager, PageInfo

def test_name_conversion():
    """Test name conversion at each step."""
    print("=== DEBUG: Multiple Name Conversion ===")
    
    # Test problematic names
    test_names = ["HTTPTracker", "JSONValidator", "APIClient", "TestRunner"]
    
    for test_name in test_names:
        print(f"\n=== Testing: {test_name} ===")
        
        # Step 1: Test PageConfig creation
        print("\n1. Direct PageConfig Creation:")
        config = PageConfig(name=test_name, parent="Tools")
        print(f"   Input name: '{test_name}'")
        print(f"   config.name: '{config.name}'")
        print(f"   config.base_name: '{config.base_name}'")
        print(f"   config.page_name: '{config.page_name}'")
        print(f"   config.page_id: '{config.page_id}'")
    
    # Step 2: Test PageConfigManager storage/retrieval
    print("\n2. PageConfigManager Storage/Retrieval:")
    with tempfile.TemporaryDirectory() as temp_dir:
        config_manager = PageConfigManager(temp_dir)
        
        # Simulate the preregistration process
        child_info = PageInfo(
            id="APITester".lower(),  # This becomes "apitester"
            name="APITester",        # Original name
            type="child",
            parent_id="tools",
            has_mobile=True
        )
        config_manager.add_page(child_info)
        print(f"   Stored PageInfo.name: '{child_info.name}'")
        print(f"   Stored PageInfo.id: '{child_info.id}'")
        
        # Retrieve children and convert to PageConfig
        children_info = config_manager.get_children_for_parent("tools")
        if children_info:
            retrieved_child = children_info[0]
            print(f"   Retrieved child_info.name: '{retrieved_child.name}'")
            print(f"   Retrieved child_info.id: '{retrieved_child.id}'")
            
            # Convert to PageConfig (like the generator does)
            converted_config = PageConfig(
                name=retrieved_child.name,
                parent="tools",
                mobile=retrieved_child.has_mobile
            )
            print(f"   Converted config.name: '{converted_config.name}'")
            print(f"   Converted config.base_name: '{converted_config.base_name}'")
    
    # Step 3: Test variable generation
    print("\n3. Variable Generation:")
    var_gen = VariableGenerator()
    
    # Simulate how routing variables are generated
    wrapper_name = f"{config.base_name}PageWrapper"
    import_path = f"../../components/{config.parent_id}/{config.base_name}PageWrapper"
    
    print(f"   wrapper_name: '{wrapper_name}'")
    print(f"   import_path: '{import_path}'")
    
    # Step 4: Test routing generation with list
    print("\n4. Routing Generation:")
    routing_vars = var_gen.generate_routing_variables([config])
    print(f"   CHILD_IMPORTS:")
    print(f"   {routing_vars['CHILD_IMPORTS']}")
    print(f"   CHILD_ROUTING_LOGIC:")
    print(f"   {routing_vars['CHILD_ROUTING_LOGIC']}")

if __name__ == "__main__":
    test_name_conversion()