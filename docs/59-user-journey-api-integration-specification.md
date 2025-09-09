# Document 20: User Journey & API Integration Specification

**Created**: 2025-08-30  
**Phase**: Implementation Ready - Complete User Flow Documentation  
**Related Documents**: 
- [Document 17](./17-dashboard-layout-post-authentication.md) - Dashboard implementation
- [Document 18](./18-ui-components-shadcn-integration.md) - Component methodology  
- [Document 19](./19-dashboard-improvements-and-global-architecture.md) - Architecture planning

## Overview

Complete specification of user journeys through the chess training application with exact API integration points, data flows, error handling, and performance considerations. This document serves as the definitive implementation guide for frontend-backend integration.

## 🚀 Application Startup & Authentication Flow

### **Initial App Load**
```typescript
// App.tsx - Application initialization
useEffect(() => {
  const initializeApp = async () => {
    try {
      // Step 1: Show splash screen while checking auth
      setSplashVisible(true)
      
      // Step 2: Check existing authentication
      const response = await fetch('/api/auth/me', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      
      if (response.ok) {
        const userData = await response.json()
        setUser(userData.user)
        setIsAuthenticated(true)
        navigate('/dashboard')
      } else {
        // Token invalid/expired
        localStorage.removeItem('token')
        navigate('/login')
      }
    } catch (error) {
      console.error('App initialization failed:', error)
      navigate('/login')
    } finally {
      setSplashVisible(false)
    }
  }
  
  initializeApp()
}, [])
```

### **Authentication Journey**

#### **Login Flow**:
```typescript
// LoginPage.tsx - User login
const handleLogin = async (credentials: LoginCredentials) => {
  try {
    setLoading(true)
    
    // API Call: Authenticate user
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      
      // Store authentication data
      localStorage.setItem('token', data.token)
      localStorage.setItem('refreshToken', data.refreshToken)
      
      // Update global state
      setUser(data.user)
      setIsAuthenticated(true)
      
      // Success feedback
      soundFX.playSuccess()
      showToast('Welcome back!', 'success')
      
      // Navigate after brief success animation
      setTimeout(() => navigate('/dashboard'), 300)
      
    } else {
      const error = await response.json()
      showToast(error.error || 'Login failed', 'error')
    }
  } catch (error) {
    console.error('Login error:', error)
    showToast('Connection error. Please try again.', 'error')
  } finally {
    setLoading(false)
  }
}
```

## 🏠 Dashboard Experience & Data Loading

### **Dashboard Initialization**
```typescript
// DashboardPage.tsx - Complete dashboard data loading
const useDashboard = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData>({
    stats: null,
    recentGames: [],
    puzzleProgress: null,
    achievements: [],
    dailyGoals: [],
    isLoading: true,
    error: null
  })
  
  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        // Parallel API calls for better performance
        const [statsResponse, gamesResponse, puzzleResponse, achievementsResponse] = await Promise.all([
          fetch('/api/user/dashboard-stats', {
            headers: { 'Authorization': `Bearer ${getToken()}` }
          }),
          fetch('/api/games?limit=5&status=completed', {
            headers: { 'Authorization': `Bearer ${getToken()}` }
          }),
          fetch('/api/puzzles/stats', {
            headers: { 'Authorization': `Bearer ${getToken()}` }
          }),
          fetch('/api/achievements?recent=true', {
            headers: { 'Authorization': `Bearer ${getToken()}` }
          })
        ])
        
        // Process responses
        const stats = await statsResponse.json()
        const recentGames = await gamesResponse.json()
        const puzzleProgress = await puzzleResponse.json()
        const achievements = await achievementsResponse.json()
        
        setDashboardData({
          stats: stats.data,
          recentGames: recentGames.data,
          puzzleProgress: puzzleProgress.data,
          achievements: achievements.data,
          dailyGoals: calculateDailyGoals(stats.data),
          isLoading: false,
          error: null
        })
        
      } catch (error) {
        console.error('Dashboard loading failed:', error)
        setDashboardData(prev => ({
          ...prev,
          isLoading: false,
          error: 'Failed to load dashboard data'
        }))
      }
    }
    
    loadDashboardData()
  }, [])
  
  return dashboardData
}
```

