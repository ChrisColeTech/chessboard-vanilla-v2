#!/usr/bin/env python3
"""
Domain-Driven Frontend Generator V4
Refactored version using modular components for better maintainability
"""

import sys
from pathlib import Path

# Add the frontend-tools directory to the path
sys.path.append(str(Path(__file__).parent / "frontend-tools"))

from frontend_orchestrator import FrontendOrchestrator

class RefactoredFrontendGenerator:
    """
    Refactored frontend generator that uses modular components
    This is a lightweight wrapper around the FrontendOrchestrator
    """
    
    def __init__(self, frontend_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2"):
        self.orchestrator = FrontendOrchestrator(frontend_path)
    
    def generate_all_domains(self):
        """Generate all domain files following the architecture"""
        return self.orchestrator.generate_all_domains()
    
    def generate_specific_domain(self, domain: str):
        """Generate files for a specific domain only"""
        return self.orchestrator.generate_specific_domain(domain)
    
    def list_available_domains(self):
        """List all available domains"""
        return self.orchestrator.list_available_domains()
    
    def load_backend_config(self, config_path: str = "backend_config.json"):
        """Load backend configuration"""
        return self.orchestrator.load_backend_config(config_path)
    
    def generate_mobile_page(self, page_name: str, parent: str, icon: str = "Navigation", description: str = ""):
        """Generate mobile page variant with desktop/mobile switching support"""
        return self.orchestrator.dynamic_system_generator.generate_mobile_page_variant(page_name, parent, icon, description)

def main():
    """Main function to run the refactored generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Refactored Domain-Driven Frontend Generator V4')
    parser.add_argument('--domain', type=str, help='Generate specific domain only')
    parser.add_argument('--list', action='store_true', help='List available domains')
    parser.add_argument('--frontend-path', type=str, default="/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2", 
                       help='Path to frontend directory')
    
    args = parser.parse_args()
    
    generator = RefactoredFrontendGenerator(args.frontend_path)
    
    if args.list:
        generator.list_available_domains()
    elif args.domain:
        generator.generate_specific_domain(args.domain)
    else:
        generator.generate_all_domains()

if __name__ == "__main__":
    main()