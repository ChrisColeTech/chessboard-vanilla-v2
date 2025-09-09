# Source Code Examples for Example Project Implementation

This document contains all the TypeScript/JavaScript source code examples extracted from the Phase 9 implementation plan. These examples demonstrate the architecture patterns and implementation approaches for the chessboard-vanilla-v2 example project.

## Demo Services

### DemoConfigService.ts

```typescript
// services/demo/DemoConfigService.ts
export class DemoConfigService {
  public getBasicConfig(): ChessboardConfig {
    return {
      initialFen: STARTING_POSITION_FEN,
      boardTheme: "classic",
      pieceSet: "classic",
      showCoordinates: true,
      animationsEnabled: true,
    };
  }
}
```

### ExampleGeneratorService.ts

```typescript
// services/demo/ExampleGeneratorService.ts
export class ExampleGeneratorService {
  public generateAdvancedExample(config: AdvancedConfig): string {
    return `<Chessboard
  pieceSet="${config.pieceSet}"
  boardTheme="${config.boardTheme}"
  animationDuration={${config.animationDuration}}
  showCoordinates={${config.showCoordinates}}
/>`;
  }
}
```

### MigrationService.ts

```typescript
// services/demo/MigrationService.ts
export class MigrationService {
  public generatePOCExample(): POCExample {
    return {
      oldAPI: `<Chessboard FEN={fen} onChange={handleChange} playerColor="white" boardSize={400} />`,
      newAPI: `<Chessboard initialFen={fen} onMove={handleMove} boardOrientation="white" width={400} />`,
    };
  }

  public getMigrationGuide(): MigrationStep[] {
    return [
      { from: "FEN", to: "initialFen", description: "Renamed for clarity" },
      {
        from: "onChange",
        to: "onMove",
        description: "More specific callback name",
      },
    ];
  }
}
```

### ResponsiveTestService.ts

```typescript
// services/performance/ResponsiveTestService.ts
export class ResponsiveTestService {
  public generateContainerSizes(): ContainerSize[] {
    return [
      { name: "Mobile", width: 320, height: 568 },
      { name: "Tablet", width: 768, height: 1024 },
      { name: "Desktop", width: 1920, height: 1080 },
    ];
  }

  public measureLayoutShift(element: HTMLElement): LayoutShiftMetrics {
    // Implementation for measuring layout stability
  }
}
```

## API Clients

### ChessTrainingAPIClient.ts

```typescript
// services/clients/ChessTrainingAPIClient.ts
export class ChessTrainingAPIClient {
  private readonly baseURL = "http://localhost:3000/api";

  constructor(private readonly httpClient: HttpClient) {}

  public async authenticateUser(
    credentials: LoginCredentials
  ): Promise<AuthResult> {
    try {
      const response = await this.httpClient.post("/auth/login", {
        email: credentials.email,
        password: credentials.password,
      });

      return {
        success: true,
        token: response.data.token,
        refreshToken: response.data.refreshToken,
        user: response.data.user,
      };
    } catch (error) {
      throw new ChessTrainingAPIError("Authentication failed", error);
    }
  }

  public async createGame(gameConfig: GameConfig): Promise<GameResult> {
    try {
      const response = await this.httpClient.post("/games/create", {
        aiLevel: gameConfig.difficulty,
        color: gameConfig.playerColor,
        timeControl: gameConfig.timeControl,
      });

      return this.mapToGameResult(response.data);
    } catch (error) {
      throw new ChessTrainingAPIError("Game creation failed", error);
    }
  }

  public async submitMove(
    gameId: string,
    move: ChessMove
  ): Promise<MoveResult> {
    try {
      const response = await this.httpClient.post(`/games/${gameId}/move`, {
        move: {
          from: move.from,
          to: move.to,
          promotion: move.promotion,
        },
        timeSpent: move.timeSpent,
      });

      return {
        success: true,
        playerMove: response.data.playerMove,
        aiMove: response.data.aiMove,
        newFen: response.data.newFen,
        gameStatus: response.data.gameStatus,
      };
    } catch (error) {
      throw new ChessTrainingAPIError("Move submission failed", error);
    }
  }
}
```

### PuzzleAPIClient.ts

