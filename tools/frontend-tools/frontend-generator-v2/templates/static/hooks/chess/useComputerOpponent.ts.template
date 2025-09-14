// useComputerOpponent.ts - Computer opponent specific hook  
// Phase 7: State Management Hooks - Computer opponent state management
import { useState, useCallback, useRef, useEffect } from 'react';
import { ComputerOpponentService } from '../../services/chess/ComputerOpponentService';
import { StockfishEngineClient } from '../../services/clients/StockfishEngineClient';
import type { 
  ComputerDifficulty,
  ComputerOpponentConfig,
  ComputerThinkingState,
  ComputerOpponentStatus,
  ComputerMoveRequest,
  ComputerMoveResult
} from '../../types';

export const useComputerOpponent = (initialDifficulty: ComputerDifficulty = 5) => {
  // Service instances (stable across renders)
  const computerServiceRef = useRef<ComputerOpponentService | null>(null);
  const engineClientRef = useRef<StockfishEngineClient | null>(null);
  
  // Computer state
  const [difficulty, setDifficulty] = useState<ComputerDifficulty>(initialDifficulty);
  const [thinkingState, setThinkingState] = useState<ComputerThinkingState>({ isThinking: false });
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [engineStats, setEngineStats] = useState<any>(null);

  // Initialize services
  useEffect(() => {
    const initializeServices = async () => {
      try {
        console.log('🤖 [USE COMPUTER OPPONENT] Initializing computer services...');
        
        // Initialize services
        computerServiceRef.current = new ComputerOpponentService(initialDifficulty);
        engineClientRef.current = new StockfishEngineClient();
        
        // Wait for engine readiness
        await engineClientRef.current.waitForReady();
        
        // Set initial difficulty
        await engineClientRef.current.setDifficulty(initialDifficulty);
        
        setIsReady(true);
        setEngineStats(engineClientRef.current.getStats());
        
        console.log('✅ [USE COMPUTER OPPONENT] Computer services ready');
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to initialize computer opponent';
        console.error('❌ [USE COMPUTER OPPONENT] Initialization error:', errorMessage);
        setError(errorMessage);
        setIsReady(false);
      }
    };

    initializeServices();
  }, [initialDifficulty]);

  // Request computer move
  const requestMove = useCallback(async (fen: string, timeLimit?: number): Promise<ComputerMoveResult> => {
    if (!computerServiceRef.current || !engineClientRef.current || !isReady) {
      return {
        move: '',
        success: false,
        error: 'Computer opponent not ready'
      };
    }

    try {
      console.log('🎯 [USE COMPUTER OPPONENT] Requesting move...', { difficulty, timeLimit });
      
      // Create thinking state
      const expectedDuration = computerServiceRef.current.generateThinkingDelay(difficulty);
      setThinkingState({
        isThinking: true,
        startTime: Date.now(),
        expectedDuration: timeLimit || expectedDuration
      });

      // Create move request
      const request: ComputerMoveRequest = {
        fen,
        difficulty,
        timeLimit: timeLimit || expectedDuration
      };

      // Request move through engine client
      const result = await engineClientRef.current.requestMove(request);
      
      // Update stats
      if (result.success) {
        const thinkingTime = Date.now() - (thinkingState.startTime || Date.now());
        computerServiceRef.current.updateThinkingStats(thinkingTime);
        setEngineStats(engineClientRef.current.getStats());
      }

      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get computer move';
      console.error('❌ [USE COMPUTER OPPONENT] Move request error:', errorMessage);
      
      return {
        move: '',
        success: false,
        error: errorMessage
      };
    } finally {
      // Clear thinking state
      setThinkingState({ isThinking: false });
    }
  }, [difficulty, thinkingState.startTime, isReady]);

  // Update difficulty level
  const updateDifficulty = useCallback(async (newDifficulty: ComputerDifficulty) => {
    if (!computerServiceRef.current || !engineClientRef.current) {
      console.warn('⚠️ [USE COMPUTER OPPONENT] Services not ready for difficulty update');
      return;
    }

    try {
      console.log('🔧 [USE COMPUTER OPPONENT] Updating difficulty:', newDifficulty);
      
      // Update both services
      computerServiceRef.current.setDifficulty(newDifficulty);
      await engineClientRef.current.setDifficulty(newDifficulty);
      
      setDifficulty(newDifficulty);
      setError(null);
      
      console.log('✅ [USE COMPUTER OPPONENT] Difficulty updated successfully');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update difficulty';
      console.error('❌ [USE COMPUTER OPPONENT] Difficulty update error:', errorMessage);
      setError(errorMessage);
    }
  }, []);

  // Get current difficulty configuration
  const getDifficultyConfig = useCallback((): ComputerOpponentConfig | null => {
    if (!computerServiceRef.current) {
      return null;
    }
    
    return computerServiceRef.current.getDifficultyConfig(difficulty);
  }, [difficulty]);

  // Get difficulty description
  const getDifficultyDescription = useCallback((): string => {
    if (!computerServiceRef.current) {
      return `Level ${difficulty}`;
    }
    
    return computerServiceRef.current.formatComputerStatus(false, difficulty);
  }, [difficulty]);

  // Get all available difficulty levels
  const getAllDifficultyLevels = useCallback(() => {
    if (!computerServiceRef.current) {
      return [];
    }
    
    return computerServiceRef.current.getAllDifficultyLevels();
  }, []);

  // Get computer status for display
  const getStatus = useCallback((): ComputerOpponentStatus => {
    const stats = computerServiceRef.current?.getStats();
    
    return {
      isReady,
      difficulty,
      thinking: thinkingState,
      error: error ?? undefined,
      stats: stats ? {
        movesCalculated: stats.movesCalculated,
        averageThinkingTime: stats.averageThinkingTime,
        currentSearchDepth: stats.currentSearchDepth
      } : undefined
    };
  }, [isReady, difficulty, thinkingState, error]);

  // Format thinking time for display
  const formatThinkingTime = useCallback((milliseconds: number): string => {
    if (milliseconds < 1000) {
      return `${milliseconds}ms`;
    }
    
    const seconds = (milliseconds / 1000).toFixed(1);
    return `${seconds}s`;
  }, []);

  // Calculate thinking progress (0-100)
  const getThinkingProgress = useCallback((): number => {
    if (!thinkingState.isThinking || !thinkingState.startTime || !thinkingState.expectedDuration) {
      return 0;
    }
    
    const elapsed = Date.now() - thinkingState.startTime;
    const progress = Math.min((elapsed / thinkingState.expectedDuration) * 100, 95); // Cap at 95%
    
    return Math.round(progress);
  }, [thinkingState]);

  // Get personality traits for current difficulty
  const getPersonalityTraits = useCallback(() => {
    if (!computerServiceRef.current) {
      return null;
    }
    
    return computerServiceRef.current.getPersonalityTraits(difficulty);
  }, [difficulty]);

  // Evaluate a position (useful for analysis)
  const evaluatePosition = useCallback(async (fen: string, depth?: number): Promise<number> => {
    if (!engineClientRef.current || !isReady) {
      console.warn('⚠️ [USE COMPUTER OPPONENT] Engine not ready for position evaluation');
      return 0;
    }

    try {
      return await engineClientRef.current.evaluatePosition(fen, depth);
    } catch (err) {
      console.error('❌ [USE COMPUTER OPPONENT] Position evaluation error:', err);
      return 0;
    }
  }, [isReady]);

  // Reset computer opponent stats
  const resetStats = useCallback(() => {
    if (computerServiceRef.current) {
      computerServiceRef.current.resetStats();
      setEngineStats(engineClientRef.current?.getStats() || null);
    }
  }, []);

  // Check if computer should resign (for lower difficulty levels)
  const shouldResign = useCallback((evaluation: number): boolean => {
    if (!computerServiceRef.current) {
      return false;
    }
    
    return computerServiceRef.current.shouldResign(evaluation, difficulty);
  }, [difficulty]);

  // Public interface
  return {
    // Core state
    isReady,
    difficulty,
    thinkingState,
    error,
    engineStats,
    
    // Actions
    requestMove,
    updateDifficulty,
    evaluatePosition,
    resetStats,
    
    // Information getters
    getDifficultyConfig,
    getDifficultyDescription,
    getAllDifficultyLevels,
    getStatus,
    getPersonalityTraits,
    
    // Helper functions
    formatThinkingTime,
    getThinkingProgress,
    shouldResign,
    
    // Service access for advanced usage
    computerService: computerServiceRef.current,
    engineClient: engineClientRef.current
  };
};