### **Theme Switching (Client-Side)**
```typescript
// ThemeStore.ts - No API calls needed
const useThemeStore = create<ThemeState>((set, get) => ({
  currentTheme: 'shadow-knight',
  
  setTheme: (themeId: string) => {
    const theme = themes[themeId]
    if (theme) {
      set({ currentTheme: themeId })
      
      // Persist to localStorage (no API call)
      localStorage.setItem('selectedTheme', themeId)
      
      // Sound feedback
      soundFX.playThemeSwitch()
      
      // Optional: Save to user preferences (background API call)
      updateUserPreferences({ theme: themeId }).catch(console.error)
    }
  }
}))
```

## 🎮 Play Computer - Complete Game Flow

### **Game Setup & Creation**
```typescript
// PlayComputerPage.tsx - Game initialization
const startNewGame = async (gameSetup: GameSetup) => {
  try {
    setGameState('creating')
    
    // API Call: Create new game
    const response = await fetch('/api/games/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        aiLevel: gameSetup.difficulty, // 1-5
        color: gameSetup.playerColor,  // 'white', 'black', 'random'
        timeControl: gameSetup.timeControl || '10+0'
      })
    })
    
    if (response.ok) {
      const gameData = await response.json()
      
      setCurrentGame({
        id: gameData.gameId,
        fen: gameData.currentFen,
        playerColor: gameData.playerColor,
        aiLevel: gameData.aiLevel,
        status: 'active',
        moves: [],
        timeControl: gameData.timeControl
      })
      
      setGameState('playing')
      
      // Start game clock
      startGameClock(gameData.timeControl)
      
      // Play game start sound
      soundFX.playGameStart()
      
    } else {
      const error = await response.json()
      throw new Error(error.error || 'Failed to create game')
    }
  } catch (error) {
    console.error('Game creation failed:', error)
    setGameState('error')
    showToast('Failed to start game. Please try again.', 'error')
  }
}
```

