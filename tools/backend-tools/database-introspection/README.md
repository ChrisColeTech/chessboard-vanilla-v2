# Database Introspection Tool

A comprehensive toolkit for automatically generating and validating API configurations from live database schemas. This tool eliminates schema drift by ensuring your API configurations always match your actual database structure.

## 🎯 Overview

The Database Introspection Tool solves the critical problem of configuration drift between your API definitions and actual database schema. Instead of manually maintaining configuration files that can become outdated, this tool:

1. **Automatically introspects** your PostgreSQL database schema
2. **Generates accurate API configurations** with correct field types and constraints
3. **Validates existing configurations** against the live database
4. **Detects schema drift** and provides detailed reports
5. **Merges configurations** while preserving custom settings

## 🏗️ Architecture

```
database-introspection/
├── README.md                    # This comprehensive guide
├── db_config_tool.py           # Main CLI tool (entry point)
├── schema_introspector.py      # Database schema analysis
├── config_validator.py         # Configuration validation
└── examples/                   # Usage examples and sample configs
    ├── sample_validation.py
    └── sample_configs/
```

## ✨ Key Features

### 🔍 **Schema Introspection**
- **Complete table analysis**: Columns, data types, constraints, relationships
- **Constraint detection**: Primary keys, foreign keys, NOT NULL constraints
- **Type mapping**: PostgreSQL types → API configuration types
- **Relationship mapping**: Foreign key relationships and dependencies

### ⚡ **Automatic Configuration Generation**
- **Standard REST endpoints**: GET, POST, PUT, DELETE operations
- **Proper field types**: Accurate type mapping from database to API
- **Required field detection**: Identifies non-nullable fields without defaults
- **Metadata inclusion**: Timestamps, generation info, table relationships

### 🔎 **Advanced Validation**
- **Schema drift detection**: Finds differences between config and database
- **Missing field analysis**: Identifies required fields missing from config
- **Type compatibility checking**: Ensures config types match database types
- **Detailed reporting**: Comprehensive validation reports with actionable insights

### 🔄 **Configuration Management**
- **Smart merging**: Preserves custom configurations during updates
- **Comparison tools**: Side-by-side configuration comparison
- **Backup and versioning**: Safe configuration updates with rollback capability
- **Multiple output formats**: JSON configuration with proper formatting

## 🚀 Quick Start

### Prerequisites

```bash
# Install required Python packages (if not already installed)
pip install psycopg2-binary python-dotenv
```

### Basic Usage

```bash
# Navigate to the tool directory
cd tools/backend-tools/database-introspection

# Generate new configuration from database (exports to /config/backend_config.json by default)
python db_config_tool.py generate

# Validate existing configuration
python db_config_tool.py validate --config /mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json

# Compare two configurations
python db_config_tool.py compare old_config.json new_config.json

# Update existing configuration with current schema
python db_config_tool.py update --config old_config.json --output updated_config.json
```

## 📚 Detailed Usage

### 1. Schema Introspection

```bash
# Generate complete configuration from live database
python db_config_tool.py generate --verbose

# Or specify custom output location
python db_config_tool.py generate --output custom_config.json --verbose

# Example output:
# 🔍 Introspecting database schema...
# 📋 Found 13 tables: users, games, puzzles, achievements, ...
# 🔎 Analyzing table: users
# 🔎 Analyzing table: games
# ...
# ✅ Configuration generated successfully!
# 📊 Generated config for 13 tables
```

**What it generates:**
```json
{
  "description": "Auto-generated configuration from database schema introspection",
  "generated_at": "2025-09-14T16:30:00.000Z",
  "endpoints": {
    "users": {
      "entity": "User",
      "entities": "users", 
      "table_name": "users",
      "properties": {
        "id": "string",
        "username": "string",
        "email": "string",
        "password_hash": "string",
        "chess_elo": "number",
        "puzzle_rating": "number",
        "preferences": "string",
        "created_at": "string",
        "updated_at": "string"
      },
      "methods": [
        "createUser",
        "getUserById", 
        "updateUser",
        "deleteUser",
        "listUsers"
      ],
      "endpoints": [
        {
          "method": "POST",
          "path": "/",
          "handler": "createUser",
          "auth_required": true
        }
        // ... more endpoints
      ]
    }
    // ... more tables
  }
}
```

