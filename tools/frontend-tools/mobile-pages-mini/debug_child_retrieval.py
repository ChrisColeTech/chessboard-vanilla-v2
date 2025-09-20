#!/usr/bin/env python3
"""
Debug script to trace child retrieval and PageConfig conversion.
"""

import sys
import tempfile
from pathlib import Path

# Add directories to path
parent_dir = Path(__file__).parent.parent.parent
shared_dir = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(shared_dir))

from modules.config import PageConfig, GenerationContext, ProjectCapabilities
from modules.variable_generator import VariableGenerator
from page_config_manager import PageConfigManager, PageInfo

def debug_child_retrieval():
    """Debug the exact child retrieval process."""
    print("=== DEBUG: Child Retrieval Process ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_manager = PageConfigManager(temp_dir)
        
        # 1. Simulate preregistration (what main.py does)
        print("\n1. Preregistration Process:")
        child_name = "APITester"
        parent_name = "Tools"
        
        child_info = PageInfo(
            id=child_name.lower(),  # "apitester"
            name=child_name,        # "APITester"
            type="child",
            parent_id=parent_name.lower(),  # "tools"
            has_mobile=True
        )
        config_manager.add_page(child_info)
        print(f"   Stored PageInfo: id='{child_info.id}', name='{child_info.name}'")
        
        # 2. Simulate parent generation (what _get_existing_children does)
        print("\n2. Child Retrieval Process:")
        children_info = config_manager.get_children_for_parent("tools")
        print(f"   Retrieved {len(children_info)} children")
        
        if children_info:
            retrieved_child = children_info[0]
            print(f"   Retrieved PageInfo: id='{retrieved_child.id}', name='{retrieved_child.name}'")
            
            # 3. Convert to PageConfig (the critical step)
            print("\n3. PageConfig Conversion:")
            child_config = PageConfig(
                name=retrieved_child.name,  # This should be "APITester"
                parent="tools",
                mobile=retrieved_child.has_mobile
            )
            print(f"   PageConfig: name='{child_config.name}', base_name='{child_config.base_name}'")
            
            # 4. Generate routing variables
            print("\n4. Routing Variable Generation:")
            var_gen = VariableGenerator()
            routing_vars = var_gen.generate_routing_variables([child_config])
            
            print(f"   Generated import:")
            print(f"   {routing_vars['CHILD_IMPORTS']}")
            print(f"   Generated routing:")
            print(f"   {routing_vars['CHILD_ROUTING_LOGIC']}")

if __name__ == "__main__":
    debug_child_retrieval()