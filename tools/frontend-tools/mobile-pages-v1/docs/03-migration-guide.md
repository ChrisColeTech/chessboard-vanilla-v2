# Migration Guide: From Old Generators to Template-Based System

This guide helps you migrate from the old page generators to the new template-based system.

## Overview

The new template-based system (mobile-pages-v2) replaces the old generators with:
- **Template-based generation** with 16 specialized templates
- **Phase 2 Mobile Switching Architecture** (mobile switching in child wrappers, not parents)
- **Automatic capability detection** and adaptive wrapper selection  
- **Comprehensive validation** and error handling
- **Better project structure preservation**

## Quick Migration

### Automatic Migration (Recommended)

Use the migration script for automatic detection and conversion:

```bash
# Analyze what needs migration (dry run)
python tools/frontend-tools/mobile-pages-v2/migration/migrate_from_old_generators.py /path/to/frontend --analyze-only

# Preview migration plan
python tools/frontend-tools/mobile-pages-v2/migration/migrate_from_old_generators.py /path/to/frontend --dry-run

# Execute migration
python tools/frontend-tools/mobile-pages-v2/migration/migrate_from_old_generators.py /path/to/frontend --execute
```

### Manual Migration

If you prefer manual migration or need to migrate specific components:

1. **Replace old generator commands:**

   ```bash
   # Old
   python tools/frontend-tools/mobile-pages/page_generator.py parent Settings
   python tools/frontend-tools/mobile-pages/dynamic_page_generator.py child UserProfile --parent Settings
   
   # New
   python tools/frontend-tools/mobile-pages-v2/main.py parent Settings
   python tools/frontend-tools/mobile-pages-v2/main.py child UserProfile --parent Settings
   ```

2. **Analyze your project first:**
   ```bash
   python tools/frontend-tools/mobile-pages-v2/main.py analyze
   ```

3. **Validate everything works:**
   ```bash
   python tools/frontend-tools/mobile-pages-v2/main.py validate
   ```

## Key Architectural Changes

### 1. Phase 2 Mobile Switching Architecture

**Old System (Phase 1):**
- Mobile switching happened in parent pages
- Parent wrappers handled mobile detection
- Complex parent page logic

**New System (Phase 2):**
- Mobile switching happens in child wrappers
- Parent pages are simplified
- Each child wrapper handles its own mobile detection

### 2. Template-Based Generation

**Old System:**
- Hardcoded component generation
- Fixed patterns for all projects
- Difficult to customize

**New System:**
- 16 specialized templates
- Capability-based template selection
- Easy customization through templates

### 3. Capability Detection

**Old System:**
- Assumed all projects had same capabilities
- Manual configuration required

**New System:**
- Automatic detection of project capabilities:
  - Page hooks (usePageInstructions, usePageActions)
  - Mobile hook (useIsMobile)
  - DataTable component
  - Existing parent/child structure

## Migration Scenarios

### Scenario 1: Fresh Project (No Existing Pages)

Simply start using the new generator:

```bash
# Create your first parent page
python tools/frontend-tools/mobile-pages-v2/main.py parent Dashboard

# Add child pages
python tools/frontend-tools/mobile-pages-v2/main.py child Analytics --parent Dashboard
python tools/frontend-tools/mobile-pages-v2/main.py child Reports --parent Dashboard --mobile
```

### Scenario 2: Project with Old Generator Output

1. **Run automatic migration:**
   ```bash
   python tools/frontend-tools/mobile-pages-v2/migration/migrate_from_old_generators.py . --execute
   ```

2. **Or manually remove old parent wrappers:**
   - Delete any parent wrapper components (these are no longer needed)
   - Parent pages should only contain routing logic, not mobile switching

3. **Regenerate child wrappers:**
   - Use the new generator to create child pages
   - New child wrappers will handle mobile switching

### Scenario 3: Mixed Project (Some Old, Some New)

1. **Analyze current state:**
   ```bash
   python tools/frontend-tools/mobile-pages-v2/main.py analyze
   ```

2. **Migrate gradually:**
   - Start with new pages using the new generator
   - Migrate existing pages one at a time
   - Use validation to ensure consistency

### Scenario 4: Legacy Project (No Hooks)

The new generator detects capabilities automatically:

```bash
# Analyze capabilities first
python tools/frontend-tools/mobile-pages-v2/main.py analyze

# Generator will use appropriate templates based on detected capabilities
python tools/frontend-tools/mobile-pages-v2/main.py parent Settings
# Will use templates without hooks if hooks are not detected
```

## File Changes Required

### 1. Parent Pages

**Old Structure:**
```typescript
// Parent page with mobile switching logic
const SettingsPage = () => {
  const isMobile = useIsMobile();
  
  if (isMobile) {
    return <MobileSettingsWrapper />; // ← Remove this
  }
  
  return <DesktopSettingsWrapper />; // ← Remove this  
};
```

**New Structure:**
```typescript
// Simplified parent page with just routing
const SettingsPage = () => {
  const [currentPage, setCurrentPage] = useState('main');
  
  const routes = [
    { path: 'main', label: 'Main' },
    // Child page routes (auto-injected)
  ];
  
  const renderPage = (page) => {
    switch(page) {
      case 'main':
        return <SettingsMainPage />;
      // Child page components (auto-injected)
      default:
        return <SettingsMainPage />;
    }
  };
  
  return <div>{renderPage(currentPage)}</div>;
};
```

