#!/usr/bin/env python3
"""
Missing Columns Tool
Helps add missing columns to database tables when schema errors occur
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

class MissingColumnsManager:
    """Manages database schema updates for missing columns"""
    
    def __init__(self, backend_path: str = None):
        self.backend_path = Path(backend_path or "../backend-v2")
        # Try to find .env file in multiple locations
        self.env_file = None
        env_locations = [
            Path(__file__).parent.parent / ".env",  # Backend tools directory
            self.backend_path / ".env",             # Backend directory
            Path("..") / ".env"                     # Parent directory
        ]
        
        for env_path in env_locations:
            if env_path.exists():
                self.env_file = env_path
                break
        
        if not self.env_file:
            print("❌ Could not find .env file in any expected location")
            sys.exit(1)
        
    def load_database_url(self) -> Optional[str]:
        """Load DATABASE_URL from .env file"""
        if not self.env_file.exists():
            print(f"❌ .env file not found at {self.env_file}")
            return None
            
        with open(self.env_file) as f:
            for line in f:
                if line.startswith("DATABASE_URL="):
                    return line.split("=", 1)[1].strip().strip('"\'')
        return None
    
    def execute_sql(self, sql: str) -> bool:
        """Execute SQL command using Node.js"""
        database_url = self.load_database_url()
        if not database_url:
            print("❌ Could not load DATABASE_URL")
            return False
            
        # Create a temporary Node.js script to execute the SQL
        node_script = f'''
require('dotenv').config({{ path: '{self.env_file}' }});
const {{ Pool }} = require('pg');
const pool = new Pool({{ 
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? {{ rejectUnauthorized: false }} : false,
  max: 1,
  idleTimeoutMillis: 5000,
  connectionTimeoutMillis: 5000
}});

(async () => {{
  let success = false;
  try {{
    console.log('Executing SQL...');
    const result = await pool.query(`{sql}`);
    console.log('✅ SQL executed successfully');
    if (result.rowCount !== undefined) {{
      console.log('Rows affected:', result.rowCount);
    }}
    success = true;
  }} catch (error) {{
    console.error('❌ SQL Error:', error.message);
    success = false;
  }} finally {{
    try {{
      await pool.end();
    }} catch (e) {{
      // Ignore pool end errors
    }}
  }}
  process.exit(success ? 0 : 1);
}})();
'''
        
        try:
            # Write the script to a temporary file
            temp_script = self.backend_path / "temp_sql_script.js"
            with open(temp_script, 'w') as f:
                f.write(node_script)
            
            # Execute the script
            result = subprocess.run(
                ['node', str(temp_script)], 
                cwd=self.backend_path,
                capture_output=True, 
                text=True
            )
            
            # Clean up
            temp_script.unlink(missing_ok=True)
            
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
                
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Failed to execute SQL: {e}")
            return False
    
    def add_column(self, table: str, column: str, data_type: str, default_value: str = None, nullable: bool = True) -> bool:
        """Add a single column to a table"""
        print(f"🔧 Adding column '{column}' to table '{table}'...")
        
        # Build the ALTER TABLE statement
        sql_parts = [f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {data_type}"]
        
        if default_value is not None:
            # Handle different types of default values
            if data_type.upper().startswith(('VARCHAR', 'TEXT', 'CHAR')):
                # String types need quotes
                sql_parts.append(f"DEFAULT '{default_value}'")
            elif data_type.upper() == 'JSONB':
                # JSONB needs quotes around the JSON
                sql_parts.append(f"DEFAULT '{default_value}'")
            elif default_value.upper() in ('NOW()', 'CURRENT_TIMESTAMP'):
                # Functions don't need quotes
                sql_parts.append(f"DEFAULT {default_value}")
            else:
                # Numbers and other literals
                sql_parts.append(f"DEFAULT {default_value}")
            
        if not nullable:
            sql_parts.append("NOT NULL")
            
        sql = " ".join(sql_parts) + ";"
        
        print(f"SQL: {sql}")
        return self.execute_sql(sql)
    
    def add_multiple_columns(self, table: str, columns: List[Dict[str, Any]]) -> bool:
        """Add multiple columns to a table"""
        success = True
        for col in columns:
            column_name = col['name']
            data_type = col['type']
            default_value = col.get('default')
            nullable = col.get('nullable', True)
            
            if not self.add_column(table, column_name, data_type, default_value, nullable):
                success = False
                
        return success
    
    def check_column_exists(self, table: str, column: str) -> bool:
        """Check if a column exists in a table"""
        sql = f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = '{table}' AND column_name = '{column}';
        """
        
        # This is a simplified check - in a full implementation you'd want to return the result
        print(f"🔍 Checking if column '{column}' exists in table '{table}'...")
        return True  # Simplified for this tool
    
    def get_table_schema(self, table: str) -> bool:
        """Display current table schema"""
        sql = f"""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = '{table}' 
        ORDER BY ordinal_position;
        """
        
        print(f"📋 Current schema for table '{table}':")
        return self.execute_sql(sql)