### **Move Processing & AI Response**
```typescript
// ChessBoard.tsx - Move handling
const handlePlayerMove = async (move: ChessMove) => {
  try {
    // Optimistic UI update
    setIsProcessingMove(true)
    updateBoardPosition(move) // Show move immediately
    
    // API Call: Send move to backend
    const response = await fetch(`/api/games/${currentGame.id}/move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        move: {
          from: move.from,
          to: move.to,
          promotion: move.promotion
        },
        timeSpent: getCurrentMoveTime()
      })
    })
    
    if (response.ok) {
      const moveResult = await response.json()
      
      // Update game state with server response
      setCurrentGame(prev => ({
        ...prev,
        fen: moveResult.newFen,
        moves: [...prev.moves, moveResult.playerMove, moveResult.aiMove],
        status: moveResult.gameStatus,
        lastMoveTime: Date.now()
      }))
      
      // Play AI move with animation
      if (moveResult.aiMove) {
        setTimeout(() => {
          animateMove(moveResult.aiMove)
          soundFX.playMove()
        }, 500) // Brief delay for realism
      }
      
      // Handle game end
      if (moveResult.gameStatus !== 'active') {
        handleGameEnd(moveResult)
      }
      
    } else {
      // Revert optimistic update
      revertBoardPosition()
      const error = await response.json()
      showToast(error.error || 'Invalid move', 'error')
    }
    
  } catch (error) {
    console.error('Move processing failed:', error)
    revertBoardPosition()
    showToast('Connection error. Move not processed.', 'error')
  } finally {
    setIsProcessingMove(false)
  }
}
```

### **Game Completion & Statistics**
```typescript
// PlayComputerPage.tsx - Game end handling
const handleGameEnd = async (gameResult: GameResult) => {
  try {
    // Stop game clock
    stopGameClock()
    
    // Show game result modal
    setGameResult(gameResult)
    
    // Play appropriate sound
    if (gameResult.result.includes('wins')) {
      soundFX.playGameWin()
    } else if (gameResult.result === 'draw') {
      soundFX.playGameDraw()
    } else {
      soundFX.playGameLoss()
    }
    
    // Background API calls for progress tracking
    await Promise.all([
      // Update user statistics
      updateUserProgress({
        gamesPlayed: 1,
        eloChange: gameResult.eloChange,
        timeSpent: gameResult.totalTime
      }),
      
      // Check for new achievements
      checkAchievements({
        trigger: 'game_completed',
        gameResult: gameResult.result,
        aiLevel: currentGame.aiLevel
      })
    ])
    
  } catch (error) {
    console.error('Game end processing failed:', error)
    // Don't show error to user - game completed successfully
  }
}
```

## 📊 Game Review - Post-Game Analysis

### **Game Review Loading**
```typescript
// GameReviewPage.tsx - Review system
const useGameReview = () => {
  const [reviewState, setReviewState] = useState<GameReviewState>({
    availableGames: [],
    currentGame: null,
    moves: [],
    currentMoveIndex: 0,
    analysisData: null,
    isLoading: true,
    isAnalyzing: false
  })
  
  // Load available games for review
  useEffect(() => {
    const loadGames = async () => {
      try {
        const response = await fetch('/api/game-reviews?limit=20', {
          headers: { 'Authorization': `Bearer ${getToken()}` }
        })
        
        const gamesData = await response.json()
        setReviewState(prev => ({
          ...prev,
          availableGames: gamesData.data,
          isLoading: false
        }))
        
      } catch (error) {
        console.error('Failed to load games for review:', error)
        setReviewState(prev => ({
          ...prev,
          isLoading: false,
          error: 'Failed to load games'
        }))
      }
    }
    
    loadGames()
  }, [])
  
  // Load specific game for review
  const loadGameReview = async (gameId: string) => {
    try {
      setReviewState(prev => ({ ...prev, isLoading: true }))
      
      // Parallel loading of game data and moves
      const [gameResponse, movesResponse] = await Promise.all([
        fetch(`/api/game-reviews/${gameId}`, {
          headers: { 'Authorization': `Bearer ${getToken()}` }
        }),
        fetch(`/api/game-reviews/${gameId}/moves`, {
          headers: { 'Authorization': `Bearer ${getToken()}` }
        })
      ])
      
      const gameData = await gameResponse.json()
      const movesData = await movesResponse.json()
      
      setReviewState(prev => ({
        ...prev,
        currentGame: gameData.data,
        moves: movesData.data,
        currentMoveIndex: 0,
        isLoading: false
      }))
      
      // Generate analysis if not exists
      if (!gameData.data.analyzed) {
        generateGameAnalysis(gameId)
      }
      
    } catch (error) {
      console.error('Failed to load game review:', error)
      setReviewState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Failed to load game review'
      }))
    }
  }
  
  return { reviewState, loadGameReview }
}
```

### **Game Analysis Generation**
```typescript
// GameReviewPage.tsx - Analysis processing
const generateGameAnalysis = async (gameId: string) => {
  try {
    setReviewState(prev => ({ ...prev, isAnalyzing: true }))
    
    // API Call: Request game analysis
    const response = await fetch(`/api/games/${gameId}/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        engine: 'stockfish',
        depth: 15,
        includeBlunders: true,
        includeMissedTactics: true
      })
    })
    
    if (response.ok) {
      const analysisData = await response.json()
      
      setReviewState(prev => ({
        ...prev,
        analysisData: analysisData.data,
        isAnalyzing: false
      }))
      
      showToast('Game analysis completed!', 'success')
      
    } else {
      throw new Error('Analysis failed')
    }
    
  } catch (error) {
    console.error('Game analysis failed:', error)
    setReviewState(prev => ({ ...prev, isAnalyzing: false }))
    showToast('Analysis failed. Please try again.', 'error')
  }
}
```

### **Move Navigation & Blunder Highlighting**
```typescript
// GameReviewPage.tsx - Move navigation
const navigateToMove = (moveIndex: number) => {
  const move = reviewState.moves[moveIndex]
  
  if (move) {
    // Update board position (no API call)
    setReviewState(prev => ({
      ...prev,
      currentMoveIndex: moveIndex
    }))
    
    // Update chess board with position
    updateBoardToMove(move.fen)
    
    // Highlight if blunder/mistake
    if (move.evaluation?.isBlunder) {
      highlightBlunder(move)
      showMoveAnalysis({
        move: move.move,
        evaluation: move.evaluation.score,
        bestMove: move.evaluation.bestMove,
        explanation: move.evaluation.explanation
      })
    }
    
    // Play move sound
    soundFX.playMove()
  }
}
```

## 🔬 Analysis Board - Teaching & Free Play

### **Position Analysis**
```typescript
// AnalysisBoardPage.tsx - Position analysis
const analyzePosition = async (fen: string) => {
  try {
    setAnalysisState(prev => ({ ...prev, isAnalyzing: true }))
    
    // Check for cached analysis first
    const cachedResponse = await fetch(`/api/analysis/stored/${encodeURIComponent(fen)}`, {
      headers: { 'Authorization': `Bearer ${getToken()}` }
    })
    
    if (cachedResponse.ok) {
      const cachedData = await cachedResponse.json()
      displayAnalysis(cachedData.data)
      return
    }
    
    // No cached analysis - request new analysis
    const response = await fetch('/api/analysis/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        fen: fen,
        depth: 18,
        multiPV: 3, // Show top 3 moves
        includeEvaluation: true
      })
    })
    
    if (response.ok) {
      const analysisData = await response.json()
      displayAnalysis(analysisData.data)
      
      // Cache analysis for future use (background call)
      cacheAnalysis(fen, analysisData.data).catch(console.error)
      
    } else {
      throw new Error('Analysis failed')
    }
    
  } catch (error) {
    console.error('Position analysis failed:', error)
    showToast('Analysis failed. Please try again.', 'error')
  } finally {
    setAnalysisState(prev => ({ ...prev, isAnalyzing: false }))
  }
}
```

### **Best Move Recommendation**
```typescript
// AnalysisBoardPage.tsx - Best move suggestion
const getBestMove = async (fen: string) => {
  try {
    const response = await fetch('/api/analysis/best-move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        fen: fen,
        depth: 15
      })
    })
    
    if (response.ok) {
      const bestMoveData = await response.json()
      
      // Highlight best move on board
      highlightMove({
        from: bestMoveData.bestMove.from,
        to: bestMoveData.bestMove.to,
        evaluation: bestMoveData.evaluation
      })
      
      // Show move explanation
      showMoveExplanation({
        move: bestMoveData.bestMove.notation,
        explanation: bestMoveData.explanation,
        evaluation: bestMoveData.evaluation
      })
      
    } else {
      throw new Error('Best move lookup failed')
    }
    
  } catch (error) {
    console.error('Best move failed:', error)
    showToast('Could not determine best move', 'error')
  }
}
```

### **Opening Identification**
```typescript
// AnalysisBoardPage.tsx - Opening identification
const identifyOpening = async (moves: string[]) => {
  try {
    const response = await fetch('/api/analysis/opening', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        moves: moves
      })
    })
    
    if (response.ok) {
      const openingData = await response.json()
      
      setOpeningInfo({
        name: openingData.opening.name,
        eco: openingData.opening.eco,
        moves: openingData.opening.moves,
        description: openingData.opening.description,
        frequency: openingData.opening.frequency
      })
      
    } else {
      setOpeningInfo(null)
    }
    
  } catch (error) {
    console.error('Opening identification failed:', error)
    setOpeningInfo(null)
  }
}
```

## 🧩 Puzzle System - Learning & Practice

### **Next Puzzle Loading**
```typescript
// PuzzlePage.tsx - Puzzle system
const useNextPuzzle = () => {
  const [puzzleState, setPuzzleState] = useState<PuzzleState>({
    currentPuzzle: null,
    isLoading: true,
    userRating: 1200,
    streak: 0,
    todaysSolved: 0
  })
  
  const loadNextPuzzle = async () => {
    try {
      setPuzzleState(prev => ({ ...prev, isLoading: true }))
      
      // API Call: Get personalized next puzzle
      const response = await fetch('/api/puzzles/next', {
        headers: { 'Authorization': `Bearer ${getToken()}` }
      })
      
      if (response.ok) {
        const puzzleData = await response.json()
        
        setPuzzleState(prev => ({
          ...prev,
          currentPuzzle: {
            id: puzzleData.puzzle.id,
            fen: puzzleData.puzzle.fen,
            themes: puzzleData.puzzle.themes,
            rating: puzzleData.puzzle.rating,
            description: puzzleData.puzzle.description,
            solutionMoves: [], // Hidden from user
            hintsUsed: 0
          },
          isLoading: false
        }))
        
        // Initialize puzzle board
        initializePuzzleBoard(puzzleData.puzzle.fen)
        
      } else {
        throw new Error('No puzzles available')
      }
      
    } catch (error) {
      console.error('Failed to load puzzle:', error)
      setPuzzleState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Failed to load puzzle'
      }))
    }
  }
  
  return { puzzleState, loadNextPuzzle }
}
```

### **Puzzle Solution Submission**
```typescript
// PuzzlePage.tsx - Solution processing
const submitPuzzleSolution = async (moves: string[]) => {
  try {
    const startTime = puzzleState.startTime
    const timeTaken = Date.now() - startTime
    
    // API Call: Submit puzzle solution
    const response = await fetch(`/api/puzzles/${puzzleState.currentPuzzle.id}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        moves: moves,
        timeTaken: timeTaken,
        hintsUsed: puzzleState.currentPuzzle.hintsUsed
      })
    })
    
    if (response.ok) {
      const solutionResult = await response.json()
      
      if (solutionResult.correct) {
        // Success feedback
        showSuccessAnimation()
        soundFX.playPuzzleSuccess()
        
        // Update statistics
        setPuzzleState(prev => ({
          ...prev,
          userRating: solutionResult.newRating,
          streak: prev.streak + 1,
          todaysSolved: prev.todaysSolved + 1
        }))
        
        showToast(`Correct! +${solutionResult.ratingChange} rating`, 'success')
        
        // Show complete solution
        setTimeout(() => {
          playSolutionSequence(solutionResult.solution)
        }, 1500)
        
      } else {
        // Incorrect solution
        showErrorAnimation()
        soundFX.playPuzzleError()
        
        setPuzzleState(prev => ({
          ...prev,
          streak: 0 // Reset streak on failure
        }))
        
        showToast('Not quite right. Try again!', 'warning')
        
        // Reset board position
        resetBoardToStartingPosition()
      }
      
    } else {
      throw new Error('Solution submission failed')
    }
    
  } catch (error) {
    console.error('Puzzle solution failed:', error)
    showToast('Failed to submit solution', 'error')
  }
}
```

### **Puzzle Hints**
```typescript
// PuzzlePage.tsx - Hint system
const getPuzzleHint = async () => {
  try {
    // API Call: Request hint
    const response = await fetch(`/api/puzzles/${puzzleState.currentPuzzle.id}/hint`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      }
    })
    
    if (response.ok) {
      const hintData = await response.json()
      
      // Update puzzle state
      setPuzzleState(prev => ({
        ...prev,
        currentPuzzle: {
          ...prev.currentPuzzle,
          hintsUsed: hintData.hintsUsed
        }
      }))
      
      // Show hint to user
      showHint({
        text: hintData.hint,
        hintNumber: hintData.hintsUsed,
        maxHints: hintData.maxHints
      })
      
      // Play hint sound
      soundFX.playHint()
      
    } else {
      throw new Error('Hint request failed')
    }
    
  } catch (error) {
    console.error('Puzzle hint failed:', error)
    showToast('Hint not available', 'error')
  }
}
```

## 📈 Progress Tracking & Achievements

### **Background Progress Updates**
```typescript
// ProgressService.ts - Automatic progress tracking
const updateUserProgress = async (progressData: ProgressUpdate) => {
  try {
    // API Call: Update user progress (background)
    const response = await fetch('/api/user/progress', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify(progressData)
    })
    
    if (response.ok) {
      const updatedStats = await response.json()
      
      // Update global user state
      updateUserStats(updatedStats.stats)
      
      // Check for rating milestones
      if (updatedStats.milestones?.length > 0) {
        showMilestoneNotifications(updatedStats.milestones)
      }
    }
    
  } catch (error) {
    console.error('Progress update failed:', error)
    // Don't show error to user - this is background operation
  }
}
```

### **Achievement System**
```typescript
// AchievementService.ts - Achievement checking
const checkAchievements = async (trigger: AchievementTrigger) => {
  try {
    // API Call: Check for new achievements
    const response = await fetch('/api/achievements/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify(trigger)
    })
    
    if (response.ok) {
      const achievementResult = await response.json()
      
      if (achievementResult.newAchievements?.length > 0) {
        // Show achievement notifications
        achievementResult.newAchievements.forEach((achievement, index) => {
          setTimeout(() => {
            showAchievementUnlock(achievement)
            soundFX.playAchievement()
          }, index * 1000) // Stagger multiple achievements
        })
      }
    }
    
  } catch (error) {
    console.error('Achievement check failed:', error)
    // Don't show error to user - this is background operation
  }
}
```

## ⚙️ Settings & Preferences

### **User Preferences Management**
```typescript
// SettingsPage.tsx - Settings management
const updateUserPreferences = async (preferences: UserPreferences) => {
  try {
    // Optimistic UI update
    updateLocalPreferences(preferences)
    
    // API Call: Save preferences
    const response = await fetch('/api/user/preferences', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify(preferences)
    })
    
    if (response.ok) {
      showToast('Preferences saved', 'success')
    } else {
      // Revert optimistic update
      revertLocalPreferences()
      throw new Error('Failed to save preferences')
    }
    
  } catch (error) {
    console.error('Preferences update failed:', error)
    showToast('Failed to save preferences', 'error')
  }
}
```

### **Board Theme Management**
```typescript
// BoardSettingsPage.tsx - Board customization
const loadBoardThemes = async () => {
  try {
    const [boardThemesResponse, pieceThemesResponse] = await Promise.all([
      fetch('/api/settings/board-themes'),
      fetch('/api/settings/piece-themes')
    ])
    
    const boardThemes = await boardThemesResponse.json()
    const pieceThemes = await pieceThemesResponse.json()
    
    setBoardCustomization({
      availableBoardThemes: boardThemes.data,
      availablePieceThemes: pieceThemes.data,
      isLoading: false
    })
    
  } catch (error) {
    console.error('Failed to load board themes:', error)
    showToast('Failed to load customization options', 'error')
  }
}
```

## 🔄 Error Handling & Retry Logic

### **Network Error Recovery**
```typescript
// ApiService.ts - Centralized error handling
const apiCall = async (url: string, options: RequestInit, retries = 3): Promise<any> => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getToken()}`,
          ...options.headers
        }
      })
      
      if (response.status === 401) {
        // Token expired - attempt refresh
        const refreshSuccess = await refreshAuthToken()
        if (refreshSuccess && attempt < retries) {
          continue // Retry with new token
        } else {
          // Refresh failed - redirect to login
          logout()
          navigate('/login')
          return null
        }
      }
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error(`API call failed (attempt ${attempt}/${retries}):`, error)
      
      if (attempt === retries) {
        // Final attempt failed
        if (isNetworkError(error)) {
          showNetworkErrorDialog()
        }
        throw error
      }
      
      // Exponential backoff before retry
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000))
    }
  }
}
```

