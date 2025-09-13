// useChessGame.ts - Main chess game state management
import { useState, useEffect, useRef, useCallback } from 'react';
import { ChessGameService } from '../../services/chess/ChessGameService';
import type { ChessGameState, ChessMoveInput, PieceType } from '../../types/chess/chess.types';

export interface UseChessGameHook {
  gameState: ChessGameState | null;
  isLoading: boolean;
  makeMove: (from: string, to: string, promotion?: PieceType) => Promise<boolean>;
  undoMove: () => boolean;
  resetGame: (fen?: string) => void;
  getValidMoves: (square?: string) => string[];
  isGameOver: boolean;
  error: string | null;
}

export const useChessGame = (initialFen?: string): UseChessGameHook => {
  const [gameState, setGameState] = useState<ChessGameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const gameServiceRef = useRef<ChessGameService>(new ChessGameService());

  // Initialize game service
  useEffect(() => {
    try {
      gameServiceRef.current = new ChessGameService(initialFen);
      setGameState(gameServiceRef.current.getCurrentState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize game');
    } finally {
      setIsLoading(false);
    }
  }, [initialFen]);

  const makeMove = useCallback(async (
    from: string, 
    to: string, 
    promotion?: PieceType
  ): Promise<boolean> => {
    if (!gameServiceRef.current) {
      setError('Game not initialized');
      return false;
    }

    try {
      setError(null);
      const moveInput: ChessMoveInput = { from, to, promotion };
      const result = gameServiceRef.current.makeMove(moveInput);
      
      if (result.success) {
        setGameState(result.gameState);
        return true;
      } else {
        setError(result.error || 'Invalid move');
        return false;
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Move failed';
      setError(errorMessage);
      return false;
    }
  }, []);

  const undoMove = useCallback((): boolean => {
    if (!gameServiceRef.current) {
      setError('Game not initialized');
      return false;
    }

    try {
      setError(null);
      const success = gameServiceRef.current.undoLastMove();
      
      if (success) {
        setGameState(gameServiceRef.current.getCurrentState());
        return true;
      }
      
      return false;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Undo failed');
      return false;
    }
  }, []);

  const resetGame = useCallback((fen?: string): void => {
    if (!gameServiceRef.current) {
      return;
    }

    try {
      setError(null);
      gameServiceRef.current.resetGame(fen);
      setGameState(gameServiceRef.current.getCurrentState());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Reset failed');
    }
  }, []);

  const getValidMoves = useCallback((square?: string): string[] => {
    if (!gameServiceRef.current) {
      return [];
    }

    try {
      return gameServiceRef.current.getValidMoves(square);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get valid moves');
      return [];
    }
  }, []);

  return {
    gameState,
    isLoading,
    makeMove,
    undoMove,
    resetGame,
    getValidMoves,
    isGameOver: gameState?.isGameOver || false,
    error
  };
};