```typescript
// services/clients/PuzzleAPIClient.ts
export class PuzzleAPIClient {
  private readonly baseURL = "http://localhost:3000/api";

  constructor(private readonly httpClient: HttpClient) {}

  public async getNextPuzzle(): Promise<PuzzleData> {
    try {
      const response = await this.httpClient.get("/puzzles/next");

      return {
        id: response.data.puzzle.id,
        fen: response.data.puzzle.fen,
        themes: response.data.puzzle.themes,
        rating: response.data.puzzle.rating,
        description: response.data.puzzle.description,
      };
    } catch (error) {
      throw new ChessTrainingAPIError("Puzzle loading failed", error);
    }
  }

  public async submitPuzzleSolution(
    puzzleId: string,
    solution: PuzzleSolution
  ): Promise<SolutionResult> {
    try {
      const response = await this.httpClient.post(
        `/puzzles/${puzzleId}/solve`,
        {
          moves: solution.moves,
          timeTaken: solution.timeTaken,
          hintsUsed: solution.hintsUsed,
        }
      );

      return {
        correct: response.data.correct,
        newRating: response.data.newRating,
        ratingChange: response.data.ratingChange,
        solution: response.data.solution,
      };
    } catch (error) {
      throw new ChessTrainingAPIError(
        "Puzzle solution submission failed",
        error
      );
    }
  }
}
```

## React Hooks

### useDemoState.ts

```typescript
// hooks/demo/useDemoState.ts
export const useDemoState = (): DemoStateHook => {
  const configService = useRef(new DemoConfigService());
  const [config, setConfig] = useState(configService.current.getBasicConfig());

  return { config, setConfig };
};
```

### useControlPanel.ts

```typescript
// hooks/demo/useControlPanel.ts
export const useControlPanel = (): ControlPanelHook => {
  const configService = useRef(new DemoConfigService());
  const [settings, setSettings] = useState(
    configService.current.getAdvancedConfig()
  );

  const updateSetting = useCallback((key: string, value: any) => {
    setSettings((prev) =>
      configService.current.updateSetting(prev, key, value)
    );
  }, []);

  return { settings, updateSetting };
};
```

### useAuthentication.ts

```typescript
// hooks/auth/useAuthentication.ts
export const useAuthentication = (): AuthenticationHook => {
  const apiClient = useRef(new ChessTrainingAPIClient(httpClient));
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    token: null,
    user: null,
    isLoading: true,
  });

  const login = useCallback(async (credentials: LoginCredentials) => {
    try {
      const result = await apiClient.current.authenticateUser(credentials);

      localStorage.setItem("token", result.token);
      localStorage.setItem("refreshToken", result.refreshToken);

      setAuthState({
        isAuthenticated: true,
        token: result.token,
        user: result.user,
        isLoading: false,
      });

      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }, []);

  return { authState, login };
};
```

### useChessTrainingGame.ts

```typescript
// hooks/chess/useChessTrainingGame.ts
export const useChessTrainingGame = (): ChessTrainingGameHook => {
  const apiClient = useRef(new ChessTrainingAPIClient(httpClient));
  const [gameState, setGameState] = useState<ChessTrainingGameState | null>(
    null
  );

  const createGame = useCallback(async (config: GameConfig) => {
    try {
      const result = await apiClient.current.createGame(config);
      setGameState(result);
      return { success: true, gameId: result.id };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }, []);

  const makeMove = useCallback(
    async (move: ChessMove) => {
      if (!gameState) return { success: false, error: "No active game" };

      try {
        const result = await apiClient.current.submitMove(gameState.id, move);
        setGameState((prev) => ({
          ...prev,
          fen: result.newFen,
          moves: [...prev.moves, result.playerMove, result.aiMove].filter(
            Boolean
          ),
          status: result.gameStatus,
        }));
        return { success: true, result };
      } catch (error) {
        return { success: false, error: error.message };
      }
    },
    [gameState]
  );

  return { gameState, createGame, makeMove };
};
```

### useGameQueries.ts

```typescript
// hooks/queries/useGameQueries.ts
export const useGameHistory = () => {
  const { token } = useAuthStore();

  return useQuery({
    queryKey: ["game-history"],
    queryFn: async () => {
      const apiClient = new ChessTrainingAPIClient();
      return await apiClient.getGameHistory();
    },
    enabled: !!token,
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  });
};

export const usePuzzleData = () => {
  const { token } = useAuthStore();

  return useQuery({
    queryKey: ["current-puzzle"],
    queryFn: async () => {
      const puzzleClient = new PuzzleAPIClient();
      return await puzzleClient.getNextPuzzle();
    },
    enabled: !!token,
    refetchOnMount: true, // Always get fresh puzzle
  });
};
```

