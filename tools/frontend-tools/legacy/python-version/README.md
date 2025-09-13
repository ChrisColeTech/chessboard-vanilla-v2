# Python Index Generator

A modular Python rewrite of the JavaScript TypeScript index generator with separated concerns and clean architecture.

## Architecture

The Python version separates functionality into distinct modules:

### Core Modules

- **`index_generator.py`** - Main orchestrator class that coordinates all other modules
- **`export_strategy.py`** - Determines export strategies (barrel vs namespaced) based on directory analysis
- **`conflict_resolver.py`** - Detects and resolves naming conflicts between exports
- **`file_analyzer.py`** - Analyzes TypeScript/JavaScript files to extract export information
- **`export_generator.py`** - Generates TypeScript export statements with aliasing
- **`validator.py`** - Validates directory structure and generated files

### Key Improvements

1. **Separation of Concerns** - Each module has a single, well-defined responsibility
2. **Type Safety** - Uses Python type hints and dataclasses for better code reliability
3. **Async Support** - Proper async/await patterns for file I/O operations
4. **Modular Design** - Easy to test, extend, and maintain individual components
5. **Clear Interfaces** - Well-defined APIs between modules

## Usage

### Command Line Interface

```bash
# Basic usage
python index_generator.py ./src/components

# Dry run to see what would be generated
python index_generator.py ./src --dry-run

# Non-recursive processing
python index_generator.py ./src/hooks --no-recursive
```

### Programmatic Usage

```python
import asyncio
from index_generator import IndexGenerator

async def generate_indices():
    generator = IndexGenerator()
    await generator.generate_index_files('./src', {
        'recursive': True,
        'dry_run': False
    })

# Run the generator
asyncio.run(generate_indices())
```

## Module Details

### ExportStrategy

Determines the best export strategy based on:
- Directory type (types, components, etc.)
- Number of subdirectories and exports
- Conflict potential analysis

### ConflictResolver

Handles export naming conflicts using strategies:
- **Explicit Alias** - Rename conflicting exports with module prefixes
- **Namespace** - Group exports under module namespaces
- **Skip** - Skip conflicting modules entirely

### FileAnalyzer

Extracts export information from TypeScript files:
- Default exports
- Named exports
- Type-only exports
- Multiline export blocks

### ExportGenerator

Generates clean TypeScript export statements:
- Proper type vs value export separation
- Conflict resolution with aliasing
- Deduplication of duplicate exports

### Validator

Comprehensive validation system:
- Pre-generation structure validation
- Post-generation file validation
- Circular reference detection
- Export conflict warnings

## Features

- ✅ **Modular Architecture** - Clean separation of concerns
- ✅ **Type Safety** - Python type hints throughout
- ✅ **Async I/O** - Non-blocking file operations
- ✅ **Conflict Resolution** - Automatic handling of naming conflicts
- ✅ **Validation** - Comprehensive pre/post validation
- ✅ **Special Cases** - Handles types directories and other edge cases
- ✅ **Dry Run Support** - Preview generation without writing files
- ✅ **CLI Interface** - Command-line tool with options

## Comparison with JavaScript Version

| Feature | JavaScript | Python |
|---------|------------|--------|
| Modularity | ❌ Monolithic | ✅ Separated modules |
| Type Safety | ❌ Basic JSDoc | ✅ Full type hints |
| Async Support | ✅ Promises | ✅ async/await |
| Testing | ❌ Hard to test | ✅ Modular & testable |
| Maintainability | ❌ Complex | ✅ Clean architecture |
| Extensibility | ❌ Tightly coupled | ✅ Pluggable modules |