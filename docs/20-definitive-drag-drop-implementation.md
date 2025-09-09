# Definitive Drag and Drop Implementation Guide

**Document 20 - Final Decision & Implementation Pattern**
_Created: 2025-09-02_

## Executive Summary

After extensive research and multiple attempts with different approaches, this document establishes the **final, definitive drag and drop implementation pattern** for the responsive chessboard project. This decision is **locked in** and should not be changed without exceptional justification.

## Research History & Failed Approaches ❌

### Approach 1: HTML5 Drag & Drop API ❌ REJECTED

**Attempted**: Native browser drag and drop with `draggable={true}`, `onDragStart`, `onDrop`
**Failures**:

- No mobile/touch support
- Browser inconsistencies (Safari, Firefox differences)
- Event handler interruption during React re-renders
- Drag state lost when components remount due to key changes
- Complex event handling with `dragenter`, `dragover`, `dragleave`

**Research Finding**: Document 1 Research #13 explicitly states "HTML5 Drag & Drop API has no mobile support and browser inconsistencies"

### Approach 2: @dnd-kit/core Library ❌ REJECTED

**Attempted**: Modern drag and drop library with accessibility features
**Failures**:

- Transform conflicts: CSS `translate(-50%, -50%)` vs dnd-kit `translate3d(x, y, 0)`
- Redux dependency conflicts causing "Could not find 'store' in the context" errors
- Over-engineering for simple mouse-based interactions
- Bundle size increase (+111 packages)
- Complex integration with existing chess logic

**Research Finding**: Document 15 states "@dnd-kit integration has created unnecessary complexity and transform conflicts"

### Approach 3: @hello-pangea/dnd ❌ REJECTED

**Attempted**: React Beautiful DND successor
**Failures**:

- Redux dependency conflicts
- "Could not find 'store' in the context of 'Connect(Hm)'" errors
- Not suitable for grid-based interactions

## ✅ DEFINITIVE SOLUTION: POC Mouse Event Pattern

### Core Implementation Pattern

Based on the proven POC implementation at `/mnt/c/Projects/chessboard-vanilla-v2-poc/`, the definitive solution uses:

1. **Mouse Events Only**: `onMouseDown`, `onMouseMove`, `onMouseUp`
2. **Fixed Positioning**: Dragged piece follows cursor with `position: fixed`
3. **Document-Level Listeners**: Global mouse tracking during drag operation
4. **State-Based Approach**: React state manages drag context

### Reference Implementation

The proven pattern from `/mnt/c/Projects/chessboard-vanilla-v2-poc/src/ChessBoard/`:

```typescript
// 1. Drag State Management (useChessBoardInteractive.ts)
const [holdedFigure, setHoldedFigure] = useState<Figure>();
const [grabbingPos, setGrabbingPos] = useState<CellPos>([-1, -1]);
const [fromPos, setFromPos] = useState<CellPos>([-1, -1]);
const [possibleMoves, setPossibleMoves] = useState<CellPos[]>([]);

const handleGrabbing = (x: number, y: number) => {
  setGrabbingPos([x, y]);
};

const selectHoverFrom = (cellPos: CellPos) => {
  const { figure, nextMoves } = selectFigureFrom(cellPos);
  if (!figure) return;

  setHoldedFigure(figure);
  setPossibleMoves(nextMoves);
  setFromPos(cellPos);
};

const handleGrabEnd = (cellPos: CellPos) => {
  // Validate move and update game state
  const { moveData } = moveFigure(fromPos, cellPos, holdedFigure);
  if (moveData) {
    onChange(moveData);
  }
  clearGrabbingPos();
};
```

```typescript
// 2. Cursor-Following Component (HoldedFigure.tsx)
export const HoldedFigure: FC<HoldedFigureProps> = ({
  holdedFigure,
  grabbingPos,
  boardConfig,
}) => {
  const isCanShowFigure =
    holdedFigure && grabbingPos[0] > -1 && grabbingPos[1] > -1;

  return (
    isCanShowFigure && (
      <div
        style={{
          position: "fixed",
          zIndex: 6,
          top: `${grabbingPos[1] - boardConfig.cellSize / 2}px`,
          left: `${grabbingPos[0] - boardConfig.cellSize / 2}px`,
          width: boardConfig.cellSize,
          height: boardConfig.cellSize,
        }}
      >
        {/* Render piece SVG */}
      </div>
    )
  );
};
```

