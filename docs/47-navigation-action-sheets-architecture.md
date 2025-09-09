# Navigation & Action Sheets Architecture

## Overview

This document provides a comprehensive guide to the application's navigation system, tab management, action sheet configuration, and child page integration. The architecture uses Zustand for state management, HeadlessUI for components, and a clean hook-based pattern for page context.

## Table of Contents

1. [Navigation Stack Overview](#navigation-stack-overview)
2. [Tab System Architecture](#tab-system-architecture)  
3. [Action Sheet System](#action-sheet-system)
4. [Child Page Navigation](#child-page-navigation)
5. [Store Integration](#store-integration)
6. [Hook Patterns](#hook-patterns)
7. [Configuration Guide](#configuration-guide)
8. [Best Practices](#best-practices)

## Navigation Stack Overview

The application uses a multi-layer navigation system:

```
┌─────────────────────────────────────────┐
│                App Layout               │
├─────────────────────────────────────────┤
│              Tab Navigation             │
├─────────────────────────────────────────┤
│              Page Content               │
│  ┌───────────────────────────────────┐  │
│  │         Child Pages               │  │
│  │    (dragtest, uiaudiotest)        │  │
│  └───────────────────────────────────┘  │
├─────────────────────────────────────────┤
│             Action Sheets               │
└─────────────────────────────────────────┘
```

### Key Components

- **App Store** (`appStore.ts`) - Central state management with Zustand
- **Tab Bar** (`TabBar.tsx`) - Main navigation interface
- **Action Sheets** (`ActionSheetContainer.tsx`) - Context-sensitive actions
- **Page Instructions** (`usePageInstructions.ts`) - Automated instruction loading
- **Child Page Navigation** - Store-integrated sub-page system

## Tab System Architecture

### Tab Configuration

Tabs are defined in `src/components/layout/types.ts`:

```typescript
export type TabId = 'layout' | 'worker' | 'uitests' | 'slots' | 'play' | 'splash'
```

### Tab Flow

```
User Click → TabBar → onTabChange → setSelectedTab (store) → App re-renders
```

**Code Path:**
1. `TabBar.tsx` - User clicks tab button
2. **Child page clearing** - If tab supports child pages (`uitests` or `splash`), clear child page state
3. `onTabChange(tab.id)` - Callback to App.tsx
4. `setSelectedTab()` - Updates Zustand store
5. `App.tsx` - Re-renders with new selectedTab
6. Page routing renders appropriate component

**Critical Tab Behavior:**
- Clicking **UI Tests** or **Splash** tabs always returns to main page and clears child navigation
- This ensures consistent "back to home" behavior for hierarchical navigation
- Implementation: `if (tab.id === 'uitests' || tab.id === 'splash') { setCurrentChildPage(null) }`

### Tab State Management

```typescript
// Store state
interface AppState {
  selectedTab: TabId
  currentChildPage: string | null
}

// Usage in components
const selectedTab = useSelectedTab()
const setSelectedTab = useAppStore((state) => state.setSelectedTab)
```

## Action Sheet System

### Architecture Overview

Action sheets provide context-sensitive actions for each page using HeadlessUI Dialog components.

```
┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Page Actions   │───▶│  Action Sheet   │───▶│   HeadlessUI     │
│   Constants      │    │   Container     │    │    Dialog        │
└──────────────────┘    └─────────────────┘    └──────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   useXActions    │    │  Action Mapping │    │  User Interface  │
│     Hooks        │    │   & Execution   │    │                  │
└──────────────────┘    └─────────────────┘    └──────────────────┘
```

### Action Configuration

Actions are defined in `src/constants/actions/page-actions.constants.ts`:

```typescript
export const PAGE_ACTIONS: Record<string, ActionSheetAction[]> = {
  uitests: [
    {
      id: 'run-ui-tests',
      label: 'Run UI Tests',
      icon: TestTube,
      variant: 'default'
    },
    {
      id: 'go-to-drag-test',
      label: 'Go to Drag Test',
      icon: Navigation,
      variant: 'secondary'
    }
  ]
}
```

### Action Handler Mapping

```typescript
// ActionSheetContainer.tsx
const actionMap: Record<string, Record<string, Fn>> = {
  uitests: {
    'run-ui-tests': uiTestsActions.runUITests,
    'go-to-drag-test': uiTestsActions.goToDragTest,
  }
}
```

### Page Context Resolution

```typescript
// Determine which actions to show
const currentChildPage = useAppStore((state) => state.currentChildPage)
const actionSheetPage = currentChildPage || currentPage

// Show actions for child page or main tab
const actions = PAGE_ACTIONS[actionSheetPage] || []
```

## Child Page Navigation

### Problem Solved

Traditional tab-based navigation doesn't support hierarchical pages. Our solution enables:

- Navigate to child pages without changing tabs
- Child pages have their own instructions and actions
- Proper back navigation to parent page
- State persistence across app reloads

### Implementation

#### 1. Store State

```typescript
interface AppState {
  selectedTab: TabId          // Main tab (uitests, worker, etc.)
  currentChildPage: string | null  // Child page (dragtest, uiaudiotest)
}
```

#### 2. Navigation Actions

```typescript
// Navigate to child page
const goToDragTest = useCallback(() => {
  setCurrentChildPage('dragtest')
  playMove(false)
}, [setCurrentChildPage, playMove])

// Return to main page
const backToMain = useCallback(() => {
  setCurrentChildPage(null)
}, [setCurrentChildPage])
```

#### 3. Page Rendering

```typescript
// UITestPage.tsx
const currentChildPage = useAppStore((state) => state.currentChildPage)

let CurrentPageComponent = UITestsMainPage

if (currentChildPage === 'dragtest') {
  CurrentPageComponent = DragTestPageWrapper
} else if (currentChildPage === 'uiaudiotest') {
  CurrentPageComponent = UIAudioTestPageWrapper
}

return <CurrentPageComponent />
```

#### 4. Context Switching

Child pages automatically load their own instructions and actions:

```typescript
// DragTestPageWrapper.tsx
export const DragTestPageWrapper: React.FC = () => {
  usePageInstructions('dragtest')  // Loads dragtest instructions
  usePageActions('dragtest')       // Loads dragtest actions
  
  return <DragTestPage />
}
```

### Navigation Flow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ UI Tests    │───▶│ Action Sheet │───▶│ Child Page  │
│ Main Page   │    │ "Go to Drag" │    │ (dragtest)  │
└─────────────┘    └──────────────┘    └─────────────┘
       ▲                                       │
       │            ┌──────────────┐          │
       └────────────│ Click Tab    │◀─────────┘
                    │ "UI Tests"   │
                    └──────────────┘
```

## Store Integration

### Zustand Configuration

```typescript
export const useAppStore = create<AppStore>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        // Navigation state
        selectedTab: 'layout',
        currentChildPage: null,
        
        // Actions
        setSelectedTab: (tab) => set({ selectedTab: tab }),
        setCurrentChildPage: (childPage) => set({ currentChildPage: childPage }),
      }),
      {
        name: 'chess-app-store',
        partialize: (state) => ({
          selectedTab: state.selectedTab,
          currentChildPage: state.currentChildPage, // Persisted!
          // ... other state
        })
      }
    )
  )
)
```

### Persistence Benefits

- **App reloads**: Child page state survives refresh
- **Browser navigation**: Back/forward works correctly  
- **Session continuity**: User returns to same child page
- **Development**: Hot reload preserves navigation state

## Hook Patterns

### usePageInstructions

Automatically loads page-specific instructions:

```typescript
export const usePageInstructions = (pageId: string) => {
  const { setInstructions } = useInstructions()

  useEffect(() => {
    const pageInstructions = instructionsService.getInstructions(pageId)
    if (pageInstructions) {
      setInstructions(pageInstructions.title, [...pageInstructions.instructions])
    }
  }, [pageId, setInstructions])
}
```

### usePageActions

Sets page context for action sheets:

```typescript
export const usePageActions = (pageId: string) => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)
  
  useEffect(() => {
    setCurrentChildPage(pageId)
    
    return () => {
      setCurrentChildPage(null) // Cleanup on unmount
    }
  }, [pageId, setCurrentChildPage])
}
```

### Wrapper Component Pattern

Child pages use wrapper components for context:

```typescript
export const DragTestPageWrapper: React.FC = () => {
  usePageInstructions('dragtest')  // Instructions context
  usePageActions('dragtest')       // Actions context
  
  return <DragTestPage />          // Actual page content
}
```

## Configuration Guide

### Adding a New Tab

1. **Update types:**
```typescript
// src/components/layout/types.ts
export type TabId = 'layout' | 'worker' | 'uitests' | 'slots' | 'play' | 'splash' | 'newtab'
```

2. **Add tab configuration:**
```typescript
// src/components/layout/TabBar.tsx
const tabs: Tab[] = [
  // existing tabs...
  {
    id: "newtab",
    label: "New Tab",
    icon: YourIcon,
    description: "Description",
  }
]
```

3. **Add routing:**
```typescript
// src/App.tsx
{selectedTab === 'newtab' && <NewTabPage />}
```

4. **Add actions:**
```typescript
// src/constants/actions/page-actions.constants.ts
export const PAGE_ACTIONS: Record<string, ActionSheetAction[]> = {
  newtab: [
    {
      id: 'new-action',
      label: 'New Action',
      icon: ActionIcon,
      variant: 'default'
    }
  ]
}
```

### Adding a Child Page

1. **Create page wrapper:**
```typescript
// src/components/ChildPageWrapper.tsx
export const ChildPageWrapper: React.FC = () => {
  usePageInstructions('childpage')
  usePageActions('childpage')
  
  return <ChildPage />
}
```

2. **Add navigation action:**
```typescript
// Parent page actions hook
const goToChildPage = useCallback(() => {
  setCurrentChildPage('childpage')
  playMove(false)
}, [setCurrentChildPage, playMove])
```

3. **Update parent page rendering:**
```typescript
// Parent page component
if (currentChildPage === 'childpage') {
  CurrentPageComponent = ChildPageWrapper
}
```

4. **Add child page actions:**
```typescript
// src/constants/actions/page-actions.constants.ts
export const PAGE_ACTIONS: Record<string, ActionSheetAction[]> = {
  childpage: [
    {
      id: 'child-action',
      label: 'Child Action',
      icon: ChildIcon,
      variant: 'default'
    }
  ]
}
```

### Adding Instructions

1. **Create instruction file:**
```typescript
// src/services/instructions/pages/newpage.instructions.ts
export const newpageInstructions: InstructionsConfig = {
  title: "New Page Instructions",
  instructions: [
    "Step 1: Do something",
    "Step 2: Do something else",
  ]
}
```

2. **Register instructions:**
```typescript
// src/services/instructions/InstructionsService.ts
const instructionsMap: Record<string, InstructionsConfig> = {
  newpage: newpageInstructions,
  // ... existing instructions
}
```

## Best Practices

### State Management

1. **Always use the store** - Never bypass with global variables
2. **Clean up effects** - Clear state on component unmount
3. **Persist navigation state** - Include in store persistence
4. **Use type-safe actions** - Leverage TypeScript for action IDs

### Component Architecture

1. **Wrapper pattern** - Use wrappers for child pages
2. **Single responsibility** - Each hook has one purpose
3. **Consistent naming** - Follow established patterns
4. **Clean imports** - Import only what you need

### Navigation UX

1. **Clear context** - Users should know where they are
2. **Easy back navigation** - Tab click returns to main
3. **Persistent state** - Don't lose user's place
4. **Audio feedback** - Provide sound feedback for actions

### Action Design

1. **Contextual actions** - Show relevant actions for current page
2. **Clear labeling** - Action labels should be descriptive
3. **Consistent icons** - Use appropriate Lucide icons
4. **Proper variants** - Use semantic button variants

## Debugging Tips

### Common Issues

1. **Actions not showing**: Check PAGE_ACTIONS configuration
2. **Wrong instructions**: Verify pageId in usePageInstructions
3. **State not persisting**: Ensure store partialize includes your state
4. **Child pages not rendering**: Check currentChildPage logic

### Debug Tools

1. **React DevTools** - Inspect Zustand store state
2. **Console logs** - Already in place for navigation events
3. **Store subscriptions** - Monitor state changes
4. **Component keys** - Add keys to debug re-renders

### Testing

1. **Reload testing** - Verify state persists across reloads
2. **Navigation flows** - Test all navigation paths
3. **Action execution** - Verify all actions work correctly
4. **Edge cases** - Test rapid navigation, back button, etc.

## Lessons Learned

### Research Insights

During the development of this navigation system, we explored several approaches and learned valuable lessons about implementing hierarchical navigation in React SPAs.

#### Navigation Patterns Research

**What We Discovered:**
- **Navigation Stack Pattern**: Mobile-style push/pop navigation is ideal for drill-down experiences
- **Drill-down Navigation**: Best suited for 2-3 levels max, users should spend time at leaf nodes
- **State Management**: Navigation state must be properly persisted to survive reloads
- **Context Switching**: Instructions and actions need to automatically update with navigation

**Key Research Sources:**
- React Navigation patterns for mobile-first applications
- PatternFly navigation design guidelines  
- HTML5 History API for web-based navigation stacks
- Expo Router and Ionic navigation implementation patterns

#### What Didn't Work

**❌ View Swapping Hack:**
```typescript
// Initial flawed approach
const [currentView, setCurrentView] = useState('main')
if (currentView === 'dragtest') return <DragTestPage />
```
**Problems:** No persistence, breaks instructions, inconsistent with app architecture.

**❌ Window Global Variables:**
```typescript
// Bypassing the store - BAD
(window as any).currentActionSheetPage = 'dragtest'
```  
**Problems:** No persistence, bypasses store, breaks on reload, not reactive.

**❌ Adding More Tabs:**
Adding 8-9 tabs would completely break the UI grid layout and create navigation clutter.

**❌ URL-based Routing:**
While React Router would work, it was overkill for this use case and would complicate the existing tab-based system.

#### What Worked

**✅ Store-Integrated Navigation:**
```typescript
interface AppState {
  selectedTab: TabId           // Main navigation
  currentChildPage: string | null  // Child page state
}
```
**Benefits:** Persistent, reactive, consistent with existing architecture.

**✅ Hook-Based Context:**
```typescript
usePageInstructions('dragtest')  // Auto-loads instructions
usePageActions('dragtest')       // Auto-loads actions
```
**Benefits:** Automatic context switching, cleanup on unmount, consistent pattern.

**✅ Wrapper Component Pattern:**
```typescript
export const DragTestPageWrapper: React.FC = () => {
  usePageInstructions('dragtest')
  usePageActions('dragtest')
  return <DragTestPage />
}
```
**Benefits:** Separation of concerns, reusable, clean composition.

### Implementation Lessons

#### Store Design Principles

1. **Never Bypass the Store**: All navigation state must go through Zustand
2. **Persistence is Critical**: Child page state must survive reloads
3. **Reactivity First**: Use store subscriptions, not manual updates
4. **Type Safety**: Leverage TypeScript for navigation state

#### Component Architecture Insights

1. **Wrapper Pattern**: Child pages need context wrappers for instructions/actions
2. **Conditional Rendering**: Simple `if/else` beats complex routing for child pages
3. **Effect Cleanup**: Always clean up navigation state on unmount
4. **Single Responsibility**: Each hook should have one clear purpose

#### UX Design Learnings

1. **Clear Mental Model**: Users need to understand they're still "within" a tab
2. **Easy Back Navigation**: Tab click should always return to main page
3. **Audio Feedback**: Sound cues help users understand navigation actions
4. **Context Preservation**: Don't lose user's place in navigation hierarchy

#### Development Process Insights

1. **Research First**: Understanding existing patterns saved significant refactoring
2. **Prototype Early**: The "view swapping" approach revealed fundamental issues quickly  
3. **Store Integration**: Fighting the architecture is always harder than working with it
4. **Documentation Matters**: Complex navigation systems need thorough documentation

### Common Pitfalls to Avoid

#### State Management Antipatterns

```typescript
// ❌ DON'T: Bypass store with globals
(window as any).navigationState = 'child'

// ✅ DO: Use store actions
setCurrentChildPage('child')
```

#### Navigation Antipatterns

```typescript
// ❌ DON'T: Complex view swapping
const [views, setViews] = useState(['main'])
const currentView = views[views.length - 1]

// ✅ DO: Simple state-based rendering  
const currentChild = useAppStore(state => state.currentChildPage)
```

#### Context Switching Antipatterns

```typescript
// ❌ DON'T: Manual context management
useEffect(() => {
  setInstructions(getInstructions(pageId))
  setActions(getActions(pageId))
}, [pageId])

// ✅ DO: Dedicated hooks
usePageInstructions(pageId)
usePageActions(pageId)
```

### Performance Considerations

#### What We Learned

1. **Conditional Rendering**: More efficient than maintaining multiple component instances
2. **Store Subscriptions**: Zustand's selector pattern prevents unnecessary re-renders
3. **Effect Dependencies**: Proper dependencies prevent infinite render loops
4. **Component Keys**: Not needed for conditional rendering, saves React work

#### Optimization Strategies

1. **Minimal State**: Only store essential navigation state in the store
2. **Selector Specificity**: Use specific selectors to minimize re-renders
3. **Effect Cleanup**: Always clean up effects to prevent memory leaks
4. **Lazy Loading**: Child pages could be lazy-loaded if they become heavy

### Scalability Insights

#### Adding New Navigation Levels

The current system easily supports:
- **Main Tabs** (6 current, could handle 8-10)
- **Child Pages** (unlimited per tab)  
- **Grandchild Pages** (would need additional store state)

#### Extension Points

1. **Navigation History**: Could add navigation history stack
2. **Deep Linking**: Could integrate with URL fragments
3. **Animation**: Could add page transition animations
4. **Breadcrumbs**: Could show navigation path

### Testing Insights

#### What to Test

1. **State Persistence**: Navigation state survives reload
2. **Context Switching**: Instructions and actions update correctly
3. **Cleanup**: No memory leaks from unmounted components
4. **Edge Cases**: Rapid navigation, back button, deep links

#### Testing Strategies

1. **Integration Tests**: Test full navigation flows
2. **Store Tests**: Test state transitions and persistence
3. **Component Tests**: Test context hook integration
4. **Manual Testing**: Test actual user workflows

## Architecture Benefits

This navigation system provides:

- **Scalability** - Easy to add new tabs and child pages
- **Maintainability** - Clear separation of concerns
- **User Experience** - Smooth navigation with persistence
- **Developer Experience** - Consistent patterns and hooks
- **Performance** - Efficient re-renders and state updates
- **Accessibility** - Built on HeadlessUI primitives

The architecture successfully balances simplicity with flexibility, providing a robust foundation for complex navigation requirements while maintaining clean, maintainable code.