### 2. Child Wrappers

**Old Structure:**
```typescript
// No mobile switching in child wrappers
const UserProfileWrapper = () => {
  return <UserProfilePage />; // ← No mobile logic
};
```

**New Structure:**
```typescript
// Mobile switching in child wrapper (Phase 2)
const UserProfileWrapper = () => {
  const isMobile = useIsMobile(); // ← Mobile detection here
  
  if (isMobile) {
    return <MobileUserProfilePage />;
  }
  
  return <UserProfilePage />;
};
```

### 3. File Organization

**Old System:**
```
src/pages/settings/
├── SettingsPage.tsx           (complex with mobile switching)
├── SettingsWrapper.tsx        (parent wrapper - remove)
├── UserProfilePage.tsx
└── UserProfileWrapper.tsx     (no mobile logic)
```

**New System:**
```
src/pages/settings/
├── SettingsPage.tsx           (simplified routing only)
├── SettingsMainPage.tsx       (landing page)
├── UserProfilePage.tsx
├── MobileUserProfilePage.tsx  (if mobile variant exists)
└── components/settings/
    └── UserProfileWrapper.tsx (mobile switching here)
```

## Validation and Testing

### 1. Pre-Migration Validation

```bash
# Check current project structure
python tools/frontend-tools/mobile-pages-v2/main.py analyze

# Run migration analysis
python tools/frontend-tools/mobile-pages-v2/migration/migrate_from_old_generators.py . --analyze-only
```

### 2. Post-Migration Validation

```bash
# Validate all files were created correctly
python tools/frontend-tools/mobile-pages-v2/main.py validate

# Run integration tests
python tools/frontend-tools/mobile-pages-v2/tests/integration/test_full_generation.py
python tools/frontend-tools/mobile-pages-v2/tests/integration/test_project_compatibility.py
```

### 3. Manual Testing

1. **Test mobile switching:**
   - Verify mobile switching works in child wrappers
   - Check that parent pages no longer handle mobile switching

2. **Test routing:**
   - Verify all child routes are properly configured in parent pages
   - Check navigation between child pages

3. **Test capability detection:**
   - Verify hooks are used correctly based on project capabilities
   - Check that templates match project structure

## Common Issues and Solutions

### Issue 1: "Parent wrapper not found"

**Cause:** Parent wrapper components are no longer needed in Phase 2 architecture.

**Solution:** Remove parent wrapper components and update parent page to use direct routing.

### Issue 2: "Mobile switching not working"

**Cause:** Mobile switching moved from parent to child wrappers in Phase 2.

**Solution:** 
1. Remove mobile switching from parent pages
2. Regenerate child wrappers with new generator
3. Ensure useIsMobile hook is available

### Issue 3: "Hooks not detected"

**Cause:** New system detects capabilities automatically.

**Solution:**
1. Check if hooks exist in `src/hooks/core/`
2. Run capability analysis: `main.py analyze`
3. Create missing hooks if needed, or accept no-hooks templates

### Issue 4: "Routing not updated"

**Cause:** Parent page routing markers missing.

**Solution:**
1. Add routing markers to parent pages:
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

### Issue 5: "Templates not found"

**Cause:** Templates directory missing or incorrect path.

**Solution:**
1. Ensure templates are in `tools/frontend-tools/mobile-pages-v2/templates/`
2. Check template directory structure matches requirements

## Rollback Plan

If migration fails, you can rollback:

1. **Restore from backups:**
   ```bash
   # Migration creates .backup files
   find . -name "*.backup" -exec bash -c 'mv "$1" "${1%.backup}"' _ {} \;
   ```

2. **Use old generators temporarily:**
   - Old generators still work but show deprecation warnings
   - You have time to fix issues and re-migrate

3. **Report issues:**
   - Document any migration problems
   - Update migration scripts based on learnings

## Best Practices

### 1. Migration Strategy

- **Start with analysis:** Always run `--analyze-only` first
- **Use dry-run:** Preview changes with `--dry-run`
- **Backup everything:** Migration creates backups, but manual backup is safer
- **Migrate gradually:** Don't migrate everything at once
- **Validate continuously:** Run validation after each migration step

### 2. Testing Strategy

- **Test mobile switching thoroughly**
- **Verify all routes work correctly**
- **Check hook integration**
- **Test with different project capabilities**

### 3. Documentation

- **Update project documentation** to reference new generator
- **Document any custom modifications**
- **Keep migration notes for future reference**

## Support

For migration assistance:

1. **Run diagnostics:**
   ```bash
   python tools/frontend-tools/mobile-pages-v2/main.py analyze
   python tools/frontend-tools/mobile-pages-v2/main.py validate
   ```

2. **Check logs:**
   - Migration script provides detailed logging
   - Validation reports highlight specific issues

3. **Troubleshooting:**
   - See `04-troubleshooting-guide.md` for common issues
   - Integration tests provide examples of correct usage

The new template-based system provides significant improvements while maintaining full backward compatibility with existing projects.