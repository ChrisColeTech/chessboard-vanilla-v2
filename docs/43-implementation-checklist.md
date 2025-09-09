# Play Page Implementation Checklist
## Detailed Task List for Phases 3-10

This checklist tracks the remaining 21 tasks to complete the Play page implementation.

### **Phase 3: Business Logic Services** (2 tasks)

- [ ] **Task 1**: Create `src/services/chess/PlayGameService.ts`
  - Core play game business logic
  - Pure business logic, no external communication
  - Wraps ChessGameService with play-specific logic
  - Methods: `makePlayerMove`, `isPlayerTurn`, `switchTurn`, `resetGame`

- [ ] **Task 2**: Create `src/services/chess/ComputerOpponentService.ts`  
  - Computer opponent logic
  - Pure business logic for AI behavior
  - Methods: `getDifficultyConfig`, `calculateSearchDepth`, `generateThinkingDelay`

### **Phase 4: External Communication** (1 task)

- [ ] **Task 3**: Create `src/services/clients/StockfishEngineClient.ts`
  - Stockfish Worker communication layer
  - External communication only, no business logic
  - Wraps existing StockfishService with clean interface
  - Methods: `isReady`, `requestMove`, `setSkillLevel`

### **Phase 5: State Management Hooks** (2 tasks)

- [ ] **Task 4**: Create `src/hooks/chess/usePlayGame.ts`
  - Main play game state management hook
  - React state management, bridges services to UI
  - Combines PlayGameService + StockfishEngineClient
  - Manages human moves → computer moves pipeline

- [ ] **Task 5**: Create `src/hooks/chess/useComputerOpponent.ts`
  - Computer opponent specific hook
  - AI state management and thinking indicators
  - Skill level management and move requests

### **Phase 6: UI Components** (6 tasks)

- [ ] **Task 6**: Create `src/components/play/PlayerStatus.tsx`
  - Human/Computer player status display
  - Shows current turn, thinking state, captured pieces
  - Props: `isHuman`, `color`, `isCurrentTurn`, `isThinking`, `capturedPieces`

- [ ] **Task 7**: Create `src/components/play/GameControls.tsx`
  - New game, resign, settings controls
  - Game management buttons with proper states
  - Props: `onNewGame`, `onResign`, `onFlipBoard`, `isGameActive`

- [ ] **Task 8**: Create `src/components/play/DifficultySelector.tsx`
  - AI difficulty selection (1-10)
  - Visual skill level picker with descriptions
  - Props: `currentLevel`, `onLevelChange`, `disabled`

- [ ] **Task 9**: Create `src/components/play/ComputerThinking.tsx`
  - AI thinking indicator with animation
  - Brain icon animation, progress display
  - Props: `thinkingState`, `difficulty`, `showProgress`

- [ ] **Task 10**: Create `src/components/play/GameStatusBar.tsx`
  - Current game status and turn indicator
  - Game state, move number, timer display
  - Props: `currentPlayer`, `gameResult`, `isComputerThinking`

- [ ] **Task 11**: Create `src/components/play/PlaySettings.tsx`
  - Game settings panel
  - Player color, difficulty, audio, hints toggles
  - Props: `onPlayerColorChange`, `onDifficultyChange`, `onAudioToggle`

### **Phase 7: Board Integration** (2 tasks)

- [ ] **Task 12**: Create `src/components/play/PlayChessboard.tsx`
  - Chessboard wrapper with play-specific features
  - 8x8 professional chessboard with drag & drop
  - Real chess.js move validation, promotion handling
  - Integration with usePlayGame hook

- [ ] **Task 13**: Modify `src/components/TestBoard.tsx`
  - Extract reusable patterns for PlayChessboard
  - Document drag & drop integration patterns
  - Preserve existing TestBoard functionality

### **Phase 8: Play Page Assembly** (4 tasks)

- [ ] **Task 14**: Create `src/pages/PlayPage.tsx`
  - Complete play page implementation
  - Chessboard-first design with minimal UI
  - Player status bars, game controls, difficulty selector
  - Audio integration and instructions system

- [ ] **Task 15**: Modify `src/pages/index.ts`
  - Export PlayPage
  - Add to page exports barrel

- [ ] **Task 16**: Modify `src/App.tsx`
  - Add play page routing
  - Handle 'play' tab selection
  - Route to PlayPage component

- [ ] **Task 17**: Modify `src/components/layout/types.ts`
  - Add 'play' tab type
  - Update TabId type definition

### **Phase 9: Navigation Integration** (2 tasks)

- [ ] **Task 18**: Modify `src/components/layout/TabBar.tsx`
  - Add play tab with chess icon
  - Chess piece icon for play tab
  - Proper tab switching integration

- [ ] **Task 19**: Modify `src/stores/appStore.ts`
  - Update initial state if needed
  - Set play as potential default tab
  - Ensure state compatibility

### **Phase 10: Audio Integration** (2 tasks)

- [ ] **Task 20**: Modify `src/hooks/chess/usePlayGame.ts`
  - Add audio integration
  - Move sounds, check sounds, game end sounds
  - Computer move audio feedback

- [ ] **Task 21**: Modify `src/services/audioService.ts`
  - Add computer-specific sounds if needed
  - Thinking sounds, AI move confirmation
  - Ensure all play-specific audio events covered

---

## Implementation Notes

### Architecture Compliance
- **Phase 3-4**: Follow SRP - Services handle business logic, Clients handle external communication
- **Phase 5**: Hooks bridge services to React components, manage UI state only  
- **Phase 6-7**: Components are pure presentation, receive props and emit events
- **Phase 8-10**: Page assembly follows existing patterns from DragTestPage

### Dependencies
- Each phase depends on completion of previous phases
- All infrastructure already exists (chess.js, Stockfish, drag & drop, audio)
- Use existing patterns from TestBoard, WorkerTestPage, DragTestPage

### Testing Strategy
- Test each service independently in Phase 3-4
- Test hooks in isolation in Phase 5
- Test components with storybook-style testing in Phase 6-7
- Integration testing in Phase 8-10

### Success Criteria
- Complete human vs computer chess gameplay
- 10 difficulty levels with meaningful differences
- Professional UI following style guide
- Audio feedback for all game events
- Responsive design on all screen sizes

---

## Status: 0/21 Tasks Complete
**Next Task**: Phase 3, Task 1 - Create PlayGameService.ts