### 2. Configuration Validation

```bash
# Validate existing configuration against database
python db_config_tool.py validate 

# Example output:
# ❌ Configuration validation failed:
# 📋 Extra tables in config: old_table_name
# ⚠️  Tables with issues: 3
#    • users: Missing required fields: password_hash
#    • users: Config has non-existent fields: email_verified, games_played
# 🔀 Type mismatches: 2 tables affected  
#    • puzzles.themes: Config: string, DB: array
```

### 3. Configuration Comparison

```bash
# Compare two configuration files
python db_config_tool.py compare old_config.json new_config.json --verbose

# Shows differences in:
# - Table presence/absence
# - Field differences per table
# - Type mismatches
# - Structural changes
```

### 4. Smart Configuration Updates

```bash
# Update configuration while preserving custom settings
python db_config_tool.py update --config existing_config.json --output updated_config.json

# This will:
# 1. Generate new config from current database
# 2. Merge with existing config
# 3. Preserve any custom_methods or custom_endpoints
# 4. Update field definitions to match database
```

## 🔧 Advanced Features

### Custom Type Mapping

The tool includes intelligent type mapping from PostgreSQL to API types:

```python
# PostgreSQL → API Type Mapping
{
    'character varying': 'string',
    'varchar': 'string',
    'text': 'string',
    'integer': 'number',
    'bigint': 'number', 
    'boolean': 'boolean',
    'json': 'object',
    'jsonb': 'object',
    'timestamp without time zone': 'string',
    'uuid': 'string'
}
```

### Constraint Analysis

The tool analyzes database constraints to provide accurate configuration:

- **NOT NULL constraints** → Required fields in API
- **Foreign key relationships** → Related entity references
- **Primary keys** → Unique identifiers
- **Default values** → Optional field detection

### Schema Evolution Tracking

Track how your schema evolves over time:

```bash
# Generate baseline configuration
python db_config_tool.py generate --output baseline_config.json

# After schema changes, compare with current state
python db_config_tool.py generate --output current_config.json
python db_config_tool.py compare baseline_config.json current_config.json
```

## 🛠️ Integration with Existing Tools

### Payload Generator Integration

Use the generated configuration with the payload generator:

```bash
# Generate fresh configuration
python db_config_tool.py generate --output ../payload-generator/fresh_config.json

# Use with payload generator
cd ../payload-generator
python payload_generator.py --config fresh_config.json
```

### CI/CD Integration

Add validation to your deployment pipeline:

```bash
#!/bin/bash
# validate-schema.sh

echo "🔍 Validating API configuration against database..."
python tools/backend-tools/database-introspection/db_config_tool.py validate

if [ $? -ne 0 ]; then
    echo "❌ Schema validation failed - deployment blocked"
    exit 1
fi

echo "✅ Schema validation passed - continuing deployment"
```

## 📋 Database Schema Requirements

### Supported PostgreSQL Features

- **All standard data types**: varchar, text, integer, boolean, json, etc.
- **Constraints**: NOT NULL, PRIMARY KEY, FOREIGN KEY, CHECK constraints  
- **Indexes**: Automatically detected but not included in config
- **Views**: Treated as read-only tables
- **Schemas**: Currently supports `public` schema

### Unsupported Features

- **Custom types**: Enum types treated as strings
- **Array columns**: Detected but may need manual handling
- **Materialized views**: Not automatically detected
- **Partitioned tables**: Treated as regular tables

## 🔍 Troubleshooting

### Common Issues

**1. Connection Errors**
```bash
❌ Error: connection to server at "localhost" (127.0.0.1), port 5432 failed
```
**Solution:** Ensure database is running and connection string is correct in `.env`

**2. Permission Errors**  
```bash
❌ Error: permission denied for schema information_schema
```
**Solution:** Ensure database user has SELECT permissions on `information_schema`

**3. Missing Tables**
```bash
📋 Found 0 tables
```
**Solution:** Check if you're connected to the correct database and schema