### **Token Refresh Flow**
```typescript
// AuthService.ts - Token management
const refreshAuthToken = async (): Promise<boolean> => {
  try {
    const refreshToken = localStorage.getItem('refreshToken')
    if (!refreshToken) return false
    
    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refreshToken })
    })
    
    if (response.ok) {
      const data = await response.json()
      
      // Update stored tokens
      localStorage.setItem('token', data.token)
      localStorage.setItem('refreshToken', data.refreshToken)
      
      return true
    } else {
      // Refresh failed - clear tokens
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      return false
    }
    
  } catch (error) {
    console.error('Token refresh failed:', error)
    return false
  }
}
```

## 📊 Performance Optimization

### **Data Caching Strategy**
```typescript
// CacheService.ts - Client-side caching
const cache = new Map<string, CachedData>()

const getCachedData = (key: string, maxAge = 300000): any => { // 5 minutes default
  const cached = cache.get(key)
  if (cached && Date.now() - cached.timestamp < maxAge) {
    return cached.data
  }
  return null
}

const setCachedData = (key: string, data: any): void => {
  cache.set(key, {
    data,
    timestamp: Date.now()
  })
}

// Usage in components
const loadDashboardStats = async () => {
  const cacheKey = 'dashboard-stats'
  const cached = getCachedData(cacheKey)
  
  if (cached) {
    setStats(cached)
    return
  }
  
  const response = await fetch('/api/user/dashboard-stats')
  const data = await response.json()
  
  setCachedData(cacheKey, data)
  setStats(data)
}
```

