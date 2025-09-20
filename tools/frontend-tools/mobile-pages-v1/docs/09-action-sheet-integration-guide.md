# Action Sheet Integration Guide - Generated Pages to TabBar System

## Overview

This document covers the complete integration process required to connect generated parent pages with the existing TabBar navigation system. This was discovered while fixing missing "Go to Analytics" and "Go to Dashboard" buttons in the testsection action sheet.

## Root Cause Analysis

The mobile-pages-v2 generator successfully creates all the necessary scaffolding (action definitions, placeholder hooks, page components) but does **not** automatically integrate with the existing navigation system. Four critical integration points were missing:

1. **Action Definitions** - Generated correctly ✅
2. **Hook Implementation** - Missing actual navigation methods ❌
3. **ActionSheetContainer Integration** - Missing testsection actionMap ❌
4. **PAGE_ACTIONS Registration** - Missing testsection import/registration ❌

## Complete Integration Process

### Problem: Empty Action Sheets

**Symptoms:**
- Action sheet appears but shows no navigation buttons
- "Go to [ChildPage]" buttons missing from parent action sheets
- Console warnings: `No handler found for action: go-to-analytics on page: testsection`

**Root Cause:** Generated code not integrated into TabBar navigation system

### Step 1: Implement Hook Methods

**File:** `/src/hooks/{parent}/use{Parent}Actions.ts`

**Issue:** Generated hook was a placeholder with commented code

**Before:**
```typescript
export function useTestsectionActions() {
  // const { setSelectedTab, setCurrentChildPage } = useAppStore();
  // Navigation methods will be added here when children are created

  return {
    // Action methods will be returned here when children are created
  }
}
```

**After:**
```typescript
import { useAppStore } from '../../stores/appStore';

export function useTestsectionActions() {
  const { setCurrentChildPage } = useAppStore();

  const goToAnalytics = () => {
    setCurrentChildPage('analytics');
  };

  const goToDashboard = () => {
    setCurrentChildPage('dashboard');
  };

  return {
    goToAnalytics,
    goToDashboard
  }
}
```

**Key Points:**
- Use `setCurrentChildPage()` for child navigation (not `setSelectedTab()`)
- Method names must match action IDs: `go-to-analytics` → `goToAnalytics`
- Return object must export all navigation methods

### Step 2: ActionSheetContainer Integration

**File:** `/src/components/action-sheet/ActionSheetContainer.tsx`

**Issue:** Generated parent page not included in action mapping system

**Required Changes:**

**A. Import the hook:**
```typescript
import { useTestsectionActions } from "../../hooks/testsection/useTestsectionActions";
```

**B. Initialize the hook:**
```typescript
const testsectionActions = useTestsectionActions();
```

**C. Add to actionMap (around line 189):**
```typescript
testsection: {
  "go-to-analytics": testsectionActions.goToAnalytics,
  "go-to-dashboard": testsectionActions.goToDashboard,
},
```

**D. Add to dependency array (around line 238):**
```typescript
testsectionActions,
```

### Step 3: PAGE_ACTIONS Registration

**File:** `/src/constants/actions/page-actions.constants.ts`

**Issue:** Generated actions not registered in the main PAGE_ACTIONS lookup

**Required Changes:**

**A. Import the generated actions:**
```typescript
import { pageActions as testsectionActions } from './pages/testsection'
```

**B. Register in PAGE_ACTIONS object:**
```typescript
testsection: testsectionActions.actions,
```

## Architecture Understanding

### Action Sheet Flow
Complete action flow requires all four components:

```
Action Definition → PAGE_ACTIONS → ActionSheet → ActionSheetContainer → Hook Method
     ↓                 ↓              ↓              ↓                  ↓
  Generated        Missing        Works          Missing           Missing
```

### Navigation Method Patterns

**Parent Tab Navigation:**
```typescript
const goToChildPage = () => {
  setCurrentChildPage('childpage');  // Child page navigation
};
```

**Main Tab Navigation:**
```typescript
const goToMainTab = () => {
  setSelectedTab('maintab');  // Main tab navigation
};
```

### Action ID Mapping
Action IDs in generated files use kebab-case, but hook methods use camelCase:

```typescript
// In action definition:
id: 'go-to-analytics'

// In hook method:
goToAnalytics: () => { ... }

// In actionMap:
"go-to-analytics": testsectionActions.goToAnalytics
```