**4. Type Mapping Warnings**
```bash
⚠️  Unknown data type: custom_enum (udt: custom_enum) - defaulting to 'string'
```
**Solution:** This is expected for custom types. Add custom type mapping if needed.

### Debug Mode

Enable verbose output for detailed debugging:

```bash
python db_config_tool.py generate --verbose --output debug_config.json
```

This will show:
- SQL queries being executed
- Table analysis details
- Type mapping decisions
- Configuration generation steps

## 📊 Performance Considerations

### Database Impact

- **Read-only operations**: Tool only performs SELECT queries
- **Minimal load**: Uses efficient information_schema queries
- **Connection pooling**: Single connection for entire operation
- **Transaction safety**: No data modification operations

### Large Schema Handling

For databases with many tables:

```bash
# Generate config for specific tables only (future enhancement)
python db_config_tool.py generate --tables users,games,puzzles --output partial_config.json
```

## 🔮 Future Enhancements

### Planned Features

1. **Selective table introspection**: Target specific tables or schemas
2. **Custom endpoint generation**: Beyond standard CRUD operations
3. **API documentation generation**: OpenAPI/Swagger spec generation
4. **Schema migration detection**: Track and report schema changes
5. **Multiple database support**: MySQL, SQLite, etc.
6. **Configuration templates**: Predefined patterns for common scenarios

### Extension Points

The tool is designed to be extensible:

```python
# Custom type mapper
class CustomTypeMapper:
    def map_type(self, pg_type: str) -> str:
        # Custom logic for specific types
        if pg_type == 'my_custom_enum':
            return 'string'
        return default_mapping.get(pg_type, 'string')

# Custom endpoint generator  
class CustomEndpointGenerator:
    def generate_endpoints(self, table_info: TableInfo) -> List[Dict]:
        # Generate custom endpoint patterns
        pass
```

## 🧪 Testing

### Unit Tests

```bash
# Run unit tests (when available)
python -m pytest tests/

# Test specific modules
python -m pytest tests/test_schema_introspector.py
python -m pytest tests/test_config_validator.py
```

### Integration Tests

```bash
# Test against live database
python db_config_tool.py validate --config test_configs/valid_config.json
python db_config_tool.py validate --config test_configs/invalid_config.json
```

## 🤝 Contributing

### Development Setup

```bash
cd tools/backend-tools/database-introspection

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt  # When available

# Run code formatting
black *.py
flake8 *.py
```

### Adding New Features

1. **New introspection capabilities**: Extend `SchemaIntrospector`
2. **Custom validation rules**: Add to `ConfigValidator`
3. **New output formats**: Extend `ConfigGenerator`
4. **Additional database types**: Update type mapping

## 📄 License

This tool is part of the Chess Training Platform project. All rights reserved.

---

## 📞 Support

### Getting Help

1. **Check this README** for common solutions
2. **Review the validation output** - it's usually quite specific
3. **Enable verbose mode** for detailed debugging information
4. **Test with a simple configuration** to isolate issues

### Reporting Issues

When reporting problems, please include:

- Command used
- Complete error message
- Database schema details (table structure)
- Configuration file being validated
- PostgreSQL version

---

**Remember:** This tool is designed to eliminate schema drift and ensure your API configurations always match your actual database structure. Regular use in your development workflow will prevent the configuration sync issues that cause null constraint violations and API failures! 🚀

## 🎯 Real-World Example

Here's how this tool solves the exact problem we encountered:

### The Problem
```bash
# API test failure
❌ 400 Bad Request: null value in column "password_hash" violates not-null constraint
```

### The Solution
```bash
# 1. Validate current config to see the problem
python db_config_tool.py validate 
# Result: Shows missing required field 'password_hash'

# 2. Generate correct config from database  
python db_config_tool.py generate --output corrected_config.json

# 3. Use corrected config with payload generator
cd ../payload-generator
python payload_generator.py --config ../database-introspection/corrected_config.json

# 4. Run API tests - they now pass! ✅
```

This demonstrates the complete workflow from problem identification to resolution! 🎊