# Frontend Tools

Collection of tools for managing and maintaining frontend codebases.

## Index Generator

Automatically generates modern `index.ts` files that follow best practices for exports.

### Usage

```bash
# Generate index.ts files for all subdirectories
node index-generator.js ./src/components --dry-run

# Actually generate the files (remove --dry-run)
node index-generator.js ./src/components

# Non-recursive (only specified directory)
node index-generator.js ./src/hooks/auth --no-recursive
```

### Features

- **Recursive scanning** - processes all subdirectories
- **Modern exports** - uses `export { Name } from './file'` syntax
- **Barrel exports** - creates `export * from './subdir'` for parent directories
- **Smart detection** - finds all export patterns automatically
- **Dry run mode** - preview changes without writing files
- **Auto exclusions** - skips test files, config files, etc.

### Example Output

The tool generates two types of index files:

**Individual directory index.ts:**
```typescript
// Auto-generated index file
// Run `npm run generate:index` to regenerate

export { AuthComponent } from './AuthComponent';
export { AuthRouter } from './AuthRouter';
```

**Barrel index.ts (for parent directories):**
```typescript
// Auto-generated barrel index file
// Run `npm run generate:index` to regenerate

export * from './auth';
export * from './components';
export * from './hooks';
```

This enables clean imports like:
```typescript
import { AuthComponent, Button, UserHook } from '@/components';
```

## Navigation Integration System

Automated navigation system that tracks parent pages and dynamically generates navigation components.

### Key Components

- **Navigation Generator Module** (`shared/navigation_generator.py`) - Core automation logic
- **Template Integration** - Navigation variables injected into templates
- **Config Tracking** - Parent pages stored in `pages.config.json` as source of truth

### Lessons Learned

#### Navigation Template Integration Challenges

1. **Template Variable Timing Issue**
   - **Problem**: Template variables (like `{{TAB_IDS_TYPE}}`) were processed by dependency manager before navigation data was available
   - **Solution**: Post-process generated files after navigation data is available rather than pre-process templates
   - **Key Learning**: Multi-stage template processing needed for dynamic data dependencies

2. **Duplicate Content Generation**
   - **Problem**: Navigation content was being added multiple times due to variable substitution logic
   - **Solution**: Check for template variable existence before substitution to avoid duplicates
   - **Implementation**: `if '{{VARIABLE}}' in content:` guards before replacement

3. **Static Tab Integration**
   - **Problem**: Static tabs (like "play") weren't included in generated TabId types
   - **Solution**: Navigation generator includes both dynamic parent pages AND static tabs in type generation
   - **Key Learning**: Template system needs to handle both generated and static content

4. **Icon Mapping Automation**
   - **Achievement**: Automatic icon assignment based on page names (shop → ShoppingBag, cart → ShoppingCart)
   - **Implementation**: Icon mapping dictionary in variable generator
   - **Benefit**: Eliminates manual icon selection for common page types

#### Technical Implementation Success

1. **Configuration-Driven Approach**
   - Parent pages tracked in `pages.config.json` with metadata
   - Navigation system acts as single source of truth
   - Enables consistent navigation across entire application

2. **Template Variable System**
   - Variables: `{{TAB_IDS_TYPE}}`, `{{TAB_CONFIG_ARRAY}}`, `{{PAGE_IMPORTS}}`, `{{ROUTING_CONDITIONS}}`, `{{ICON_IMPORTS}}`
   - Clean separation between template structure and dynamic content
   - Maintainable and extensible for future navigation features

3. **Comprehensive Test Coverage**
   - 15 passing tests covering all navigation generator functionality
   - Tests validate config management, code generation, and template integration
   - Ensures reliability of automated navigation system

#### Development Experience Improvements

1. **Zero Manual Navigation Updates**
   - Adding parent pages automatically updates TabBar, routing, types, and imports
   - Eliminates common developer mistakes in navigation maintenance
   - Consistent navigation UX across all generated apps

2. **Production Build Validation**
   - Navigation system generates TypeScript-compliant code
   - Build times: ~41 seconds for complete app with 227 components
   - Zero TypeScript errors in generated navigation code

#### Future Recommendations

1. **Template Processing Pipeline**
   - Consider formal multi-stage template processing for complex dependencies
   - Separate static template processing from dynamic content injection
   - Define clear dependency graphs for template variables

2. **Navigation Feature Extensions**
   - Child page navigation automation
   - Dynamic route parameter handling
   - Navigation analytics and tracking integration

3. **Generator Pattern Replication**
   - Apply similar patterns to forms, API endpoints, and state management
   - Standardize configuration-driven code generation across the stack