## Integration Checklist

When adding a new generated parent page to the TabBar system:

### Generated Code Verification
- [ ] Action definitions generated correctly in `/constants/actions/pages/{parent}.ts`
- [ ] Hook placeholder created in `/hooks/{parent}/use{Parent}Actions.ts` 
- [ ] Page components generated in `/pages/{parent}/`

### Manual Integration Required
- [ ] Implement actual navigation methods in hook (replace placeholders)
- [ ] Import and initialize hook in `ActionSheetContainer.tsx`
- [ ] Add actionMap entry for the parent page in `ActionSheetContainer.tsx`
- [ ] Add hook to dependency array in `ActionSheetContainer.tsx`
- [ ] Import and register actions in `page-actions.constants.ts`

### Testing Verification
- [ ] Build succeeds without TypeScript errors
- [ ] Action sheet appears with correct navigation buttons
- [ ] Button clicks navigate to correct child pages
- [ ] No console warnings about missing handlers

## Common Integration Issues

### Issue 1: Hook Methods Not Called
**Symptoms:** Buttons appear but don't navigate
**Cause:** Missing actionMap entry in ActionSheetContainer
**Solution:** Add parent page to actionMap with correct method mapping

### Issue 2: Empty Action Sheet
**Symptoms:** Action sheet shows no buttons
**Cause:** Parent page not registered in PAGE_ACTIONS
**Solution:** Import and register actions in page-actions.constants.ts

### Issue 3: Console Warnings
**Symptoms:** `No handler found for action: go-to-analytics`
**Cause:** Hook methods not implemented or not properly mapped
**Solution:** Implement actual methods in hook and verify actionMap

### Issue 4: TypeScript Errors
**Symptoms:** Build fails with hook-related errors
**Cause:** Missing imports or incorrect method signatures
**Solution:** Verify all imports and method return types

## Generator Improvements Needed

Based on this integration experience, the generator should be enhanced to:

1. **Auto-generate hook implementations** with actual `setCurrentChildPage()` calls
2. **Auto-update ActionSheetContainer** to add import, initialization, and actionMap entries  
3. **Auto-update PAGE_ACTIONS** to register new parent page actions
4. **Integration validation** to detect missing integration points
5. **Documentation generation** for required manual steps

## Files Modified Example

For testsection integration, these files were modified:

1. `/src/hooks/testsection/useTestsectionActions.ts` - Added navigation methods
2. `/src/components/action-sheet/ActionSheetContainer.tsx` - Added testsection integration
3. `/src/constants/actions/page-actions.constants.ts` - Registered testsection actions

## Testing Commands

```bash
# Build verification
npm run build

# Development testing  
npm run dev

# Manual testing checklist:
# 1. Navigate to parent tab
# 2. Open action sheet
# 3. Verify "Go to [Child]" buttons appear
# 4. Click buttons to verify navigation
# 5. Check browser console for errors
```

## Integration Impact

This integration process must be completed for **every parent page** generated by mobile-pages-v2. Without these steps:

- Action sheets will be empty or non-functional
- Child page navigation will not work  
- Console will show handler warnings
- Generated code remains disconnected from app

## Future Automation

Consider automating these integration steps in future generator versions:

- Template-based ActionSheetContainer updates
- Automatic PAGE_ACTIONS registration
- Hook implementation generation
- Integration validation scripts

This would reduce the manual integration overhead and prevent missing integration points.

## CRITICAL GAP: Child Page Action Integration Failure

### Overview

After analyzing the `base-app` source code structure, a critical gap was discovered that is causing child page actions to fail completely. The issue extends beyond parent page integration and affects the fundamental architecture of child page action sheets.

### Problem: Child Pages Missing Common Actions

**Symptoms:**
- Child pages like `analytics` and `dashboard` only show their page-specific actions
- Missing sibling navigation buttons (e.g., no "Go to Dashboard" on Analytics page)
- Missing utility actions like "Toggle Fullscreen" and "Restart Animation"
- Child pages feel isolated and disconnected from navigation system

### Root Cause Analysis

#### 1. Child Pages Not Registered in PAGE_ACTIONS

**Critical Issue:** Generated child page actions are NOT included in the main `PAGE_ACTIONS` registry:

