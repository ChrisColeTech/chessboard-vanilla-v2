#!/usr/bin/env python3
"""
Database Schema Introspector

Automatically generates API configuration by introspecting the actual database schema.
This ensures payload generators always have up-to-date field definitions.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# Add the database manager to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'payload-generator', 'seeders'))

from database_manager import DatabaseManager


@dataclass
class ColumnInfo:
    """Represents a database column with its properties"""
    name: str
    data_type: str
    is_nullable: bool
    default_value: Optional[str] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_table: Optional[str] = None
    foreign_column: Optional[str] = None


@dataclass 
class TableInfo:
    """Represents a database table with its columns and constraints"""
    name: str
    columns: List[ColumnInfo]
    primary_keys: List[str]
    foreign_keys: Dict[str, Dict[str, str]]  # {column: {table: table, column: column}}


class SchemaIntrospector:
    """Introspects database schema and generates API configuration"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.tables: Dict[str, TableInfo] = {}
        
    def introspect_database(self) -> Dict[str, TableInfo]:
        """Get complete schema information for all tables"""
        print("🔍 Introspecting database schema...")
        
        # Get list of tables
        table_names = self._get_table_names()
        print(f"📋 Found {len(table_names)} tables: {', '.join(table_names)}")
        
        # Introspect each table
        for table_name in table_names:
            print(f"🔎 Analyzing table: {table_name}")
            self.tables[table_name] = self._introspect_table(table_name)
            
        return self.tables
        
    def _get_table_names(self) -> List[str]:
        """Get all table names from the database"""
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """
        
        results = self.db.execute_query(query)
        return [row[0] for row in results]
        
    def _introspect_table(self, table_name: str) -> TableInfo:
        """Get detailed information about a specific table"""
        columns = self._get_column_info(table_name)
        primary_keys = self._get_primary_keys(table_name)
        foreign_keys = self._get_foreign_keys(table_name)
        
        # Mark primary and foreign key columns
        for col in columns:
            if col.name in primary_keys:
                col.is_primary_key = True
            if col.name in foreign_keys:
                col.is_foreign_key = True
                col.foreign_table = foreign_keys[col.name]['table']
                col.foreign_column = foreign_keys[col.name]['column']
        
        return TableInfo(
            name=table_name,
            columns=columns,
            primary_keys=primary_keys,
            foreign_keys=foreign_keys
        )
        
    def _get_column_info(self, table_name: str) -> List[ColumnInfo]:
        """Get column information for a table"""
        query = """
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default,
            udt_name,
            character_maximum_length,
            numeric_precision,
            numeric_scale
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = %s
        ORDER BY ordinal_position;
        """
        
        results = self.db.execute_query(query, (table_name,))
        columns = []
        
        for row in results:
            col_name, data_type, is_nullable, default_value, udt_name, char_length, num_precision, num_scale = row
            
            columns.append(ColumnInfo(
                name=col_name,
                data_type=self._normalize_data_type(data_type, udt_name),
                is_nullable=is_nullable == 'YES',
                default_value=default_value
            ))
            
        return columns
        
    def _get_primary_keys(self, table_name: str) -> List[str]:
        """Get primary key columns for a table"""
        query = """
        SELECT column_name
        FROM information_schema.key_column_usage kcu
        JOIN information_schema.table_constraints tc
        ON kcu.constraint_name = tc.constraint_name
        WHERE tc.table_schema = 'public'
        AND tc.table_name = %s
        AND tc.constraint_type = 'PRIMARY KEY'
        ORDER BY kcu.ordinal_position;
        """
        
        results = self.db.execute_query(query, (table_name,))
        return [row[0] for row in results]
        
    def _get_foreign_keys(self, table_name: str) -> Dict[str, Dict[str, str]]:
        """Get foreign key relationships for a table"""
        query = """
        SELECT 
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.key_column_usage kcu
        JOIN information_schema.constraint_column_usage ccu
        ON kcu.constraint_name = ccu.constraint_name
        JOIN information_schema.table_constraints tc
        ON kcu.constraint_name = tc.constraint_name
        WHERE tc.table_schema = 'public'
        AND tc.table_name = %s
        AND tc.constraint_type = 'FOREIGN KEY';
        """
        
        results = self.db.execute_query(query, (table_name,))
        foreign_keys = {}
        
        for row in results:
            col_name, foreign_table, foreign_column = row
            foreign_keys[col_name] = {
                'table': foreign_table,
                'column': foreign_column
            }
            
        return foreign_keys
        
    def _normalize_data_type(self, data_type: str, udt_name: str) -> str:
        """Convert PostgreSQL data types to API config types"""
        type_mapping = {
            # String types
            'character varying': 'string',
            'varchar': 'string', 
            'text': 'string',
            'character': 'string',
            'char': 'string',
            'uuid': 'string',
            
            # Number types
            'integer': 'number',
            'int': 'number',
            'int4': 'number',
            'bigint': 'number',
            'int8': 'number',
            'smallint': 'number',
            'int2': 'number',
            'decimal': 'number',
            'numeric': 'number',
            'real': 'number',
            'float4': 'number',
            'double precision': 'number',
            'float8': 'number',
            
            # Boolean types
            'boolean': 'boolean',
            'bool': 'boolean',
            
            # Date/time types
            'timestamp without time zone': 'string',
            'timestamp with time zone': 'string',
            'timestamp': 'string',
            'timestamptz': 'string',
            'date': 'string',
            'time': 'string',
            
            # JSON types
            'json': 'object',
            'jsonb': 'object',
            
            # Array types
            'ARRAY': 'array',
        }
        
        # Use udt_name for more specific type info
        if udt_name in type_mapping:
            return type_mapping[udt_name]
        
        # Fall back to data_type
        if data_type in type_mapping:
            return type_mapping[data_type]
            
        # Handle array types
        if data_type == 'ARRAY' or udt_name.startswith('_'):
            return 'array'
            
        # Default to string for unknown types
        print(f"⚠️  Unknown data type: {data_type} (udt: {udt_name}) - defaulting to 'string'")
        return 'string'


class ConfigGenerator:
    """Generates API configuration from database schema"""
    
    def __init__(self, schema_introspector: SchemaIntrospector):
        self.introspector = schema_introspector
        
    def generate_config(self, tables: Dict[str, TableInfo]) -> Dict[str, Any]:
        """Generate API configuration from schema information"""
        print("🔧 Generating API configuration...")
        
        config = {
            "description": "Auto-generated configuration from database schema introspection",
            "generated_at": self._get_timestamp(),
            "endpoints": {}
        }
        
        # Detect authentication patterns and add auth endpoint
        if self._has_authentication_tables(tables):
            print("🔐 Detected authentication tables - adding auth endpoint")
            config["endpoints"]["auth"] = self._generate_auth_endpoint_config(tables)
        
        for table_name, table_info in tables.items():
            # Skip system/utility tables
            if self._should_skip_table(table_name):
                print(f"⏭️  Skipping table: {table_name}")
                continue
                
            print(f"⚙️  Generating config for: {table_name}")
            config["endpoints"][table_name] = self._generate_table_config(table_info)
            
        return config
        
    def _should_skip_table(self, table_name: str) -> bool:
        """Determine if a table should be skipped in API generation"""
        skip_patterns = [
            'schema_migrations',
            'ar_internal_metadata', 
            'pg_',
            'information_schema',
            '_temp',
            '_backup'
        ]
        
        return any(pattern in table_name.lower() for pattern in skip_patterns)
        
    def _generate_table_config(self, table_info: TableInfo) -> Dict[str, Any]:
        """Generate configuration for a single table"""
        entity_name = self._to_pascal_case(table_info.name.rstrip('s'))  # Remove plural 's'
        
        config = {
            "entity": entity_name,
            "entities": table_info.name,
            "table_name": table_info.name,
            "properties": self._generate_properties(table_info),
            "methods": self._generate_methods(entity_name),
            "endpoints": self._generate_endpoints(entity_name)
        }
        
        return config
        
    def _generate_properties(self, table_info: TableInfo) -> Dict[str, str]:
        """Generate properties section from table columns"""
        properties = {}
        
        for col in table_info.columns:
            # Skip certain system columns that shouldn't be in API payloads
            if col.name in ['created_at', 'updated_at'] and not col.is_primary_key:
                # Include these as strings but they're usually auto-managed
                properties[col.name] = 'string'
            else:
                properties[col.name] = col.data_type
                
        return properties
        
    def _generate_methods(self, entity_name: str) -> List[str]:
        """Generate standard CRUD methods for an entity"""
        lower_entity = entity_name.lower()
        return [
            f"create{entity_name}",
            f"get{entity_name}ById", 
            f"update{entity_name}",
            f"delete{entity_name}",
            f"list{entity_name}s"
        ]
        
    def _generate_endpoints(self, entity_name: str) -> List[Dict[str, Any]]:
        """Generate standard REST endpoints for an entity"""
        return [
            {
                "method": "POST",
                "path": "/",
                "handler": f"create{entity_name}",
                "auth_required": True
            },
            {
                "method": "GET", 
                "path": "/:id",
                "handler": f"get{entity_name}ById",
                "auth_required": True
            },
            {
                "method": "PUT",
                "path": "/:id", 
                "handler": f"update{entity_name}",
                "auth_required": True
            },
            {
                "method": "DELETE",
                "path": "/:id",
                "handler": f"delete{entity_name}",
                "auth_required": True
            },
            {
                "method": "GET",
                "path": "/",
                "handler": f"list{entity_name}s",
                "auth_required": True
            }
        ]
        
    def _to_pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase"""
        components = snake_str.split('_')
        return ''.join(word.capitalize() for word in components)
        
    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    def _has_authentication_tables(self, tables: Dict[str, TableInfo]) -> bool:
        """Detect if database has authentication-related tables"""
        table_names = [name.lower() for name in tables.keys()]
        
        # Look for common authentication table patterns
        auth_patterns = [
            'users',        # User accounts
            'user',         # Single user table
            'accounts',     # Account table
            'auth_users',   # Authentication users
            'members',      # Member accounts
        ]
        
        session_patterns = [
            'user_sessions',    # User session tracking
            'sessions',         # Session management
            'auth_sessions',    # Authentication sessions
            'login_sessions',   # Login tracking
            'user_tokens',      # Token management
            'refresh_tokens',   # Refresh token storage
        ]
        
        # Check if we have user tables
        has_user_table = any(pattern in table_names for pattern in auth_patterns)
        
        # Check if we have session/token tables (optional but common)
        has_session_table = any(pattern in table_names for pattern in session_patterns)
        
        # Consider it an auth system if we have user tables
        # Session tables are optional but indicate a more complete auth system
        if has_user_table:
            auth_type = "complete" if has_session_table else "basic"
            print(f"🔍 Authentication system detected: {auth_type} (users: {has_user_table}, sessions: {has_session_table})")
            return True
            
        return False
        
    def _generate_auth_endpoint_config(self, tables: Dict[str, TableInfo]) -> Dict[str, Any]:
        """Generate authentication endpoint configuration with appropriate auth response properties"""
        # Auth responses should only include safe, public user fields
        # Exclude sensitive fields like password_hash and internal fields
        auth_properties = {
            "id": "string",
            "username": "string",
            "email": "string",
            "created_at": "string", 
            "updated_at": "string"
        }
            
        return {
            "entity": "Auth",
            "entities": "auth",
            "table_name": "users",  # Auth operations work with users table
            "special_routing": True,
            "domain": "authentication",
            "properties": auth_properties,
            "methods": [
                "login",
                "register",
                "logout",
                "forgotPassword",
                "resetPassword",
                "verifyToken",
                "refreshUser",
                "getCurrentUser"
            ],
            "endpoints": []
        }


def main():
    """Main execution function"""
    print("🚀 Database Schema Introspection Tool")
    print("=" * 50)
    
    try:
        # Initialize database connection
        print("📡 Connecting to database...")
        db_manager = DatabaseManager()
        
        # Introspect schema
        introspector = SchemaIntrospector(db_manager)
        tables = introspector.introspect_database()
        
        # Generate configuration
        config_generator = ConfigGenerator(introspector)
        config = config_generator.generate_config(tables)
        
        # Save configuration
        output_file = Path(__file__).parent / "auto_generated_config.json"
        
        print(f"💾 Saving configuration to: {output_file}")
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"✅ Configuration generated successfully!")
        print(f"📊 Generated config for {len(config['endpoints'])} tables")
        print(f"📁 Output: {output_file}")
        
        # Print summary
        print("\n📋 Generated Endpoints:")
        for table_name, table_config in config['endpoints'].items():
            entity = table_config['entity']
            prop_count = len(table_config['properties'])
            print(f"   • {table_name} -> {entity} ({prop_count} properties)")
            
    except Exception as error:
        print(f"❌ Error: {error}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())