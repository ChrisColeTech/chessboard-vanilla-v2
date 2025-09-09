// usePlayGame.ts - Main play game state management hook
// Phase 7: State Management Hooks - React state bridge to services
import { useState, useCallback, useRef, useEffect } from 'react';
import { PlayGameService } from '../../services/chess/PlayGameService';
import { StockfishEngineClient } from '../../services/clients/StockfishEngineClient';
import { useChessAudio } from '../../services/audio/audioService';
import type { 
  ChessGameState,
  PieceType,
  PieceColor,
  ComputerDifficulty,
  PlayGameState
} from '../../types';
import { parseEngineMove } from '../../utils/chess/computer-chess.utils';

export const usePlayGame = (initialPlayerColor: PieceColor = 'white') => {
  // Service instances (stable across renders)
  const playGameServiceRef = useRef<PlayGameService | null>(null);
  const engineClientRef = useRef<StockfishEngineClient | null>(null);
  
  // Audio integration following DragTestPage pattern
  const { playMove, playError, playCheck, playGameStart, playGameEnd } = useChessAudio();

  // UI state only - services handle business logic
  const [gameState, setGameState] = useState<ChessGameState | null>(null);
  const [isComputerThinking, setIsComputerThinking] = useState(false);
  const [skillLevel, setSkillLevel] = useState<ComputerDifficulty>(5);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize services on first mount
  useEffect(() => {
    const initializeServices = async () => {
      try {
        console.log('🎮 [USE PLAY GAME] Initializing services...');
        
        // Initialize services
        playGameServiceRef.current = new PlayGameService(initialPlayerColor);
        engineClientRef.current = new StockfishEngineClient();
        
        // Wait for engine to be ready
        await engineClientRef.current.waitForReady();
        
        // Get initial game state
        const initialState = playGameServiceRef.current.getCurrentState();
        setGameState(initialState);
        
        setIsLoading(false);
        console.log('✅ [USE PLAY GAME] Services initialized successfully');
        
        // Play game start sound
        playGameStart();
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to initialize game services';
        console.error('❌ [USE PLAY GAME] Initialization error:', errorMessage);
        setError(errorMessage);
        setIsLoading(false);
      }
    };

    initializeServices();
  }, [initialPlayerColor, playGameStart]);

  // Computer move handler
  const handleComputerTurn = useCallback(async () => {
    if (!playGameServiceRef.current || !engineClientRef.current) {
      console.error('❌ [USE PLAY GAME] Services not initialized');
      return;
    }

    setIsComputerThinking(true);
    setError(null);

    try {
      console.log('🤖 [USE PLAY GAME] Computer turn starting...');
      
      const currentState = playGameServiceRef.current.getCurrentState();
      
      // Update thinking state in service
      playGameServiceRef.current.setThinkingState({
        isThinking: true,
        startTime: Date.now()
      });
      
      // Request computer move
      const computerMove = await engineClientRef.current.getBestMove(
        currentState.fen, 
        skillLevel
      );
      
      if (computerMove) {
        // Parse UCI format (e.g., "e2e4" or "e7e8q")
        const moveComponents = parseEngineMove(computerMove);
        const { from, to, promotion } = moveComponents;
        
        console.log('🎯 [USE PLAY GAME] Computer move received:', { from, to, promotion });
        
        // Execute move through service
        const result = playGameServiceRef.current.makeComputerMove(
          from, 
          to, 
          promotion as PieceType
        );
        
        if (result.success && result.gameState) {
          // Update UI state
          setGameState(result.gameState);
          
          // Play appropriate sound following DragTestPage pattern
          if (result.gameState.isCheckmate) {
            playGameEnd();
          } else if (result.gameState.isCheck) {
            playCheck();
          } else {
            // Check if move was a capture
            const wasCapture = !!result.move?.capturedPiece;
            playMove(wasCapture);
          }
          
          console.log('✅ [USE PLAY GAME] Computer move executed successfully');
        } else {
          setError(result.error || 'Computer move failed');
          playError();
        }
      } else {
        setError('Computer failed to generate move');
        playError();
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Computer move failed';
      console.error('❌ [USE PLAY GAME] Computer move error:', errorMessage);
      setError(errorMessage);
      playError();
    } finally {
      setIsComputerThinking(false);
      
      // Clear thinking state in service
      if (playGameServiceRef.current) {
        playGameServiceRef.current.setThinkingState({ isThinking: false });
      }
    }
  }, [skillLevel, playMove, playCheck, playGameStart, playGameEnd, playError]);

  // Player move handler
  const makeMove = useCallback(async (from: string, to: string, promotion?: PieceType): Promise<boolean> => {
    if (!playGameServiceRef.current) {
      console.error('❌ [USE PLAY GAME] Service not initialized');
      return false;
    }

    try {
      setError(null);
      console.log('🎯 [USE PLAY GAME] Player move attempt:', { from, to, promotion });
      
      // Execute move through service (includes turn validation)
      const result = playGameServiceRef.current.makePlayerMove(from, to, promotion);
      
      if (!result.success) {
        setError(result.error || 'Invalid move');
        playError();
        return false;
      }

      // Update UI state
      setGameState(result.gameState!);

      // Play appropriate sound following DragTestPage pattern
      if (result.gameState!.isCheckmate) {
        playGameEnd();
      } else if (result.gameState!.isCheck) {
        playCheck();
      } else {
        // Check if move was a capture
        const wasCapture = !!result.move?.capturedPiece;
        playMove(wasCapture);
      }

      console.log('✅ [USE PLAY GAME] Player move successful');

      // Handle computer turn if needed (don't await - let it run async)
      if (playGameServiceRef.current.shouldComputerMove()) {
        // Small delay for better UX
        setTimeout(() => {
          handleComputerTurn();
        }, 300);
      }

      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Move failed';
      console.error('❌ [USE PLAY GAME] Player move error:', errorMessage);
      setError(errorMessage);
      playError();
      return false;
    }
  }, [handleComputerTurn, playMove, playCheck, playGameEnd, playError]);

  // Update skill level
  const updateSkillLevel = useCallback(async (level: ComputerDifficulty) => {
    if (!engineClientRef.current || !playGameServiceRef.current) {
      return;
    }

    try {
      console.log('🔧 [USE PLAY GAME] Updating skill level:', level);
      
      await engineClientRef.current.setDifficulty(level);
      playGameServiceRef.current.updateDifficulty(level);
      setSkillLevel(level);
      
      console.log('✅ [USE PLAY GAME] Skill level updated');
    } catch (err) {
      console.error('❌ [USE PLAY GAME] Error updating skill level:', err);
      setError('Failed to update difficulty level');
    }
  }, []);

  // Reset game
  const resetGame = useCallback((playerColor?: PieceColor) => {
    if (!playGameServiceRef.current) {
      return;
    }

    try {
      console.log('🔄 [USE PLAY GAME] Resetting game...');
      
      // Reset service state
      playGameServiceRef.current.resetGame();
      
      // Handle color change if specified
      if (playerColor && playerColor !== playGameServiceRef.current.getPlayerColor()) {
        playGameServiceRef.current.flipColors();
      }
      
      // Update UI state
      const newGameState = playGameServiceRef.current.getCurrentState();
      setGameState(newGameState);
      setIsComputerThinking(false);
      setError(null);
      
      // Play game start sound
      playGameStart();
      
      console.log('✅ [USE PLAY GAME] Game reset successfully');
    } catch (err) {
      console.error('❌ [USE PLAY GAME] Error resetting game:', err);
      setError('Failed to reset game');
    }
  }, [playGameStart]);

  // Get valid moves
  const getValidMoves = useCallback((square?: string): string[] => {
    if (!playGameServiceRef.current) {
      return [];
    }
    
    return playGameServiceRef.current.getValidMoves(square);
  }, []);

  // Get play game state
  const getPlayGameState = useCallback((): PlayGameState | null => {
    if (!playGameServiceRef.current) {
      return null;
    }
    
    return playGameServiceRef.current.getPlayGameState();
  }, []);

  // Public interface
  return {
    // Core game state
    gameState,
    isLoading,
    error,
    
    // Computer state
    isComputerThinking,
    skillLevel,
    
    // Game state helpers
    isPlayerTurn: playGameServiceRef.current?.isPlayerTurn() ?? false,
    isComputerTurn: playGameServiceRef.current?.isComputerTurn() ?? false,
    canPlayerMakeMove: playGameServiceRef.current?.canPlayerMakeMove() ?? false,
    
    // Actions
    makeMove,
    updateSkillLevel,
    resetGame,
    getValidMoves,
    getPlayGameState,
    
    // Service access for advanced usage
    playGameService: playGameServiceRef.current,
    engineClient: engineClientRef.current
  };
};