# Vanilla Chessboard Implementation Plan - Document 21

## Required Reading

**MANDATORY**: These documents must be read and understood before beginning implementation:

1. **Document 02: Architecture Guide** - Core principles, layer separation, anti-patterns
2. **Document 08: Implementation Plan** - Phase methodology and success criteria  
3. **Document 22: Code Examples** - Reference implementations for all components
4. **Chess.js Documentation**: https://github.com/jhlywa/chess.js/blob/master/README.md
5. **Stockfish.js Documentation**: https://github.com/nmrugg/stockfish.js/

## Work Progress Tracking

| Phase | Priority | Status | Files Created | Integration Points | Notes |
|-------|----------|--------|---------------|-------------------|-------|
| Foundation Layer | 1 - Critical | ⏳ Pending | 0/8 files | N/A - Base layer | Type safety foundation |
| Chess Engine Services | 2 - Critical | ⏳ Pending | 0/3 files | Foundation types | Core game logic |  
| Hooks Layer | 3 - Critical | ⏳ Pending | 0/4 files | Services, React | State management bridge |
| Responsive Grid System | 4 - Critical | ⏳ Pending | 0/3 files | Hooks | CSS Grid layout |
| Components Layer | 5 - Critical | ⏳ Pending | 0/5 files | Hooks, CSS | Presentation layer |
| Integration & Polish | 6 - High | ⏳ Pending | 0/4 files | All layers | Final assembly |

## Overview

This document outlines the complete implementation plan for creating a **chessboard-vanilla** project in the `/poc` folder. This will be a React Vite application featuring a responsive chessboard built with vanilla HTML, CSS, and JavaScript (no UI frameworks), integrated with chess.js for move validation and Stockfish.js for computer opponent functionality.

## Project Goals

- **Primary**: Demonstrate clean architecture principles from Document 02
- **Secondary**: Showcase responsive design without CSS frameworks
- **Tertiary**: Provide working chess.js and Stockfish.js integration
- **Architecture Focus**: Foundation-first development with strict layer separation

## Implementation Strategy

Following the **Architecture Guide (Document 02)** foundation-first approach with **chess engines prioritized**:
**Foundation → Chess Engine Services (Priority) → Hooks → Components → Integration**

---

## Phase-by-Phase Implementation Plan

### Phase 1: Foundation Layer (Priority 1 - Critical)

**Files to Create:**
- `/src/types/chess.types.ts` - Core chess domain types
- `/src/types/component.types.ts` - React component prop types  
- `/src/types/index.ts` - Type exports barrel
- `/src/utils/chess.utils.ts` - Chess utility functions
- `/src/utils/coordinate.utils.ts` - Board coordinate system
- `/src/utils/index.ts` - Utils exports barrel
- `/src/constants/chess.constants.ts` - Chess game constants
- `/src/constants/pieces.constants.ts` - Piece set definitions

**Integration Points:**
- None (base foundation layer)

**Success Criteria:**
- ✅ All types compile without errors
- ✅ Utility functions have unit tests
- ✅ ESLint passes with strict rules
- ✅ TypeScript strict mode enabled

---

### Phase 2: Chess Engine Services (Priority 2 - Critical)

**Files to Create:**
- `/src/services/ChessGameService.ts` - chess.js wrapper service
- `/src/services/StockfishService.ts` - Stockfish Web Worker service
- `/src/services/FenService.ts` - FEN parsing and validation

**Integration Points:**
- **Uses**: `/src/types/chess.types.ts` for type definitions
- **Uses**: `/src/utils/chess.utils.ts` for utility functions
- **Uses**: `/src/constants/chess.constants.ts` for game constants

**Key Features:**
- ChessGameService: Move validation, FEN parsing, game state management
- StockfishService: UCI protocol, computer moves, position evaluation
- FenService: FEN string parsing, validation, game phase detection

**Success Criteria:**
- ✅ Services have no React dependencies
- ✅ chess.js v1.4.0 API integration works perfectly
- ✅ Stockfish.js v17.1 Web Worker functional
- ✅ UCI protocol commands working
- ✅ 95%+ test coverage

---

### Phase 3: Hooks Layer (Priority 3 - Critical)

