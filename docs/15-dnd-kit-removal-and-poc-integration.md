# DND-Kit Removal & POC Integration Rework

## Document 15: Comprehensive Component Deletion & Recreation Plan

---

## Overview

This document outlines the complete removal of @dnd-kit integration from the chessboard-vanilla-v2 project and replacement with the proven POC (Proof of Concept) drag-and-drop implementation. The current @dnd-kit approach has created transform conflicts and overcomplicated what should be a simple mouse-based drag system.

## Root Problem Analysis

### Current Issue: Transform Conflicts

The handoff document (Document 14) identified **Suspect #1: DragProvider Transform Conflicts** as the primary issue:

- **CSS centering**: `transform: translate(-50%, -50%)`
- **@dnd-kit positioning**: `transform: translate3d(x, y, 0)`
- **Mouse cursor tracking**: Fixed positioning with cursor coordinates

These three transform approaches conflict with each other, causing pieces to appear duplicated, offset, or invisible during drag operations.

### POC Solution: Simple State Management

The POC implementation at `/mnt/c/Projects/chessboard-vanilla-v2-poc/` uses a much simpler approach:

1. **Direct positioning**: `position: fixed` with pixel coordinates
2. **State-driven**: React state updates for cursor position
3. **No transforms**: Avoids CSS transform conflicts entirely
4. **Mouse events**: Simple onMouseDown/Move/Up handlers

---

## Deletion Plan

### ❌ FILES TO DELETE ENTIRELY

#### 1. `/src/providers/DragProvider.tsx`

**Reason for deletion**:

- Complex @dnd-kit integration with transform conflicts
- Attempts to manage drag state through context instead of simple hooks
- Cursor-following implementation conflicts with CSS centering
- Contains debug logging and TypeScript assertion hacks (`draggedPiece!`)

**Lines of evidence**:

```typescript
// Transform conflicts - this is the core problem
top: cursorPosition!.y - 30,
left: cursorPosition!.x - 30,

// Complex event management that POC doesn't need
document.addEventListener('mousemove', mouseMoveHandlerRef.current);
document.addEventListener('mouseup', mouseUpHandlerRef.current);
```

#### 2. `/src/components/chessboard/AnimatedPiece/AnimatedPiece.tsx`

**Reason for deletion**:

- Built specifically for @dnd-kit integration
- Not present in POC implementation
- Unnecessary complexity for basic drag functionality

### 🔄 FILES TO COMPLETELY REWRITE

#### 1. `/src/components/chessboard/Square/Square.tsx`

**Current problems**:

- `useDragContext()` dependency on deleted DragProvider
- Complex drag state calculations: `isDragSource`, `isValidDropTarget`, `shouldBlurPiece`
- @dnd-kit event handlers: `onDragStart`, `onDragEnd`, `onDrop`, `onDragOver`
- Transform-based positioning conflicts

**POC replacement approach**:

```typescript
// Simple mouse event handlers (from POC)
onMouseDown: () => selectHoverFrom(cellPos);
onMouseMove: () => handleGrabbing(x, y);
onMouseUp: () => handleGrabEnd(cellPos);
```

#### 2. `/src/components/chessboard/Piece/Piece.tsx`

**Current problems**:

- Drag event handlers: `onDragStart`, `draggable` attribute
- `isDragging` opacity management conflicts with Square opacity
- React Spring animations tied to drag state
- CSS cursor management conflicts

**POC replacement**: Simple piece rendering without drag concerns

#### 3. `/src/components/chessboard/Board/Board.tsx`

**Current problems**:

- Dependency on DragProvider context
- Passes drag-related props to Square components
- Complex state management for drag operations

**POC replacement**: Simple grid rendering with mouse event delegation

#### 4. `/src/components/chessboard/Chessboard.tsx`

**Current problems**:

- Wraps everything in `<DragProvider>` which will be deleted
- Complex animation coordination with drag system
- Theme integration mixed with drag state

**POC replacement**: Use `useChessBoardInteractive` hook directly

---

## Creation Plan

### ✨ NEW FILES TO CREATE

#### 1. `/src/hooks/useChessBoardInteractive.ts`

**Source**: Port from `/mnt/c/Projects/chessboard-vanilla-v2-poc/src/ChessBoard/useChessBoardInteractive.ts`

**Key functions to port**:

- `selectHoverFrom(cellPos)` - Start drag operation
- `handleGrabbing(x, y)` - Update cursor position during drag
- `handleGrabEnd(cellPos)` - Complete drag operation
- `moveFigure(from, to, figure)` - Execute validated moves

**Integration points**:

- Replace Chess.js calls with our existing services
- Maintain our TypeScript type definitions
- Keep our FEN/position management approach

#### 2. `/src/components/chessboard/HoldedFigure/HoldedFigure.tsx`

**Source**: Port from `/mnt/c/Projects/chessboard-vanilla-v2-poc/src/ChessBoard/HoldedFigure.tsx`

**Key features**:

```typescript
// Simple fixed positioning - no transforms
style={{
    position: 'fixed',
    top: `${grabbingPos[1] - boardConfig.cellSize / 2}px`,
    left: `${grabbingPos[0] - boardConfig.cellSize / 2}px`,
}}
```

**Why this works**:

- Direct pixel positioning
- No CSS transform conflicts
- Simple state-driven updates
- Follows cursor smoothly

