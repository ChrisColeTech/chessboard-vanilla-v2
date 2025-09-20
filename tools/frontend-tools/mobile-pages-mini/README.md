# Mobile Pages Mini - Template-Based Page Generator

## Overview

Mobile Pages Mini is a streamlined version of the Template-Based Page Generator v2 that eliminates massive static file copying while maintaining full integration functionality. It creates React pages using only dynamic templates, avoiding the copying of 200+ static template files while preserving all sophisticated integration features.

## Key Features

### ✅ **Mini Version Benefits**
- **No Static File Copying**: Avoids copying 200+ static template files
- **Dynamic Templates Only**: Uses only essential dynamic templates for generation
- **Full Integration Features**: Maintains complete action registry, container integration, hook management
- **Sophisticated Functionality**: All advanced features without massive file operations

### ✅ **Architecture Improvements**
- **No Parent Wrappers**: Parents are direct tab targets (fixes architectural flaw)
- **Proper Phase 2 Mobile Switching**: Single wrapper per child with internal mobile/desktop switching
- **Dynamic Template Generation**: Uses NavigationGenerator for dynamic file creation
- **Adaptive Template Selection**: Based on detected project capabilities

### ✅ **Code Quality**
- **Single Responsibility Principle**: Each module handles one specific concern
- **Complete Integration System**: Action registry, container integration, hook management
- **Domain-Driven Design**: Clear boundaries between template engine, project detection, file operations
- **Comprehensive Testing**: Unit and integration tests for all components

### ✅ **Developer Experience**
- **Project-Agnostic**: Works with any React/TypeScript project structure
- **Automatic Capability Detection**: Adapts to available hooks and components
- **Streamlined Operations**: Fast generation without massive file copying
- **Comprehensive Validation**: Clear error messages with actionable guidance

## Project Structure

```
mobile-pages-mini/
├── main.py                              # ✅ Main CLI entry point
├── modules/                             # ✅ Complete modules from v2
│   ├── config.py                        # PageConfig and data structures
│   ├── template_engine.py               # Template loading and rendering
│   ├── project_detector.py              # Project capability detection
│   ├── file_writer.py                   # File writing with validation
│   ├── dependency_manager.py            # Streamlined dependency management (no static copying)
│   ├── parent_generator.py              # Parent page generation
│   ├── child_generator.py               # Child page generation
│   ├── action_registry_manager.py       # Action registration system
│   ├── container_integrator.py          # Container integration features
│   ├── hook_integrator.py               # Hook integration functionality
│   ├── integration_validator.py         # Integration validation
│   ├── error_handling.py                # Comprehensive error handling
│   └── validation.py                    # Core validation framework
├── templates/                           # ✅ Dynamic templates only (no static)
│   └── dynamic/                         # Only dynamic template files
│       ├── nav/                         # Navigation templates
│       ├── pages/                       # Page templates
│       ├── components/                  # Component templates
│       ├── hooks/                       # Hook templates
│       ├── actions/                     # Action templates
│       ├── instructions/                # Instruction templates
│       └── dependencies/                # Dependency templates
├── tests/                               # ✅ Test suites
├── migration/                           # ✅ Migration utilities
└── docs/                                # ✅ Comprehensive documentation
    └── 00-changes-from-v2.md            # Documentation of mini version changes
```

## Quick Start

> **Note**: Mobile Pages Mini is ready to use with full functionality. The only difference from v2 is the elimination of static file copying while maintaining all sophisticated features.

### Installation
```bash
cd /path/to/mobile-pages-mini
npm install  # Installs package.json for simplified usage
```

### Environment File System
The tool automatically saves your frontend location after first use:

#### First Run (Required)
```bash
npm run mobile -- --frontend-root /path/to/your/frontend analyze
```
*Shows: "📁 Using specified frontend root: /path/to/your/frontend"*  
*Shows: "💾 Frontend location saved to: /path/to/mobile-pages-mini/.env"*

#### Subsequent Runs (Automatic)
```bash
npm run mobile -- analyze
```
*Shows: "📁 Using saved frontend location: /path/to/your/frontend"*  
*Shows: "(Use --frontend-root to specify a different location)"*

