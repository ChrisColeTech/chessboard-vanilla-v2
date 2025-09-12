# Frontend Page Generator Tools

Tools for generating React pages following the **Phase 2 Mobile Switching Architecture** with lessons learned and architectural improvements.

## Overview

This directory contains three specialized tools:

1. **🚀 `dynamic_page_generator.py` (RECOMMENDED)** - Creates new pages with responsive wrappers
2. **🔄 `legacy_migrator.py` (CONVERSION)** - Migrates monolithic files to dynamic system  
3. **⚠️ `page_generator.py` (DEPRECATED)** - Legacy string manipulation approach

## Key Architectural Lessons Learned

### ✅ Single Responsive Wrapper Pattern
**Old approach (deprecated):**
```
MyPagePageWrapper.tsx        (desktop wrapper)
MobileMyPagePageWrapper.tsx  (mobile wrapper - duplicate logic)
```

**New approach (current):**
```
MyPagePageWrapper.tsx        (single responsive wrapper with internal mobile switching)
```

### ✅ Mobile Switching Logic Location  
**Wrapper handles mobile detection internally** instead of parent page conditional logic:

```tsx
// NEW: Inside wrapper (better)
export const MyPageWrapper = () => {
  const isMobile = useIsMobile();
  return isMobile ? <MobileMyPage /> : <MyPage />;
};

// OLD: In parent page (removed)
CurrentPageComponent = isMobile ? MobileMyPageWrapper : MyPageWrapper;
```

### ✅ Reduced Component Duplication
- **Before:** 2 wrappers per page (desktop + mobile) with identical logic
- **After:** 1 wrapper per page with conditional rendering
- **Benefit:** 50% fewer wrapper components, easier maintenance

## 🚀 Dynamic Page Generator (Recommended)

### Features
- ✅ **Zero File Corruption** - Only creates files, never modifies existing ones
- ✅ **Auto-Discovery** - Files are automatically loaded using `import.meta.glob`
- ✅ **Single Responsive Wrapper** - No wrapper duplication
- ✅ **Automatic Parent Updates** - Adds routing logic to parent pages
- ✅ **Dynamic Imports** - Uses new dynamic instruction/action system
- ✅ **Type Safe** - All generated code compiles correctly

### New Architecture Improvements
- **Single wrapper per page** instead of desktop/mobile pairs
- **Internal mobile switching** using `useIsMobile()` hook
- **Automatic parent page updates** with routing logic
- **Dynamic instruction/action loading** with `import.meta.glob`

### Architecture

The dynamic system uses two auto-discovery patterns:

#### Instructions Auto-Discovery
```
src/services/instructions/pages/
├── layout.ts           # Auto-discovered by import.meta.glob
├── worker.ts           # Each file exports pageInstructions
└── mypage.ts           # Drop new files here
```

#### Actions Auto-Discovery
```
src/constants/actions/pages/
├── worker.ts           # Auto-discovered by import.meta.glob  
├── uitests.ts          # Each file exports pageActions
└── mypage.ts           # Drop new files here
```

### Usage

#### Basic Child Page
```bash
python dynamic_page_generator.py child MyPage --parent uitests --description "My awesome page"
```

#### Child Page with Mobile Variant
```bash
python dynamic_page_generator.py child MyPage --parent uitests --mobile --description "My responsive page"
```

#### Full Example
```bash
python dynamic_page_generator.py child Settings \
  --parent uitests \
  --mobile \
  --icon "Settings" \
  --description "Application settings and preferences"
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `command` | Page type (`child` only currently) | `child` |
| `name` | Page name in PascalCase | `MyPage` |
| `--parent` | Parent page name (required) | `--parent uitests` |
| `--mobile` | Create mobile variant | `--mobile` |
| `--icon` | Lucide icon name | `--icon "Settings"` |
| `--description` | Page description | `--description "My page"` |
| `--frontend-root` | Frontend directory path | `--frontend-root ../../../frontend` |

### Generated Files

For `python dynamic_page_generator.py child MyPage --parent uitests --mobile`:

#### React Components (New Architecture)
```
src/pages/uitests/
├── MyPagePage.tsx                 # Desktop page component
└── MobileMyPagePage.tsx           # Mobile page component

