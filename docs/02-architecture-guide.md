# Architecture Guide - React Chessboard Component

## Core Principles

This architecture guide enforces **Single Responsibility Principle (SRP)**, **Don't Repeat Yourself (DRY)**, and established React best practices while providing safeguards against common anti-patterns.

### Fundamental Rules

1. **Single Responsibility Principle**: Each module, class, or function should have only one reason to change
2. **Don't Repeat Yourself**: Avoid code duplication through shared utilities, types, and components
3. **Separation of Concerns**: Business logic, UI logic, and data access must be separated
4. **Dependency Inversion**: Depend on abstractions, not concretions
5. **No Inline Definitions**: No inline interfaces, API calls, or business logic in components
6. **Type Safety**: Comprehensive TypeScript coverage with strict mode

---

## Project Structure

```
src/
├── components/           # Pure UI components (presentation layer)
│   ├── ui/              # Generic reusable UI components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.types.ts
│   │   │   ├── Button.styles.ts
│   │   │   └── index.ts
│   │   └── index.ts
│   └── chessboard/      # Chess-specific components
│       ├── Chessboard/
│       │   ├── Chessboard.tsx
│       │   ├── Chessboard.types.ts
│       │   ├── Chessboard.styles.ts
│       │   └── index.ts
│       ├── Board/
│       ├── Square/
│       ├── Piece/
│       └── index.ts
├── hooks/               # Custom React hooks (state management)
│   ├── demo/
│   │   ├── useDemoNavigation.ts
│   │   ├── useDemoState.ts
│   │   └── useControlPanel.ts
│   ├── chess/
│   │   ├── useChessGame.ts
│   │   ├── useChessTrainingGame.ts
│   │   ├── useDragAndDrop.ts
│   │   ├── useChessAnimation.ts
│   │   └── useResponsiveBoard.ts
│   ├── queries/         # React Query hooks
│   │   ├── useGameQueries.ts
│   │   ├── usePuzzleQueries.ts
│   │   └── useAnalysisQueries.ts
│   ├── mutations/       # React Query mutations
│   │   ├── useGameMutations.ts
│   │   ├── usePuzzleMutations.ts
│   │   └── useAuthMutations.ts
│   └── index.ts
├── services/            # Business logic and external integrations
│   ├── chess/
│   │   ├── ChessGameService.ts
│   │   ├── FenService.ts
│   │   ├── MoveValidationService.ts
│   │   └── index.ts
│   ├── animation/
│   │   ├── AnimationService.ts
│   │   └── index.ts
│   └── storage/
│       ├── GameStorageService.ts
│       └── index.ts
├── types/               # TypeScript type definitions
│   ├── chess.types.ts
│   ├── ui.types.ts
│   ├── animation.types.ts
│   ├── events.types.ts
│   └── index.ts
├── utils/               # Pure utility functions
│   ├── chess.utils.ts
│   ├── validation.utils.ts
│   ├── coordinate.utils.ts
│   └── index.ts
├── constants/           # Application constants
│   ├── chess.constants.ts
│   ├── ui.constants.ts
│   └── index.ts
├── assets/              # Static assets
│   ├── pieces/
│   │   ├── classic/
│   │   ├── modern/
│   │   └── tournament/
│   └── styles/
│       ├── variables.css
│       └── global.css
├── stores/              # Global state management (Zustand)
│   ├── authStore.ts
│   ├── demoStore.ts
│   ├── gameStore.ts
│   └── index.ts
├── providers/           # React context providers
│   ├── QueryProvider.tsx
│   ├── ToastProvider.tsx
│   └── index.ts
└── index.ts             # Main export file
```

## File Organization Standard

**Golden Rule**: All files must be organized by **domain** in subfolders, not flat structures. This enforces SRP and DRY principles by grouping related functionality.

### **Domain Organization Requirements**

#### **types/** - Must be organized by domain:
```
types/
├── auth/            # Authentication domain types
├── chess/           # Chess domain types  
├── demo/            # Demo domain types
├── api/             # API domain types
├── performance/     # Performance domain types
└── ui/              # UI domain types
```

