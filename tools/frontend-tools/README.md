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
