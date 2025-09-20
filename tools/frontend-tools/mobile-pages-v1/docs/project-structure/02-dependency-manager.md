# Dependency Manager: modules/dependency_manager.py

## Overview
Manages creation of missing project dependencies including hooks, components, root files, and static templates. Orchestrates the resolution and creation of all static template dependencies required by dynamic page generation.

## Imports

### Standard Library
- `pathlib.Path` - File path handling
- `typing.Dict` - Type hints
- `subprocess` - External process execution
- `sys` - System operations
- `shutil` - File operations
- `json` - JSON file handling
- `re` - Regular expressions for import analysis

### Local Modules
- `config` - ProjectCapabilities, GenerationContext
- `template_engine` - TemplateEngine for template rendering
- `file_writer` - FileWriter for file operations

## Class: DependencyManager

### Constructor
```python
def __init__(self, template_engine: TemplateEngine, file_writer: FileWriter)
```
- Stores references to template engine and file writer
- No initialization logic beyond parameter storage

## Core Dependency Creation Methods

### ensure_use_page_data_hook(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Creates usePageData hook if it doesn't exist
**Path:** `src/hooks/core/usePageData.ts`
**Template:** `dependencies/use-page-data-hook.ts.template`
**Behavior:** Skips if file already exists, renders template with DependencyManager variables

### ensure_data_table_component(context: GenerationContext)
**Parameters:** `context` - Generation context  
**Purpose:** Creates DataTable component if it doesn't exist
**Path:** `src/components/ui/DataTable.tsx`
**Template:** `dependencies/data-table-component.tsx.template`
**Behavior:** Skips if file already exists, renders template with DependencyManager variables

### ensure_all_dependencies(context: GenerationContext, required_templates: set = None)
**Parameters:**
- `context` - Generation context
- `required_templates` - Set of template paths to create (optional)
**Purpose:** Main orchestration method for ensuring all dependencies exist
**Calls:**
- `ensure_use_page_data_hook()` - Always create if missing
- `ensure_data_table_component()` - Only if capabilities indicate it's missing
- `ensure_static_components()` - Create static template dependencies

## Root File Management Methods

### validate_and_create_root_files(context: GenerationContext, force: bool = False)
**Parameters:**
- `context` - Generation context
- `force` - Whether to overwrite existing files
**Purpose:** Creates missing root configuration files
**Files Managed:**
- `index.html` - Basic HTML template (manual creation)
- `vite.config.ts` - Vite configuration (manual creation)
- `tsconfig.json` - TypeScript configuration (skipped if exists)
- `tsconfig.node.json` - Node TypeScript configuration (manual creation)
- `src/main.tsx` - Application entry point (from template)
- `src/App.tsx` - Main App component (from template)
- `src/App.css` - Application styles (from template)
- `src/index.css` - Global styles (from template)
- `src/vite-env.d.ts` - Vite type definitions (from template)
**Behavior:** Uses templates when available, manual creation for others, respects force flag

### _create_manual_root_file(file_path: Path, context: GenerationContext)
**Parameters:**
- `file_path` - Path to file to create
- `context` - Generation context
**Purpose:** Creates root files that don't have templates
**Files Created:**
- `index.html` - Standard React HTML template
- `vite.config.ts` - React + path alias configuration
- `tsconfig.node.json` - Node configuration for Vite

### _update_package_json(file_path: Path)
**Parameters:** `file_path` - Path to package.json
**Purpose:** Updates package.json with required scripts and dependencies
**Status:** Method exists but not called (commented out in root files list)
**Dependencies Added:** React ecosystem, TypeScript, Vite, Zustand, Lucide React

## Styles Directory Management

### ensure_styles_directory(context: GenerationContext, force: bool = False)
**Parameters:**
- `context` - Generation context
- `force` - Whether to overwrite existing files
**Purpose:** Copies all styles from static templates to project
**Source:** `template_engine.static_dir/styles`
**Target:** `context.frontend_root/src/styles`
**Behavior:** 
- Recursively copies all files and subdirectories
- Processes `.template` files through template engine
- Copies non-template files directly
- Respects force flag for overwriting

## Static Template Management

### ensure_static_components(context: GenerationContext, required_templates: set = None)
**Parameters:**
- `context` - Generation context
- `required_templates` - Set of specific templates to create (optional)
**Purpose:** Creates static components from template dependencies
**Logic:**
- If `required_templates` provided: Creates only specified templates
- If not provided: Falls back to `_analyze_generated_imports()` for discovery
- **Key Behavior:** Only creates files if they don't exist (`if not output_path.exists()`)
- Renders templates with context variables for navigation support

### _template_to_output_path(template_rel_path: str, context: GenerationContext)
**Parameters:**
- `template_rel_path` - Relative path to template
- `context` - Generation context
**Purpose:** Converts template path to output file path
**Logic:** Removes `.template` extension, prepends `context.frontend_root/src/`

## Template Dependency Analysis Methods

### _analyze_generated_imports(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Recursively analyzes template imports to find all static dependencies
**Process:**
1. Gets essential templates via `_detect_required_static_templates()`
2. Recursively processes each template to find imports
3. Uses regex to find import statements
4. Converts imports to template paths via `_find_template_for_import()`
5. Returns list of (template_path, output_path) tuples

### _detect_required_static_templates(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Finds static templates referenced by dynamic templates and core templates
**Process:**
1. Scans all core templates in static directory root
2. Scans all dynamic templates recursively
3. Uses regex to find import statements in each template
4. Converts imports to static template paths via `_import_path_to_static_template()`
5. Returns list of required static template paths