#### **utils/** - Must be organized by domain:
```
utils/
├── chess/           # Chess domain utilities
├── demo/            # Demo domain utilities
├── performance/     # Performance domain utilities
├── api/             # API domain utilities
├── common/          # Shared utilities
└── ui/              # UI domain utilities
```

#### **constants/** - Must be organized by domain:
```
constants/
├── auth/            # Authentication constants
├── chess/           # Chess constants
├── demo/            # Demo constants
├── api/             # API constants
├── performance/     # Performance constants
└── ui/              # UI constants
```

## Implementation Priority Standard

**Golden Rule**: Always build from foundation → infrastructure → data → presentation → features

### **Priority 1: Foundation Layer**
- **types/** - All TypeScript definitions organized by domain
- **utils/** - Pure utility functions organized by domain  
- **constants/** - Application constants organized by domain
- **HTTP Client** - Base communication infrastructure

**Why First**: Everything else depends on these. No circular dependencies possible.

### **Priority 2: Infrastructure Layer**  
- **services/** - Business logic services organized by domain
- **clients/** - API communication clients

**Why Second**: Provides business logic and external communication. Components and hooks will use these.

### **Priority 3: Data Layer**
- **stores/** - Global state management (Zustand)
- **hooks/** - React state management organized by domain
- **providers/** - React context providers

**Why Third**: Bridges services to components. Must exist before components can consume data.

### **Priority 4: Presentation Layer**
- **components/** - Reusable UI components organized by domain

**Why Fourth**: Pure presentation components that consume data from hooks/stores.

### **Priority 5+: Feature Layer**
- **pages/** - Route-level components that compose everything together

**Why Last**: Features combine all lower layers to create user-facing functionality.

---

## Layer Architecture

### 1. Types Layer (`/types`)

**Purpose**: Define all TypeScript interfaces and types
**Responsibility**: Type safety and contract definitions
**Rule**: No implementation, only type definitions

```typescript
// types/chess.types.ts
export interface ChessPosition {
  readonly rank: Rank;
  readonly file: File;
}

export interface ChessPiece {
  readonly type: PieceType;
  readonly color: PieceColor;
  readonly id: string;
}

export interface ChessMove {
  readonly from: ChessPosition;
  readonly to: ChessPosition;
  readonly piece: ChessPiece;
  readonly capturedPiece?: ChessPiece;
  readonly isPromotion: boolean;
  readonly promotionPiece?: PieceType;
}

export interface ChessGameState {
  readonly position: Map<string, ChessPiece>;
  readonly activeColor: PieceColor;
  readonly castlingRights: CastlingRights;
  readonly enPassantTarget?: ChessPosition;
  readonly halfmoveClock: number;
  readonly fullmoveNumber: number;
  readonly isCheck: boolean;
  readonly isCheckmate: boolean;
  readonly isStalemate: boolean;
}
```

### 2. Services Layer (`/services`)

**Purpose**: Business logic and data processing  
**Rule**: Pure functions and classes, no React dependencies

The Services layer is divided into two distinct categories:

#### 2a. Services - Business Logic (`/services/chess/`, `/services/demo/`, etc.)
**Responsibility**: Domain logic, data transformation, validation, calculations
**Rules**:
- No external API calls or HTTP requests
- No React dependencies 
- Pure business logic only
- Can depend on other services
- Should be easily testable in isolation

#### 2b. Clients - External Communication (`/services/clients/`)
**Responsibility**: External API communication, data fetching
**Rules**:
- Handle HTTP requests and external API calls
- Transform external API responses to internal types
- Manage authentication headers and request configuration
- Error handling for network failures
- No business logic - only communication

**Example - Business Logic Service:**
```typescript
// services/chess/ChessGameService.ts
export class ChessGameService {
  private gameEngine: Chess;

  constructor(initialFen?: string) {
    this.gameEngine = new Chess(initialFen);
  }

  public makeMove(move: ChessMoveInput): ChessMoveResult {
    try {
      const chessMove = this.gameEngine.move({
        from: move.from,
        to: move.to,
        promotion: move.promotion
      });

      if (!chessMove) {
        return {
          success: false,
          error: 'Invalid move',
          gameState: this.getCurrentState()
        };
      }

      return {
        success: true,
        move: this.mapToChessMove(chessMove),
        gameState: this.getCurrentState()
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        gameState: this.getCurrentState()
      };
    }
  }

  public getCurrentState(): ChessGameState {
    return {
      position: this.parsePosition(),
      activeColor: this.gameEngine.turn() === 'w' ? 'white' : 'black',
      isCheck: this.gameEngine.inCheck(),
      isCheckmate: this.gameEngine.isCheckmate(),
      isStalemate: this.gameEngine.isStalemate(),
      // ... other state properties
    };
  }

  private parsePosition(): Map<string, ChessPiece> {
    // Implementation details...
  }

  private mapToChessMove(engineMove: any): ChessMove {
    // Implementation details...
  }
}
```

**Example - External API Client:**
```typescript
// services/clients/ChessAPIClient.ts
export class ChessAPIClient {
  private readonly baseURL = 'http://localhost:3000/api';
  
  constructor(private readonly httpClient: HttpClient) {}
  
  public async createGame(gameConfig: GameConfig): Promise<GameResult> {
    try {
      const response = await this.httpClient.post('/games/create', {
        aiLevel: gameConfig.difficulty,
        color: gameConfig.playerColor,
        timeControl: gameConfig.timeControl
      });
      
      // Transform external API response to internal types
      return this.mapToGameResult(response.data);
    } catch (error) {
      throw new ChessAPIClientError('Game creation failed', error);
    }
  }
  
  public async submitMove(gameId: string, move: ChessMove): Promise<MoveResult> {
    try {
      const response = await this.httpClient.post(`/games/${gameId}/move`, {
        move: {
          from: move.from,
          to: move.to,
          promotion: move.promotion
        },
        timeSpent: move.timeSpent
      });
      
      return this.mapToMoveResult(response.data);
    } catch (error) {
      throw new ChessAPIClientError('Move submission failed', error);
    }
  }
  
  private mapToGameResult(apiData: any): GameResult {
    // Transform API response to internal types
  }
  
  private mapToMoveResult(apiData: any): MoveResult {
    // Transform API response to internal types
  }
}
```

### 3. Hooks Layer (`/hooks`)

**Purpose**: State management and React-specific logic
**Responsibility**: Bridge between services/clients and components
**Rules**: 
- Use services for business logic
- Use clients for external data fetching
- Manage React state only
- No direct API calls (use clients instead)

The Hooks layer is organized into subcategories:

#### 3a. Domain Hooks (`/hooks/chess/`, `/hooks/demo/`)
**Responsibility**: Domain-specific state management
**Examples**: `useChessGame`, `useDemoState`, `useControlPanel`

#### 3b. Query Hooks (`/hooks/queries/`)
**Responsibility**: Server state management with React Query
**Examples**: `useGameQueries`, `usePuzzleQueries`, `useAnalysisQueries`
**Rules**: Handle caching, loading states, background refetching

#### 3c. Mutation Hooks (`/hooks/mutations/`)
**Responsibility**: Server mutations with React Query
**Examples**: `useGameMutations`, `usePuzzleMutations`, `useAuthMutations`
**Rules**: Handle optimistic updates, error handling, cache invalidation

**Example - Local Game Hook (Uses Service Only):**
```typescript
// hooks/useChessGame.ts
export const useChessGame = (initialFen?: string): ChessGameHook => {
  const [gameState, setGameState] = useState<ChessGameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const gameServiceRef = useRef<ChessGameService>();

  useEffect(() => {
    gameServiceRef.current = new ChessGameService(initialFen);
    setGameState(gameServiceRef.current.getCurrentState());
    setIsLoading(false);
  }, [initialFen]);

  const makeMove = useCallback(async (move: ChessMoveInput): Promise<boolean> => {
    if (!gameServiceRef.current) return false;

    // Use service for business logic
    const result = gameServiceRef.current.makeMove(move);
    
    if (result.success) {
      setGameState(result.gameState);
      return true;
    }
    
    return false;
  }, []);

  const resetGame = useCallback((fen?: string) => {
    if (!gameServiceRef.current) return;
    
    gameServiceRef.current = new ChessGameService(fen);
    setGameState(gameServiceRef.current.getCurrentState());
  }, []);

  return {
    gameState,
    isLoading,
    makeMove,
    resetGame,
    isGameOver: gameState?.isCheckmate || gameState?.isStalemate || false
  };
};
```

**Example - Backend-Connected Hook (Uses Both Service and Client):**
```typescript
// hooks/useChessTrainingGame.ts
export const useChessTrainingGame = (): ChessTrainingGameHook => {
  const gameServiceRef = useRef(new ChessGameService()); // Business logic
  const apiClientRef = useRef(new ChessAPIClient(httpClient)); // External communication
  const [gameState, setGameState] = useState<ChessTrainingGameState | null>(null);
  
  const createGame = useCallback(async (config: GameConfig) => {
    try {
      // Use client for external API call
      const result = await apiClientRef.current.createGame(config);
      
      // Use service to validate/process result
      gameServiceRef.current = new ChessGameService(result.initialFen);
      
      setGameState(result);
      return { success: true, gameId: result.id };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }, []);
  
  const makeMove = useCallback(async (move: ChessMove) => {
    if (!gameState) return { success: false, error: 'No active game' };
    
    try {
      // First validate move locally with service
      const localResult = gameServiceRef.current.makeMove(move);
      if (!localResult.success) {
        return { success: false, error: localResult.error };
      }
      
      // Then submit to backend via client
      const result = await apiClientRef.current.submitMove(gameState.id, move);
      
      setGameState(prev => ({
        ...prev,
        fen: result.newFen,
        moves: [...prev.moves, result.playerMove, result.aiMove].filter(Boolean),
        status: result.gameStatus
      }));
      
      return { success: true, result };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }, [gameState]);
  
  return { gameState, createGame, makeMove };
};
```

### 4. Stores Layer (`/stores`)

**Purpose**: Global state management with Zustand
**Responsibility**: Cross-component state that persists during app lifecycle
**Rules**:
- Use for authentication state, user preferences, global UI state
- No business logic - delegate to services
- Actions should call services/clients for side effects
- Keep stores focused and domain-specific

```typescript
// stores/authStore.ts
interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  isAuthenticated: false,
  user: null,
  token: localStorage.getItem('token'),
  
  login: async (credentials) => {
    // Use client for API call
    const apiClient = new ChessTrainingAPIClient(httpClient);
    const result = await apiClient.authenticateUser(credentials);
    
    // Update global state
    localStorage.setItem('token', result.token);
    set({
      isAuthenticated: true,
      user: result.user,
      token: result.token
    });
  },
  
  logout: () => {
    localStorage.removeItem('token');
    set({ isAuthenticated: false, user: null, token: null });
  },
  
  refreshToken: async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      const apiClient = new ChessTrainingAPIClient(httpClient);
      const result = await apiClient.refreshToken(refreshToken);
      
      localStorage.setItem('token', result.token);
      set({ token: result.token });
      return true;
    } catch {
      get().logout();
      return false;
    }
  }
}));

// stores/demoStore.ts
interface DemoState {
  currentPage: string;
  chessboardSettings: ChessboardSettings;
  updateSettings: (settings: Partial<ChessboardSettings>) => void;
}

export const useDemoStore = create<DemoState>((set) => ({
  currentPage: 'free-play',
  chessboardSettings: {
    pieceSet: 'classic',
    boardTheme: 'classic',
    showCoordinates: true,
    animationsEnabled: true
  },
  
  updateSettings: (settings) =>
    set((state) => ({
      chessboardSettings: { ...state.chessboardSettings, ...settings }
    }))
}));
```

### 5. Providers Layer (`/providers`)

**Purpose**: React context setup and configuration
**Responsibility**: Initialize global providers for the application
**Rules**:
- Keep minimal - only for library configuration
- No business logic
- Provide configuration for React Query, Toast systems, etc.

```typescript
// providers/QueryProvider.tsx
export const QueryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5 * 60 * 1000, // 5 minutes
        retry: 3,
        refetchOnWindowFocus: false
      },
      mutations: {
        retry: 1
      }
    }
  });

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
};

// providers/ToastProvider.tsx
export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <>
      {children}
      <Toast.Provider>
        <Toast.Viewport />
      </Toast.Provider>
    </>
  );
};
```

### 6. Components Layer (`/components`)

**Purpose**: Pure UI presentation
**Responsibility**: Render UI based on props, emit events
**Rule**: No business logic, no direct service calls, no inline types

```typescript
// components/chessboard/Chessboard/Chessboard.tsx
export const Chessboard: React.FC<ChessboardProps> = ({
  gameState,
  onMove,
  onSquareClick,
  orientation = 'white',
  pieceSet = 'classic',
  showCoordinates = true,
  boardWidth,
  className,
  ...rest
}) => {
  const { 
    boardSize, 
    containerRef 
  } = useResponsiveBoard(boardWidth);
  
  const {
    draggedPiece,
    handleDragStart,
    handleDragEnd,
    handleDrop
  } = useDragAndDrop({
    onMove,
    gameState
  });

  const {
    animatedPieces,
    isAnimating
  } = useChessAnimation({
    pieces: gameState?.position,
    lastMove: gameState?.lastMove
  });

  const handleSquareClickInternal = useCallback((position: ChessPosition) => {
    onSquareClick?.(position);
  }, [onSquareClick]);

  return (
    <div 
      ref={containerRef}
      className={cn('chessboard', className)}
      style={boardSize}
      {...rest}
    >
      <Board
        gameState={gameState}
        orientation={orientation}
        onSquareClick={handleSquareClickInternal}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
        onDrop={handleDrop}
        animatedPieces={animatedPieces}
        isAnimating={isAnimating}
        showCoordinates={showCoordinates}
        pieceSet={pieceSet}
      />
    </div>
  );
};
```

---

## Anti-Patterns and Safeguards

### ❌ Anti-Patterns to Avoid

#### 1. Inline Type Definitions
```typescript
// ❌ BAD: Inline interface
const Component: React.FC<{
  position: { rank: number; file: string };
  onMove: (from: string, to: string) => void;
}> = ({ position, onMove }) => {
  // Component implementation
};

// ✅ GOOD: Separate type definition
const Component: React.FC<ComponentProps> = ({ position, onMove }) => {
  // Component implementation
};
```

#### 2. Business Logic in Components
```typescript
// ❌ BAD: Business logic in component
const Chessboard = () => {
  const [fen, setFen] = useState('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
  
  const makeMove = (from: string, to: string) => {
    const chess = new Chess(fen);
    const move = chess.move({ from, to });
    if (move) {
      setFen(chess.fen());
    }
  };
  // ...
};

// ✅ GOOD: Use service through hook
const Chessboard = () => {
  const { gameState, makeMove } = useChessGame();
  // Component only handles UI
};
```

#### 3. Direct API Calls in Components
```typescript
// ❌ BAD: Direct client/service instantiation in components
const Component = () => {
  const gameService = new ChessGameService();
  const apiClient = new ChessAPIClient();
  // ...
};

// ❌ BAD: Direct API calls in components
const Component = () => {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch('/api/games')
      .then(res => res.json())
      .then(setData);
  }, []);
  // ...
};

// ✅ GOOD: Use through hooks
const Component = () => {
  const { gameState, makeMove } = useChessGame();
  const { gameData, isLoading } = useChessTrainingGame();
  // ...
};
```

#### 4. Mixing Services and Clients
```typescript
// ❌ BAD: Service making API calls
export class ChessGameService {
  public async makeMove(move: ChessMove): Promise<MoveResult> {
    // Business logic
    const validatedMove = this.validateMove(move);
    
    // ❌ API call in service - should be in client
    const response = await fetch('/api/games/move', {
      method: 'POST',
      body: JSON.stringify(validatedMove)
    });
    
    return response.json();
  }
}

// ✅ GOOD: Clear separation
export class ChessGameService {
  public makeMove(move: ChessMove): MoveResult {
    // Only business logic - no API calls
    return this.validateMove(move);
  }
}

export class ChessAPIClient {
  public async submitMove(gameId: string, move: ChessMove): Promise<APIResponse> {
    // Only API communication - no business logic
    const response = await this.httpClient.post(`/games/${gameId}/move`, move);
    return this.mapResponse(response.data);
  }
}
```

### ✅ Safeguards and Best Practices

#### 1. ESLint Rules
```json
// .eslintrc.json
{
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "error",
    "react-hooks/exhaustive-deps": "error",
    "react/no-inline-styles": "error",
    "import/no-default-export": "error" // Prefer named exports
  }
}
```

#### 2. File Naming Conventions
- Components: PascalCase (`Chessboard.tsx`)
- Hooks: camelCase with `use` prefix (`useChessGame.ts`)
- Services: PascalCase with `Service` suffix (`ChessGameService.ts`)
- Types: camelCase with `.types.ts` suffix (`chess.types.ts`)
- Utils: camelCase with `.utils.ts` suffix (`chess.utils.ts`)

#### 3. Import/Export Patterns
```typescript
// ✅ GOOD: Barrel exports in index.ts files
// components/chessboard/index.ts
export { Chessboard } from './Chessboard';
export { Board } from './Board';
export { Square } from './Square';
export { Piece } from './Piece';

// ✅ GOOD: Named imports
import { ChessGameService, FenService } from '@/services/chess';
import { ChessPosition, ChessPiece } from '@/types';
```

#### 4. Dependency Injection Pattern
```typescript
// services/chess/ChessGameService.ts
export class ChessGameService {
  constructor(
    private readonly fenService: FenService,
    private readonly validationService: MoveValidationService
  ) {}
}

// hooks/useChessGame.ts
export const useChessGame = (
  services: ChessGameServices = defaultServices
): ChessGameHook => {
  // Use injected services
};
```

---

## Testing Strategy

### Unit Tests Structure
```
__tests__/
├── components/
│   ├── Chessboard.test.tsx
│   ├── Square.test.tsx
│   └── Piece.test.tsx
├── hooks/
│   ├── useChessGame.test.ts
│   └── useDragAndDrop.test.ts
├── services/
│   ├── ChessGameService.test.ts
│   └── FenService.test.ts
└── utils/
    └── chess.utils.test.ts
```

### Test Isolation Rules
- Services: Test business logic with mocked dependencies
- Hooks: Test with React Testing Library and mocked services
- Components: Test UI behavior with mocked hooks
- Utils: Test pure functions in isolation

---

## Performance Guidelines

### 1. Memoization Strategy
```typescript
// ✅ Memoize expensive calculations
const validMoves = useMemo(() => 
  gameService.getValidMoves(selectedSquare), 
  [selectedSquare, gameState]
);

// ✅ Memoize callback functions
const handleSquareClick = useCallback((square: ChessPosition) => {
  onSquareClick(square);
}, [onSquareClick]);
```

### 2. Component Optimization
```typescript
// ✅ Memoize components that receive stable props
export const Square = React.memo<SquareProps>(({ 
  position, 
  piece, 
  isHighlighted, 
  onClick 
}) => {
  // Component implementation
});
```

### 3. Bundle Optimization
- Tree-shake unused piece sets
- Lazy load heavy components
- Use dynamic imports for optional features

This architecture ensures maintainable, testable, and scalable code while strictly enforcing separation of concerns and preventing common React anti-patterns.