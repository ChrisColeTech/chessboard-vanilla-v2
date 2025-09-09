# 51 - Comprehensive Layout System Guide

## Overview

This document provides a complete guide to the two different layout systems in the responsive chessboard application: the desktop **ChessboardLayout** and the mobile **MobileChessboardLayout**. These layouts handle different form factors and interaction patterns while maintaining consistent visual design.

## Architecture Overview

```
App.tsx
├── AppLayout (Fixed Header/Footer Container)
│   ├── Header (Fixed top-10, z-20)
│   ├── Main Content Area (absolute top-10 bottom-[84px])
│   │   └── Page Components
│   │       ├── Desktop: ChessboardLayout (3x3 Grid)
│   │       └── Mobile: MobileChessboardLayout (3x1 Grid)
│   └── TabBar (Fixed bottom-0, z-20)
```

## Layout Systems

### 1. ChessboardLayout (Desktop - 3x3 Grid)

**File:** `src/components/ChessboardLayout.tsx`

**Purpose:** Desktop and tablet layout using a 3x3 CSS Grid system with flexible positioning.

**Grid Structure:**
```css
grid-template-areas: 
  "top-left    top-center    top-right"
  "center-left center       center-right"  
  "bottom-left bottom-center bottom-right"
```

**Props Interface:**
```typescript
interface ChessboardLayoutProps {
  top?: React.ReactNode      // Top row (captured pieces)
  left?: React.ReactNode     // Left column (captured pieces)
  center: React.ReactNode    // Center (chess board)
  right?: React.ReactNode    // Right column (captured pieces)
  bottom?: React.ReactNode   // Bottom row (captured pieces)
  className?: string
}
```

**Key Features:**
- **Flexible positioning:** Captured pieces can be positioned in any combination (top/bottom, left/right, or both)
- **Resizable container:** Desktop version includes resize handles for testing
- **Responsive scaling:** Uses CSS Grid `1fr` units for automatic sizing
- **Content overflow protection:** Center area uses flexbox centering with `minHeight: '0'` and `minWidth: '0'`

**Usage Example:**
```typescript
<ChessboardLayout
  top={<CapturedPieces pieces={whitePieces} />}
  left={piecesPosition === 'left-right' ? <CapturedPieces pieces={whitePieces} /> : undefined}
  center={<TestBoard onSquareClick={handleClick} />}
  right={piecesPosition === 'left-right' ? <CapturedPieces pieces={blackPieces} /> : undefined}
  bottom={<CapturedPieces pieces={blackPieces} />}
  className="h-full"
/>
```

### 2. MobileChessboardLayout (Mobile - 3x1 Grid)

**File:** `src/components/MobileChessboardLayout.tsx`

**Purpose:** Mobile-optimized vertical layout using a single-column CSS Grid.

**Grid Structure:**
```css
grid-template-rows: '80px auto 80px'
```

**Props Interface:**
```typescript
interface MobileChessboardLayoutProps {
  topPieces?: React.ReactNode     // Top section (captured pieces)
  center: React.ReactNode         // Middle section (chess board) 
  bottomPieces?: React.ReactNode  // Bottom section (captured pieces)
  className?: string
}
```

**Key Features:**
- **Vertical stacking:** Single column layout optimized for portrait mobile screens
- **Auto-sizing center:** Middle row uses `auto` to fit content without gaps
- **Fixed top/bottom heights:** 80px allocated for captured pieces sections
- **Full-width components:** Uses flex containers with `flex: 1` to ensure components span full width
- **Proper padding:** `paddingTop: '40px'` accounts for mobile header overlay

**Cell Container Structure:**
```typescript
// Top & Bottom Pieces Containers
<div style={{
  display: 'flex',
  alignItems: 'center',        // Vertical centering
  width: '100%',
  height: '100%',
  boxSizing: 'border-box',
  overflow: 'hidden'
}}>
  <div style={{ flex: 1, width: '100%', height: '100%' }}>
    {pieces}  // This ensures components span full width/height
  </div>
</div>

// Center Container
<div style={{ 
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',    // Center the chess board
  width: '100%',
  height: '100%',
  minHeight: '0',
  boxSizing: 'border-box',
  overflow: 'hidden'
}}>
  {center}
</div>
```

## Layout Detection & Switching

### Mobile Detection Hook

**File:** `src/hooks/useIsMobile.ts`

```typescript
export function useIsMobile(breakpoint: number = 768): boolean {
  // Returns true for screens < 768px width
  // Automatically updates on window resize
}
```

### Conditional Layout Rendering