src/components/uitests/
└── MyPagePageWrapper.tsx          # Single responsive wrapper (handles mobile switching)
```

#### Auto-Discovered Configs
```
src/services/instructions/pages/
└── mypage.ts                      # Instructions (auto-loaded)

src/constants/actions/pages/
└── mypage.ts                      # Actions (auto-loaded)
```

### Automatic Integration (No Manual Steps!)

The tool now handles all integration automatically:

1. ✅ **Routing Logic Added** to parent page automatically:
   ```typescript
   // Automatically added to parent page:
   if (currentChildPage === "mypage") {
     CurrentPageComponent = MyPagePageWrapper; // Single wrapper handles mobile switching
   }
   ```

2. ✅ **Dynamic Imports Ready** - Generated code uses new dynamic system:
   ```typescript
   // Wrapper automatically uses:
   usePageInstructions("mypage");  // → dynamicInstructionsService
   usePageActions("mypage");       // → DYNAMIC_PAGE_ACTIONS
   ```

3. ✅ **Parent Page Updated** - Import statements and routing logic added automatically

## 🔄 Legacy Migrator (For Existing Codebases)

Converts existing monolithic instruction/action files to the new dynamic system.

### What it does:
- ✅ **Extracts instructions** from `InstructionsService.ts` → individual page files
- ✅ **Extracts actions** from `page-actions.constants.ts` → individual page files  
- ✅ **Creates dynamic services** that use `import.meta.glob` for auto-discovery
- ✅ **Updates existing services** to use dynamic loading

### Usage:
```bash
python legacy_migrator.py --frontend-root ../../../frontend
```

### Services Updated:
- **`usePageInstructions`** → now uses `dynamicInstructionsService`
- **`ActionSheetContainer`** → now uses `DYNAMIC_PAGE_ACTIONS`  
- **Monolithic files** → archived (can be safely removed)

## ⚠️ Legacy Page Generator (Deprecated)

**DEPRECATED**: The legacy `page_generator.py` has been replaced by the dynamic generator.

### Issues with Legacy Tool
- ❌ String manipulation corrupts import statements
- ❌ Creates duplicate wrappers (desktop + mobile)
- ❌ Manual parent page updates required
- ❌ Complex 547-line codebase
- ❌ No dynamic import support

## Complete Migration Workflow

For existing codebases, follow this workflow:

### Step 1: Convert Existing Codebase
```bash
cd tools/frontend-tools/mobile-pages
python legacy_migrator.py --frontend-root ../../../frontend
```

### Step 2: Create New Pages (Optional)
```bash
python dynamic_page_generator.py child NewPage --parent uitests --mobile --description "My new page"
```

### Step 3: Verify Dynamic System
- ✅ Check `usePageInstructions` uses dynamic loading
- ✅ Check `ActionSheetContainer` uses `DYNAMIC_PAGE_ACTIONS`
- ✅ Test instructions and actions load correctly
- ✅ Test mobile/desktop switching works

## Architecture Documentation

### Key Principles Learned:
1. **Single Responsibility** - Wrappers handle mobile switching, not parent pages
2. **Dynamic Discovery** - Use `import.meta.glob` for auto-discovery
3. **Reduce Duplication** - One wrapper per page, not desktop/mobile pairs
4. **Automated Integration** - Tools should wire everything together automatically

### Related Documentation:
- `/docs/47-navigation-action-sheets-architecture.md` - Phase 2 Mobile Switching Architecture
- Implementation evolved beyond documented patterns based on practical experience

## Development

### Requirements
- Python 3.7+
- Node.js frontend environment
- TypeScript compilation

### Testing
```bash
# Test dynamic generator
python dynamic_page_generator.py child TestPage --parent uitests --mobile

# Verify build
npm run build
```

### Contributing

When adding new features:
1. Use the dynamic file loading approach
2. Avoid file modification/string manipulation
3. Test TypeScript compilation
4. Follow existing naming conventions
5. Update this README with new features

## Troubleshooting

### Build Errors After Generation
- Ensure all TypeScript imports are valid
- Check for missing parent page routing logic
- Verify dynamic service integration

### Tool Execution Issues
```bash
# Make executable
chmod +x dynamic_page_generator.py

# Check Python path
python3 dynamic_page_generator.py --help
```

### File Path Issues
```bash
# Use absolute paths if relative paths fail
python dynamic_page_generator.py child MyPage --parent uitests --frontend-root /absolute/path/to/frontend
```