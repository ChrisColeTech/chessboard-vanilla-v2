# Troubleshooting Guide: Template-Based Page Generator

This guide helps diagnose and resolve common issues with the template-based page generator.

## Quick Diagnostics

### 1. Run Analysis First

Always start with project analysis to understand current state:

```bash
python tools/frontend-tools/mobile-pages-v2/main.py analyze
```

### 2. Validate System Health

Check overall system validation:

```bash
python tools/frontend-tools/mobile-pages-v2/main.py validate
```

### 3. Check Templates

Verify templates are available:

```bash
ls -la tools/frontend-tools/mobile-pages-v2/templates/
```

## Common Error Messages

### Error: "Frontend root directory not found"

**Symptoms:**
```
❌ Frontend root directory not found: /path/to/frontend
```

**Causes:**
- Incorrect path to frontend directory
- Running from wrong directory
- Frontend directory doesn't exist

**Solutions:**
1. **Verify path exists:**
   ```bash
   ls -la /path/to/frontend/src
   ```

2. **Use absolute path:**
   ```bash
   python main.py parent Settings --frontend-root /absolute/path/to/frontend
   ```

3. **Run from correct directory:**
   ```bash
   cd /path/to/frontend
   python tools/frontend-tools/mobile-pages-v2/main.py analyze
   ```

### Error: "Templates directory not found"

**Symptoms:**
```
❌ Templates directory not found: /path/to/templates
```

**Causes:**
- Templates directory missing
- Incorrect template path
- Corrupted installation

**Solutions:**
1. **Check templates exist:**
   ```bash
   find tools/frontend-tools/mobile-pages-v2 -name "*.template" -type f
   ```

2. **Reinstall templates:**
   - Verify all 16 templates are present
   - Check template directory structure

3. **Use custom template path:**
   ```bash
   python main.py parent Settings --templates-dir /custom/path/templates
   ```

### Error: "Parent page 'X' not found"

**Symptoms:**
```
❌ Parent page 'Settings' not found. Create it first.
```

**Causes:**
- Trying to create child page before parent exists
- Parent page directory doesn't exist
- Parent page file not properly named

**Solutions:**
1. **Create parent first:**
   ```bash
   python main.py parent Settings
   ```

2. **Check parent exists:**
   ```bash
   ls src/pages/settings/SettingsPage.tsx
   ```

3. **Verify parent directory structure:**
   ```bash
   ls -la src/pages/settings/
   ```

### Error: "Template rendering failed"

**Symptoms:**
```
❌ Template rendering failed: KeyError: 'PARENT_NAME'
```

**Causes:**
- Missing template variables
- Corrupted template file
- Invalid template syntax

**Solutions:**
1. **Check template variables:**
   - Verify all required variables are provided
   - Check variable casing (PARENT_NAME vs parent_name)

2. **Validate template syntax:**
   ```bash
   cat tools/frontend-tools/mobile-pages-v2/templates/pages/child-page.tsx.template
   ```

3. **Regenerate from known working template:**
   - Compare with working examples
   - Reset template to default if corrupted

### Error: "File write permission denied"

**Symptoms:**
```
❌ PermissionError: [Errno 13] Permission denied: '/path/to/file'
```

**Causes:**
- Insufficient file permissions
- File is locked by another process
- Directory doesn't exist

**Solutions:**
1. **Check permissions:**
   ```bash
   ls -la src/pages/
   chmod 755 src/pages/
   ```

2. **Close file if open in editor**

3. **Run with proper permissions:**
   ```bash
   sudo python main.py parent Settings
   ```

## Capability Detection Issues

### Issue: "Hooks not detected but they exist"

**Symptoms:**
- Analysis shows `has_page_hooks: False`
- But hooks exist in `src/hooks/core/`

**Diagnostic:**
```bash
ls src/hooks/core/usePageInstructions.ts
ls src/hooks/core/usePageActions.ts
ls src/hooks/core/useIsMobile.ts
```

**Solutions:**
1. **Check hook file contents:**
   ```typescript
   // Make sure hooks actually export something
   export const usePageInstructions = () => { /* implementation */ };
   ```

2. **Verify hook location:**
   - Must be in `src/hooks/core/`
   - Must be named exactly: `usePageInstructions.ts`, `usePageActions.ts`, `useIsMobile.ts`

3. **Force capability detection refresh:**
   ```bash
   # Clear any cached detection
   rm -rf __pycache__/
   python main.py analyze
   ```

### Issue: "Wrong wrapper template selected"

**Symptoms:**
- Generated wrapper doesn't match project capabilities
- Missing expected hooks or mobile logic

