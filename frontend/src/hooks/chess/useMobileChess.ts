// useMobileChess.ts - Mobile-optimized chess game state management
// Phase 4: Mobile Chess Interaction Hooks - State management hook with mobile optimizations

import { useState, useEffect, useRef, useCallback } from 'react';
import { MobileChessGameService } from '../../services/chess/MobileChessGameService';
import type { 
  MobileChessGameState, 
  MobileChessMoveResult,
  ChessMoveInput, 
  ChessPosition,
  PieceType,
  MobileChessConfig,
  MobileChessInteraction 
} from '../../types';

export interface UseMobileChessHook {
  gameState: MobileChessGameState | null;
  isLoading: boolean;
  makeMove: (from: ChessPosition, to: ChessPosition, promotion?: PieceType) => Promise<MobileChessMoveResult>;
  selectSquare: (position: ChessPosition) => void;
  getValidMoves: (position: ChessPosition) => ChessPosition[];
  recordInteraction: (interaction: MobileChessInteraction) => void;
  updateConfig: (config: Partial<MobileChessConfig>) => void;
  resetGame: (fen?: string) => void;
  flipBoard: () => void;
  loadFen: (fen: string) => boolean;
  getFen: () => string;
  getPgn: () => string;
  isGameOver: boolean;
  isPlayerTurn: (playerColor: 'white' | 'black') => boolean;
  error: string | null;
}

export const useMobileChess = (
  initialFen?: string,
  mobileConfig: Partial<MobileChessConfig> = {}
): UseMobileChessHook => {
  const [gameState, setGameState] = useState<MobileChessGameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const gameServiceRef = useRef<MobileChessGameService | null>(null);

  // Initialize mobile chess service
  useEffect(() => {
    try {
      gameServiceRef.current = new MobileChessGameService(initialFen, mobileConfig);
      setGameState(gameServiceRef.current.getMobileGameState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize mobile chess game');
    } finally {
      setIsLoading(false);
    }
  }, [initialFen, mobileConfig]);

  // Make a move with mobile-specific feedback
  const makeMove = useCallback(async (
    from: ChessPosition,
    to: ChessPosition,
    promotion?: PieceType
  ): Promise<MobileChessMoveResult> => {
    if (!gameServiceRef.current) {
      const errorResult: MobileChessMoveResult = {
        isValid: false,
        move: null,
        gameState: gameState!,
        error: 'Game not initialized',
        feedback: {
          playSuccessSound: false,
          playErrorSound: true,
          triggerHaptic: false,
          visualFeedback: 'error'
        }
      };
      setError('Game not initialized');
      return errorResult;
    }

    try {
      setError(null);
      const moveInput: ChessMoveInput = { from, to, promotion };
      const result = gameServiceRef.current.makeMobileMove(moveInput);
      
      if (result.isValid) {
        setGameState(result.gameState);
      } else {
        setError(result.error);
      }
      
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to make move';
      const errorResult: MobileChessMoveResult = {
        isValid: false,
        move: null,
        gameState: gameState!,
        error: errorMessage,
        feedback: {
          playSuccessSound: false,
          playErrorSound: true,
          triggerHaptic: false,
          visualFeedback: 'error'
        }
      };
      setError(errorMessage);
      return errorResult;
    }
  }, [gameState]);

  // Select a square (mobile tap-to-select)
  const selectSquare = useCallback((position: ChessPosition) => {
    if (!gameServiceRef.current) {
      setError('Game not initialized');
      return;
    }

    try {
      gameServiceRef.current.selectSquare(position);
      setGameState(gameServiceRef.current.getMobileGameState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to select square');
    }
  }, []);

  // Get valid moves for a position
  const getValidMoves = useCallback((position: ChessPosition): ChessPosition[] => {
    if (!gameServiceRef.current) {
      return [];
    }

    try {
      return gameServiceRef.current.getValidMoves(position);
    } catch (err) {
      console.warn('Error getting valid moves:', err);
      return [];
    }
  }, []);

  // Record mobile interaction for gesture recognition
  const recordInteraction = useCallback((interaction: MobileChessInteraction) => {
    if (!gameServiceRef.current) {
      return;
    }

    try {
      gameServiceRef.current.recordInteraction(interaction);
      setGameState(gameServiceRef.current.getMobileGameState());
    } catch (err) {
      console.warn('Error recording interaction:', err);
    }
  }, []);

  // Update mobile configuration
  const updateConfig = useCallback((config: Partial<MobileChessConfig>) => {
    if (!gameServiceRef.current) {
      return;
    }

    try {
      gameServiceRef.current.updateMobileConfig(config);
      setGameState(gameServiceRef.current.getMobileGameState());
    } catch (err) {
      console.warn('Error updating mobile config:', err);
    }
  }, []);

  // Reset game to initial state
  const resetGame = useCallback((fen?: string) => {
    if (!gameServiceRef.current) {
      return;
    }

    try {
      gameServiceRef.current.reset(fen);
      setGameState(gameServiceRef.current.getMobileGameState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset game');
    }
  }, []);

  // Flip board orientation
  const flipBoard = useCallback(() => {
    if (!gameServiceRef.current) {
      return;
    }

    try {
      gameServiceRef.current.flipBoard();
      setGameState(gameServiceRef.current.getMobileGameState());
    } catch (err) {
      console.warn('Error flipping board:', err);
    }
  }, []);

  // Load game from FEN string
  const loadFen = useCallback((fen: string): boolean => {
    if (!gameServiceRef.current) {
      setError('Game not initialized');
      return false;
    }

    try {
      const success = gameServiceRef.current.loadFen(fen);
      if (success) {
        setGameState(gameServiceRef.current.getMobileGameState());
        setError(null);
      } else {
        setError('Invalid FEN string');
      }
      return success;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load FEN');
      return false;
    }
  }, []);

  // Get current FEN string
  const getFen = useCallback((): string => {
    if (!gameServiceRef.current) {
      return '';
    }
    return gameServiceRef.current.getFen();
  }, []);

  // Get game PGN
  const getPgn = useCallback((): string => {
    if (!gameServiceRef.current) {
      return '';
    }
    return gameServiceRef.current.getPgn();
  }, []);

  // Check if it's player's turn
  const isPlayerTurn = useCallback((playerColor: 'white' | 'black'): boolean => {
    if (!gameServiceRef.current) {
      return false;
    }
    return gameServiceRef.current.isPlayerTurn(playerColor);
  }, []);

  // Computed properties
  const isGameOver = gameState?.isGameOver ?? false;

  return {
    gameState,
    isLoading,
    makeMove,
    selectSquare,
    getValidMoves,
    recordInteraction,
    updateConfig,
    resetGame,
    flipBoard,
    loadFen,
    getFen,
    getPgn,
    isGameOver,
    isPlayerTurn,
    error
  };
};