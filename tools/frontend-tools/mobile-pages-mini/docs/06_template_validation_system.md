# Template Validation System

## Overview

The Template-Based Page Generator implements a **validation-first architecture** that ensures all template dependencies are available before any code generation begins. This prevents partial generation failures and provides clear feedback about missing requirements.

## Architecture Principles

### 1. Validate Before Generate
- **All dependencies must be validated upfront** before any file generation
- The system analyzes the complete dependency graph of templates
- Generation only proceeds if all required templates are available
- Fail fast with clear error messages if dependencies are missing

### 2. Dependency Discovery
The system discovers dependencies through multiple methods:

#### Static Template Analysis
- Parses import statements in static templates
- Builds a dependency graph of required files
- Recursively analyzes dependencies of dependencies

#### Dynamic Template Analysis  
- Analyzes dynamic templates to find static component references
- Maps import paths to static template files
- Identifies essential building blocks needed for generation

## Validation Process

### Phase 1: Template Discovery
```
1. Scan dynamic templates for import statements
2. Map imports to static template files
3. Build initial dependency list
```

### Phase 2: Recursive Dependency Analysis
```
1. For each required static template:
   a. Parse its import statements
   b. Find dependent static templates
   c. Add to dependency graph
2. Continue until all dependencies mapped
```

### Phase 3: Availability Validation
```
1. Check that all required static templates exist
2. Validate template syntax and structure
3. Report missing or invalid templates
4. Fail generation if any dependencies missing
```

### Phase 4: Generation (Only if validation passes)
```
1. Create all required static components
2. Generate dynamic pages and components
3. Update routing and index files
```

## Dependency Types

### Essential Static Templates
Core templates that dynamic templates always reference:
- `hooks/core/usePageActions.ts.template`
- `hooks/core/usePageInstructions.ts.template`
- `hooks/core/useIsMobile.ts.template`
- `stores/appStore.ts.template`
- `types/core/action-sheet.types.ts.template`
- `components/chess/ChessboardLayout.tsx.template`
- `components/chess/MobileChessboardLayout.tsx.template`

### Transitive Dependencies
Static templates that other static templates import:
- Context files (InstructionsContext, etc.)
- Service files (InstructionsService, etc.)
- Utility types and constants
- Theme and configuration files

### Dynamic Dependencies
Templates chosen based on project capabilities:
- Wrapper components (based on mobile/hooks support)
- Route configurations
- Specialized hooks or services

## Error Handling

### Missing Template Errors
```
❌ Missing required template: hooks/core/usePageActions.ts.template
   Referenced by: dynamic/pages/parent-page.tsx.template
   Location: templates/static/hooks/core/
```

### Circular Dependency Errors
```
❌ Circular dependency detected:
   A.ts.template → B.ts.template → C.ts.template → A.ts.template
```

### Invalid Template Errors
```
❌ Template syntax error in: stores/appStore.ts.template
   Line 15: Unmatched braces in template variable
```

## Implementation Details

### DependencyManager Responsibilities
- **Primary validation orchestrator**
- Discovers all template dependencies
- Validates template availability and syntax
- Creates static components only after validation passes

### Template Analysis Methods
```python
def _analyze_template_dependencies(self, template_path: Path) -> Set[str]:
    """Extract all import dependencies from a template file."""
    
def _validate_template_syntax(self, template_path: Path) -> List[str]:
    """Check template for syntax errors and issues."""
    
def _build_dependency_graph(self, root_templates: List[str]) -> Dict[str, Set[str]]:
    """Build complete dependency graph from root templates."""
```

### Validation Pipeline
```python
def validate_before_generation(self, context: GenerationContext) -> bool:
    """Complete validation pipeline - returns True if safe to generate."""
    
    # 1. Discover required templates
    required_templates = self._discover_required_templates(context)
    
    # 2. Build dependency graph
    dependency_graph = self._build_dependency_graph(required_templates)
    
    # 3. Check availability
    missing_templates = self._check_template_availability(dependency_graph)
    
    # 4. Validate syntax
    syntax_errors = self._validate_template_syntax_all(dependency_graph)
    
    # 5. Report errors and return result
    return len(missing_templates) == 0 and len(syntax_errors) == 0
```

## Benefits

### 1. Predictable Generation
- No partial failures during generation
- Clear upfront feedback about requirements
- Consistent output regardless of project state

### 2. Better Error Messages
- Specific information about missing dependencies
- Clear guidance on what templates need to be created
- Dependency chain information for debugging

### 3. Faster Development
- Fail fast on missing requirements
- No need to debug partially generated projects
- Clear validation before time-intensive generation

### 4. Template Quality Assurance
- Syntax validation catches template errors early
- Dependency analysis ensures template completeness
- Prevents runtime import errors in generated code

## Future Enhancements

### Template Versioning
- Version compatibility checks between templates
- Migration guidance for template updates
- Backward compatibility validation

### Smart Dependency Resolution
- Automatic template creation for simple missing dependencies
- Template suggestion system for common patterns
- Auto-healing of broken dependency chains

### Performance Optimization
- Caching of dependency graphs
- Incremental validation for partial updates
- Parallel template analysis for large projects