**Pattern used in pages:**
```typescript
export const DragTestPage: React.FC = () => {
  const isMobile = useIsMobile();
  
  return (
    <div className="relative min-h-full">
      {/* Background effects */}
      
      {isMobile ? (
        <MobileChessboardLayout
          topPieces={<CapturedPieces pieces={whitePieces} />}
          center={<TestBoard />}
          bottomPieces={<CapturedPieces pieces={blackPieces} />}
        />
      ) : (
        <ChessboardLayout
          top={<CapturedPieces pieces={whitePieces} />}
          center={<TestBoard />}
          bottom={<CapturedPieces pieces={blackPieces} />}
          className="h-full"
        />
      )}
    </div>
  );
};
```

## AppLayout Integration

### Fixed Positioning System

The AppLayout uses fixed positioning for header and footer with an absolute-positioned main content area:

```css
/* Header */
position: fixed
top: 10px (40px - accounts for TitleBar)
z-index: 20

/* Main Content Area */  
position: absolute
top: 10px (below TitleBar, behind header)
bottom: 84px (above TabBar)
z-index: 10

/* TabBar */
position: fixed
bottom: 0
z-index: 20
```

### Z-Index Layers
- **30:** TitleBar (mobile only)
- **20:** Header & TabBar (overlays)
- **10:** Main content (behind header, above background)

### Mobile Considerations

**TitleBar (Mobile Only):**
- Fixed at `top-0` with 40px height
- Only visible on mobile screens
- Pushes header to `top-10` (40px)

**Header Transparency:**
- Semi-transparent glassmorphism design
- Overlays content rather than pushing it down
- Main content starts at `top-10` (behind header, below TitleBar)

## Component Sizing Best Practices

### Full-Width/Height Components

When components need to fill their container completely:

```typescript
// ✅ Correct - Full container fill
<div style={{ 
  flex: 1, 
  width: '100%', 
  height: '100%' 
}}>
  {component}
</div>

// ❌ Incorrect - May not fill completely
<div style={{ width: '100%', height: '100%' }}>
  {component}
</div>
```

### Grid Cell Overflow Prevention

Always use `boxSizing: 'border-box'` and `overflow: 'hidden'`:

```typescript
// ✅ Correct - Prevents overflow
<div style={{
  width: '100%',
  height: '100%',
  boxSizing: 'border-box',
  overflow: 'hidden'
}}>
  {content}
</div>
```

### Center Content Auto-Sizing

For content that should size to fit (like chess boards):

```typescript
// ✅ Correct - Auto-sizes to content
gridTemplateRows: '80px auto 80px'

// ❌ Incorrect - Forces expansion, creates gaps  
gridTemplateRows: '80px 1fr 80px'
```

## Layout Debugging Tips

### Common Issues & Solutions

**1. Grid Cell Overflow:**
- Remove padding/margins from grid containers
- Use `boxSizing: 'border-box'` 
- Remove conflicting CSS classes (like `w-full h-full` in inappropriate contexts)

**2. Components Not Spanning Full Width:**
- Remove `justifyContent: 'center'` from flex containers
- Add wrapper div with `flex: 1, width: '100%', height: '100%'`

**3. Content Gaps in Mobile Layout:**
- Use `auto` instead of `1fr` for center grid row
- Remove min/max height constraints that conflict with grid sizing

**4. Mobile Header Overlap:**
- Ensure main content starts at `top-10` (below TitleBar, behind header)
- Don't push content down further - header should overlay

### Debugging Grid Layout

Use browser dev tools grid inspector:

```css
/* Temporary debugging styles */
.debug-grid {
  grid-template-areas: 
    "top-left    top-center    top-right"
    "center-left center       center-right"  
    "bottom-left bottom-center bottom-right";
}

.debug-grid > * {
  border: 1px solid red;
  background: rgba(255, 0, 0, 0.1);
}
```

## File Structure

```
src/
├── components/
│   ├── ChessboardLayout.tsx          # Desktop 3x3 grid layout
│   ├── MobileChessboardLayout.tsx    # Mobile 3x1 grid layout
│   └── layout/
│       └── AppLayout.tsx             # Main app container
├── hooks/
│   └── useIsMobile.ts                # Mobile detection hook
└── pages/
    └── uitests/
        ├── DragTestPage.tsx          # Example of layout switching
        └── MobileDragTestPage.tsx    # Mobile-specific page
```

## Best Practices Summary

1. **Always use conditional rendering** based on `useIsMobile()` for responsive layouts
2. **Prevent grid overflow** by avoiding padding/borders on grid containers  
3. **Use `flex: 1` wrappers** to ensure components fill their containers completely
4. **Use `auto` sizing** for content that should fit naturally (chess boards)
5. **Use `boxSizing: 'border-box'`** consistently to prevent sizing conflicts
6. **Let headers overlay content** rather than pushing content down on mobile
7. **Test both layouts** during development using browser responsive tools

This dual-layout system provides optimal user experience across all device types while maintaining code organization and reusability.