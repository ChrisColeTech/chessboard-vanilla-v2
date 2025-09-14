#!/usr/bin/env python3
"""
Configuration Loader
Responsible for loading and validating JSON configuration files
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Loads and manages configuration files"""
    
    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent.parent / "config"
        self.logger = logging.getLogger("config_loader")
        
        # Cache for loaded configs
        self._config_cache: Dict[str, Dict[str, Any]] = {}
    
    def load_config(self, filename: str, use_cache: bool = True) -> Dict[str, Any]:
        """Load a configuration file"""
        if use_cache and filename in self._config_cache:
            return self._config_cache[filename]
        
        config_file = self.config_dir / filename
        if not config_file.exists():
            self.logger.error(f"❌ Config file not found: {config_file}")
            return {}
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            if use_cache:
                self._config_cache[filename] = config
            
            self.logger.debug(f"✅ Loaded config: {filename}")
            return config
            
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Invalid JSON in {filename}: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"❌ Error loading {filename}: {e}")
            return {}
    
    def load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load all required configuration files"""
        config_files = [
            "handler_mappings.json",
            "entity_overrides.json", 
            "method_templates.json",
            "infrastructure_templates.json"
        ]
        
        configs = {}
        for filename in config_files:
            key = filename.replace('.json', '')
            configs[key] = self.load_config(filename)
        
        self.logger.info(f"📚 Loaded {len(configs)} configuration files")
        return configs
    
    def validate_config(self, config: Dict[str, Any], config_type: str) -> bool:
        """Validate configuration structure"""
        validators = {
            'handler_mappings': self._validate_handler_mappings,
            'entity_overrides': self._validate_entity_overrides,
            'method_templates': self._validate_method_templates,
            'infrastructure_templates': self._validate_infrastructure_templates
        }
        
        validator = validators.get(config_type)
        if not validator:
            self.logger.warning(f"⚠️ No validator for config type: {config_type}")
            return True
        
        return validator(config)
    
    def _validate_handler_mappings(self, config: Dict[str, Any]) -> bool:
        """Validate handler mappings configuration"""
        required_keys = ['exact_mappings', 'pattern_rules']
        
        for key in required_keys:
            if key not in config:
                self.logger.error(f"❌ Missing required key in handler_mappings: {key}")
                return False
        
        # Validate pattern rules structure
        for rule in config.get('pattern_rules', []):
            if not all(k in rule for k in ['pattern', 'parameters', 'description']):
                self.logger.error(f"❌ Invalid pattern rule structure: {rule}")
                return False
        
        return True
    
    def _validate_entity_overrides(self, config: Dict[str, Any]) -> bool:
        """Validate entity overrides configuration"""
        required_keys = ['entity_overrides', 'property_mappings', 'parameter_mappings']
        
        for key in required_keys:
            if key not in config:
                self.logger.error(f"❌ Missing required key in entity_overrides: {key}")
                return False
        
        return True
    
    def _validate_method_templates(self, config: Dict[str, Any]) -> bool:
        """Validate method templates configuration"""
        required_keys = ['method_templates', 'specialized_methods']
        
        for key in required_keys:
            if key not in config:
                self.logger.error(f"❌ Missing required key in method_templates: {key}")
                return False
        
        # Validate template structure
        for template_name, template_config in config.get('method_templates', {}).items():
            if not all(k in template_config for k in ['pattern', 'template']):
                self.logger.error(f"❌ Invalid template structure: {template_name}")
                return False
        
        return True
    
    def _validate_infrastructure_templates(self, config: Dict[str, Any]) -> bool:
        """Validate infrastructure templates configuration"""
        if 'templates' not in config:
            self.logger.error("❌ Missing 'templates' key in infrastructure_templates")
            return False
        
        return True
    
    def get_handler_parameters(self, handler: str, path: str, method: str, entity_lower: str, configs: Dict[str, Any]) -> str:
        """Get parameters for a handler using configuration"""
        handler_mappings = configs.get('handler_mappings', {})
        
        # Check exact mappings first
        exact_mappings = handler_mappings.get('exact_mappings', {})
        if handler in exact_mappings:
            return exact_mappings[handler]
        
        # Check pattern rules
        import re
        pattern_rules = handler_mappings.get('pattern_rules', [])
        for rule in pattern_rules:
            if re.match(rule['pattern'], handler):
                return rule['parameters']
        
        # Check special cases
        special_cases = handler_mappings.get('special_cases', {})
        for case_name, case_config in special_cases.items():
            if re.search(case_config['pattern'], f"{handler}{path}{entity_lower}"):
                return case_config['parameters']
        
        # Default fallback based on common patterns
        if ':id' in path and method.upper() in ['PUT', 'PATCH']:
            return 'req.params.id, req.body'
        elif ':id' in path and method.upper() == 'DELETE':
            return 'req.params.id'
        elif ':id' in path:
            return 'req.params.id'
        elif method.upper() in ['POST', 'PUT', 'PATCH']:
            return 'req.body'
        else:
            return ''
    
    def clear_cache(self):
        """Clear the configuration cache"""
        self._config_cache.clear()
        self.logger.debug("🗑️ Configuration cache cleared")