**Diagnostic:**
Run capability analysis and check wrapper selection logic:

```bash
python -c "
import sys; sys.path.append('tools/frontend-tools/mobile-pages-v2')
from modules.project_detector import ProjectCapabilityDetector
from modules.wrapper_selector import WrapperSelector

detector = ProjectCapabilityDetector('.')
capabilities = detector.detect_capabilities()
selector = WrapperSelector()
wrapper_type = selector.select_wrapper_template(capabilities)

print(f'Detected capabilities: {capabilities}')
print(f'Selected wrapper: {wrapper_type}')
"
```

**Solutions:**
1. **Update hook availability:**
   - Create missing hooks if needed
   - Remove hooks if not wanted

2. **Force specific wrapper type:**
   - Modify templates to use desired wrapper type
   - Update capability detection logic

## Generation Issues

### Issue: "Child page created but routing not updated"

**Symptoms:**
- Child page files created successfully
- But parent page routing not updated
- Child not accessible via navigation

**Diagnostic:**
```bash
# Check parent page content
cat src/pages/settings/SettingsPage.tsx | grep -A5 -B5 "Child page"
```

**Solutions:**
1. **Check routing markers:**
   Parent page must have routing markers:
   ```typescript
   // Child page imports
   
   const routes = [
     { path: 'main', label: 'Main' }
     // Child page routes
   ];
   
   switch(page) {
     case 'main':
       return <MainPage />;
     // Child page components
     default:
       return <MainPage />;
   }
   ```

2. **Manually update routing:**
   ```bash
   python -c "
   import sys; sys.path.append('tools/frontend-tools/mobile-pages-v2')
   from modules.routing_updater import ParentRoutingUpdater
   from modules.config import GenerationContext, PageConfig, ProjectCapabilities
   # Update routing manually
   "
   ```

3. **Regenerate parent page:**
   ```bash
   # Backup existing parent
   cp src/pages/settings/SettingsPage.tsx src/pages/settings/SettingsPage.tsx.backup
   
   # Regenerate with routing markers
   python main.py parent Settings
   ```

### Issue: "Mobile variant not working"

**Symptoms:**
- Mobile page created but doesn't display on mobile
- Mobile switching not working in wrapper

**Diagnostic:**
1. **Check mobile page exists:**
   ```bash
   ls src/pages/settings/MobileUserProfilePage.tsx
   ```

2. **Check wrapper mobile logic:**
   ```bash
   grep -A10 "useIsMobile" src/components/settings/UserProfileWrapper.tsx
   ```

**Solutions:**
1. **Verify useIsMobile hook:**
   ```bash
   ls src/hooks/core/useIsMobile.ts
   ```

2. **Check wrapper template used:**
   - Should be `child-wrapper-full-hooks.tsx.template` or similar with mobile support
   - Not `child-wrapper-no-mobile.tsx.template`

3. **Manually fix wrapper:**
   ```typescript
   import { useIsMobile } from '@/hooks/core/useIsMobile';
   
   const UserProfileWrapper = () => {
     const isMobile = useIsMobile();
     
     if (isMobile) {
       return <MobileUserProfilePage />;
     }
     
     return <UserProfilePage />;
   };
   ```

## Validation Issues

### Issue: "Validation shows missing dependencies"

**Symptoms:**
```
⚠️  Missing Dependencies:
  - usePageInstructions
  - DataTable component
```

**Diagnostic:**
```bash
python main.py validate
```

**Solutions:**
1. **Create missing dependencies:**
   ```bash
   # Create missing hooks
   mkdir -p src/hooks/core
   echo "export const usePageInstructions = () => {};" > src/hooks/core/usePageInstructions.ts
   ```

2. **Use no-dependencies templates:**
   - Templates automatically adapt to available dependencies
   - Missing dependencies result in simpler templates being used

3. **Ignore non-critical dependencies:**
   - Some dependencies are optional (like DataTable)
   - Validation warnings (not errors) can often be ignored

### Issue: "Routing sync validation fails"

**Symptoms:**
```
⚠️  Routing sync issues for Settings:
  📄 Files missing from routing:
    - userprofile
```

**Diagnostic:**
```bash
python -c "
import sys; sys.path.append('tools/frontend-tools/mobile-pages-v2')
from modules.routing_updater import ParentRoutingUpdater
from modules.config import GenerationContext, PageConfig, ProjectCapabilities

# Check routing sync manually
"
```

**Solutions:**
1. **Update parent routing:**
   ```bash
   # Regenerate child to update routing
   python main.py child UserProfile --parent Settings
   ```

