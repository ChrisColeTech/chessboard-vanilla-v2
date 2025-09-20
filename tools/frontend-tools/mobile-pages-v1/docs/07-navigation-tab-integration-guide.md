# Navigation and Tab Integration Guide

## Overview

This document provides a comprehensive guide for integrating new pages into the navigation system, including tab updates, routing configuration, and parent-child page structures. This is the **foundational step** required before implementing any page functionality.

## Files to Create/Update

### Basic Tab Addition (Minimum Required)
```
src/
├── components/layout/
│   ├── types.ts                     # ✏️  UPDATE: Add new TabId
│   └── TabBar.tsx                   # ✏️  UPDATE: Add tab config + grid layout
├── pages/
│   ├── index.ts                     # ✏️  UPDATE: Export new page
│   └── YourNewPage.tsx              # 🆕 CREATE: New page component
└── App.tsx                          # ✏️  UPDATE: Add import + routing
```

### Parent-Child Navigation (Full Implementation)
```
src/
├── components/
│   ├── action-sheet/
│   │   └── ActionSheetContainer.tsx # ✏️  UPDATE: Add action mapping
│   ├── layout/
│   │   ├── types.ts                 # ✏️  UPDATE: Add new TabId
│   │   └── TabBar.tsx               # ✏️  UPDATE: Add tab + child clearing
│   └── yournewpage/                 # 🆕 CREATE: Page-specific components
│       ├── ChildPageWrapper.tsx     # 🆕 CREATE: Child page wrapper
│       └── AnotherChildWrapper.tsx  # 🆕 CREATE: Additional child wrapper
├── constants/actions/
│   └── page-actions.constants.ts    # ✏️  UPDATE: Add page actions
├── hooks/
│   ├── core/
│   │   ├── usePageInstructions.ts   # ✏️  UPDATE: Add page instructions
│   │   └── usePageActions.ts        # ✏️  UPDATE: Add page context
│   └── yournewpage/                 # 🆕 CREATE: Page-specific hooks
│       └── useYourPageActions.ts    # 🆕 CREATE: Navigation actions
├── pages/
│   ├── index.ts                     # ✏️  UPDATE: Export new pages
│   └── yournewpage/                 # 🆕 CREATE: Page directory
│       ├── YourNewPageParent.tsx    # 🆕 CREATE: Parent router
│       ├── YourNewPageMain.tsx      # 🆕 CREATE: Main page
│       ├── ChildPage.tsx            # 🆕 CREATE: Child page
│       └── AnotherChildPage.tsx     # 🆕 CREATE: Another child page
├── stores/
│   └── appStore.ts                  # ✏️  UPDATE: Add persistence (if needed)
└── App.tsx                          # ✏️  UPDATE: Add import + routing
```