```typescript
// 3. Square Mouse Event Handlers
const handleMouseDown = (e: React.MouseEvent, cellPos: CellPos) => {
  if (!piece) return;

  e.preventDefault();
  selectHoverFrom(cellPos); // Set up drag state

  const handleMouseMove = (moveEvent: MouseEvent) => {
    handleGrabbing(moveEvent.clientX, moveEvent.clientY);
  };

  const handleMouseUp = (upEvent: MouseEvent) => {
    document.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", handleMouseUp);

    // Determine target square from cursor position
    const target = document.elementFromPoint(upEvent.clientX, upEvent.clientY);
    const targetSquare = target?.getAttribute("data-square");
    if (targetSquare) {
      handleGrabEnd(parseSquareNotation(targetSquare));
    }
  };

  document.addEventListener("mousemove", handleMouseMove);
  document.addEventListener("mouseup", handleMouseUp);
};
```

## Required Components

### 1. Drag Context Provider

```typescript
// src/providers/DragProvider.tsx
interface DragContextType {
  draggedPiece: ChessPiece | null;
  draggedFrom: SquareNotation | null;
  cursorPosition: { x: number; y: number };
  validMoves: SquareNotation[];
  startDrag: (piece: ChessPiece, from: SquareNotation) => void;
  updateCursor: (x: number, y: number) => void;
  endDrag: (to: SquareNotation) => void;
  clearDrag: () => void;
}
```

### 2. Cursor-Following Piece Component

```typescript
// src/components/chessboard/DraggedPiece/DraggedPiece.tsx
interface DraggedPieceProps {
  piece: ChessPiece;
  position: { x: number; y: number };
  size: number;
  pieceSet: PieceSet;
}

// Fixed positioning following cursor
style={{
  position: 'fixed',
  top: position.y - size / 2,
  left: position.x - size / 2,
  width: size,
  height: size,
  zIndex: 1000,
  pointerEvents: 'none'
}}
```

### 3. Square Event Handlers

```typescript
// src/components/chessboard/Square/Square.tsx
const handleMouseDown = (e: React.MouseEvent) => {
  if (!piece) return;

  e.preventDefault();
  e.stopPropagation();

  startDrag(piece, square);

  const handleGlobalMouseMove = (e: MouseEvent) => {
    updateCursor(e.clientX, e.clientY);
  };

  const handleGlobalMouseUp = (e: MouseEvent) => {
    cleanup();

    const targetElement = document.elementFromPoint(e.clientX, e.clientY);
    const targetSquare = targetElement?.getAttribute("data-square");

    if (targetSquare) {
      endDrag(targetSquare as SquareNotation);
    } else {
      clearDrag();
    }
  };

  const cleanup = () => {
    document.removeEventListener("mousemove", handleGlobalMouseMove);
    document.removeEventListener("mouseup", handleGlobalMouseUp);
  };

  document.addEventListener("mousemove", handleGlobalMouseMove);
  document.addEventListener("mouseup", handleGlobalMouseUp);
};
```

## Implementation Rules & Guidelines

### ✅ DO:

1. **Use mouse events only**: `onMouseDown`, `onMouseMove`, `onMouseUp`
2. **Fixed positioning**: Dragged piece follows cursor exactly
3. **Document-level listeners**: Track mouse globally during drag
4. **React state management**: No external libraries for drag state
5. **Prevent default**: Stop browser's native drag behavior
6. **Z-index layering**: Dragged piece above all other elements
7. **Pointer events none**: Dragged piece doesn't interfere with drop detection
8. **Element detection**: Use `document.elementFromPoint()` for drop targets

### ❌ DON'T:

1. **Don't use HTML5 drag API**: No `draggable={true}`, `onDragStart`, `onDrop`
2. **Don't use drag libraries**: No @dnd-kit, @hello-pangea/dnd, react-beautiful-dnd
3. **Don't use CSS transforms**: Avoid transform conflicts
4. **Don't use relative positioning**: Use fixed positioning only
5. **Don't add complex state**: Keep drag state minimal and focused