**Files to Create:**
- `/src/hooks/useChessGame.ts` - Main chess game state management
- `/src/hooks/useStockfish.ts` - Computer opponent integration
- `/src/hooks/useResponsiveBoard.ts` - Responsive board sizing
- `/src/hooks/useDragAndDrop.ts` - Drag and drop interactions

**Integration Points:**
- **Uses**: All services from Phase 2 (ChessGameService, StockfishService)
- **Uses**: Types from `/src/types/` for interfaces
- **Uses**: React hooks (useState, useEffect, useCallback, useRef)

**Success Criteria:**
- ✅ Hooks bridge services to React cleanly
- ✅ No business logic in hooks (delegated to services)
- ✅ Proper error handling and loading states
- ✅ React state updates don't cause render storms
- ✅ Hooks follow Single Responsibility Principle

---

### Phase 4: Responsive Grid System (Priority 4 - Critical)

**Files to Create:**
- `/src/styles/chessboard.css` - Core chessboard styling
- `/src/styles/global.css` - Global styles and resets
- `/src/styles/app.css` - Application layout styles

**Integration Points:**
- **Uses**: `/src/hooks/useResponsiveBoard.ts` for size calculations
- **References**: CSS custom properties for theming
- **Integrates**: ResizeObserver API for responsive behavior

**Success Criteria:**
- ✅ Perfect squares at all screen sizes
- ✅ Smooth resizing without layout thrashing
- ✅ No flickering during resize operations
- ✅ CSS Grid + aspect-ratio working perfectly

---

### Phase 5: Components Layer (Priority 5 - Critical)

**Files to Create:**
- `/src/components/chessboard/Chessboard.tsx` - Main chessboard component
- `/src/components/chessboard/Board.tsx` - 8x8 board grid
- `/src/components/chessboard/Square.tsx` - Individual squares
- `/src/components/chessboard/Piece.tsx` - Chess pieces
- `/src/components/index.ts` - Component exports

**Integration Points:**
- **Uses**: All hooks from Phase 3 for state management
- **Uses**: `/src/types/component.types.ts` for prop definitions
- **Uses**: `/src/styles/chessboard.css` for styling
- **Uses**: `/src/utils/chess.utils.ts` for coordinate conversion
- **References**: SVG assets from `/public/pieces/` folder

**Success Criteria:**
- ✅ Components are pure presentation layer
- ✅ Zero business logic in components
- ✅ Proper React.memo optimization
- ✅ Stable keys prevent piece reshuffling
- ✅ Full keyboard and screen reader accessibility

---

### Phase 6: Integration & Polish (Priority 6 - High)

**Files to Create:**
- `/src/App.tsx` - Main application component
- `/src/main.tsx` - React application entry point
- `package.json` - Dependencies and scripts
- `vite.config.ts` - Vite configuration

**Integration Points:**
- **Uses**: `/src/components/chessboard/Chessboard.tsx` as main component
- **Uses**: `/src/styles/app.css` for application layout
- **Integrates**: chess.js and stockfish.js dependencies
- **References**: SVG assets from `/assets/` folder
- **Configures**: Vite build system and development server

**Success Criteria:**
- ✅ Complete chess game functionality
- ✅ Working computer opponent integration
- ✅ Proper error handling and loading states
- ✅ Smooth user experience
- ✅ All edge cases covered

---

## Final Project Structure

```
/poc/chessboard-vanilla/
├── public/
│   ├── pieces/
│   │   ├── classic/
│   │   ├── modern/
│   │   ├── tournament/
│   │   ├── executive/
│   │   └── conqueror/
│   └── index.html
├── src/
│   ├── types/
│   │   ├── chess.types.ts
│   │   ├── component.types.ts
│   │   ├── service.types.ts
│   │   └── index.ts
│   ├── utils/
│   │   ├── chess.utils.ts
│   │   ├── coordinate.utils.ts
│   │   ├── validation.utils.ts
│   │   └── index.ts
│   ├── constants/
│   │   ├── chess.constants.ts
│   │   ├── pieces.constants.ts
│   │   ├── ui.constants.ts
│   │   └── index.ts
│   ├── services/
│   │   ├── ChessGameService.ts
│   │   ├── FenService.ts
│   │   ├── StockfishService.ts
│   │   └── index.ts
│   ├── hooks/
│   │   ├── useChessGame.ts
│   │   ├── useResponsiveBoard.ts
│   │   ├── useDragAndDrop.ts
│   │   ├── useStockfish.ts
│   │   └── index.ts
│   ├── components/
│   │   ├── chessboard/
│   │   │   ├── Chessboard.tsx
│   │   │   ├── Board.tsx
│   │   │   ├── Square.tsx
│   │   │   ├── Piece.tsx
│   │   │   └── DraggedPiece.tsx
│   │   ├── ui/
│   │   │   ├── ErrorBoundary.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── Button.tsx
│   │   └── index.ts
│   ├── styles/
│   │   ├── global.css
│   │   ├── chessboard.css
│   │   ├── pieces.css
│   │   ├── app.css
│   │   └── index.css
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
├── tsconfig.json
├── eslint.config.js
└── README.md
```