```typescript
// In page-actions.constants.ts - MISSING:
// analytics: mergeWithCommonActions([...], ['go-to-dashboard']),
// dashboard: mergeWithCommonActions([...], ['go-to-analytics']),
```

**Current Broken State:**
```typescript
// analytics.ts - standalone, isolated
export const pageActions = {
  id: 'analytics',
  actions: [
    { id: 'toggle-analytics', label: 'Toggle Analytics', icon: EyeOff, variant: 'default' }
  ]
}
// This file exists but is NEVER referenced by the main system!
```

#### 2. Missing Common Action Integration

**Working Example (Existing Pages):**
```typescript
// dragtest has full common action integration
dragtest: mergeWithCommonActions([
  { id: 'reset-board', label: 'Reset Board', icon: RotateCcw, variant: 'secondary' }
], ['go-to-audio-test', 'go-to-layout-test', 'go-to-mobile-drag-test']),
```

**Broken Example (Generated Pages):**
```typescript
// analytics has NO common action integration
// Missing: sibling navigation, utilities, proper merging
```

#### 3. Generator Gap: Incomplete Integration

The `ChildPageGenerator` creates individual action files but:
- ❌ Doesn't add child pages to main `PAGE_ACTIONS` registry
- ❌ Doesn't merge with common actions for sibling navigation
- ❌ Doesn't import child action files in `page-actions.constants.ts`
- ❌ Doesn't update the main actions registry

### Child Action Integration Architecture

#### Expected Flow for Child Pages
```
Child Page Action File → Import in page-actions.constants.ts → mergeWithCommonActions → PAGE_ACTIONS Registry
        ↓                           ↓                              ↓                        ↓
    Generated ✅              Missing ❌                      Missing ❌              Missing ❌
```

#### Critical Missing Components

**1. Import Statements Missing:**
```typescript
// Should be in page-actions.constants.ts but MISSING:
import { pageActions as analyticsActions } from './pages/analytics'
import { pageActions as dashboardActions } from './pages/dashboard'
```

**2. Registry Entries Missing:**
```typescript
// Should be in PAGE_ACTIONS but MISSING:
analytics: mergeWithCommonActions([
  ...analyticsActions.actions
], ['go-to-dashboard']), // sibling navigation

dashboard: mergeWithCommonActions([
  ...dashboardActions.actions  
], ['go-to-analytics']), // sibling navigation
```

**3. Sibling Action Groups Missing:**
```typescript
// Should be in COMMON_ACTION_GROUPS but MISSING:
testsectionSiblings: [
  'go-to-analytics',
  'go-to-dashboard'
],
```

### Complete Child Action Integration Fix

#### Step 1: Update COMMON_ACTIONS
```typescript
// Add to common-actions.constants.ts
export const COMMON_ACTIONS: Record<string, ActionSheetAction> = {
  // ... existing actions
  "go-to-analytics": {
    id: "go-to-analytics",
    label: "→ Analytics",
    icon: Navigation,
    variant: "secondary",
  },
  "go-to-dashboard": {
    id: "go-to-dashboard", 
    label: "→ Dashboard",
    icon: Navigation,
    variant: "secondary",
  },
};
```

#### Step 2: Update COMMON_ACTION_GROUPS
```typescript
// Add to common-actions.constants.ts
export const COMMON_ACTION_GROUPS = {
  // ... existing groups
  testsectionSiblings: [
    'go-to-analytics',
    'go-to-dashboard'
  ],
};
```

#### Step 3: Import and Register Child Actions
```typescript
// Add to page-actions.constants.ts
import { pageActions as analyticsActions } from './pages/analytics'
import { pageActions as dashboardActions } from './pages/dashboard'

export const PAGE_ACTIONS: Record<string, ActionSheetAction[]> = {
  // ... existing pages
  analytics: mergeWithCommonActions([
    ...analyticsActions.actions
  ], ['go-to-dashboard']),
  
  dashboard: mergeWithCommonActions([
    ...dashboardActions.actions
  ], ['go-to-analytics']),
};
```

#### Step 4: Update ActionSheetContainer
```typescript
// Add to ActionSheetContainer.tsx
import { useTestsectionActions } from "../../hooks/testsection/useTestsectionActions";

const testsectionActions = useTestsectionActions();

const actionMap: Record<string, Record<string, Fn>> = {
  // ... existing mappings
  analytics: {
    "toggle-analytics": () => console.log("Analytics toggle"),
    "go-to-dashboard": testsectionActions.goToDashboard,
  },
  dashboard: {
    "toggle-dashboard": () => console.log("Dashboard toggle"), 
    "go-to-analytics": testsectionActions.goToAnalytics,
  },
};
```