### Create Parent Page
```bash
npm run mobile -- parent TestSection
```
*Automatically registers page in `pages.config.json` and regenerates navigation files*

### Create Child Page
```bash  
npm run mobile -- child LayoutTest --parent testsection
```
*Automatically registers page in `pages.config.json` and regenerates navigation files*

### Create Parent with Children (One-Shot)
```bash
npm run mobile -- create WorkflowTest --children ChildPage1 ChildPage2
```
*Creates parent page 'WorkflowTest' with children 'ChildPage1' and 'ChildPage2' (all mobile-enabled)*

### Note on Mobile Support
All pages are generated with mobile variants by default in this version. The `--mobile` flag is not needed.

## Enhanced Workflow with Config Management

### Central Configuration
The generator now maintains a central page registry in `pages.config.json` at your project root:
```json
{
  "version": "1.0.0",
  "pages": {
    "testsection": {
      "id": "testsection", 
      "name": "TestSection",
      "type": "parent",
      "icon": "Settings",
      "component_name": "TestSectionPage"
    }
  }
}
```

### Auto-Generated Navigation Files
After each page creation, navigation files are automatically generated dynamically:
- `src/components/layout/types.ts` - TypeScript types
- `src/components/layout/TabBar.tsx` - Navigation component  
- `src/App.tsx` - Main app routing
- `src/stores/appStore.ts` - App state management

### Integrated Workflow (Mini Version)
1. **Create page files** (using dynamic templates only)
2. **Register in config** (central page registry)
3. **Generate navigation dynamically** (via NavigationGenerator)
4. **Full integration** (action registry, container integration, hook management)
5. **Skip static file copying** (mini version benefit)

## Generated File Structure

### Parent Page Generation (5 files):
```
src/pages/testsection/
├── TestSectionPage.tsx              # Main routing page (NO WRAPPER!)
└── TestSectionMainPage.tsx          # Landing page

src/hooks/testsection/
└── useTestSectionActions.ts         # Navigation hook

src/constants/actions/pages/
└── testsection.ts                   # Action sheet config

src/services/instructions/pages/
└── testsection.ts                   # Instructions config
```

### Child Page Generation (4-5 files):
```
src/pages/testsection/
├── LayoutTestPage.tsx               # Desktop child page  
└── MobileLayoutTestPage.tsx         # Mobile child page (if --mobile)

src/components/testsection/
└── LayoutTestPageWrapper.tsx        # Single wrapper with mobile switching

src/constants/actions/pages/
└── layouttest.ts                    # Action sheet config

src/services/instructions/pages/  
└── layouttest.ts                    # Instructions config
```

## Architecture Compliance

### ✅ **Phase 2 Mobile Switching Architecture**
```
Tab Click → Parent Page → Child Wrapper → useIsMobile() → Mobile/Desktop Page
                   ↑              ↑              ↑
              Child routing   Context hooks   Device switching
```

### ❌ **Old Architecture (Eliminated)**
```
Tab Click → Parent Wrapper → Parent Page → Separate Mobile Actions
                ↑                              ↑
        Unnecessary layer              Duplicate configurations
```

### **Key Architectural Rules**
1. **No Parent Wrappers**: Parents apply hooks directly and are tab targets
2. **Wrapper-Based Mobile Switching**: Child wrappers handle device detection internally  
3. **Shared PageId**: Mobile/desktop variants use same context (instructions/actions)
4. **Single Wrapper Per Child**: One wrapper handles both mobile detection and context

## Template System

### **Adaptive Template Selection**
The generator detects your project's capabilities and selects appropriate templates:

```python
# Full hooks + mobile support
if has_page_hooks and has_mobile_hook and mobile_requested:
    template = 'child-wrapper-full-hooks.tsx.template'

# Page hooks only  
elif has_page_hooks and not has_mobile_hook:
    template = 'child-wrapper-basic-hooks.tsx.template'

# Minimal support
else:
    template = 'child-wrapper-no-hooks.tsx.template'
```

### **Project Capability Detection**
```python
ProjectCapabilities(
    has_page_hooks=True,      # usePageInstructions, usePageActions exist
    has_mobile_hook=True,     # useIsMobile exists
    has_data_table=True,      # DataTable component exists  
    existing_parents=['uitests', 'layout'],
    existing_children={'uitests': ['dragtest', 'audiotest']}
)
```

