#!/usr/bin/env python3
"""
Frontend Orchestrator
Main orchestrator class that coordinates all generators
"""

from pathlib import Path
from base_generator import BaseFrontendGenerator
from domain_mapping import DomainMapping
from types_generator import TypesGenerator
from services_generator import ServicesGenerator
from hooks_generator import HooksGenerator
from components_generator import ComponentsGenerator
from clients_generator import ClientsGenerator
from stores_generator import StoresGenerator
from pages_generator import PagesGenerator
from layout_generator import LayoutGenerator

class FrontendOrchestrator(BaseFrontendGenerator):
    """Main orchestrator that coordinates all frontend generation"""
    
    def __init__(self, frontend_path: str = "../frontend-v2"):
        super().__init__(frontend_path)
        self.domain_mapping = DomainMapping()
        
        # Initialize all generators
        self.types_generator = TypesGenerator(frontend_path)
        self.services_generator = ServicesGenerator(frontend_path)
        self.hooks_generator = HooksGenerator(frontend_path)
        self.components_generator = ComponentsGenerator(frontend_path)
        self.clients_generator = ClientsGenerator(frontend_path)
        self.stores_generator = StoresGenerator(frontend_path)
        self.pages_generator = PagesGenerator(frontend_path)
        self.layout_generator = LayoutGenerator(frontend_path)
    
    def create_directory_structure(self):
        """Create domain-driven directory structure"""
        src_path = self.get_src_path()
        
        # Get all directories from domain mapping
        directories = self.domain_mapping.get_directory_structure()
        
        for directory in directories:
            (src_path / directory).mkdir(parents=True, exist_ok=True)
        
        print("📁 Created domain-driven directory structure")
    
    def generate_all_domains(self):
        """Generate all domain files following the architecture"""
        print("🚀 Domain-Driven Frontend Generator Starting...")
        
        # Load backend configuration
        self.load_backend_config()
        
        # Share backend config with all generators
        self._share_backend_config()
        
        # Create directory structure
        self.create_directory_structure()
        
        # Generate common types first
        self.types_generator.generate_common_types()
        
        # Group endpoints by domain
        domains = self.domain_mapping.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        print(f"📊 Organized {len(self.backend_config['endpoints'])} endpoints into {len(domains)} domains")
        
        # Generate files for each domain following priority order
        for domain, endpoints in domains.items():
            print(f"🔧 Generating {domain} domain...")
            
            # Priority 1: Foundation Layer
            self.types_generator.generate_domain_types(domain, endpoints)
            
            # Priority 2: Infrastructure Layer 
            self.services_generator.generate_domain_services(domain, endpoints)
            
            # Priority 3: Data Layer
            self.hooks_generator.generate_domain_hooks(domain, endpoints)
            
            # Priority 4: Presentation Layer
            self.components_generator.generate_domain_components(domain, endpoints)
            
            # Priority 5: Pages Layer (handled separately at the end)
        
        # Generate domain-specific clients (Priority 2)
        self.clients_generator.generate_domain_clients()
        
        # Generate global stores (Priority 3)
        self.stores_generator.generate_domain_stores()
        
        # Generate main React entry files
        self.components_generator.generate_main_entry_files()
        
        # Generate core infrastructure
        self.pages_generator.generate_core_infrastructure()
        
        # Generate grouped pages (Priority 5)
        all_endpoints = list(self.backend_config['endpoints'].keys())
        page_domains = self.pages_generator.group_endpoints_by_page_domain(all_endpoints)
        self.pages_generator.generate_all_domain_pages(all_endpoints)
        
        # Generate layout system (Priority 6) 
        domain_list = list(page_domains.keys())
        self.layout_generator.generate_complete_app_infrastructure(domain_list)
        
        # Generate index files for easier imports
        self._generate_final_indices()
        
        print("✅ Domain-driven frontend generation complete!")
    
    def _share_backend_config(self):
        """Share backend config with all generators"""
        generators = [
            self.types_generator,
            self.services_generator, 
            self.hooks_generator,
            self.components_generator,
            self.clients_generator,
            self.stores_generator,
            self.pages_generator,
            self.layout_generator
        ]
        
        for generator in generators:
            generator.backend_config = self.backend_config
    
    def _generate_final_indices(self):
        """Generate final index files with proper exports"""
        # Generate main index files using individual generators
        self.types_generator.generate_main_types_index()
        self.hooks_generator.generate_main_hooks_index()
        self.components_generator.generate_main_components_index()
        
        print("📝 Generated final index files")
    
    def generate_specific_domain(self, domain: str):
        """Generate files for a specific domain only"""
        print(f"🔧 Generating {domain} domain specifically...")
        
        # Load backend configuration if not already loaded
        if not self.backend_config:
            self.load_backend_config()
            self._share_backend_config()
        
        # Get endpoints for this domain
        domains = self.domain_mapping.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        if domain not in domains:
            print(f"❌ Domain '{domain}' not found in available domains: {list(domains.keys())}")
            return
        
        endpoints = domains[domain]
        
        # Generate files for this domain
        self.types_generator.generate_domain_types(domain, endpoints)
        self.services_generator.generate_domain_services(domain, endpoints)
        self.hooks_generator.generate_domain_hooks(domain, endpoints)
        self.components_generator.generate_domain_components(domain, endpoints)
        
        print(f"✅ {domain} domain generation complete!")
    
    def list_available_domains(self):
        """List all available domains"""
        if not self.backend_config:
            self.load_backend_config()
        
        domains = self.domain_mapping.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        print("📋 Available domains:")
        for domain, endpoints in domains.items():
            print(f"  • {domain}: {len(endpoints)} endpoints")
            for endpoint in endpoints:
                print(f"    - {endpoint}")
        
        return list(domains.keys())