### **Optimistic Updates Pattern**
```typescript
// OptimisticUpdate.ts - UI responsiveness
const optimisticUpdate = async <T>(
  updateFn: () => void,
  revertFn: () => void,
  apiCall: () => Promise<T>
): Promise<T> => {
  // Apply optimistic update immediately
  updateFn()
  
  try {
    // Execute API call
    const result = await apiCall()
    return result
  } catch (error) {
    // Revert on failure
    revertFn()
    throw error
  }
}

// Usage example
const makeMove = async (move: ChessMove) => {
  return optimisticUpdate(
    () => updateBoardPosition(move),        // Optimistic update
    () => revertBoardPosition(),            // Revert function
    () => submitMoveToAPI(move)             // API call
  )
}
```

## 📱 Real-time Updates (Future Enhancement)

### **WebSocket Integration**
```typescript
// WebSocketService.ts - Real-time features (future)
const useWebSocket = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null)
  
  useEffect(() => {
    const ws = new WebSocket('wss://api.chess-training.com/ws')
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setSocket(ws)
    }
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data)
      handleRealtimeMessage(message)
    }
    
    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setSocket(null)
      // Implement reconnection logic
    }
    
    return () => ws.close()
  }, [])
  
  const handleRealtimeMessage = (message: RealtimeMessage) => {
    switch (message.type) {
      case 'achievement_unlocked':
        showAchievementNotification(message.data)
        break
      case 'rating_updated':
        updateUserRating(message.data)
        break
      case 'puzzle_streak_milestone':
        showStreakMilestone(message.data)
        break
    }
  }
}
```