### useGameMutations.ts

```typescript
// hooks/mutations/useGameMutations.ts
export const useSubmitPuzzleSolution = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ puzzleId, solution }: PuzzleSolutionInput) => {
      const puzzleClient = new PuzzleAPIClient();
      return await puzzleClient.submitSolution(puzzleId, solution);
    },
    onSuccess: () => {
      // Invalidate and refetch puzzle data
      queryClient.invalidateQueries({ queryKey: ["current-puzzle"] });
      queryClient.invalidateQueries({ queryKey: ["puzzle-stats"] });
    },
  });
};
```

## Zustand Stores

### authStore.ts

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
  token: localStorage.getItem("token"),

  login: async (credentials) => {
    const apiClient = new ChessTrainingAPIClient();
    const result = await apiClient.authenticateUser(credentials);

    localStorage.setItem("token", result.token);
    localStorage.setItem("refreshToken", result.refreshToken);

    set({
      isAuthenticated: true,
      user: result.user,
      token: result.token,
    });
  },

  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    set({ isAuthenticated: false, user: null, token: null });
  },

  refreshToken: async () => {
    // Token refresh logic
    try {
      const refreshToken = localStorage.getItem("refreshToken");
      // Call refresh API
      return true;
    } catch {
      get().logout();
      return false;
    }
  },
}));
```

### demoStore.ts

```typescript
// stores/demoStore.ts
interface DemoState {
  currentPage: string;
  chessboardSettings: ChessboardSettings;
  updateSettings: (settings: Partial<ChessboardSettings>) => void;
  setCurrentPage: (page: string) => void;
}

export const useDemoStore = create<DemoState>((set) => ({
  currentPage: "free-play",
  chessboardSettings: {
    pieceSet: "classic",
    boardTheme: "classic",
    showCoordinates: true,
    animationsEnabled: true,
    animationDuration: 300,
  },

  updateSettings: (settings) =>
    set((state) => ({
      chessboardSettings: { ...state.chessboardSettings, ...settings },
    })),

  setCurrentPage: (page) => set({ currentPage: page }),
}));
```

### gameStore.ts

```typescript
// stores/gameStore.ts
interface GameState {
  activeGames: Map<string, ChessTrainingGameState>;
  currentGameId: string | null;
  createGame: (config: GameConfig) => Promise<string>;
  makeMove: (gameId: string, move: ChessMove) => Promise<boolean>;
  endGame: (gameId: string) => void;
}