## Final Page Layout (ASCII Mockup)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Vanilla Chessboard                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌─────────────────────────────────────────────────────────┐     │
│    │  8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8                               │     │
│    │  7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟  7                               │     │
│    │  6                   6                               │     │
│    │  5                   5                               │     │
│    │  4                   4                               │     │
│    │  3                   3                               │     │
│    │  2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  2                               │     │
│    │  1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖  1                               │     │
│    │    a b c d e f g h                                  │     │
│    └─────────────────────────────────────────────────────────┘     │
│                                                                     │
│               [New Game]  [Flip Board]  [vs Computer]               │
│                                                                     │
│               Status: White to move | Computer: ● Thinking...       │
│                                                                     │
│  Features Demonstrated:                                             │
│  ✓ Responsive CSS Grid layout    ✓ chess.js v1.4.0 integration     │
│  ✓ Drag & drop + click-to-move   ✓ Stockfish.js v17.1 Web Worker   │
│  ✓ Multiple piece sets           ✓ Move validation & UCI protocol   │
│  ✓ Vanilla CSS (no frameworks)   ✓ Clean architecture patterns     │
└─────────────────────────────────────────────────────────────────────┘
```

## Success Metrics

### Performance Requirements
- **First Render**: < 100ms
- **Move Response**: < 50ms  
- **Computer Move**: < 2s (skill level 8)
- **Bundle Size**: < 500KB gzipped
- **Lighthouse Score**: 90+ on all metrics

### Quality Gates (Each Phase)
- ✅ 90%+ test coverage
- ✅ Zero ESLint errors with strict rules
- ✅ TypeScript strict mode compilation
- ✅ No React anti-patterns detected
- ✅ WCAG 2.1 AA accessibility compliance
- ✅ Cross-browser compatibility (Chrome, Firefox, Safari, Edge)

### Architecture Compliance
- ✅ **SRP**: Each component/service has single responsibility
- ✅ **DRY**: No code duplication across layers
- ✅ **Clean Architecture**: Foundation → Services → Hooks → Components
- ✅ **Type Safety**: 100% TypeScript coverage with strict mode
- ✅ **Performance**: React.memo, stable keys, proper dependencies

## Risk Mitigation

### High-Risk Areas
1. **Drag & Drop**: Cross-browser compatibility, mobile touch events
2. **Stockfish Integration**: Worker management, memory usage
3. **Responsive Design**: CSS Grid browser support, aspect-ratio polyfill

### Mitigation Strategies
- **Extensive Testing**: Chrome, Firefox, Safari, Edge + mobile devices
- **Progressive Enhancement**: Fallback to click-to-move if drag fails
- **Error Boundaries**: Graceful degradation for component failures
- **Performance Monitoring**: Bundle analysis, runtime performance tracking


## Implementation Notes

### Development Approach
1. **Build incrementally** - Complete each phase before moving to next
2. **Test continuously** - Unit tests for each layer as built
3. **Follow architecture** - Strict adherence to Document 02 principles
4. **Performance first** - Monitor bundle size and runtime performance
5. **Mobile responsive** - Test on actual devices, not just dev tools

### Key Dependencies
```json
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0", 
    "chess.js": "^1.4.0",
    "stockfish.js": "^10.0.2"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^5.0.0",
    "typescript": "~5.8.0",
    "vite": "^7.0.0",
    "eslint": "^9.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0"
  }
}
```

This plan ensures a production-ready, maintainable, and performant chessboard component following clean architecture principles while demonstrating vanilla CSS capabilities and modern React patterns.