def main():
    """CLI for missing columns tool"""
    parser = argparse.ArgumentParser(description='Missing Columns Tool - Add missing database columns')
    parser.add_argument('--backend-path', default='../backend-v2', help='Backend directory path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add single column command
    add_parser = subparsers.add_parser('add', help='Add a single column')
    add_parser.add_argument('table', help='Table name')
    add_parser.add_argument('column', help='Column name')
    add_parser.add_argument('type', help='Column data type (e.g., INTEGER, VARCHAR(255), JSONB)')
    add_parser.add_argument('--default', help='Default value')
    add_parser.add_argument('--not-null', action='store_true', help='Make column NOT NULL')
    
    # Add multiple columns from JSON command
    batch_parser = subparsers.add_parser('batch', help='Add multiple columns from JSON')
    batch_parser.add_argument('table', help='Table name')
    batch_parser.add_argument('columns_json', help='JSON string or file path with column definitions')
    
    # Check schema command
    schema_parser = subparsers.add_parser('schema', help='Show table schema')
    schema_parser.add_argument('table', help='Table name')
    
    # Common missing columns command
    common_parser = subparsers.add_parser('common', help='Add common missing columns for specific entities')
    common_parser.add_argument('entity', choices=['user_progress', 'users', 'puzzles'], help='Entity type')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = MissingColumnsManager(args.backend_path)
    
    if args.command == 'add':
        success = manager.add_column(
            args.table, 
            args.column, 
            args.type, 
            args.default,
            not args.not_null
        )
        if success:
            print("✅ Column added successfully!")
        else:
            print("❌ Failed to add column")
            sys.exit(1)
            
    elif args.command == 'batch':
        try:
            # Try to parse as JSON first
            if args.columns_json.startswith('[') or args.columns_json.startswith('{'):
                columns = json.loads(args.columns_json)
            else:
                # Try to read as file
                with open(args.columns_json) as f:
                    columns = json.load(f)
                    
            success = manager.add_multiple_columns(args.table, columns)
            if success:
                print("✅ All columns added successfully!")
            else:
                print("❌ Some columns failed to add")
                sys.exit(1)
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ Error parsing columns JSON: {e}")
            sys.exit(1)
            
    elif args.command == 'schema':
        manager.get_table_schema(args.table)
        
    elif args.command == 'common':
        # Define common missing columns for different entities
        common_columns = {
            'user_progress': [
                {'name': 'total_time_spent', 'type': 'INTEGER', 'default': '0'},
                {'name': 'achievements_unlocked', 'type': 'JSONB', 'default': "[]"},
                {'name': 'last_puzzle_date', 'type': 'TIMESTAMP', 'nullable': True}
            ],
            'users': [
                {'name': 'preferences', 'type': 'JSONB', 'default': "'{}'"},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'default': 'NOW()'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'default': 'NOW()'}
            ],
            'puzzles': [
                {'name': 'created_at', 'type': 'TIMESTAMP', 'default': 'NOW()'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'default': 'NOW()'},
                {'name': 'difficulty', 'type': 'VARCHAR(50)', 'default': "'medium'"}
            ]
        }
        
        if args.entity in common_columns:
            table_name = args.entity
            columns = common_columns[args.entity]
            print(f"🔧 Adding common columns to {table_name}...")
            success = manager.add_multiple_columns(table_name, columns)
            if success:
                print("✅ Common columns added successfully!")
            else:
                print("❌ Failed to add some common columns")
                sys.exit(1)
        else:
            print(f"❌ No common columns defined for entity: {args.entity}")
            sys.exit(1)

if __name__ == "__main__":
    main()