### Generator Architecture Failure Points

#### Critical Missing Features

**1. Child Action Registry Integration:**
- Generator creates standalone action files
- Never adds them to main PAGE_ACTIONS registry
- Child actions remain orphaned and unused

**2. Common Action Merging:**
- No integration with `mergeWithCommonActions()`
- No sibling navigation generation
- No utility action inheritance

**3. Sibling Relationship Management:**
- Generator knows about sibling relationships
- But doesn't create cross-navigation actions
- Siblings can't navigate to each other

**4. ActionSheet Context Resolution:**
- Child pages need their pageId in action resolution
- But their actions aren't registered for lookup
- Results in empty action sheets

### Impact Assessment

#### Severity: Critical
- Child pages have broken action sheets
- Navigation system doesn't work as intended  
- Generated pages feel incomplete and isolated
- User experience is severely degraded

#### Scope: All Generated Child Pages
- Any child page generated by mobile-pages-v2
- Affects all parent/child page relationships
- Compounds as more pages are generated

#### Business Impact:
- Generated pages appear unfinished
- Users can't navigate between related pages
- Action sheets don't provide expected functionality
- Generator appears to be broken to end users

### Automation Requirements

#### Generator Enhancements Needed:

**1. Child Action Registry Integration:**
```python
# In child_generator.py - ADD:
def update_page_actions_registry(self, child_pages, parent_id):
    """Add child pages to main PAGE_ACTIONS registry with common action merging"""
    # Update page-actions.constants.ts with imports and registrations
```

**2. Sibling Navigation Generation:**
```python
# In child_generator.py - ADD:
def generate_sibling_navigation(self, siblings):
    """Generate cross-navigation actions between sibling pages"""
    # Add sibling actions to COMMON_ACTIONS
    # Create sibling action group in COMMON_ACTION_GROUPS
```

**3. Common Action Merging Integration:**
```python
# In child_generator.py - ADD:
def merge_with_common_actions(self, child_actions, siblings):
    """Integrate child actions with common action system"""
    # Use mergeWithCommonActions pattern for all child pages
```

**4. ActionSheetContainer Integration:**
```python
# In child_generator.py - ADD:
def update_action_sheet_container(self, child_pages, parent_actions):
    """Add child page action mappings to ActionSheetContainer"""
    # Add child page entries to actionMap
```

### Testing Strategy for Child Actions

#### Manual Verification Checklist:
- [ ] Child page actions appear in action sheet
- [ ] Sibling navigation buttons work correctly
- [ ] Utility actions (fullscreen, restart) available
- [ ] No console warnings about missing handlers
- [ ] Child pages feel integrated, not isolated

#### Automated Testing Needs:
- [ ] Action registry completeness validation
- [ ] Sibling navigation link verification
- [ ] Common action inheritance testing
- [ ] ActionSheet context resolution testing

### Lessons Learned: Architecture Gaps

#### Key Insights:

**1. Generator vs Integration Distinction:**
- Generators can create code scaffolding
- But integration into existing systems requires architectural understanding
- Missing integration points cause complete feature failure

**2. Action System Complexity:**
- Child actions require multiple integration points
- One missing link breaks the entire chain
- Common action merging is not optional - it's architectural

**3. Testing Insufficient:**
- Generator tests passed but feature was broken
- Need end-to-end integration testing
- Manual verification still required for complex systems

**4. Documentation Gaps:**
- Focused on parent integration, missed child integration
- Architecture assumptions not documented
- Integration requirements not explicit

#### Architecture Principles Violated:

**1. Single Source of Truth:**
- Child actions created but not registered centrally
- Multiple disconnected action definitions

**2. Consistent Patterns:**
- Generated child actions don't follow existing patterns
- Missing common action merging breaks consistency

**3. Integration Completeness:**  
- Partial integration creates broken user experience
- All integration points must be completed for feature to work

### Future Prevention Strategies

#### 1. Integration-First Generator Design:
- Generate + integrate in single operation
- No orphaned files that aren't connected to main system
- Validate integration completeness automatically

