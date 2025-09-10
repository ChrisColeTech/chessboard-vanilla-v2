#!/usr/bin/env python3
"""
Base Method Generator
Abstract base class for all method generators
"""

from abc import ABC, abstractmethod


class BaseMethodGenerator(ABC):
    """Base class for all method generators"""
    
    @abstractmethod
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate a service method implementation"""
        pass
    
    def _create_stub_method(self, method_name: str) -> str:
        """Create a default stub method"""
        return f'''  async {method_name}(...args: any[]): Promise<any> {{
    // TODO: Implement {method_name}
    throw new Error('{method_name} not implemented');
  }}'''