### Legend
- 🆕 **CREATE** - New file to create
- ✏️ **UPDATE** - Existing file to modify
- 📁 **Directory** - Folder structure

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Basic Tab Addition](#basic-tab-addition)
3. [Parent-Child Page Integration](#parent-child-page-integration)
4. [Advanced Configuration](#advanced-configuration)
5. [Testing and Validation](#testing-and-validation)
6. [Troubleshooting](#troubleshooting)
7. [Implementation Examples](#implementation-examples)

## Prerequisites

### Required Files Structure
```
src/
├── components/layout/
│   ├── types.ts              # TabId definitions
│   ├── TabBar.tsx           # Tab configuration and layout
│   └── AppLayout.tsx        # Layout wrapper (no changes needed)
├── pages/
│   ├── index.ts             # Page exports
│   └── {YourPage}/          # Your new page directory
├── stores/
│   └── appStore.ts          # Navigation state management
└── App.tsx                  # Main routing logic
```

### Understanding the Navigation Flow
```
User Click → TabBar → onTabChange → setSelectedTab (store) → App re-renders → Page Component
```

## Basic Tab Addition

### Step 1: Update Type Definitions (Critical First)

**File:** `src/components/layout/types.ts`

**Action:** Add your new tab to the TabId union type

```typescript
// BEFORE:
export type TabId = 'worker' | 'uitests' | 'casino' | 'play'

// AFTER:
export type TabId = 'worker' | 'uitests' | 'casino' | 'play' | 'yournewpage'
```

**Why First:** TypeScript compilation will fail until all references are updated, forcing you to complete all required changes.

### Step 2: Configure TabBar

**File:** `src/components/layout/TabBar.tsx`

#### A. Import Required Icons

```typescript
import { Settings, Target, Coins, YourIcon } from "lucide-react";
```

#### B. Add Tab Configuration

```typescript
const tabs: Tab[] = [
  {
    id: "worker",
    label: "Stockfish",
    icon: Settings,
    description: "Engine Testing",
  },
  {
    id: "uitests", 
    label: "UI Tests",
    icon: Target,
    description: "UI Testing Hub",
  },
  {
    id: "casino",
    label: "Casino",
    icon: Coins,
    description: "Casino Games",
  },
  {
    id: "play",
    label: "Play",
    icon: Target,
    description: "vs Computer",
  },
  // ADD THIS:
  {
    id: "yournewpage",
    label: "Your Page",
    icon: YourIcon,
    description: "Your Description",
  },
];
```

#### C. Update Grid Layout (Critical)

**Find this line (around line 67):**
```typescript
className="
  w-full h-[57px] 
  grid grid-cols-5 
"
```

**Update to:**
```typescript
className="
  w-full h-[57px] 
  grid grid-cols-6   // Increment by 1 for each new tab
"
```

**Grid Layout Math:**
- 4 tabs + 1 menu button = `grid-cols-5`
- 5 tabs + 1 menu button = `grid-cols-6`
- 6 tabs + 1 menu button = `grid-cols-7`

#### D. Add Child Page Clearing (If Supporting Child Pages)

**Find the onClick handler (around line 82):**
```typescript
onClick={() => {
  // If clicking on UI Tests, Casino, or YOUR NEW PAGE tab, clear any child page
  if (tab.id === 'uitests' || tab.id === 'casino' || tab.id === 'yournewpage') {
    setCurrentChildPage(null);
  }
  
  onTabChange(tab.id);
}}
```

**Note:** Only add your tab to this condition if it will support child page navigation.

### Step 3: Update App Routing

**File:** `src/App.tsx`

#### A. Import Page Component

```typescript
import {
  WorkerTestPage,
  UITestPage,
  PlayPage,
  YourNewPage,  // ADD THIS
} from "./pages";
import { CasinoPage } from "./pages/casino/CasinoPage";
```

#### B. Add Routing Condition

**Find the routing section (around line 96):**
```typescript
{/* Page routing with mobile/desktop switching */}
{selectedTab === "worker" && <WorkerTestPage />}
{selectedTab === "uitests" && <UITestPage />}
{selectedTab === "casino" && <CasinoPage />}
{selectedTab === "play" && <PlayPage />}
{selectedTab === "yournewpage" && <YourNewPage />} {/* ADD THIS */}
```

### Step 4: Create Page Component

#### A. Create Page File

**File:** `src/pages/YourNewPage.tsx` (or `src/pages/yournewpage/YourNewPageMain.tsx`)

```typescript
import React from 'react'

export const YourNewPage: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Your New Page</h1>
      <p>Welcome to your new page! Use the action sheet to access page features.</p>
      
      {/* Your page content here */}
      <div className="mt-8">
        <h2 className="text-lg font-semibold mb-4">Page Features</h2>
        <ul className="list-disc list-inside space-y-2">
          <li>Feature 1</li>
          <li>Feature 2</li>
          <li>Feature 3</li>
        </ul>
      </div>
    </div>
  )
}
```

#### B. Export from Pages Index

**File:** `src/pages/index.ts`

```typescript
// ADD THIS LINE:
export { YourNewPage } from './YourNewPage'

// OR if using directory structure:
export { YourNewPage } from './yournewpage/YourNewPageMain'

// ... existing exports
export { WorkerTestPage } from './worker/WorkerTestPage'
export { UITestPage } from './uitests/UITestPage'
export { PlayPage } from './play/PlayPage'
```

## Parent-Child Page Integration

### When to Use Parent-Child Structure

Use parent-child navigation when your page needs:
- Multiple sub-pages or views
- Drill-down navigation patterns
- Context-specific actions and instructions
- Complex functionality split across multiple screens

### Implementation Steps

#### Step 1: Update Store Persistence (If Child Pages Need Persistence)

**File:** `src/stores/appStore.ts`

**Find the partialize section:**
```typescript
partialize: (state) => ({
  selectedTab: state.selectedTab,
  currentChildPage: state.currentChildPage, // Ensure this exists
  // ... other persisted state
})
```

#### Step 2: Create Parent Page Structure

**File:** `src/pages/yournewpage/YourNewPageParent.tsx`

```typescript
import React from 'react'
import { useAppStore } from '../../stores/appStore'
import { YourNewPageMain } from './YourNewPageMain'
import { YourChildPageWrapper } from '../../components/yournewpage/YourChildPageWrapper'
import { AnotherChildPageWrapper } from '../../components/yournewpage/AnotherChildPageWrapper'

export const YourNewPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage)
  
  // Default to main page
  let CurrentPageComponent = YourNewPageMain
  
  // Child page routing
  if (currentChildPage === 'yourchildpage') {
    CurrentPageComponent = YourChildPageWrapper
  } else if (currentChildPage === 'anotherchildpage') {
    CurrentPageComponent = AnotherChildPageWrapper
  }
  
  return (
    <CurrentPageComponent 
      key={`yournewpage-${currentChildPage || 'main'}`}
    />
  )
}
```

#### Step 3: Create Main Page Component

**File:** `src/pages/yournewpage/YourNewPageMain.tsx`

```typescript
import React from 'react'

export const YourNewPageMain: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Your New Page</h1>
      <p className="mb-6">This is the main page. Use the action sheet to navigate to child pages.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card-gaming p-4">
          <h3 className="font-semibold mb-2">Child Page 1</h3>
          <p className="text-sm text-muted-foreground">
            Access Child Page 1 through the action sheet menu.
          </p>
        </div>
        
        <div className="card-gaming p-4">
          <h3 className="font-semibold mb-2">Child Page 2</h3>
          <p className="text-sm text-muted-foreground">
            Access Child Page 2 through the action sheet menu.
          </p>
        </div>
      </div>
    </div>
  )
}
```

#### Step 4: Create Child Page Wrappers

**File:** `src/components/yournewpage/YourChildPageWrapper.tsx`

```typescript
import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { YourChildPage } from '../../pages/yournewpage/YourChildPage'

export const YourChildPageWrapper: React.FC = () => {
  usePageInstructions('yourchildpage')
  usePageActions('yourchildpage')
  
  return <YourChildPage />
}
```

#### Step 5: Create Child Page Components

**File:** `src/pages/yournewpage/YourChildPage.tsx`

```typescript
import React from 'react'

export const YourChildPage: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Child Page</h1>
      <p className="mb-6">This is a child page of Your New Page.</p>
      
      <div className="space-y-4">
        <div className="card-gaming p-4">
          <h3 className="font-semibold mb-2">Child Page Content</h3>
          <p>Specific functionality for this child page goes here.</p>
        </div>
        
        <div className="card-gaming p-4">
          <h3 className="font-semibold mb-2">Navigation</h3>
          <p>Use the action sheet to access child page actions or return to main page.</p>
        </div>
      </div>
    </div>
  )
}
```

#### Step 6: Create Navigation Actions Hook

**File:** `src/hooks/yournewpage/useYourNewPageActions.ts`

```typescript
import { useCallback } from 'react'
import { useAppStore } from '../../stores/appStore'

export const useYourNewPageActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)
  
  const goToChildPage = useCallback(() => {
    setCurrentChildPage('yourchildpage')
  }, [setCurrentChildPage])
  
  const goToAnotherChildPage = useCallback(() => {
    setCurrentChildPage('anotherchildpage')
  }, [setCurrentChildPage])
  
  const backToMain = useCallback(() => {
    setCurrentChildPage(null)
  }, [setCurrentChildPage])
  
  return {
    goToChildPage,
    goToAnotherChildPage,
    backToMain
  }
}
```

#### Step 7: Add Actions to Page Actions Configuration

**File:** `src/constants/actions/page-actions.constants.ts`

```typescript
export const PAGE_ACTIONS: Record<string, ActionSheetAction[]> = {
  // Parent page actions (navigation to child pages)
  yournewpage: [
    {
      id: 'go-to-child-page',
      label: 'Go to Child Page',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'go-to-another-child-page',
      label: 'Go to Another Child Page',
      icon: Navigation,
      variant: 'secondary'
    }
  ],
  
  // Child page actions
  yourchildpage: [
    {
      id: 'child-action-1',
      label: 'Child Action 1',
      icon: TestTube,
      variant: 'default'
    },
    {
      id: 'child-action-2',
      label: 'Child Action 2',
      icon: Settings,
      variant: 'secondary'
    }
  ],
  
  anotherchildpage: [
    {
      id: 'another-child-action',
      label: 'Another Child Action',
      icon: Target,
      variant: 'default'
    }
  ]
}
```

#### Step 8: Update Action Sheet Container

**File:** `src/components/action-sheet/ActionSheetContainer.tsx`

**Import your actions hook:**
```typescript
import { useYourNewPageActions } from '../../hooks/yournewpage/useYourNewPageActions'
```

**Add to actionMap:**
```typescript
const actionMap: Record<string, Record<string, Fn>> = {
  yournewpage: {
    'go-to-child-page': yourNewPageActions.goToChildPage,
    'go-to-another-child-page': yourNewPageActions.goToAnotherChildPage,
  },
  yourchildpage: {
    'child-action-1': yourChildPageActions.childAction1,
    'child-action-2': yourChildPageActions.childAction2,
  },
  anotherchildpage: {
    'another-child-action': anotherChildPageActions.anotherChildAction,
  }
}
```

**Add context resolution:**
```typescript
const currentChildPage = useAppStore((state) => state.currentChildPage)
const actionSheetPage = currentChildPage || currentPage
const actions = PAGE_ACTIONS[actionSheetPage] || []
```

## Advanced Configuration

### Instructions Integration

**File:** `src/hooks/core/usePageInstructions.ts`

```typescript
const INSTRUCTIONS_MAP: Record<string, { title: string; instructions: string[] }> = {
  yournewpage: {
    title: "Your New Page Instructions",
    instructions: [
      "Welcome to your new page",
      "Use the action sheet to navigate",
      "Explore available features"
    ]
  },
  yourchildpage: {
    title: "Child Page Instructions",
    instructions: [
      "This is a child page",
      "Use actions to interact with content",
      "Return to main page via tab click"
    ]
  }
}
```

### Mobile/Desktop Responsive Pages

If you need separate mobile and desktop versions:

```typescript
// In parent page component
import { useIsMobile } from '../../hooks/core/useIsMobile'

export const YourNewPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage)
  const isMobile = useIsMobile()
  
  let CurrentPageComponent = YourNewPageMain
  
  if (currentChildPage === 'yourchildpage') {
    CurrentPageComponent = isMobile ? MobileYourChildPageWrapper : YourChildPageWrapper
  }
  
  return (
    <CurrentPageComponent 
      key={`yournewpage-${currentChildPage || 'main'}-${isMobile ? 'mobile' : 'desktop'}`}
    />
  )
}
```

## Testing and Validation

### Manual Testing Checklist

#### Basic Tab Integration
- [ ] New tab appears in TabBar with correct icon and label
- [ ] Clicking tab navigates to correct page
- [ ] Grid layout remains properly spaced (no overflow/collapse)
- [ ] TypeScript compiles without errors
- [ ] Page content renders correctly
- [ ] Other tabs still work (regression test)

#### Parent-Child Navigation (If Applicable)
- [ ] Action sheet shows navigation actions on main page
- [ ] Clicking navigation action navigates to child page
- [ ] Child page shows correct content and actions
- [ ] Instructions update automatically
- [ ] Clicking parent tab returns to main page
- [ ] State persists through page reloads (if configured)

#### Mobile Responsiveness
- [ ] Tab layout works on mobile devices
- [ ] Page content is mobile-friendly
- [ ] Action sheet functions on touch devices
- [ ] Grid layout adjusts properly on small screens

### Build Testing

```bash
# Verify TypeScript compilation
npm run build

# Verify no layout issues
npm run dev

# Test responsive behavior
# - Resize browser window
# - Test on mobile device/emulator
```

### Common Issues and Solutions

#### Issue: Grid Layout Collapse
**Symptoms:** Tabs appear squished or overlapping
**Solution:** Ensure `grid-cols-X` matches tab count + 1 (for menu button)

#### Issue: TypeScript Compilation Errors
**Symptoms:** Build fails with TabId errors
**Solution:** Update all files in correct order: types.ts → TabBar.tsx → App.tsx → Page Component

#### Issue: Child Page State Not Persisting
**Symptoms:** Child page navigation resets on reload
**Solution:** Ensure `currentChildPage` is included in store `partialize` configuration

#### Issue: Missing Action Sheet Actions
**Symptoms:** Action sheet appears empty or with wrong actions
**Solution:** Verify `PAGE_ACTIONS` configuration and `actionMap` in ActionSheetContainer

## Implementation Examples

### Example 1: Simple Page (No Child Pages)

**Files to Create/Modify:**
1. `src/components/layout/types.ts` - Add TabId
2. `src/components/layout/TabBar.tsx` - Add tab config and grid update
3. `src/App.tsx` - Add routing
4. `src/pages/SimplePage.tsx` - Create page component
5. `src/pages/index.ts` - Export page

### Example 2: Complex Page with Child Navigation

**Files to Create/Modify:**
1. `src/components/layout/types.ts` - Add TabId
2. `src/components/layout/TabBar.tsx` - Add tab config, grid update, child clearing
3. `src/App.tsx` - Add routing
4. `src/pages/complex/ComplexPageParent.tsx` - Parent router
5. `src/pages/complex/ComplexPageMain.tsx` - Main page
6. `src/pages/complex/ChildPage.tsx` - Child page(s)
7. `src/components/complex/ChildPageWrapper.tsx` - Child wrapper(s)
8. `src/hooks/complex/useComplexPageActions.ts` - Navigation actions
9. `src/constants/actions/page-actions.constants.ts` - Action config
10. `src/components/action-sheet/ActionSheetContainer.tsx` - Action mapping
11. `src/pages/index.ts` - Export pages

### File Structure Examples

#### Simple Page Structure:
```
src/pages/
├── SimplePage.tsx
└── index.ts
```

#### Complex Page Structure:
```
src/pages/complex/
├── ComplexPageParent.tsx
├── ComplexPageMain.tsx
├── ChildPageOne.tsx
└── ChildPageTwo.tsx

src/components/complex/
├── ChildPageOneWrapper.tsx
└── ChildPageTwoWrapper.tsx

src/hooks/complex/
└── useComplexPageActions.ts
```

## Summary

This guide covers the complete process of integrating new pages into the navigation system:

1. **Basic Tab Addition** - Essential for any new page
2. **Parent-Child Navigation** - For complex multi-page features
3. **Advanced Configuration** - Instructions, mobile support, actions
4. **Testing and Validation** - Ensuring proper implementation

**Critical Success Factors:**
- Update files in correct order (types → TabBar → App → pages)
- Calculate grid layout correctly (tabs + 1 menu button)
- Include proper child page clearing if needed
- Test on multiple devices and screen sizes

**Remember:** Start with basic tab addition first, then add child page navigation if needed. The architecture is designed to be incrementally enhanced without breaking existing functionality.