#### 2. Architecture Compliance Testing:
- Test generated code follows existing patterns
- Verify common action merging integration
- Validate action registry completeness

#### 3. End-to-End Feature Testing:
- Test complete user workflows, not just code generation
- Verify action sheets work correctly for generated pages
- Test navigation flows between generated pages

#### 4. Documentation Architecture Focus:
- Document integration requirements explicitly
- Explain all connection points between systems
- Provide troubleshooting for integration failures

This analysis reveals that the child action integration failure is a systemic issue requiring fundamental generator architecture changes, not just bug fixes.

## COMPREHENSIVE GENERATOR & TEMPLATE IMPLEMENTATION FIXES

### Overview of Required Changes

Based on the analysis, the generator system needs complete overhaul in multiple areas:

1. **Template Updates** - Remove placeholders, add dynamic variables
2. **Hook Template Completion** - Full implementation instead of placeholders  
3. **Variable Generator Enhancement** - Create new dynamic variables for complete integration
4. **Parent Generator Integration** - Auto-update ActionSheetContainer and PAGE_ACTIONS
5. **Child Generator Integration** - Complete child action registry integration

### 1. TEMPLATE FIXES

#### A. Parent Actions Template Fix

**File:** `/templates/dynamic/actions/parent-actions.ts.template`

**Current Issues:**
- Contains placeholder actions (`overview`, `grid`, `settings`)
- Uses static action structure
- No dynamic page-specific actions

**Required Fix:**
```typescript
import { Navigation } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: '{{PARENT_ID}}',
  actions: [
    // Child navigation actions  
    {{CHILD_NAVIGATION_ACTIONS}}
    // Page-specific actions
    {{PAGE_SPECIFIC_ACTIONS}}
  ] as ActionSheetAction[]
}
```

**Key Changes:**
- ❌ Remove: `overview`, `grid`, `settings` placeholder actions
- ✅ Add: `{{PAGE_SPECIFIC_ACTIONS}}` variable for dynamic content
- ✅ Keep: `{{CHILD_NAVIGATION_ACTIONS}}` for navigation
- ✅ Simplify: Focus on actual functionality, not generic placeholders

#### B. Parent Hook Template Fix

**File:** `/templates/dynamic/hooks/parent-actions-hook.ts.template`

**Current Issues:**
- Entirely placeholder/commented code
- No actual implementation
- Requires manual replacement

**Required Fix:**
```typescript
import { useAppStore } from '../../stores/appStore';

export function use{{PARENT_NAME}}Actions() {
  const { setCurrentChildPage } = useAppStore();

  {{CHILD_NAVIGATION_METHODS}}

  {{PAGE_SPECIFIC_METHODS}}

  return {
    {{HOOK_RETURN_METHODS}}
  }
}
```

**Key Changes:**
- ✅ Add: Real import statements (no comments)
- ✅ Add: `{{CHILD_NAVIGATION_METHODS}}` for dynamic method generation  
- ✅ Add: `{{PAGE_SPECIFIC_METHODS}}` for page-specific functionality
- ✅ Add: `{{HOOK_RETURN_METHODS}}` for dynamic return object
- ❌ Remove: All placeholder comments

#### C. Child Actions Template Fix

**File:** `/templates/dynamic/actions/child-actions.ts.template`

**Current Issues:**
- Creates isolated actions not integrated with common actions
- No sibling navigation
- Missing utility actions

**Required Fix:**
```typescript
import { {{CHILD_ICONS}} } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: '{{CHILD_ID}}',  
  actions: [
    {{CHILD_SPECIFIC_ACTIONS}}
  ] as ActionSheetAction[]
}
```

**Note:** Child actions will be merged with common actions in the registry, so template stays simple.

### 2. VARIABLE GENERATOR ENHANCEMENTS

#### A. New Variables Needed

**In `variable_generator.py`, add these methods:**

