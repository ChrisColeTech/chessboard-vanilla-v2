# Template-Based Page Generator v2

## Overview

The Template-Based Page Generator v2 is a complete rewrite of the original page generators, implementing proper Phase 2 Mobile Switching Architecture with clean separation of concerns and template-based code generation.

## Key Features

### ✅ **Architecture Improvements**
- **No Parent Wrappers**: Parents are direct tab targets (fixes architectural flaw)
- **Proper Phase 2 Mobile Switching**: Single wrapper per child with internal mobile/desktop switching
- **Template-Based Generation**: Maintainable `.template` files instead of hard-coded strings
- **Adaptive Template Selection**: Based on detected project capabilities

### ✅ **Code Quality**
- **Single Responsibility Principle**: Each module handles one specific concern
- **Don't Repeat Yourself**: Templates eliminate code duplication
- **Domain-Driven Design**: Clear boundaries between template engine, project detection, file operations
- **Comprehensive Testing**: Unit and integration tests for all components

### ✅ **Developer Experience**
- **Project-Agnostic**: Works with any React/TypeScript project structure
- **Automatic Capability Detection**: Adapts to available hooks and components
- **Comprehensive Validation**: Clear error messages with actionable guidance
- **Dry-Run Mode**: Safe testing without file modifications

## Project Structure

```
mobile-pages-v2/
├── main.py          # Main CLI entry point (to be created)
├── modules/                             # Core modules (to be created)
│   ├── config.py                        # PageConfig and data structures
│   ├── template_engine.py               # Template loading and rendering
│   ├── project_detector.py              # Project capability detection
│   ├── file_writer.py                   # File writing with validation
│   ├── dependency_manager.py            # Missing component creation
│   ├── parent_generator.py              # Parent page generation
│   ├── child_generator.py               # Child page generation
│   └── ...                              # Additional modules per implementation plan
├── templates/                           # ✅ Template files (16 files)
│   ├── pages/
│   ├── components/
│   ├── hooks/
│   ├── actions/
│   ├── instructions/
│   └── dependencies/
├── tests/                               # Test suites (to be created)
├── migration/                           # Migration utilities (to be created)
└── docs/                                # ✅ Comprehensive documentation
    ├── 00-comprehensive-redesign-plan.md
    ├── 01-architecture-and-template-system.md
    └── 02-comprehensive-implementation-plan.md
```

## Quick Start

> **Note**: This is the project structure after full implementation. See [Implementation Plan](docs/02-comprehensive-implementation-plan.md) for development phases.

### Create Parent Page
```bash
python main.py parent TestSection --description "Test section for UI components"
```
*Automatically registers page in `pages.config.json` and regenerates navigation files*

### Create Child Page
```bash  
python main.py child LayoutTest --parent testsection --mobile --description "Test responsive layouts"
```
*Automatically registers page in `pages.config.json` and regenerates navigation files*

### Create Child Page (Desktop Only)
```bash
python main.py child DataTest --parent testsection --description "Test data visualization"  
```
*Automatically registers page in `pages.config.json` and regenerates navigation files*

### Create Parent with Children (One-Shot)
```bash
python main.py create WorkflowTest --children ChildPage1 ChildPage2 --mobile
```
*Creates parent page 'WorkflowTest' with children 'ChildPage1' and 'ChildPage2', all with mobile variants*

### Create Parent with Children (Desktop Only)
```bash
python main.py create TestSection --children DataTest LayoutTest
```
*Creates parent page 'TestSection' with children 'DataTest' and 'LayoutTest' (desktop only)*

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
After each page creation, navigation files are automatically regenerated:
- `src/components/layout/types.ts` - TypeScript types
- `src/components/layout/TabBar.tsx` - Navigation component  
- `src/components/layout/App.tsx` - Main app routing

### Integrated Workflow
1. **Create page files** (existing behavior)
2. **Register in config** (new - central page registry)
3. **Regenerate navigation** (new - dynamic navigation from config)
4. **Replace static templates** (new - generated files replace static ones)

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
| Issue | Old Generators | Template-Based v2 |
|-------|----------------|-------------------|
| Parent Wrappers | ❌ Created unnecessary wrappers | ✅ Parents are direct tab targets |
| Mobile Switching | ❌ Parent handles mobile logic | ✅ Child wrappers handle internally |  
| Code Duplication | ❌ Hard-coded template strings | ✅ Reusable .template files |
| Project Compatibility | ❌ Hard-coded assumptions | ✅ Adaptive capability detection |
| Maintenance | ❌ 992 + 775 lines of string manipulation | ✅ Clean modular architecture |
| **Config Management** | ❌ No central page registry | ✅ **Central `pages.config.json`** |
| **Navigation Updates** | ❌ Manual navigation maintenance | ✅ **Auto-generated navigation files** |
| **Static Templates** | ❌ Static files get stale | ✅ **Dynamic generation from config** |

### **Developer Experience**
- **Single Generator**: Replaces both `dynamic_page_generator.py` and `page_generator.py`
- **No Manual Steps**: Fully automated with comprehensive validation
- **Central Config**: All pages tracked in `pages.config.json` for visibility
- **Auto-Navigation**: Navigation files regenerated after every page creation
- **Clear Error Messages**: Actionable guidance for common issues
- **Dry-Run Mode**: Test generation without file modifications
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

### Basic Usage

```bash
# Analyze project structure and capabilities
python main.py analyze

# Create parent page
python main.py parent Settings

# Create child page with mobile variant
python main.py child UserProfile --parent Settings --mobile

# Create parent with children in one command (mobile variants for all children)
python main.py create Dashboard --children Analytics Reports --mobile

# Create parent with children (desktop only)
python main.py create TestSuite --children UnitTests IntegrationTests

# Validate generated files
python main.py validate
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

✅ **PRODUCTION READY** - Complete 7-phase implementation

This represents a complete architectural rewrite focused on eliminating technical debt while implementing proper Phase 2 Mobile Switching Architecture patterns. The system has been comprehensively tested and includes full migration support from old generators.