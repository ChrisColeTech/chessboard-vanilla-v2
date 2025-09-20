#!/usr/bin/env python3
"""
Base Frontend Generator
Common functionality shared across all generator modules
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

class BaseFrontendGenerator:
    """Base class for all frontend generators"""
    
    def __init__(self, frontend_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2"):
        self.frontend_path = Path(frontend_path)
        self.backend_config = {}
        
    def load_backend_config(self, config_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json"):
        """Load backend configuration to understand API contract"""
        with open(config_path, 'r') as f:
            self.backend_config = json.load(f)
        print(f"📖 Loaded backend config with {len(self.backend_config['endpoints'])} endpoints")
    
    def ensure_directory(self, path: Path):
        """Ensure directory exists"""
        path.mkdir(parents=True, exist_ok=True)
    
    def get_src_path(self) -> Path:
        """Get the src path for the frontend"""
        return self.frontend_path / "src"
    
    def write_file(self, file_path: Path, content: str):
        """Write content to file and log the action"""
        self.ensure_directory(file_path.parent)
        file_path.write_text(content)
        print(f"📝 Generated {file_path}")
    
    def get_domain_endpoints(self, domain: str, domain_mapping: Dict[str, str]) -> List[str]:
        """Get endpoints for a specific domain"""
        endpoints = []
        for endpoint_name, endpoint_config in self.backend_config['endpoints'].items():
            mapped_domain = domain_mapping.get(endpoint_name, 'common')
            if mapped_domain == domain:
                endpoints.append(endpoint_name)
        return endpoints
    
    def get_entity_name(self, endpoint_name: str) -> str:
        """Get the entity name for an endpoint with proper naming"""
        if endpoint_name not in self.backend_config['endpoints']:
            return None
            
        endpoint_config = self.backend_config['endpoints'][endpoint_name]
        entity = endpoint_config['entity']
        
        # Fix naming inconsistencies
        if entity == 'Learningpath':
            entity = 'LearningPath'
            
        return entity
    
    def get_api_base_path(self, endpoint_name: str, endpoint_config: Dict[str, Any]) -> str:
        """Get the API base path for an endpoint"""
        if endpoint_name == 'auth':
            return '/api/auth'
        else:
            entities = endpoint_config.get("entities", endpoint_name)
            # Convert snake_case entities to camelCase for API routes
            camel_case_entities = self._snake_to_camel_case(entities)
            return f'/api/{camel_case_entities}'
    
    def _snake_to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case string to camelCase"""
        components = snake_str.split('_')
        # First component stays lowercase, subsequent ones are capitalized
        return components[0] + ''.join(word.capitalize() for word in components[1:])
    
    def capitalize_domain(self, domain: str) -> str:
        """Convert domain name to PascalCase (e.g., 'ai-opponents' -> 'AiOpponents')"""
        # Split on hyphens and underscores, capitalize each part
        parts = domain.replace('-', ' ').replace('_', ' ').split()
        return ''.join(word.capitalize() for word in parts)
    
    def camel_case_domain(self, domain: str) -> str:
        """Convert domain name to camelCase (e.g., 'ai-opponents' -> 'aiOpponents')"""
        # Split on hyphens and underscores, capitalize each part except the first
        parts = domain.replace('-', ' ').replace('_', ' ').split()
        if len(parts) == 0:
            return domain
        return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])