### _import_path_to_static_template(import_path: str, context: GenerationContext)
**Parameters:**
- `import_path` - Import path from template file
- `context` - Generation context
**Purpose:** Converts import path to corresponding static template path
**Logic:**
- Handles relative imports starting with `../`
- Excludes dynamic dependencies (usePageData, DataTable)
- Tries various file extensions (.ts, .tsx, .js, .jsx)
- Supports index files for directory imports
- Returns None if no matching template found

### _find_template_for_import(import_path, from_template_path, static_dir)
**Parameters:**
- `import_path` - Import path to resolve
- `from_template_path` - Path of template containing the import
- `static_dir` - Static templates directory
**Purpose:** Finds static template matching an import from another template
**Logic:** Resolves relative paths and tries various extensions to find matching template

## Validation Methods

### validate_all_static_dependencies(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Validates all required static dependencies exist before generation
**Returns:** Dictionary with validation results including missing templates and dependencies
**Process:**
1. Gets required templates via `_get_required_templates_for_generation()`
2. Validates each template exists
3. Validates dependencies of existing templates via `_analyze_generated_imports()`

### validate_dependencies(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Validates that core dependencies exist and are accessible
**Checks:**
- usePageData hook existence
- DataTable component existence
- Page hooks (if capabilities indicate they should exist)
- Mobile hook (if capabilities indicate it should exist)
**Returns:** Dictionary mapping dependency names to existence status

### get_missing_dependencies(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Gets list of missing dependency names
**Implementation:** Calls `validate_dependencies()` and filters for non-existent items

## External Integration Methods

### regenerate_index_files(frontend_root: Path)
**Parameters:** `frontend_root` - Project root directory
**Purpose:** Executes external index generator script
**Script Path:** `../index-generator-v2/index_generator.py`
**Execution:** Runs as subprocess with src directory as argument
**Error Handling:** Captures and reports subprocess output and errors

## Utility Methods

### create_missing_directories(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Creates required directory structure
**Directories Created:**
- Standard page/component directories from context
- Core hook directories (`src/hooks/core`)
- UI component directories (`src/components/ui`)
- Store directories (`src/stores`)
- Type directories (`src/types/core`)
- Chess component directories (`src/components/chess`)

### _get_required_templates_for_generation(context: GenerationContext)
**Parameters:** `context` - Generation context
**Purpose:** Determines specific templates needed based on generation context
**Logic:**
- Child page generation: Selects mobile or regular child templates
- Parent page generation: Selects standard parent templates
- Upgrades wrapper templates based on capabilities
- Analyzes each selected template for static dependencies
**Returns:** List of required template paths

### _analyze_template_imports(template_path: Path, context: GenerationContext)
**Parameters:**
- `template_path` - Path to template file
- `context` - Generation context
**Purpose:** Analyzes specific template file for static dependencies
**Implementation:** Uses regex to find import statements and converts to static template paths

## Lessons Learned

### Questions Answered from Code Analysis:

**✅ How exactly does the DependencyManager decide which static templates to copy?**
- Uses recursive import analysis starting from essential templates via `_detect_required_static_templates()`
- Analyzes both core templates (static directory root) and all dynamic templates
- Uses regex pattern matching to find import statements in template files
- Converts import paths to static template paths via `_import_path_to_static_template()`
- Builds complete dependency tree by recursively processing discovered templates

**✅ What's the difference between `ensure_all_dependencies()` and `ensure_static_components()`?**
- `ensure_all_dependencies()`: Main orchestration method that calls multiple dependency creation methods
- `ensure_static_components()`: Specific method that creates static template files only
- Flow: `ensure_all_dependencies()` → `ensure_use_page_data_hook()` → `ensure_data_table_component()` → `ensure_static_components()`

**✅ When do static templates get copied vs when do they get skipped?**
- Static templates are copied during `ensure_static_components()` execution
- Templates are skipped if their output file already exists: `if not output_path.exists()`
- The `force` flag in other methods doesn't apply to static template creation
- Templates are rendered with context variables for navigation support

**✅ Why does `ensure_static_components()` check `if not output_path.exists()` - is this preventing overwrites?**
- **YES - This is the root cause of the navigation generation issue**
- The check prevents overwriting existing files to avoid destroying user modifications
- Navigation files are created first by static templates, then navigation generation cannot overwrite them
- This architectural decision prioritizes file preservation over dynamic updates

### Key Architectural Insights:

**Template Processing Architecture:**
1. **Dependency Discovery**: Recursive import analysis of templates to build dependency trees
2. **Static Template Creation**: Creates files only if they don't exist (no overwrite)
3. **Dynamic Template Creation**: Page generators create specific page files
4. **Navigation Generation**: Attempts to overwrite existing navigation files (fails due to #2)

**Import Resolution Logic:**
- Starts from essential templates (core + dynamic)
- Uses regex to parse import statements: `r'import.*?from\s+[\'"]([^\'"]+)[\'"]'`
- Converts relative imports (`../`) to static template paths
- Excludes dynamic dependencies (usePageData, DataTable) from static template validation
- Supports multiple file extensions and index files

**File Creation Behavior:**
- **Root Files**: Respects `force` flag for overwriting existing files
- **Styles**: Respects `force` flag for overwriting existing files  
- **Static Templates**: Never overwrites existing files (`if not output_path.exists()`)
- **Hook/Components**: Skips creation if files already exist

**Template Variable Flow:**
- Context variables flow from GenerationContext to template rendering
- Variables support navigation-specific substitution during static template rendering
- Template engine renders with `is_static=True` flag for static templates