# Architecture & Template System - Complete Understanding

## Executive Summary

This document provides a comprehensive understanding of the Dynamic Page Generator's architecture, its alignment with the established navigation patterns, and the new template-based generation system. The redesign eliminates architectural flaws while implementing proper Phase 2 Mobile Switching Architecture patterns.

## Table of Contents

1. [Navigation Architecture Foundation](#navigation-architecture-foundation)
2. [Phase 2 Mobile Switching Architecture](#phase-2-mobile-switching-architecture)
3. [Template System Design](#template-system-design)
4. [Component Responsibility Matrix](#component-responsibility-matrix)
5. [File Generation Patterns](#file-generation-patterns)
6. [Architecture Alignment Verification](#architecture-alignment-verification)
7. [Template Variable System](#template-variable-system)
8. [Implementation Guidelines](#implementation-guidelines)

## Navigation Architecture Foundation

### Multi-Layer Navigation Stack

The application uses a sophisticated multi-layer navigation system as documented in the main architecture:

```
┌─────────────────────────────────────────┐
│                App Layout               │
├─────────────────────────────────────────┤
│              Tab Navigation             │  ← selectedTab (persisted)
├─────────────────────────────────────────┤
│              Parent Pages               │  ← Direct tab targets
│  ┌───────────────────────────────────┐  │
│  │         Child Pages               │  │  ← currentChildPage (persisted)
│  │    (dragtest, uiaudiotest)        │  │
│  └───────────────────────────────────┘  │
├─────────────────────────────────────────┤
│             Action Sheets               │  ← Context-sensitive
└─────────────────────────────────────────┘
```

### Core State Management

**Zustand Store Integration:**
```typescript
interface AppState {
  selectedTab: TabId              // Main navigation (layout, uitests, etc.)
  currentChildPage: string | null // Child page state (dragtest, layouttest, etc.)
  
  // Navigation actions
  setSelectedTab: (tab: TabId) => void
  setCurrentChildPage: (childPage: string | null) => void
}
```

**Critical Persistence:**
- Both `selectedTab` and `currentChildPage` are persisted
- Navigation state survives app reloads and browser sessions
- Enables seamless user experience continuation

## Phase 2 Mobile Switching Architecture

### Architecture Principles

**Phase 2 Key Innovation:** 
- **Single pageId** shared between mobile/desktop variants
- **Automatic device detection** with responsive switching
- **Eliminated duplicate actions/instructions**
- **Wrapper-based mobile switching** (not parent-based)

### Correct Responsibility Distribution

#### Parent Page Responsibilities ✅
- **Child page routing**: Determine which child page to show
- **Hook application**: Apply `usePageInstructions()` and `usePageActions()` directly
- **Store integration**: React to `currentChildPage` state changes
- **Simple routing logic**: `if (currentChildPage === 'X') { show XWrapper }`

#### Child Wrapper Responsibilities ✅
- **Mobile detection**: Use `useIsMobile()` hook internally
- **Device switching**: Choose between mobile/desktop page variants
- **Context application**: Apply `usePageInstructions()` and `usePageActions()`
- **Component selection**: `return isMobile ? <MobilePage /> : <DesktopPage />`

#### What Parents DON'T Do ❌
- **No mobile detection** - This happens in child wrappers
- **No mobile routing logic** - Wrappers handle device switching
- **No wrapper components** - Parents are direct tab targets

### Phase 2 Flow Pattern

**Correct Flow:**
```
Tab Click → Parent Page → Child Wrapper → useIsMobile() → Mobile/Desktop Page
                   ↑              ↑              ↑
              Child routing   Context hooks   Device switching
```

**Previous Incorrect Flow (Eliminated):**
```
Tab Click → Parent Wrapper → Parent Page → useIsMobile() + routing
                ↑                              ↑
        Unnecessary layer              Complex mobile logic
```

## Template System Design

### Template Architecture Overview

The new template system uses `.template` files with variable substitution to generate consistent, architecturally-aligned code:

```
templates/
├── pages/
│   ├── parent-page.tsx.template           # Main parent (NO wrapper!)
│   ├── parent-main-page.tsx.template      # Parent landing page
│   ├── child-page.tsx.template            # Desktop child page
│   └── mobile-child-page.tsx.template     # Mobile child page
├── components/
│   ├── child-wrapper-full-hooks.tsx.template    # Mobile switching + hooks
│   ├── child-wrapper-basic-hooks.tsx.template   # Hooks only
│   ├── child-wrapper-no-hooks.tsx.template      # Minimal wrapper
│   └── child-wrapper-no-mobile.tsx.template     # Placeholder mobile
├── hooks/
│   └── parent-actions-hook.ts.template    # Dynamic navigation hook
├── actions/
│   ├── parent-actions.ts.template         # Parent action sheet
│   └── child-actions.ts.template          # Child action sheet
├── instructions/
│   ├── parent-instructions.ts.template    # Parent instructions
│   └── child-instructions.ts.template     # Child instructions
└── dependencies/
    ├── use-page-data-hook.ts.template     # Mock data hook
    └── data-table-component.tsx.template  # Data table component
```

### Template Selection Logic

The generator will select appropriate templates based on detected project capabilities:

#### Child Wrapper Selection
```typescript
// Detected capabilities determine template choice
if (hasPageHooks && hasMobileHook && isMobileVariant) {
  template = 'child-wrapper-full-hooks.tsx.template'
} else if (hasPageHooks && !hasMobileHook) {
  template = 'child-wrapper-basic-hooks.tsx.template'  
} else if (!hasPageHooks && !hasMobileHook) {
  template = 'child-wrapper-no-hooks.tsx.template'
} else {
  template = 'child-wrapper-no-mobile.tsx.template'
}
```

#### Hook Detection System
```typescript
// Project capability detection
const hooks_dir = frontend_root / "src" / "hooks" / "core"
const hasPageHooks = (
  (hooks_dir / "usePageInstructions.ts").exists() &&
  (hooks_dir / "usePageActions.ts").exists()
)
const hasMobileHook = (hooks_dir / "useIsMobile.ts").exists()
```

## Component Responsibility Matrix

| Component Type | Navigation | Mobile Detection | Context Hooks | Routing Logic | Template Count |
|----------------|------------|------------------|---------------|---------------|----------------|
| **Parent Page** | ✅ Child routing | ❌ No | ✅ Direct application | ✅ Simple if/else | 1 |
| **Parent Main** | ❌ None | ❌ No | ❌ No | ❌ No | 1 |
| **Child Wrapper** | ❌ None | ✅ useIsMobile() | ✅ Context switching | ✅ Mobile/Desktop | 4 variants |
| **Child Page** | ❌ None | ❌ No | ❌ No | ❌ No | 1 |
| **Mobile Child** | ❌ None | ❌ No | ❌ No | ❌ No | 1 |

### Critical Architecture Rules

#### Rule 1: Single Responsibility
- **Parents**: Handle child page routing only
- **Child Wrappers**: Handle mobile switching and context only  
- **Pages**: Handle content rendering only

#### Rule 2: No Parent Wrappers
- Parent pages are **direct tab targets**
- Tab system routes directly to `ParentPage`, not `ParentPageWrapper`
- Parent hooks applied directly in parent component

#### Rule 3: Wrapper-Based Mobile Switching
- Mobile detection happens in child wrappers, not parents
- Each child wrapper internally chooses mobile vs desktop variant
- Single pageId shared between mobile/desktop for unified context

#### Rule 4: Context Consistency
- Both mobile and desktop variants use same `pageId`
- Same instructions and actions apply to both variants
- No duplicate action/instruction configurations

## File Generation Patterns

### Parent Generation (5 files total)
```
src/pages/{parent}/{Parent}Page.tsx                    # Main routing page
src/pages/{parent}/{Parent}MainPage.tsx                # Landing page
src/hooks/{parent}/use{Parent}Actions.ts               # Navigation hook
src/constants/actions/pages/{parent}.ts                # Action sheet config
src/services/instructions/pages/{parent}.ts            # Instructions config
```

**Key Changes from Old System:**
- ❌ **Eliminated**: `src/components/{parent}/{Parent}PageWrapper.tsx`
- ✅ **Direct routing**: Tab system routes directly to parent page
- ✅ **Fewer files**: 6 → 5 files per parent

### Child Generation (4-5 files total)
```
src/pages/{parent}/{Child}Page.tsx                     # Desktop page
src/pages/{parent}/Mobile{Child}Page.tsx               # Mobile page (optional)
src/components/{parent}/{Child}PageWrapper.tsx         # Mobile switching wrapper
src/constants/actions/pages/{child}.ts                 # Action sheet config  
src/services/instructions/pages/{child}.ts             # Instructions config
```

**Architecture Benefits:**
- ✅ **Single wrapper**: Handles both mobile detection and context
- ✅ **Shared pageId**: Mobile/desktop use same action/instruction config
- ✅ **Phase 2 compliant**: Eliminates duplicate mobile configurations

## Architecture Alignment Verification

### Template Code Examples

#### Parent Page Template (Correct)
```typescript
export const {{PARENT_NAME}}Page: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);
  
  // Apply hooks directly - NO WRAPPER NEEDED
  usePageInstructions("{{PARENT_ID}}");
  usePageActions("{{PARENT_ID}}");
  
  let CurrentPageComponent = {{PARENT_NAME}}MainPage;
  
  // Simple child routing - wrappers handle mobile switching
  {{CHILD_ROUTING_LOGIC}}
  
  return <CurrentPageComponent key={currentChildPage || 'main'} />;
};
```

#### Child Wrapper Template (Correct)
```typescript
export const {{CHILD_NAME}}PageWrapper: React.FC = () => {
  // Mobile detection in wrapper (Phase 2 Architecture)
  const isMobile = useIsMobile();
  
  // Apply context hooks
  usePageInstructions("{{CHILD_ID}}");
  usePageActions("{{CHILD_ID}}");

  // Internal mobile/desktop switching
  return isMobile ? <{{MOBILE_CHILD_NAME}}Page /> : <{{CHILD_NAME}}Page />;
};
```

### Routing Pattern Verification

#### Parent Child Routing Logic
```typescript
// Generated routing logic in parent template
if (currentChildPage === "layouttest") {
  CurrentPageComponent = LayoutTestPageWrapper;  // Single wrapper
} else if (currentChildPage === "dragtest") {
  CurrentPageComponent = DragTestPageWrapper;    // Single wrapper
}
```

#### Tab System Integration
```typescript
// Tab system routes directly to parent (no wrapper)
{selectedTab === 'uitests' && <UITestsPage />}  // Direct routing
{selectedTab === 'layout' && <LayoutPage />}    // Direct routing
```

## Template Variable System

### Primary Variables
```typescript
// Parent page variables
{{PARENT_NAME}}        // PascalCase: "UITests", "Layout"
{{PARENT_ID}}          // lowercase: "uitests", "layout"

// Child page variables  
{{CHILD_NAME}}         // PascalCase: "DragTest", "LayoutTest"
{{CHILD_ID}}           // lowercase: "dragtest", "layouttest"
{{CHILD_DISPLAY_NAME}} // Display: "Drag Test", "Layout Test"

// Mobile variants
{{MOBILE_CHILD_NAME}}  // PascalCase: "MobileDragTest"

// Dynamic content
{{CHILD_ROUTING_LOGIC}}   // Generated if/else routing
{{NAVIGATION_METHODS}}    // Dynamic navigation functions
{{HOOK_IMPORTS}}          // Conditional hook imports
```

### Conditional Rendering Variables
```typescript
// Hook availability
{{HOOK_IMPORTS}}       // Import statements based on detected hooks
{{HOOK_USAGE}}         // Hook calls based on availability
{{MOBILE_DETECTION}}   // useIsMobile() if available
{{MOBILE_IMPORT}}      // Mobile page import if mobile variant requested

// Wrapper variants
{{RENDER_LOGIC}}       // Mobile switching or direct render
```

### Dynamic Generation Variables
```typescript
// Navigation hook generation
{{NAVIGATION_METHODS}} // Auto-generated navigation functions:
// const goToChildPage = useCallback(() => {
//   setCurrentChildPage('childpage')
// }, [setCurrentChildPage])

{{RETURN_METHODS}}     // Auto-generated return object:
// return {
//   goToChildPage,
//   goToOtherChild,
//   // ...
// }

// Parent routing generation  
{{CHILD_ROUTING_LOGIC}} // Auto-generated routing:
// if (currentChildPage === "dragtest") {
//   CurrentPageComponent = DragTestPageWrapper;
// } else if (currentChildPage === "layouttest") {
//   CurrentPageComponent = LayoutTestPageWrapper;
// }
```

## Implementation Guidelines

### Generator Algorithm

#### 1. Project Detection Phase
```python
def detect_project_capabilities(frontend_root: Path) -> ProjectCapabilities:
    hooks_dir = frontend_root / "src" / "hooks" / "core"
    
    return ProjectCapabilities(
        has_page_hooks=(
            (hooks_dir / "usePageInstructions.ts").exists() and
            (hooks_dir / "usePageActions.ts").exists()
        ),
        has_mobile_hook=(hooks_dir / "useIsMobile.ts").exists(),
        has_data_table=(frontend_root / "src" / "components" / "ui" / "DataTable.tsx").exists(),
        # ... other capability checks
    )
```

#### 2. Template Selection Phase
```python
def select_wrapper_template(config: PageConfig, capabilities: ProjectCapabilities) -> str:
    if config.mobile and capabilities.has_page_hooks and capabilities.has_mobile_hook:
        return "child-wrapper-full-hooks.tsx.template"
    elif capabilities.has_page_hooks and not capabilities.has_mobile_hook:
        return "child-wrapper-basic-hooks.tsx.template"
    elif not capabilities.has_page_hooks and not capabilities.has_mobile_hook:
        return "child-wrapper-no-hooks.tsx.template"
    else:
        return "child-wrapper-no-mobile.tsx.template"
```

#### 3. Variable Substitution Phase
```python
def generate_variables(config: PageConfig, capabilities: ProjectCapabilities) -> Dict[str, str]:
    variables = {
        'PARENT_NAME': config.parent.capitalize(),
        'PARENT_ID': config.parent.lower(),
        'CHILD_NAME': config.page_name,
        'CHILD_ID': config.base_name.lower(),
        'CHILD_DISPLAY_NAME': config.display_name,
    }
    
    # Dynamic content generation
    if capabilities.has_mobile_hook and config.mobile:
        variables['MOBILE_DETECTION'] = 'const isMobile = useIsMobile();'
        variables['RENDER_LOGIC'] = f'isMobile ? <Mobile{config.page_name} /> : <{config.page_name} />'
    else:
        variables['RENDER_LOGIC'] = f'<{config.page_name} />'
    
    return variables
```

### Architecture Compliance Checklist

#### For Parent Pages ✅
- [ ] No wrapper component generated
- [ ] Direct hook application (usePageInstructions, usePageActions)  
- [ ] Simple child routing logic (no mobile detection)
- [ ] Store integration for currentChildPage
- [ ] Component key for re-mounting

#### For Child Pages ✅
- [ ] Wrapper component handles mobile switching
- [ ] Shared pageId between mobile/desktop variants
- [ ] Context hooks applied in wrapper
- [ ] No duplicate action/instruction configurations
- [ ] Template selection based on detected capabilities

#### For Navigation System ✅
- [ ] Store-integrated navigation state
- [ ] Persistent currentChildPage state
- [ ] Dynamic navigation hook generation
- [ ] Project-aware navigation methods (no hard-coding)

### Best Practices

#### Template Development
1. **Single Responsibility**: Each template serves one specific architectural purpose
2. **Conditional Logic**: Use template variables for conditional rendering
3. **Hook Detection**: Adapt template behavior to available project hooks
4. **Consistency**: Follow established naming and structure conventions

#### Variable Naming
1. **Case Sensitivity**: Maintain proper PascalCase/camelCase/lowercase conventions
2. **Descriptive Names**: Variable names should clearly indicate their purpose
3. **Namespace**: Group related variables with prefixes (PARENT_, CHILD_, MOBILE_)

#### Generation Logic
1. **Capability Detection**: Always detect before generating
2. **Template Selection**: Choose appropriate template based on capabilities
3. **Validation**: Verify generated code matches architecture patterns
4. **Error Handling**: Clear error messages for capability mismatches

## Conclusion

This template system successfully addresses the architectural flaws identified in the original generator while maintaining all beneficial functionality. Key achievements:

### Architectural Improvements
- ✅ **Eliminated unnecessary parent wrappers** - Parents are direct tab targets
- ✅ **Correct mobile switching responsibility** - Handled in child wrappers
- ✅ **Phase 2 compliance** - Single pageId, automatic device detection
- ✅ **Reduced file count** - 6 → 5 files per parent page

### Template System Benefits  
- ✅ **Adaptive generation** - Templates adapt to project capabilities
- ✅ **Maintainable code** - Templates separate from generation logic
- ✅ **Consistent output** - All generated code follows architectural patterns
- ✅ **Extensible design** - Easy to add new template variants

### Developer Experience
- ✅ **Clear responsibility model** - Each component has single, clear purpose
- ✅ **Project-agnostic** - Works with any React/TypeScript project structure
- ✅ **Hook-aware** - Adapts to available hooks in target project
- ✅ **Architecture-aligned** - Generated code follows documented patterns

The template system provides a solid foundation for the redesigned generator, ensuring architectural compliance while maintaining the flexibility and power of the original system.