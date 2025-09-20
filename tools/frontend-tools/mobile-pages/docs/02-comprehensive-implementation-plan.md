# Template-Based Generator - Comprehensive Implementation Plan

## Executive Summary

This document outlines the comprehensive implementation plan for replacing the existing page generators with a template-based system that follows proper Phase 2 Mobile Switching Architecture, eliminates architectural flaws, and implements clean separation of concerns through domain-driven design.

## Table of Contents

1. [Implementation Overview](#implementation-overview)
2. [Target Architecture](#target-architecture)
3. [Phase-by-Phase Implementation](#phase-by-phase-implementation)
4. [File Structure](#file-structure)
5. [Integration Points](#integration-points)
6. [Testing Strategy](#testing-strategy)
7. [Migration Strategy](#migration-strategy)

## Implementation Overview

### **Core Principles**
- **Single Responsibility Principle (SRP)**: Each module handles one specific concern
- **Don't Repeat Yourself (DRY)**: Templates eliminate code duplication
- **Domain-Driven Design**: Clear domain boundaries between template engine, project detection, file operations
- **Separation of Concerns**: Template rendering, file writing, routing updates are separate modules

### **Key Deliverables**
- Template-based generation system replacing 2 existing generators
- Elimination of architectural flaws (no parent wrappers, proper mobile switching)
- Adaptive template selection based on project capabilities
- Comprehensive validation and error handling
- Full backward compatibility with existing projects

## Target Architecture

### **Module Structure**
```
Template Engine ──► Project Detector ──► File Writer
       │                    │                 │
       ▼                    ▼                 ▼
Variable System      Capability System   Warning Headers
       │                    │                 │
       ▼                    ▼                 ▼
Template Rendering   Hook Detection    Dependency Mgmt
```

### **Data Flow**
```
CLI Input → PageConfig → Project Detection → Template Selection → Variable Generation → File Generation → Routing Updates
```

## Phase-by-Phase Implementation

### **Phase 1: Core Infrastructure & Template Engine**

**Objective**: Establish the foundational template system and project detection capabilities.

#### Files to Create:
```
mobile-pages/modules/__init__.py
mobile-pages/modules/config.py
mobile-pages/modules/template_engine.py
mobile-pages/modules/project_detector.py
mobile-pages/tests/__init__.py  
mobile-pages/tests/test_template_engine.py
mobile-pages/tests/test_project_detector.py
```

#### Files to Modify:
None (pure creation phase)

#### Integration Points:
- `templates/` directory (read-only access to .template files)
- Existing `shared/` utilities (future integration)

#### Key Deliverables:
- `PageConfig` dataclass with proper name normalization
- `TemplateEngine` class for loading and rendering templates
- `ProjectCapabilityDetector` class for scanning existing project structure
- `ProjectCapabilities` dataclass defining detected features
- Template variable substitution system
- Basic unit tests for core functionality

#### Core Components:

**PageConfig (config.py)**
```python
@dataclass
class PageConfig:
    name: str
    parent: Optional[str] = None
    mobile: bool = False
    icon: str = "Navigation" 
    description: str = ""
    # Computed properties for name normalization
```

**TemplateEngine (template_engine.py)**
```python
class TemplateEngine:
    def load_template(self, template_name: str) -> str
    def render_template(self, template_name: str, variables: Dict[str, str]) -> str
    def select_child_wrapper_template(self, config: PageConfig, capabilities: ProjectCapabilities) -> str
```

**ProjectCapabilityDetector (project_detector.py)**
```python
class ProjectCapabilityDetector:
    def detect_capabilities(self, frontend_root: Path) -> ProjectCapabilities
    def scan_existing_parents(self, frontend_root: Path) -> List[str]
    def scan_existing_children(self, frontend_root: Path) -> Dict[str, List[str]]
```

---

### **Phase 2: File Operations & Dependency Management**

**Objective**: Implement reliable file writing with warning headers and dependency management for missing components.

#### Files to Create:
```
mobile-pages/modules/file_writer.py
mobile-pages/modules/dependency_manager.py
mobile-pages/tests/test_file_writer.py
mobile-pages/tests/test_dependency_manager.py
```

#### Files to Modify:
```
mobile-pages/modules/template_engine.py  # Add dependency template support
```

#### Integration Points:
- `shared/file_utils.py` (use existing write_file_with_warning)
- `shared/import_utils.py` (use existing smart_add_import)
- `../index-generator-v2/` (call for index regeneration)
- Template files: `use-page-data-hook.ts.template`, `data-table-component.tsx.template`

#### Key Deliverables:
- `FileWriter` class with validation and warning header generation
- `DependencyManager` class for creating missing usePageData hook and DataTable component  
- Integration with existing shared utilities
- Template-based dependency creation
- File validation and safety checks

#### Core Components:

**FileWriter (file_writer.py)**
```python
class FileWriter:
    def write_file(self, file_path: Path, content: str, generator_name: str, source_file: str)
    def validate_file_content(self, content: str) -> bool
    def backup_existing_file(self, file_path: Path) -> Optional[Path]
```

**DependencyManager (dependency_manager.py)**  
```python
class DependencyManager:
    def ensure_use_page_data_hook(self, frontend_root: Path, capabilities: ProjectCapabilities)
    def ensure_data_table_component(self, frontend_root: Path, capabilities: ProjectCapabilities)
    def regenerate_index_files(self, frontend_root: Path)
```

---

### **Phase 3: Parent Page Generation System**

**Objective**: Implement complete parent page generation using the template system.

#### Files to Create:
```
mobile-pages/modules/parent_generator.py
mobile-pages/modules/variable_generator.py
mobile-pages/tests/test_parent_generator.py
mobile-pages/tests/test_variable_generator.py
```

#### Files to Modify:
```
mobile-pages/modules/template_engine.py      # Add parent template selection logic
mobile-pages/modules/dependency_manager.py  # Add parent-specific dependencies
```

#### Integration Points:
- Template files: `parent-page.tsx.template`, `parent-main-page.tsx.template`, `parent-actions.ts.template`, `parent-instructions.ts.template`, `parent-actions-hook.ts.template`
- Generated output directories: `src/pages/`, `src/hooks/`, `src/constants/actions/pages/`, `src/services/instructions/pages/`

#### Key Deliverables:
- `ParentPageGenerator` class handling complete parent page creation
- `VariableGenerator` class for template variable creation
- Dynamic navigation hook generation based on project structure
- Parent page generation without wrapper components (architectural fix)
- Template-based parent action and instruction creation

#### Core Components:

**ParentPageGenerator (parent_generator.py)**
```python
class ParentPageGenerator:
    def create_parent_page(self, config: PageConfig, capabilities: ProjectCapabilities)
    def generate_parent_files(self, config: PageConfig, variables: Dict[str, str])
    def create_navigation_hook(self, config: PageConfig, capabilities: ProjectCapabilities)
```

**VariableGenerator (variable_generator.py)**
```python
class VariableGenerator:
    def generate_parent_variables(self, config: PageConfig, capabilities: ProjectCapabilities) -> Dict[str, str]
    def generate_navigation_methods(self, config: PageConfig, capabilities: ProjectCapabilities) -> str
    def generate_return_methods(self, parent_name: str, children: List[str]) -> str
```

---

### **Phase 4: Child Page Generation & Adaptive Wrappers**

**Objective**: Implement child page generation with adaptive wrapper selection based on project capabilities.

#### Files to Create:
```
mobile-pages/modules/child_generator.py  
mobile-pages/modules/wrapper_selector.py
mobile-pages/tests/test_child_generator.py
mobile-pages/tests/test_wrapper_selector.py
```

#### Files to Modify:
```
mobile-pages/modules/template_engine.py     # Add child template selection  
mobile-pages/modules/variable_generator.py # Add child variable generation
```

#### Integration Points:
- Template files: `child-page.tsx.template`, `mobile-child-page.tsx.template`, `child-wrapper-*.tsx.template`, `child-actions.ts.template`, `child-instructions.ts.template`
- Generated output directories: `src/pages/{parent}/`, `src/components/{parent}/`, `src/constants/actions/pages/`, `src/services/instructions/pages/`

#### Key Deliverables:
- `ChildPageGenerator` class for complete child page creation
- `WrapperSelector` class for adaptive template selection based on capabilities
- Single wrapper per child with internal mobile switching (Phase 2 architecture)
- Mobile variant generation when requested
- Shared pageId between mobile/desktop variants

#### Core Components:

**ChildPageGenerator (child_generator.py)**
```python
class ChildPageGenerator:
    def create_child_page(self, config: PageConfig, capabilities: ProjectCapabilities)
    def generate_child_files(self, config: PageConfig, variables: Dict[str, str])
    def create_mobile_variant(self, config: PageConfig, capabilities: ProjectCapabilities)
```

**WrapperSelector (wrapper_selector.py)**
```python
class WrapperSelector:
    def select_wrapper_template(self, config: PageConfig, capabilities: ProjectCapabilities) -> str
    def determine_wrapper_type(self, has_page_hooks: bool, has_mobile_hook: bool, is_mobile: bool) -> WrapperType
    def generate_wrapper_variables(self, config: PageConfig, wrapper_type: WrapperType) -> Dict[str, str]
```

---

### **Phase 5: Parent Routing Updates & Integration**

**Objective**: Implement dynamic parent page routing updates using template-based injection.

#### Files to Create:
```
mobile-pages/modules/routing_updater.py
mobile-pages/templates/routing/child-route-logic.template  
mobile-pages/tests/test_routing_updater.py
```

#### Files to Modify:
```
mobile-pages/modules/child_generator.py  # Add routing update integration
mobile-pages/modules/template_engine.py # Add routing template support
```

#### Integration Points:
- Generated parent page files: `src/pages/{parent}/{Parent}Page.tsx` (modify)
- Template files: `parent-page.tsx.template` (read the {{CHILD_ROUTING_LOGIC}} placeholder)

#### Key Deliverables:
- `RoutingUpdater` class for safe parent page modification
- Template-based routing logic generation
- Dynamic import statement injection
- Proper child page routing without mobile detection in parent (Phase 2 architecture)
- Safe file modification with backup and rollback capability

#### Core Components:

**RoutingUpdater (routing_updater.py)**
```python
class RoutingUpdater:
    def add_child_route(self, parent_file: Path, config: PageConfig)
    def generate_routing_logic(self, config: PageConfig) -> str
    def inject_child_import(self, parent_content: str, config: PageConfig) -> str
    def inject_routing_condition(self, parent_content: str, config: PageConfig) -> str
```

---

### **Phase 6: CLI Interface & Comprehensive Validation**

**Objective**: Create the main CLI interface with comprehensive validation and error handling.

#### Files to Create:
```
mobile-pages/main.py  # Main CLI entry point
mobile-pages/modules/validation.py
mobile-pages/modules/error_handling.py
mobile-pages/tests/test_validation.py
mobile-pages/tests/test_cli_integration.py
```

#### Files to Modify:
```
mobile-pages/modules/config.py  # Add validation methods
All existing modules  # Add error handling integration
```

#### Integration Points:
- All previously created modules (orchestration)
- `argparse` for CLI argument parsing
- `sys` for exit codes and error reporting

#### Key Deliverables:
- Main `main.py` CLI script
- `ValidationEngine` class for input validation
- `ErrorHandler` class for consistent error reporting
- Comprehensive CLI argument parsing and validation
- Dry-run mode for safe testing
- Detailed progress reporting and logging

#### Core Components:

**Main CLI (main.py)**
```python
class TemplateBasedPageGenerator:
    def __init__(self, frontend_root: str)
    def create_parent_page(self, config: PageConfig) -> None
    def create_child_page(self, config: PageConfig) -> None
    def validate_configuration(self, config: PageConfig) -> None

def main():
    # CLI argument parsing and orchestration
```

**ValidationEngine (validation.py)**
```python
class ValidationEngine:
    def validate_page_config(self, config: PageConfig) -> List[ValidationError]  
    def validate_parent_exists(self, parent_name: str, frontend_root: Path) -> bool
    def validate_name_conflicts(self, name: str, frontend_root: Path) -> List[str]
```

---

### **Phase 7: Testing, Migration & Documentation**

**Objective**: Comprehensive testing, migration of existing projects, and complete documentation.

#### Files to Create:
```
mobile-pages/tests/integration/test_full_generation.py
mobile-pages/tests/integration/test_project_compatibility.py
mobile-pages/migration/migrate_from_old_generators.py
mobile-pages/docs/03-migration-guide.md
mobile-pages/docs/04-troubleshooting-guide.md
```

#### Files to Modify:
```
mobile-pages/dynamic_page_generator.py  # Add deprecation warnings
mobile-pages/page_generator.py         # Add deprecation warnings
mobile-pages/README.md                 # Update with new generator info
```

#### Integration Points:
- Existing generated code in target projects (analysis and migration)
- Old generator scripts (deprecation and replacement)

#### Key Deliverables:
- Complete integration test suite
- Migration script for existing projects
- Performance benchmarking and optimization
- Comprehensive documentation and troubleshooting guide
- Deprecation plan for old generators
- Final validation of architecture compliance

#### Core Components:

**Migration Tools (migration/migrate_from_old_generators.py)**
```python
class GeneratorMigrator:
    def analyze_existing_structure(self, frontend_root: Path) -> MigrationPlan
    def migrate_parent_wrappers(self, frontend_root: Path) # Remove unnecessary wrappers
    def update_mobile_switching(self, frontend_root: Path) # Fix Phase 2 architecture
```

---

## File Structure

### **Final Directory Structure**
```
mobile-pages/
├── main.py              # Main CLI entry point
├── modules/
│   ├── __init__.py                          # Package initialization
│   ├── config.py                            # PageConfig and core data structures
│   ├── template_engine.py                   # Template loading and rendering
│   ├── project_detector.py                  # Project capability detection
│   ├── file_writer.py                       # File writing with validation
│   ├── dependency_manager.py                # Missing component creation
│   ├── parent_generator.py                  # Parent page generation
│   ├── child_generator.py                   # Child page generation
│   ├── wrapper_selector.py                  # Adaptive wrapper selection
│   ├── routing_updater.py                   # Parent routing modification
│   ├── variable_generator.py                # Template variable generation
│   ├── validation.py                        # Input validation
│   └── error_handling.py                    # Error handling utilities
├── templates/                               # Template files (16 existing)
│   ├── pages/
│   ├── components/
│   ├── hooks/
│   ├── actions/
│   ├── instructions/
│   ├── dependencies/
│   └── routing/
│       └── child-route-logic.template       # New routing template
├── tests/
│   ├── __init__.py
│   ├── test_template_engine.py
│   ├── test_project_detector.py
│   ├── test_file_writer.py
│   ├── test_dependency_manager.py
│   ├── test_parent_generator.py
│   ├── test_child_generator.py
│   ├── test_wrapper_selector.py
│   ├── test_routing_updater.py
│   ├── test_variable_generator.py
│   ├── test_validation.py
│   └── integration/
│       ├── test_full_generation.py
│       └── test_project_compatibility.py
├── migration/
│   └── migrate_from_old_generators.py       # Migration utilities
├── generators/                              # Legacy generators (to be deprecated)
│   ├── dynamic_page_generator.py            # [DEPRECATED] 
│   ├── page_generator.py                    # [DEPRECATED]
│   └── parent_page_generator.py             # [DEPRECATED]
├── docs/
│   ├── 00-comprehensive-redesign-plan.md    # [EXISTING]
│   ├── 01-architecture-and-template-system.md # [EXISTING]
│   ├── 02-comprehensive-implementation-plan.md # [THIS DOCUMENT]
│   ├── 03-migration-guide.md                # [NEW]
│   └── 04-troubleshooting-guide.md          # [NEW]
└── shared/                                  # [EXISTING] Shared utilities
    ├── file_utils.py                        # File writing utilities
    └── import_utils.py                      # Import management
```

## Integration Points

### **External Dependencies**
- **Shared Utilities**: `shared/file_utils.py`, `shared/import_utils.py`
- **Index Generator**: `../index-generator-v2/index_generator.py`  
- **Template Files**: All 16 existing `.template` files
- **Python Standard Library**: `pathlib`, `argparse`, `sys`, `dataclasses`, `typing`

### **File System Integration Points**
- **Read Access**:
  - Template files (`.template` files)
  - Existing project structure for capability detection
  - Parent page files for routing updates
  
- **Write Access**:
  - Generated page files (`src/pages/`)
  - Generated component files (`src/components/`)
  - Generated hook files (`src/hooks/`)
  - Generated action files (`src/constants/actions/pages/`)
  - Generated instruction files (`src/services/instructions/pages/`)

- **Modify Access**:
  - Parent page routing files (for child route injection)
  - Index files (via external index generator)

### **Project Structure Dependencies**
```
target-project/src/
├── pages/                    # Generated parent/child pages
├── components/               # Generated wrappers  
├── hooks/
│   └── core/                 # Detection target for usePageInstructions, usePageActions, useIsMobile
├── constants/
│   └── actions/
│       └── pages/            # Generated action configurations
├── services/
│   └── instructions/
│       └── pages/            # Generated instruction configurations
└── components/
    └── ui/                   # Detection target for DataTable
```

## Testing Strategy

### **Unit Testing**
- **Template Engine**: Template loading, variable substitution, template selection
- **Project Detector**: Capability detection, existing file scanning
- **File Writer**: File creation, validation, warning headers
- **Generators**: Parent generation, child generation, routing updates
- **Validation**: Input validation, error handling, edge cases

### **Integration Testing**
- **End-to-End Generation**: Full parent + child generation workflow
- **Project Compatibility**: Testing against different project structures
- **Template System**: Complete template rendering and file generation
- **Migration**: Old generator to new generator migration

### **Test Data**
- **Mock Project Structures**: Various combinations of existing hooks and components
- **Template Test Cases**: All template variants with different variable combinations
- **Edge Cases**: Invalid inputs, missing dependencies, permission errors

## Migration Strategy

### **Backward Compatibility**
- Existing generated code continues to work without modification
- New generator produces identical output where architecturally sound
- Migration tools available for fixing architectural issues (parent wrappers)

### **Deprecation Timeline**
1. **Phase 7**: Add deprecation warnings to old generators
2. **Post-Implementation**: Update all documentation to reference new generator
3. **Future**: Remove old generators after migration period

### **Migration Support**
- Automated detection of old generator output patterns
- Batch migration tools for existing projects
- Documentation for manual migration steps
- Validation tools to verify successful migration

## Success Criteria

### **Technical Requirements**
- ✅ Zero parent wrapper generation (architectural fix)
- ✅ Proper Phase 2 mobile switching in child wrappers
- ✅ Template-based generation with 16 templates
- ✅ Adaptive template selection based on project capabilities
- ✅ Complete backward compatibility with existing projects
- ✅ Comprehensive validation and error handling

### **Quality Requirements**
- ✅ 100% unit test coverage for core modules
- ✅ Integration tests covering all generation workflows
- ✅ Performance equal or better than existing generators
- ✅ Clear separation of concerns (SRP compliance)
- ✅ DRY principle implementation through templates
- ✅ Domain-driven design with clear module boundaries

### **User Experience Requirements**
- ✅ Single CLI command replaces both old generators
- ✅ Clear error messages with actionable guidance
- ✅ Dry-run mode for safe testing
- ✅ Progress reporting during generation
- ✅ Complete documentation and troubleshooting guides

## Risk Mitigation

### **Technical Risks**
- **Template Complexity**: Mitigated by comprehensive testing and clear template structure
- **File System Operations**: Mitigated by backup/rollback mechanisms and validation
- **Project Compatibility**: Mitigated by extensive compatibility testing across project types

### **Migration Risks**  
- **Breaking Changes**: Mitigated by backward compatibility and migration tools
- **User Adoption**: Mitigated by clear documentation and migration guides
- **Legacy Code**: Mitigated by deprecation warnings and gradual transition

### **Implementation Risks**
- **Scope Creep**: Mitigated by clear phase boundaries and deliverables
- **Integration Issues**: Mitigated by integration testing at each phase
- **Performance**: Mitigated by benchmarking and optimization in Phase 7

This comprehensive implementation plan provides a clear roadmap for replacing the existing generators with a robust, architecturally-sound, template-based system that follows all established principles and patterns while eliminating known architectural flaws.