```python
def generate_page_specific_actions(self, config: PageConfig) -> str:
    """Generate page-specific actions based on page capabilities/features."""
    # Example: if page has analytics -> analytics actions
    # Example: if page has dashboard -> dashboard actions
    pass

def generate_child_navigation_methods(self, child_configs: List[PageConfig]) -> str:
    """Generate navigation method implementations for child pages."""
    if not child_configs:
        return '// No child pages configured'
    
    methods = []
    for config in child_configs:
        method = f"""  const goTo{config.base_name.capitalize()} = () => {{
    setCurrentChildPage('{config.page_id}');
  }};"""
        methods.append(method)
    
    return '\n\n'.join(methods)

def generate_page_specific_methods(self, config: PageConfig) -> str:
    """Generate page-specific method implementations."""
    # Based on page features/capabilities
    return '// Page-specific methods will be added based on features'

def generate_hook_return_methods(self, child_configs: List[PageConfig], config: PageConfig) -> str:
    """Generate the return object for the hook with all methods."""
    methods = []
    
    # Add child navigation methods
    for child_config in child_configs:
        methods.append(f"goTo{child_config.base_name.capitalize()}")
    
    # Add page-specific methods (based on features)
    # methods.extend(self.get_page_specific_method_names(config))
    
    return ',\n    '.join(methods)
```

#### B. Enhanced Parent Variable Generation

**Update `generate_parent_variables()` method:**

```python
def generate_parent_variables(self, config: PageConfig, child_configs: List[PageConfig]) -> Dict[str, str]:
    return {
        'PARENT_ID': config.page_id,
        'PARENT_NAME': config.base_name.capitalize(),
        'CHILD_NAVIGATION_ACTIONS': self.generate_child_navigation_actions(child_configs),
        'PAGE_SPECIFIC_ACTIONS': self.generate_page_specific_actions(config),
        'CHILD_NAVIGATION_METHODS': self.generate_child_navigation_methods(child_configs),
        'PAGE_SPECIFIC_METHODS': self.generate_page_specific_methods(config),
        'HOOK_RETURN_METHODS': self.generate_hook_return_methods(child_configs, config),
    }
```

### 3. PARENT GENERATOR INTEGRATION FIXES

#### A. ActionSheetContainer Auto-Integration

**In `parent_generator.py`, add method:**

```python
def update_action_sheet_container(self, config: PageConfig, child_configs: List[PageConfig]):
    """Auto-update ActionSheetContainer with new parent page integration."""
    container_path = self.output_dir / "src/components/action-sheet/ActionSheetContainer.tsx"
    
    if not container_path.exists():
        return
    
    content = container_path.read_text()
    
    # 1. Add import
    hook_import = f'import {{ use{config.base_name.capitalize()}Actions }} from "../../hooks/{config.page_id}/use{config.base_name.capitalize()}Actions";'
    
    # Find import section and add
    import_section = "import { usePlayActions }"  # Find existing pattern
    if import_section in content and hook_import not in content:
        content = content.replace(
            import_section,
            f"{hook_import}\n{import_section}"
        )
    
    # 2. Add hook initialization  
    hook_init = f"  const {config.page_id}Actions = use{config.base_name.capitalize()}Actions();"
    
    # Find hook initialization section
    hook_section = "const playActions = usePlayActions();"
    if hook_section in content and hook_init not in content:
        content = content.replace(
            hook_section,
            f"{hook_section}\n{hook_init}"
        )
    
    # 3. Add actionMap entry
    action_map_entry = self.generate_action_map_entry(config, child_configs)
    
    # Find actionMap and add entry
    if "functionalsplash: {" in content:
        content = content.replace(
            "      },\n      };",
            f"      }},\n{action_map_entry}\n      }};"
        )
    
    # 4. Add to dependency array
    dep_array_addition = f"      {config.page_id}Actions,"
    
    if "functionalSplashActions," in content:
        content = content.replace(
            "functionalSplashActions,",
            f"functionalSplashActions,\n{dep_array_addition}"
        )
    
    container_path.write_text(content)

def generate_action_map_entry(self, config: PageConfig, child_configs: List[PageConfig]) -> str:
    """Generate actionMap entry for the parent page."""
    methods = []
    
    # Add child navigation mappings
    for child_config in child_configs:
        methods.append(f'        "go-to-{child_config.page_id}": {config.page_id}Actions.goTo{child_config.base_name.capitalize()},')
    
    # Add page-specific method mappings
    # methods.extend(self.get_page_specific_mappings(config))
    
    methods_str = '\n'.join(methods)
    
    return f"""      {config.page_id}: {{
{methods_str}
      }},"""
```

#### B. PAGE_ACTIONS Registry Auto-Integration

**In `parent_generator.py`, add method:**