export const useGameStore = create<GameState>((set, get) => ({
  activeGames: new Map(),
  currentGameId: null,

  createGame: async (config) => {
    const apiClient = new ChessTrainingAPIClient();
    const result = await apiClient.createGame(config);

    set((state) => ({
      activeGames: new Map(state.activeGames).set(result.id, result),
      currentGameId: result.id,
    }));

    return result.id;
  },

  makeMove: async (gameId, move) => {
    const game = get().activeGames.get(gameId);
    if (!game) return false;

    const apiClient = new ChessTrainingAPIClient();
    const result = await apiClient.submitMove(gameId, move);

    set((state) => {
      const newGames = new Map(state.activeGames);
      newGames.set(gameId, { ...game, ...result });
      return { activeGames: newGames };
    });

    return true;
  },

  endGame: (gameId) => {
    set((state) => {
      const newGames = new Map(state.activeGames);
      newGames.delete(gameId);
      return {
        activeGames: newGames,
        currentGameId:
          state.currentGameId === gameId ? null : state.currentGameId,
      };
    });
  },
}));
```

## React Components

### BasicDemoPage.tsx

```typescript
// components/pages/BasicDemoPage/BasicDemoPage.tsx
export const BasicDemoPage: React.FC<BasicDemoPageProps> = ({ className }) => {
  const { config } = useDemoState();

  return (
    <Layout className={className}>
      <Chessboard {...config} />
      <CodeExample code={generateBasicExample(config)} />
    </Layout>
  );
};
```

### AdvancedDemoPage.tsx

```typescript
// components/pages/AdvancedDemoPage/AdvancedDemoPage.tsx
export const AdvancedDemoPage: React.FC<AdvancedDemoPageProps> = ({
  className,
}) => {
  const { settings, updateSetting } = useControlPanel();

  return (
    <Layout className={className}>
      <ControlPanel settings={settings} onSettingChange={updateSetting} />
      <Chessboard {...settings} />
      <CodeExample code={generateAdvancedExample(settings)} />
    </Layout>
  );
};
```

### FreePlayDemoPage.tsx

```typescript
// components/pages/FreePlayDemoPage/FreePlayDemoPage.tsx
export const FreePlayDemoPage: React.FC<FreePlayDemoPageProps> = ({
  className,
}) => {
  const { gameState, makeMove, resetGame } = useChessGame(); // Local chess.js instance
  const { settings, updateSetting } = useControlPanel();

  return (
    <Layout className={className}>
      <ControlPanel settings={settings} onSettingChange={updateSetting} />
      <Chessboard
        initialFen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        onMove={makeMove}
        {...settings}
      />
      <GameStatus gameState={gameState} onReset={resetGame} />
    </Layout>
  );
};
```

### ConnectedGameDemoPage.tsx

```typescript
// components/pages/ConnectedGameDemoPage/ConnectedGameDemoPage.tsx
export const ConnectedGameDemoPage: React.FC<ConnectedGameDemoPageProps> = ({
  className,
}) => {
  const { authState, login } = useAuthentication();
  const { gameState, createGame, makeMove } = useChessTrainingGame();

  useEffect(() => {
    // Auto-login demo user
    if (!authState.isAuthenticated) {
      login({
        email: "demo@responsivechessboard.com",
        password: "DemoUser2024!",
      });
    }
  }, []);

  const handleStartGame = async () => {
    await createGame({
      difficulty: 2,
      playerColor: "white",
      timeControl: "10+0",
    });
  };

  if (!authState.isAuthenticated) {
    return <LoadingSpinner message="Authenticating..." />;
  }

  return (
    <Layout className={className}>
      {!gameState ? (
        <GameSetup onStartGame={handleStartGame} />
      ) : (
        <Chessboard
          initialFen={gameState.fen}
          onMove={makeMove}
          boardTheme="classic"
          pieceSet="classic"
        />
      )}
    </Layout>
  );
};
```

### PuzzleDemoPage.tsx

```typescript
// components/pages/PuzzleDemoPage/PuzzleDemoPage.tsx
export const PuzzleDemoPage: React.FC<PuzzleDemoPageProps> = ({
  className,
}) => {
  const { authState } = useAuthentication();
  const { puzzleState, loadNextPuzzle, submitSolution } =
    useChessTrainingPuzzle();

  return (
    <Layout className={className}>
      {puzzleState.currentPuzzle ? (
        <>
          <PuzzleInfo puzzle={puzzleState.currentPuzzle} />
          <Chessboard
            initialFen={puzzleState.currentPuzzle.fen}
            onMove={submitSolution}
            boardOrientation="white"
            pieceSet="tournament"
          />
          <PuzzleControls onHint={requestHint} onNext={loadNextPuzzle} />
        </>
      ) : (
        <LoadingSpinner message="Loading puzzle..." />
      )}
    </Layout>
  );
};
```

### ControlPanel.tsx

```typescript
// components/demo/ControlPanel.tsx
export const ControlPanel: React.FC<ControlPanelProps> = ({ onSettingsChange }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedTab, setSelectedTab] = useState('appearance');
  const { chessboardSettings, updateSettings } = useDemoStore();

  const handleSettingChange = (key: string, value: any) => {
    const newSettings = { [key]: value };
    updateSettings(newSettings);
    onSettingsChange?.(newSettings);
  };

  return (
    // Component JSX
  );
};
```

## Data Flow Pattern

### Component Data Flow

```typescript
// 1. User action in component
const handleMove = (move: ChessMove) => {
  // 2. Update local UI optimistically
  setIsMoving(true);

  // 3. Call global store action
  const success = await makeMove(currentGameId, move);

  // 4. Store handles API call via client
  // 5. React Query invalidates related server data
  // 6. UI updates automatically via store subscriptions

  setIsMoving(false);
};
```

This document contains all TypeScript/JavaScript source code examples from the Phase 9 implementation plan, organized by component type and architectural layer for easy reference during development.