2. **Manual routing fix:**
   Add missing routing to parent page:
   ```typescript
   import UserProfileWrapper from '@/components/settings/UserProfileWrapper';
   
   const routes = [
     { path: 'main', label: 'Main' },
     { path: 'userprofile', label: 'UserProfile' }
   ];
   
   switch(page) {
     case 'main':
       return <SettingsMainPage />;
     case 'userprofile':
       return <UserProfileWrapper />;
     default:
       return <SettingsMainPage />;
   }
   ```

## Performance Issues

### Issue: "Generation takes too long"

**Symptoms:**
- Generator runs for minutes without completing
- System becomes unresponsive

**Diagnostic:**
1. **Check file system performance:**
   ```bash
   time ls -la src/ > /dev/null
   ```

2. **Monitor system resources:**
   ```bash
   top | grep python
   ```

**Solutions:**
1. **Reduce file scanning scope:**
   - Remove unnecessary files from src/
   - Use .gitignore patterns

2. **Run with verbose logging:**
   ```bash
   python main.py parent Settings --verbose
   ```

3. **Break down operations:**
   - Create parent and child pages separately
   - Run validation separately

## Integration Issues

### Issue: "Import paths not resolving"

**Symptoms:**
```typescript
// Generated import doesn't work
import { usePageInstructions } from '@/hooks/core/usePageInstructions';
```

**Diagnostic:**
1. **Check TypeScript config:**
   ```bash
   cat tsconfig.json | grep "@/*"
   ```

2. **Check actual file location:**
   ```bash
   find . -name "usePageInstructions.ts"
   ```

**Solutions:**
1. **Update path mapping in tsconfig.json:**
   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["./src/*"]
       }
     }
   }
   ```

2. **Use relative imports:**
   ```typescript
   import { usePageInstructions } from '../../hooks/core/usePageInstructions';
   ```

3. **Update template import patterns:**
   - Modify templates to use correct import patterns for your project

### Issue: "Build errors after generation"

**Symptoms:**
- Generated files cause TypeScript errors
- Build process fails

**Diagnostic:**
1. **Run TypeScript check:**
   ```bash
   npx tsc --noEmit
   ```

2. **Check ESLint:**
   ```bash
   npx eslint src/
   ```

**Solutions:**
1. **Fix TypeScript errors:**
   - Update generated types
   - Add missing type definitions

2. **Update ESLint config:**
   - Add exceptions for generated files
   - Update ESLint rules to match generated patterns

3. **Regenerate with correct templates:**
   - Update templates to match project coding standards
   - Ensure generated code follows project conventions

## Migration Issues

### Issue: "Migration script can't detect old patterns"

**Symptoms:**
- Migration shows "No old generator files detected"
- But old generator files definitely exist

**Diagnostic:**
```bash
python tools/frontend-tools/mobile-pages-v2/migration/migrate_from_old_generators.py . --analyze-only
```

**Solutions:**
1. **Check detection patterns:**
   - Look for generator comments in files
   - Update detection patterns if needed

2. **Manual migration:**
   - Identify files manually
   - Use new generator to replace functionality

### Issue: "Migration corrupts existing files"

**Symptoms:**
- Files become unusable after migration
- Syntax errors in migrated files

**Solutions:**
1. **Restore from backup:**
   ```bash
   find . -name "*.backup" -exec bash -c 'mv "$1" "${1%.backup}"' _ {} \;
   ```

2. **Run dry-run first:**
   ```bash
   python migration/migrate_from_old_generators.py . --dry-run
   ```

3. **Migrate gradually:**
   - Migrate one page at a time
   - Test after each migration

## Getting Help

### 1. Collect Diagnostics

Before reporting issues, collect comprehensive diagnostics:

```bash
# System information
python --version
node --version
pwd
ls -la src/

# Generator analysis
python tools/frontend-tools/mobile-pages-v2/main.py analyze > analysis.txt

# Validation report  
python tools/frontend-tools/mobile-pages-v2/main.py validate > validation.txt

# Template check
find tools/frontend-tools/mobile-pages-v2/templates -name "*.template" > templates.txt
```

### 2. Minimal Reproduction

Create minimal example that reproduces the issue:

```bash
# Create minimal project structure
mkdir test-project
cd test-project
mkdir -p src/{pages,components,hooks/core}
echo '{"name": "test"}' > package.json

# Try to reproduce issue
python ../tools/frontend-tools/mobile-pages-v2/main.py parent Test
```

### 3. Check Similar Issues

- Review migration guide for common patterns
- Check integration tests for working examples
- Compare with successful generations

The template-based system includes comprehensive error handling and validation to help diagnose issues quickly. Most problems can be resolved by understanding the capability detection system and ensuring proper project structure.