```python
def update_page_actions_registry(self, config: PageConfig):
    """Auto-update PAGE_ACTIONS registry with new parent page."""
    registry_path = self.output_dir / "src/constants/actions/page-actions.constants.ts"
    
    if not registry_path.exists():
        return
        
    content = registry_path.read_text()
    
    # 1. Add import
    import_statement = f"import {{ pageActions as {config.page_id}Actions }} from './pages/{config.page_id}'"
    
    # Find import section 
    if "import { mergeWithCommonActions" in content and import_statement not in content:
        content = content.replace(
            "import { mergeWithCommonActions",
            f"{import_statement}\n import {{ mergeWithCommonActions"
        )
    
    # 2. Add registry entry
    registry_entry = f"  {config.page_id}: {config.page_id}Actions.actions,"
    
    # Find end of PAGE_ACTIONS object
    if "}" in content:
        # Insert before the closing brace
        content = content.replace(
            "}",
            f"{registry_entry}\n}}"
        )
    
    registry_path.write_text(content)
```

### 4. CHILD GENERATOR INTEGRATION FIXES

#### A. Common Actions Integration

**In `child_generator.py`, add methods:**

```python
def update_common_actions(self, parent_config: PageConfig, child_configs: List[PageConfig]):
    """Add child navigation actions to common actions system."""
    common_actions_path = self.output_dir / "src/constants/actions/common-actions.constants.ts"
    
    if not common_actions_path.exists():
        return
        
    content = common_actions_path.read_text()
    
    # Add navigation actions for each child
    for child_config in child_configs:
        action_definition = f'''  "go-to-{child_config.page_id}": {{
    id: "go-to-{child_config.page_id}",
    label: "→ {child_config.base_name.capitalize()}",  
    icon: Navigation,
    variant: "secondary",
  }},'''
        
        # Insert before closing of COMMON_ACTIONS
        if "}" in content and action_definition not in content:
            content = content.replace(
                "};",
                f"{action_definition}\n}};"
            )
    
    # Add sibling group
    sibling_group = f'''{parent_config.page_id}Siblings: [
    {', '.join([f"'go-to-{config.page_id}'" for config in child_configs])},
  ],'''
    
    # Insert sibling group in COMMON_ACTION_GROUPS
    if "export const COMMON_ACTION_GROUPS" in content:
        content = content.replace(
            "};",
            f"{sibling_group}\n}};"
        )
    
    common_actions_path.write_text(content)

def update_child_page_actions_registry(self, parent_config: PageConfig, child_configs: List[PageConfig]):
    """Add child pages to main PAGE_ACTIONS registry with common action merging."""
    registry_path = self.output_dir / "src/constants/actions/page-actions.constants.ts"
    
    content = registry_path.read_text()
    
    # Add imports for each child
    for child_config in child_configs:
        import_stmt = f"import {{ pageActions as {child_config.page_id}Actions }} from './pages/{child_config.page_id}'"
        if import_stmt not in content:
            content = content.replace(
                "import { mergeWithCommonActions",
                f"{import_stmt}\n import {{ mergeWithCommonActions"
            )
    
    # Add registry entries for each child  
    for child_config in child_configs:
        # Get sibling list (all children except current)
        siblings = [config.page_id for config in child_configs if config.page_id != child_config.page_id]
        sibling_actions = [f"'go-to-{sibling}'" for sibling in siblings]
        
        registry_entry = f"""  {child_config.page_id}: mergeWithCommonActions([
    ...{child_config.page_id}Actions.actions
  ], [{', '.join(sibling_actions)}]),"""
        
        # Insert before closing
        content = content.replace(
            "}",
            f"{registry_entry}\n}}"
        )
    
    registry_path.write_text(content)

def update_action_sheet_container_for_children(self, parent_config: PageConfig, child_configs: List[PageConfig]):
    """Add child page action mappings to ActionSheetContainer."""
    container_path = self.output_dir / "src/components/action-sheet/ActionSheetContainer.tsx"
    
    content = container_path.read_text()
    
    # Add action mappings for each child page
    for child_config in child_configs:
        # Get navigation methods for siblings
        sibling_mappings = []
        for sibling in child_configs:
            if sibling.page_id != child_config.page_id:
                sibling_mappings.append(f'        "go-to-{sibling.page_id}": {parent_config.page_id}Actions.goTo{sibling.base_name.capitalize()},')
        
        # Add page-specific action mappings
        page_specific_mappings = [
            f'        "toggle-{child_config.page_id}": () => console.log("{child_config.base_name.capitalize()} toggle"),',
            # Add more based on page capabilities
        ]
        
        all_mappings = sibling_mappings + page_specific_mappings
        mapping_str = '\n'.join(all_mappings)
        
        child_action_map = f"""      {child_config.page_id}: {{
{mapping_str}
      }},"""
        
        # Insert into actionMap
        content = content.replace(
            "      };",
            f"{child_action_map}\n      }};"
        )
    
    container_path.write_text(content)
```