## Mini Version vs V2 Comparison

### **What's Different in Mini Version**
| Feature | v2 Version | Mini Version |
|---------|------------|--------------|
| **Static Templates** | ❌ Copies 200+ static template files | ✅ **Skips static file copying** |
| **Template Processing** | ❌ Complex static template analysis | ✅ **Dynamic templates only** |
| **Integration Features** | ✅ Complete integration system | ✅ **Same integration system** |
| **Action Registry** | ✅ Full action management | ✅ **Same action management** |
| **Container Integration** | ✅ Complete container features | ✅ **Same container features** |
| **Hook Integration** | ✅ Full hook management | ✅ **Same hook management** |
| **Navigation Generation** | ✅ NavigationGenerator integration | ✅ **Same NavigationGenerator** |
| **Error Handling** | ✅ Comprehensive error handling | ✅ **Same error handling** |
| **Validation** | ✅ Complete validation framework | ✅ **Same validation framework** |

### **Key Benefits of Mini Version**
- ✅ **No Static File Copying**: Eliminates copying 200+ template files
- ✅ **Faster Generation**: Streamlined operations without massive file copying
- ✅ **Same Functionality**: All sophisticated integration features preserved
- ✅ **Clean Architecture**: All the advanced modules from v2
- ✅ **Dynamic Navigation**: Uses NavigationGenerator for all navigation files

## Implementation Progress

✅ **IMPLEMENTATION COMPLETE** - All 7 phases implemented and tested:

- ✅ **Phase 1**: Core Infrastructure & Template Engine (config, template_engine, project_detector, file_writer, variable_generator)
- ✅ **Phase 2**: File Operations & Dependency Management (dependency_manager with shared utilities integration)  
- ✅ **Phase 3**: Parent Page Generation System (parent_generator with routing and dependency creation)
- ✅ **Phase 4**: Child Page Generation & Adaptive Wrappers (child_generator, wrapper_selector with 4 wrapper types)
- ✅ **Phase 5**: Parent Routing Updates & Integration (routing_updater with dynamic parent injection)
- ✅ **Phase 6**: CLI Interface & Comprehensive Validation (main.py, validation.py, error_handling.py)
- ✅ **Phase 7**: Testing, Migration & Documentation (integration tests, migration scripts, comprehensive documentation)

See [Implementation Plan](docs/02-comprehensive-implementation-plan.md) for detailed phase breakdown.

## Documentation

### **Design Documents**
- [00-comprehensive-redesign-plan.md](docs/00-comprehensive-redesign-plan.md) - Analysis of current generators and redesign rationale
- [01-architecture-and-template-system.md](docs/01-architecture-and-template-system.md) - Complete architecture understanding and template system design
- [02-comprehensive-implementation-plan.md](docs/02-comprehensive-implementation-plan.md) - 7-phase implementation plan with detailed deliverables

### **User Guides**
- [03-migration-guide.md](docs/03-migration-guide.md) - Complete migration guide from old generators to template-based system
- [04-troubleshooting-guide.md](docs/04-troubleshooting-guide.md) - Comprehensive troubleshooting and diagnostic guide

### **References**
- [Navigation & Action Sheets Architecture](../../../docs/47-navigation-action-sheets-architecture.md) - Core navigation patterns this generator implements

## Benefits Over Previous Generators

### **Architectural Fixes**
| Issue | Old Generators | Mobile Pages Mini |
|-------|----------------|-------------------|
| Parent Wrappers | ❌ Created unnecessary wrappers | ✅ Parents are direct tab targets |
| Mobile Switching | ❌ Parent handles mobile logic | ✅ Child wrappers handle internally |  
| Code Duplication | ❌ Hard-coded template strings | ✅ Dynamic .template files |
| Project Compatibility | ❌ Hard-coded assumptions | ✅ Adaptive capability detection |
| Maintenance | ❌ 992 + 775 lines of string manipulation | ✅ Clean modular architecture |
| **Config Management** | ❌ No central page registry | ✅ **Central `pages.config.json`** |
| **Navigation Updates** | ❌ Manual navigation maintenance | ✅ **Auto-generated navigation files** |
| **Static File Copying** | ❌ N/A (no template system) | ✅ **No massive file copying (mini benefit)** |