---

## Files to Keep

### ✅ INDEPENDENT COMPONENTS (No Changes)

#### 1. `/src/components/chessboard/CoordinateLabels/CoordinateLabels.tsx`

**Status**: KEEP - Independent visual component with no drag dependencies

#### 2. `/src/components/chessboard/SquareHighlight/SquareHighlight.tsx`

**Status**: KEEP - Independent visual component for move indicators

### ❓ FILES TO EVALUATE

#### 1. `/src/components/chessboard/BoardOverlay/BoardOverlay.tsx`

**Evaluation needed**: May contain drag-related functionality that should be removed

---

## DND-Kit Pollution Audit Results

### ✅ Package Dependencies

**Status**: CLEAN - No @dnd-kit packages found in package.json

### ⚠️ Draggable Attributes (8 files infected)

```
src/components/chessboard/AnimatedPiece/AnimatedPiece.tsx - 3 occurrences
src/components/chessboard/Chessboard.tsx - 1 occurrence
src/components/chessboard/Piece/Piece.tsx - 4 occurrences
src/components/chessboard/Square/Square.tsx - 1 occurrence
```

### 🚨 Drag Event Handlers (7 files heavily infected)

```
src/components/chessboard/Board/Board.tsx - 7 occurrences
src/components/chessboard/Piece/Piece.tsx - 7 occurrences
src/components/chessboard/Square/Square.tsx - 13 occurrences
src/hooks/useChessMaster.ts - 2 occurrences
src/hooks/useDragAndDrop.ts - 15 occurrences
src/providers/DragProvider.tsx - 12 occurrences
src/types/component.types.ts - 6 occurrences
src/types/hooks.types.ts - 2 occurrences
```

### 🚨 Drag Context Dependencies (2 files infected)

```
src/components/chessboard/Square/Square.tsx - 2 imports + usage
src/providers/DragProvider.tsx - 6 occurrences (creation + export)
```

## Complete Pollution Analysis

### Files Requiring DELETION

```
❌ src/providers/DragProvider.tsx (12+ drag references)
❌ src/components/chessboard/AnimatedPiece/AnimatedPiece.tsx (3 draggable attributes)
❌ src/hooks/useDragAndDrop.ts (15 drag event handlers) - NOT MENTIONED BEFORE
❌ src/hooks/useChessMaster.ts - MAY NEED DELETION (2 drag handlers)
```

### Files Requiring COMPLETE REWRITE

```
🔄 src/components/chessboard/Square/Square.tsx (13 drag handlers + context usage)
🔄 src/components/chessboard/Piece/Piece.tsx (7 drag handlers + draggable attributes)
🔄 src/components/chessboard/Board/Board.tsx (7 drag handlers)
🔄 src/types/component.types.ts (6 drag-related type definitions)
🔄 src/types/hooks.types.ts (2 drag-related type definitions)
```

### New Files Discovered Needing Attention

- **`src/hooks/useDragAndDrop.ts`** - 15 drag references, likely needs complete deletion
- **`src/hooks/useChessMaster.ts`** - 2 drag references, may be integration layer needing modification

---

## Integration Strategy

### Phase 1: Deletion

1. Delete `DragProvider.tsx`
2. Delete `AnimatedPiece.tsx`
3. Remove all @dnd-kit imports and dependencies

### Phase 2: Creation

1. Port and adapt `useChessBoardInteractive.ts`
2. Create `HoldedFigure.tsx` component
3. Update TypeScript type definitions

### Phase 3: Component Rewrite

1. Rewrite `Square.tsx` with simple mouse events
2. Rewrite `Piece.tsx` without drag handlers
3. Rewrite `Board.tsx` without drag context
4. Rewrite `Chessboard.tsx` with interactive hook

### Phase 4: Integration Testing

1. Verify drag functionality works
2. Test valid move indicators
3. Confirm move restriction enforcement
4. Validate visual feedback

---

## Expected Benefits

### ✅ Problems Resolved

1. **Transform conflicts eliminated** - No competing positioning systems
2. **Simplified architecture** - One clear drag implementation
3. **Better performance** - No complex @dnd-kit overhead
4. **Easier maintenance** - Straightforward mouse event handling
5. **Mobile compatibility** - Touch events work naturally with mouse events

### ✅ Features Restored

1. **Cursor-following pieces** - Clean visual feedback during drag
2. **Valid move indicators** - Clear highlighting of legal moves
3. **Move restrictions** - Prevents invalid drops
4. **Smooth animations** - No transform conflicts

---

## Risk Assessment

### Low Risk

- POC implementation is proven and working
- Simple mouse events are well-supported across browsers
- Fewer dependencies = fewer potential issues

### Medium Risk

- Integration with existing Chess.js services needs careful mapping
- TypeScript type alignment between POC and current implementation
- CSS styling may need adjustments for new positioning approach

### Mitigation Strategy

- Port POC functionality incrementally
- Maintain comprehensive testing throughout process
- Keep backups of current implementation until new system is fully validated

---

## Conclusion

The @dnd-kit integration has created unnecessary complexity and transform conflicts. The POC's simple state management approach with direct mouse events provides a cleaner, more maintainable solution that eliminates the root cause of our drag-and-drop issues.

This rework will restore full drag functionality while simplifying the codebase and improving performance.