### 5. INTEGRATION WORKFLOW UPDATES

#### A. Parent Generation Enhanced Workflow

**In `parent_generator.py`, update `generate()` method:**

```python
def generate(self, config: PageConfig) -> bool:
    """Enhanced parent generation with full integration."""
    try:
        # 1. Generate core files (existing)
        self._generate_page_components(config)
        self._generate_actions(config)
        self._generate_hooks(config)
        
        # 2. NEW: Auto-integration steps
        child_configs = self._get_existing_children(config.page_id)
        
        # Update ActionSheetContainer
        self.update_action_sheet_container(config, child_configs)
        
        # Update PAGE_ACTIONS registry  
        self.update_page_actions_registry(config)
        
        # 3. Validation
        self._validate_integration(config)
        
        return True
    except Exception as e:
        self.logger.error(f"Parent generation failed: {e}")
        return False

def _validate_integration(self, config: PageConfig):
    """Validate that all integration points are properly connected."""
    # Check ActionSheetContainer has import
    # Check PAGE_ACTIONS has registry entry
    # Check hook file has real implementation
    pass
```

#### B. Child Generation Enhanced Workflow

**In `child_generator.py`, update `generate()` method:**

```python
def generate(self, parent_config: PageConfig, child_configs: List[PageConfig]) -> bool:
    """Enhanced child generation with full integration."""
    try:
        # 1. Generate core files (existing)
        for child_config in child_configs:
            self._generate_child_page(child_config)
            self._generate_child_actions(child_config)
        
        # 2. NEW: Integration steps
        # Update common actions with child navigation
        self.update_common_actions(parent_config, child_configs)
        
        # Add children to PAGE_ACTIONS registry  
        self.update_child_page_actions_registry(parent_config, child_configs)
        
        # Update ActionSheetContainer for child mappings
        self.update_action_sheet_container_for_children(parent_config, child_configs)
        
        # Regenerate parent hook with complete implementation
        self._regenerate_parent_hook(parent_config, child_configs)
        
        return True
    except Exception as e:
        self.logger.error(f"Child generation failed: {e}")
        return False
```

### 6. TESTING & VALIDATION

#### A. Integration Tests

**New test files needed:**

```python
# test_integration_validation.py
def test_action_sheet_container_integration():
    """Verify ActionSheetContainer has all required parent/child mappings."""
    
def test_page_actions_registry_completeness():
    """Verify PAGE_ACTIONS includes all generated pages."""
    
def test_hook_implementation_complete():
    """Verify hooks have real implementations, not placeholders."""

def test_child_common_action_integration():
    """Verify child pages integrate with common actions properly."""
```

#### B. Generator Validation

**Add validation methods:**

```python
def validate_complete_integration(self, config: PageConfig) -> List[str]:
    """Validate all integration points are properly connected."""
    issues = []
    
    # Check ActionSheetContainer
    if not self._check_action_sheet_container_integration(config):
        issues.append("ActionSheetContainer missing integration")
    
    # Check PAGE_ACTIONS registry
    if not self._check_page_actions_registry(config):
        issues.append("PAGE_ACTIONS registry missing entry")
        
    # Check hook implementation
    if not self._check_hook_implementation(config):
        issues.append("Hook has placeholder implementation")
        
    return issues
```

### Summary of Implementation Strategy

This comprehensive fix addresses all the identified issues:

1. **Templates**: Remove placeholders, add dynamic variables for complete functionality
2. **Variable Generator**: Create all necessary dynamic variables for integration  
3. **Parent Generator**: Auto-integrate with ActionSheetContainer and PAGE_ACTIONS
4. **Child Generator**: Full common action integration and registry updates
5. **Validation**: Ensure integration completeness before completion

The key insight is that **generation must include integration** - it's not sufficient to create isolated files that require manual connection. The generator must understand and update the existing system architecture automatically.