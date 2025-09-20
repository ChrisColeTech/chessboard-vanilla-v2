#!/usr/bin/env python3
"""
Debug script to trace exact PageConfig processing of problematic names.
"""

import sys
import tempfile
from pathlib import Path

# Add directories to path
parent_dir = Path(__file__).parent.parent.parent
shared_dir = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(shared_dir))

from modules.config import PageConfig
from page_config_manager import PageConfigManager, PageInfo

def debug_pageconfig_processing():
    """Debug the exact PageConfig processing."""
    print("=== DEBUG: PageConfig Processing ===")
    
    # Test the exact scenario from pages.config.json
    problematic_names = [
        ("HTTPTracker", "httptracker"),
        ("JSONValidator", "jsonvalidator"), 
        ("APIClient", "apiclient"),
        ("TestRunner", "testrunner")
    ]
    
    for name, page_id in problematic_names:
        print(f"\n=== Testing: {name} ===")
        
        # Simulate what _get_existing_children does
        print(f"1. Input from pages.config.json:")
        print(f"   name: '{name}'")
        print(f"   id: '{page_id}'")
        
        # Create PageConfig exactly as _get_existing_children does
        child_config = PageConfig(
            name=name,  # This is what comes from child_info.name
            parent="analytics",
            mobile=True,
            description=""
        )
        
        print(f"2. After PageConfig processing:")
        print(f"   config.name: '{child_config.name}'")
        print(f"   config.base_name: '{child_config.base_name}'")
        print(f"   config.page_name: '{child_config.page_name}'")
        print(f"   config.page_id: '{child_config.page_id}'")
        
        # Test what generate_routing_variables would create
        wrapper_name = f"{child_config.base_name}PageWrapper"
        import_statement = f'import {{ {wrapper_name} }} from "../../components/analytics/{child_config.base_name}PageWrapper";'
        
        print(f"3. Generated import statement:")
        print(f"   {import_statement}")

if __name__ == "__main__":
    debug_pageconfig_processing()