## 🎯 API Call Summary & Performance Metrics

### **API Call Frequency by Feature**

#### **High Frequency (Real-time)**:
- `POST /api/games/:id/move` - Every chess move (2-100+ calls per game)
- `GET /api/puzzles/next` - Every puzzle (1-20+ calls per session)
- `POST /api/puzzles/:id/solve` - Every puzzle attempt (1-5 calls per puzzle)

#### **Medium Frequency (Session-based)**:
- `POST /api/games/create` - New games (1-10 calls per session)
- `POST /api/analysis/analyze` - Position analysis (1-20 calls per session)
- `GET /api/game-reviews/:id` - Game reviews (1-5 calls per session)

#### **Low Frequency (Periodic)**:
- `GET /api/user/dashboard-stats` - Dashboard loads (1-3 calls per session)
- `PUT /api/user/progress` - Progress updates (background, after games/puzzles)
- `POST /api/achievements/check` - Achievement checks (background, triggered)

### **Performance Targets**:
- **Move submission**: < 200ms response time
- **Puzzle loading**: < 300ms response time
- **Dashboard load**: < 500ms for complete data
- **Analysis requests**: < 2s for engine analysis
- **Cache hit rate**: > 80% for repeated position analysis

### **Error Recovery Times**:
- **Network errors**: 3 retry attempts with exponential backoff
- **Token refresh**: Automatic, transparent to user
- **Move conflicts**: Immediate reversion with user feedback
- **Analysis failures**: Graceful degradation to cached data

---

**Status**: 📋 **IMPLEMENTATION READY** - Complete API integration specification  
**Next Steps**: Begin frontend implementation with exact API integration patterns  
**Performance**: Optimized for responsiveness with caching and optimistic updates