### **Developer Experience**
- **Single Generator**: Replaces both `dynamic_page_generator.py` and `page_generator.py`
- **No Manual Steps**: Fully automated with comprehensive validation
- **Central Config**: All pages tracked in `pages.config.json` for visibility
- **Dynamic Navigation**: Navigation files generated dynamically (no static copying)
- **Fast Generation**: Streamlined operations without massive file copying
- **Clear Error Messages**: Actionable guidance for common issues
- **Full Integration**: Complete action registry, container, and hook management
- **Migration Tools**: Automated migration from old generators

## Testing Strategy

### **Unit Tests**
- Template engine (loading, rendering, variable substitution)
- Project detection (capability scanning, hook detection)
- File operations (writing, validation, backups)
- Generators (parent/child generation, routing updates)

### **Integration Tests**  
- End-to-end generation workflows
- Multi-project compatibility testing
- Migration from old generators
- Template system validation

## Migration from Old Generators

The template-based generator provides:
- **Backward Compatibility**: Existing generated code continues to work
- **Migration Tools**: Automated detection and fixing of architectural issues
- **Deprecation Warnings**: Clear guidance when old generators are used
- **Documentation**: Step-by-step migration guides

## Contributing

This project follows:
- **Single Responsibility Principle**: Each module has one clear purpose
- **Domain-Driven Design**: Clear boundaries between concerns  
- **Test-Driven Development**: Comprehensive test coverage
- **Template-First**: All code generation uses .template files

## Usage Examples

### Basic Usage (NPM Commands)

```bash
# First time setup - specify frontend root
npm run mobile -- --frontend-root /path/to/frontend analyze

# Subsequent runs - uses saved location automatically
npm run mobile -- analyze

# Create parent page
npm run mobile -- parent Settings

# Create child page
npm run mobile -- child UserProfile --parent Settings

# Create parent with children in one command
npm run mobile -- create Dashboard --children Analytics Reports

# Validate generated files
npm run mobile -- validate

# Override saved location
npm run mobile -- --frontend-root /different/path analyze
```

### Direct Python Usage (Advanced)

```bash
# Analyze project structure and capabilities
python main.py --frontend-root /path/to/frontend analyze

# Create parent page
python main.py parent Settings

# Create child page
python main.py child UserProfile --parent Settings

# Create parent with children in one command
python main.py create Dashboard --children Analytics Reports

# Validate generated files
python main.py validate
```

### Flexible Argument Order
Global flags can be placed before or after the subcommand:
```bash
# Both work perfectly
npm run mobile -- --frontend-root /path analyze
npm run mobile -- analyze --frontend-root /path

# Mixed order also works
npm run mobile -- --verbose parent TestPage --frontend-root /path
npm run mobile -- create Dashboard --children Analytics --force
```

### Migration from Old Generators

```bash
# Analyze what needs migration
python migration/migrate_from_old_generators.py . --analyze-only

# Preview migration (dry run)
python migration/migrate_from_old_generators.py . --dry-run

# Execute migration
python migration/migrate_from_old_generators.py . --execute
```

### Testing

```bash
# Run all unit tests
python run_all_tests.py

# Run integration tests
python tests/integration/test_full_generation.py
python tests/integration/test_project_compatibility.py
```

## Status

✅ **PRODUCTION READY** - Complete Mini Implementation

This represents a streamlined version of the Template-Based Page Generator v2 that eliminates massive static file copying while maintaining all sophisticated integration features. The mini version provides:

- **Same Architecture**: Complete Phase 2 Mobile Switching Architecture implementation
- **Full Integration**: Action registry, container integration, hook management
- **Dynamic Generation**: Uses NavigationGenerator for all navigation files  
- **No Static Copying**: Avoids copying 200+ static template files
- **Fast Operations**: Streamlined generation without massive file operations
- **Complete Validation**: Full error handling and validation framework

Perfect for projects that need the full power of v2 without the overhead of massive static template copying.