## Mobile/Touch Support

For mobile devices, add touch event handlers alongside mouse events:

```typescript
const handleTouchStart = (e: React.TouchEvent) => {
  const touch = e.touches[0];
  handleDragStart(touch.clientX, touch.clientY);
};

const handleTouchMove = (e: TouchEvent) => {
  e.preventDefault(); // Prevent scrolling
  const touch = e.touches[0];
  updateCursor(touch.clientX, touch.clientY);
};

const handleTouchEnd = (e: TouchEvent) => {
  const touch = e.changedTouches[0];
  handleDragEnd(touch.clientX, touch.clientY);
};
```

## Performance Considerations

1. **Throttle mouse moves**: Use `requestAnimationFrame` for cursor updates
2. **Minimal state updates**: Only update position state, not complex objects
3. **Event cleanup**: Always remove document listeners on unmount/drag end
4. **Prevent memory leaks**: Clear timeouts and intervals

## Testing Strategy

1. **Desktop browsers**: Chrome, Firefox, Safari, Edge
2. **Mobile devices**: iOS Safari, Android Chrome
3. **Touch interactions**: Tap and drag gestures
4. **Edge cases**: Drag outside board, rapid movements, interrupted drags
5. **Accessibility**: Keyboard navigation as fallback

## Final Decision Lock 🔒

This POC mouse event pattern is **LOCKED IN** as the definitive drag and drop solution. Any future modifications must:

1. Maintain the core mouse event + fixed positioning approach
2. Keep the cursor-following piece component pattern
3. Use React state management (no external drag libraries)
4. Preserve mobile/touch support

**Justification for Lock**: This pattern is proven to work in the existing POC, handles both desktop and mobile, requires no external dependencies, and aligns with the project's simplicity goals.

## Migration Path

For existing implementations using other approaches:

1. Remove all HTML5 drag attributes and event handlers
2. Remove @dnd-kit or other drag library imports
3. Implement DragProvider context
4. Add DraggedPiece component with fixed positioning
5. Update Square components with mouse event handlers
6. Add touch event support for mobile
7. Test thoroughly on all target devices

## Lessons Learned During Implementation 🎓

### Issue 1: Game State Integration ⚠️

**Problem**: Initial implementation called external `onMove` callback directly, bypassing internal game state management. This caused:

- ✅ Drag mechanism worked perfectly
- ✅ Move validation worked
- ✅ External callback returned `true`
- ❌ Piece didn't move visually (game state not updated)

**Root Cause**: Two separate move systems:

- Click-to-move: `handleClick` → `handleMove` → `makeMove` → updates `gameState` → calls `onMove`
- Drag-and-drop: Called `onMove` directly → skipped internal state update

**Solution**: Connect drag system to internal move handler:

```typescript
// In ChessboardInternal component
const { setMoveHandler } = useDrag();

React.useEffect(() => {
  setMoveHandler(async (move) => {
    const success = await handleMove(move); // Use same handler as click-to-move
    return success;
  });
}, [handleMove, setMoveHandler]);

// In DragProvider
const moveHandlerRef = useRef(null);
const setMoveHandler = (handler) => {
  moveHandlerRef.current = handler;
};

const endDrag = (to) => {
  // Use internal handler instead of external callback
  const moveResult = moveHandlerRef.current?.({ from: currentFrom, to });
  return moveResult;
};
```

### Issue 2: React State Race Conditions ⚠️

**Problem**: Drag state was lost between `startDrag` and `endDrag` due to asynchronous React state updates.

- State showed: `{draggedPiece: null, draggedFrom: null, validMoves: []}`
- But drag was clearly in progress

**Solution**: Use refs for immediate data access alongside state for UI updates:

```typescript
// State for UI rendering
const [draggedPiece, setDraggedPiece] = useState(null);
const [validMoves, setValidMoves] = useState([]);

// Refs for immediate access during drag operations
const dragStateRef = useRef({
  piece: null,
  from: null,
  validMoves: [],
});

const startDrag = (piece, from, moves) => {
  // Update both state and ref
  setDraggedPiece(piece);
  setValidMoves(moves);

  dragStateRef.current = { piece, from, validMoves: moves };
};

const endDrag = (to) => {
  // Use ref data instead of state for validation
  const { piece, from, validMoves } = dragStateRef.current;
  if (!validMoves.includes(to)) return false;
  // ...
};
```

### Issue 3: Excessive Re-renders ⚠️

**Problem**: DragProvider rendered 20+ times during each drag operation, causing performance issues.

**Cause**: Unstable callback references causing provider re-creation.

**Solution**: Use `useCallback` for move handlers:

```typescript
// In parent component
const handleMove = useCallback(({ from, to }) => {
  // move logic
  return true;
}, []); // Stable reference
```

## Updated Implementation Pattern

Based on lessons learned, the corrected pattern is:

```typescript
// 1. DragProvider with dual state + ref approach
const DragProvider = ({ children }) => {
  const [draggedPiece, setDraggedPiece] = useState(null); // UI state
  const dragStateRef = useRef({ piece: null, from: null, validMoves: [] }); // Immediate access
  const moveHandlerRef = useRef(null); // Internal move handler

  const startDrag = (piece, from, moves) => {
    setDraggedPiece(piece); // Trigger UI update
    dragStateRef.current = { piece, from, validMoves: moves }; // Immediate storage
  };

  const endDrag = (to) => {
    const { piece, from, validMoves } = dragStateRef.current; // Use ref data
    if (!piece || !validMoves.includes(to)) return false;

    const result = moveHandlerRef.current?.({ from, to }); // Use internal handler
    clearDrag();
    return result;
  };

  const setMoveHandler = (handler) => {
    moveHandlerRef.current = handler; // Connect to chessboard's internal logic
  };
};

// 2. Chessboard connects drag to internal move system
const ChessboardInternal = () => {
  const { setMoveHandler } = useDrag();

  const handleMove = async (move) => {
    const success = await makeMove(move); // Update internal game state
    if (success && onMove) onMove(move); // Call external callback
    return success;
  };

  useEffect(() => {
    setMoveHandler(handleMove); // Connect drag to same system as click-to-move
  }, [handleMove]);
};
```

## Key Principles Learned

1. **Unified Move System**: Both click-to-move and drag-and-drop must use the same internal move handler
2. **State + Refs Pattern**: Use React state for UI updates, refs for immediate data access during event handling
3. **Internal First**: Update internal game state first, then call external callbacks
4. **Stable References**: Use `useCallback` to prevent excessive re-renders

## Latest Implementation Session - Scaling & Responsiveness 🔧

_Updated: 2025-09-02 - Scaling and Container Responsiveness Issues_

### What We Accomplished ✅

1. **Fixed Dragged Piece Scaling**:

   - ✅ Removed hardcoded 64px size from DraggedPiece
   - ✅ Implemented dynamic square size measurement using `getBoundingClientRect()`
   - ✅ Dragged piece now matches actual board square dimensions
   - ✅ Fixed semi-transparency issues (dragged piece now fully opaque)

2. **Improved Size Calculation System**:

   - ✅ Added `boardRef` to measure actual rendered squares instead of mathematical division
   - ✅ Implemented resize event listeners for dynamic recalculation
   - ✅ Added fallback measurement system with multiple retry attempts

3. **Move Validation Foundation**:
   - ✅ Installed `chess.js` and `stockfish.js` packages
   - ✅ Ready for proper chess rule implementation

### Critical Issues Discovered During Implementation 🚨

#### Issue 4: Dragged Piece Size Mismatch ⚠️

**Problem**: Dragged piece appeared smaller/larger than board pieces despite using calculated square size.

**Root Cause**: Confusion between CSS Grid square sizing and actual piece rendering:

- Board pieces use `w-full h-full` (CSS relative sizing)
- DraggedPiece was trying to use absolute pixel sizing
- Size calculation was measuring board container instead of actual rendered squares

**Solution Applied**:

```typescript
// Measure actual square elements instead of calculating from container
const firstSquare = boardRef.current.querySelector(
  "[data-square]"
) as HTMLElement;
const squareRect = firstSquare.getBoundingClientRect();
const actualSquareSize = Math.min(squareRect.width, squareRect.height);
```

#### Issue 5: Container Responsiveness Failure ⚠️ **UNRESOLVED**

**Problem**: Chessboard refuses to shrink with browser window, overflows container, goes off-page.

**Attempted Solutions** (All Failed):

1. ❌ Removed `max-w-2xl` constraint from App.tsx → No effect
2. ❌ Changed to flexbox layout with `flex-1` containers → No effect
3. ❌ Removed `aspect-square`, used `w-full h-full` → Lost square proportions
4. ❌ Added `max-w-full max-h-full` constraints → Still overflows
5. ❌ Added explicit `minWidth: 0, minHeight: 0` styles → No effect
6. ❌ Used CSS `contain: 'layout size'` → No effect
7. ❌ Tried `min()` CSS function with viewport calculations → Still testing

**Current Status**: Board scales UP with window but refuses to scale DOWN, causing overflow.

### Work Remaining 📋

#### High Priority - Blocking Issues:

1. **Container Responsiveness**: Fix chessboard overflow/scaling down issue
2. **Chess Rule Implementation**: Replace POC "move anywhere" with real chess.js validation
3. **Turn Enforcement**: Implement proper white/black turn alternation

#### Medium Priority - Enhancements:

4. **Move History**: Track and display game moves
5. **Game State Persistence**: Save/restore game state
6. **Mobile Touch Events**: Add touch support alongside mouse events

### Prime Suspects for Next Investigation 🔍

#### 1. CSS Grid Intrinsic Sizing Conflict

**Hypothesis**: CSS Grid with `grid-cols-8 grid-rows-8` creates intrinsic content size that overrides container constraints.

- **Investigation**: Try replacing CSS Grid with flexbox or other layout methods
- **Evidence**: Grid often ignores `max-width/max-height` on container elements
- **Next Step**: Test with `display: flex` and `flex-wrap` instead of CSS Grid

#### 2. Aspect Ratio Calculation Priority

**Hypothesis**: `aspect-square` and `aspectRatio: '1 / 1'` are taking precedence over container size limits.

- **Investigation**: Check CSS cascade and specificity of aspect ratio rules
- **Evidence**: Square aspect enforcement might be preventing shrinkage
- **Next Step**: Try conditional aspect ratio only when container has excess space

#### 3. Missing CSS Containment Context

**Hypothesis**: Parent containers don't establish proper sizing context for CSS containment.

- **Investigation**: Check if flexbox parents need explicit `min-width: 0` or other containment rules
- **Evidence**: Flexbox/Grid children often ignore parent constraints without proper CSS containment
- **Next Step**: Add `contain: layout style size` to all parent containers in the chain

#### 4. Tailwind CSS Utility Conflicts

**Hypothesis**: Multiple competing Tailwind utilities creating CSS specificity issues.

- **Investigation**: Inspect computed styles to see which CSS rules are actually applied
- **Evidence**: Complex className strings might have conflicting directives
- **Next Step**: Replace compound Tailwind classes with custom CSS for critical sizing

### Implementation Priority Order 📝

1. **FIRST**: Fix container responsiveness (investigate suspects above)
2. **SECOND**: Implement chess.js validation (foundation already installed)
3. **THIRD**: Add turn enforcement and proper game state management
4. **FOURTH**: Enhance with move history and persistence features

### Key Technical Decisions Made 🔒

- ✅ **Sizing Method**: Use `getBoundingClientRect()` on actual DOM elements, not mathematical calculation
- ✅ **Piece Visibility**: Semi-transparent source piece + fully opaque dragged piece
- ✅ **Size Updates**: React state + refs pattern for immediate access during events
- ❌ **Container Strategy**: Still unresolved - responsive container approach TBD

**Status**: Core drag and drop functionality is working correctly. Scaling system implemented and functional. Container responsiveness is the primary blocking issue preventing full responsive behavior as intended for a "chessboard-vanilla-v2" project.
