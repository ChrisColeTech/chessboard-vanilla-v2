#!/usr/bin/env python3
"""
Configuration Validator

Compares API configurations with database schema to detect drift and inconsistencies.
Helps identify when configs are out of sync with the actual database.
"""

import json
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass
from pathlib import Path

from schema_introspector import TableInfo, ColumnInfo


@dataclass
class ValidationResult:
    """Results of configuration validation"""
    is_valid: bool
    missing_tables: List[str]
    extra_tables: List[str] 
    table_issues: Dict[str, List[str]]
    field_mismatches: Dict[str, Dict[str, str]]  # {table: {field: issue}}
    summary: str


class ConfigValidator:
    """Validates API configuration against actual database schema"""
    
    def __init__(self):
        self.issues = []
        
    def validate_config(self, config: Dict[str, Any], database_tables: Dict[str, TableInfo]) -> ValidationResult:
        """Compare configuration with actual database schema"""
        print("🔍 Validating configuration against database schema...")
        
        self.issues = []
        missing_tables = []
        extra_tables = []
        table_issues = {}
        field_mismatches = {}
        
        # Get sets of table names
        config_tables = set(config.get('endpoints', {}).keys())
        db_tables = set(database_tables.keys())
        
        # Find missing and extra tables
        missing_tables = list(db_tables - config_tables)
        extra_tables = list(config_tables - db_tables)
        
        # Validate each table that exists in both
        common_tables = config_tables & db_tables
        for table_name in common_tables:
            config_table = config['endpoints'][table_name]
            db_table = database_tables[table_name]
            
            issues, mismatches = self._validate_table(table_name, config_table, db_table)
            if issues:
                table_issues[table_name] = issues
            if mismatches:
                field_mismatches[table_name] = mismatches
        
        # Determine overall validity
        is_valid = (
            len(missing_tables) == 0 and 
            len(extra_tables) == 0 and 
            len(table_issues) == 0 and 
            len(field_mismatches) == 0
        )
        
        # Generate summary
        summary = self._generate_summary(is_valid, missing_tables, extra_tables, table_issues, field_mismatches)
        
        return ValidationResult(
            is_valid=is_valid,
            missing_tables=missing_tables,
            extra_tables=extra_tables,
            table_issues=table_issues,
            field_mismatches=field_mismatches,
            summary=summary
        )
        
    def _validate_table(self, table_name: str, config_table: Dict[str, Any], db_table: TableInfo) -> Tuple[List[str], Dict[str, str]]:
        """Validate a single table configuration"""
        issues = []
        field_mismatches = {}
        
        # Get field sets
        config_props = set(config_table.get('properties', {}).keys())
        db_columns = set(col.name for col in db_table.columns)
        
        # Check for missing required fields
        missing_fields = db_columns - config_props
        required_missing = []
        for col in db_table.columns:
            if col.name in missing_fields and not col.is_nullable and col.default_value is None:
                required_missing.append(col.name)
                
        if required_missing:
            issues.append(f"Missing required fields: {', '.join(required_missing)}")
            
        # Check for extra fields in config
        extra_fields = config_props - db_columns
        if extra_fields:
            issues.append(f"Config has non-existent fields: {', '.join(extra_fields)}")
            
        # Check field type mismatches
        for field_name in config_props & db_columns:
            config_type = config_table['properties'][field_name]
            db_col = next(col for col in db_table.columns if col.name == field_name)
            db_type = db_col.data_type
            
            if not self._types_compatible(config_type, db_type):
                field_mismatches[field_name] = f"Config: {config_type}, DB: {db_type}"
                
        return issues, field_mismatches
        
    def _types_compatible(self, config_type: str, db_type: str) -> bool:
        """Check if configuration type is compatible with database type"""
        # Exact matches
        if config_type == db_type:
            return True
            
        # Compatible type groups
        string_types = {'string', 'text'}
        number_types = {'number', 'integer', 'float'}
        bool_types = {'boolean', 'bool'}
        object_types = {'object', 'json', 'jsonb'}
        
        type_groups = [string_types, number_types, bool_types, object_types]
        
        for group in type_groups:
            if config_type in group and db_type in group:
                return True
                
        return False
        
    def _generate_summary(self, is_valid: bool, missing_tables: List[str], extra_tables: List[str], 
                         table_issues: Dict[str, List[str]], field_mismatches: Dict[str, Dict[str, str]]) -> str:
        """Generate a summary of validation results"""
        if is_valid:
            return "✅ Configuration is valid and matches database schema perfectly!"
            
        summary_lines = ["❌ Configuration validation failed:"]
        
        if missing_tables:
            summary_lines.append(f"📋 Missing tables in config: {', '.join(missing_tables)}")
            
        if extra_tables:
            summary_lines.append(f"📋 Extra tables in config: {', '.join(extra_tables)}")
            
        if table_issues:
            summary_lines.append(f"⚠️  Tables with issues: {len(table_issues)}")
            for table, issues in table_issues.items():
                for issue in issues:
                    summary_lines.append(f"   • {table}: {issue}")
                    
        if field_mismatches:
            summary_lines.append(f"🔀 Type mismatches: {len(field_mismatches)} tables affected")
            for table, mismatches in field_mismatches.items():
                for field, mismatch in mismatches.items():
                    summary_lines.append(f"   • {table}.{field}: {mismatch}")
                    
        return "\n".join(summary_lines)
        
    def print_detailed_report(self, result: ValidationResult) -> None:
        """Print a detailed validation report"""
        print("\n" + "=" * 60)
        print("📊 CONFIGURATION VALIDATION REPORT")
        print("=" * 60)
        
        print(f"Overall Status: {'✅ VALID' if result.is_valid else '❌ INVALID'}")
        
        if result.missing_tables:
            print(f"\n🚫 Missing Tables ({len(result.missing_tables)}):")
            for table in result.missing_tables:
                print(f"   • {table}")
                
        if result.extra_tables:
            print(f"\n➕ Extra Tables ({len(result.extra_tables)}):")
            for table in result.extra_tables:
                print(f"   • {table}")
                
        if result.table_issues:
            print(f"\n⚠️  Table Issues ({len(result.table_issues)}):")
            for table, issues in result.table_issues.items():
                print(f"   📋 {table}:")
                for issue in issues:
                    print(f"      • {issue}")
                    
        if result.field_mismatches:
            print(f"\n🔀 Field Type Mismatches ({len(result.field_mismatches)}):")
            for table, mismatches in result.field_mismatches.items():
                print(f"   📋 {table}:")
                for field, mismatch in mismatches.items():
                    print(f"      • {field}: {mismatch}")
                    
        print("\n" + "=" * 60)
        print(result.summary)
        print("=" * 60)


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")


def main():
    """Main validation function"""
    import sys
    import os
    
    # Add database manager to path
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'payload-generator', 'seeders'))
    
    from database_manager import DatabaseManager
    from schema_introspector import SchemaIntrospector
    
    print("🔍 Configuration Validator")
    print("=" * 40)
    
    try:
        # Load existing config
        config_path = "/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json"
        print(f"📄 Loading config from: {config_path}")
        config = load_config(config_path)
        
        # Get database schema
        print("📡 Connecting to database...")
        db_manager = DatabaseManager()
        introspector = SchemaIntrospector(db_manager)
        database_tables = introspector.introspect_database()
        
        # Validate
        validator = ConfigValidator()
        result = validator.validate_config(config, database_tables)
        
        # Print results
        validator.print_detailed_report(result)
        
        return 0 if result.is_valid else 1
        
    except Exception as error:
        print(f"❌ Error: {error}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())