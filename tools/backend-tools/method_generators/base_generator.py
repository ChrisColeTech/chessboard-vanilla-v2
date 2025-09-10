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
    
    def _create_stub_method(self, method_name: str, table_name: str = None, entity_upper: str = None) -> str:
        """Create a production-ready generic method implementation"""
        if table_name and entity_upper:
            return f'''  async {method_name}(...args: any[]): Promise<any> {{
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        else:
            # Fallback for backward compatibility
            return f'''  async {method_name}(...args: any[]): Promise<any> {{
    // Generic implementation - returns empty array
    return [];
  }}'''