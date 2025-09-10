#!/usr/bin/env python3
"""
Domain Mapping Module
Manages the mapping between backend endpoints and frontend domains
"""

from typing import Dict, List

class DomainMapping:
    """Manages domain mapping for the frontend generator"""
    
    def __init__(self):
        # Domain mapping - each endpoint gets its own domain for better organization
        self.domain_mapping = {
            'auth': 'auth',
            'users': 'users',
            'sessions': 'sessions',
            'profiles': 'profiles',
            'puzzles': 'puzzles',
            'games': 'games',
            'stats': 'stats',
            'learning': 'learning',
            'tutorials': 'tutorials',
            'openings': 'openings',
            'analysis': 'analysis',
            'ai-opponents': 'ai-opponents',
            'endgames': 'endgames',
            'historic-games': 'historic-games',
            'puzzle-attempts': 'puzzle-attempts',
            'puzzle-sources': 'puzzle-sources',
            'game-reviews': 'game-reviews',
            'progress': 'progress',
            'achievements': 'achievements',
            'analytics': 'analytics',
            'learning-modules': 'learning-modules',
            'tutorial-steps': 'tutorial-steps',
            'study-plans': 'study-plans',
            'help': 'help',
            'subscriptions': 'subscriptions'
        }
        
        # Generate domain directories for each unique domain
        unique_domains = list(set(self.domain_mapping.values()))
        self.domain_directories = {}
        
        for domain in unique_domains:
            self.domain_directories[domain] = [
                f"types/{domain}",
                f"utils/{domain}",
                f"constants/{domain}",
                f"services/{domain}",
                f"hooks/{domain}",
                f"components/{domain}"
            ]
        
        self.common_directories = [
            # Priority 1: Foundation Layer
            "types/common",
            "utils/common",
            
            # Priority 2: Infrastructure Layer
            "clients",
            
            # Priority 3: Data Layer
            "stores",
            "providers",
            
            # Priority 4: Presentation Layer
            "components/ui"
        ]
    
    def get_domain_for_endpoint(self, endpoint_name: str) -> str:
        """Get the domain for a given endpoint"""
        return self.domain_mapping.get(endpoint_name, 'common')
    
    def get_all_domains(self) -> List[str]:
        """Get list of all unique domains"""
        return list(set(self.domain_mapping.values()))
    
    def get_directory_structure(self) -> List[str]:
        """Get complete directory structure for all domains"""
        directories = self.common_directories.copy()
        
        for domain_dirs in self.domain_directories.values():
            directories.extend(domain_dirs)
        
        return directories
    
    def group_endpoints_by_domain(self, endpoints: Dict[str, any]) -> Dict[str, List[str]]:
        """Group endpoints by their domain"""
        domains = {}
        
        for endpoint_name in endpoints.keys():
            domain = self.get_domain_for_endpoint(endpoint_name)
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(endpoint_name)
        
        return domains
    
    def get_domain_type_imports(self, domain: str) -> List[str]:
        """Get the type imports for a specific domain"""
        # Generate basic type imports for any domain
        domain_capitalized = domain.replace('-', '').replace('_', '').capitalize()
        
        return [
            f"{domain_capitalized}Response",
            f"Create{domain_capitalized}Request", 
            f"Update{domain_capitalized}Request"
        ]