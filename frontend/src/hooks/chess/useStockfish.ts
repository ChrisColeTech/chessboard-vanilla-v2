// useStockfish.ts - Computer opponent integration
import { useState, useEffect, useRef, useCallback } from 'react';
import { getStockfishService } from '../../services/chess/stockfish-singleton';
import type { StockfishHandlers } from '../../services/chess/StockfishService';

export interface UseStockfishHook {
  isReady: boolean;
  isThinking: boolean;
  skillLevel: number;
  setSkillLevel: (level: number) => void;
  requestMove: (fen: string, timeLimit?: number) => Promise<string | null>;
  evaluatePosition: (fen: string) => Promise<number>;
  error: string | null;
}

export const useStockfish = (): UseStockfishHook => {
  const [isReady, setIsReady] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [skillLevel, setSkillLevelState] = useState(8);
  const [error, setError] = useState<string | null>(null);
  const stockfishRef = useRef<ReturnType<typeof getStockfishService> | undefined>(undefined);
  
  // Mount guard for React Strict Mode
  const mountedOnceRef = useRef(false);

  // Get singleton service and set up handlers
  useEffect(() => {
    // Mount guard for React Strict Mode - prevent double initialization in dev
    if (import.meta.env.DEV && mountedOnceRef.current) {
      console.log('🔄 [STOCKFISH] Strict Mode double-mount detected, skipping initialization');
      return;
    }
    mountedOnceRef.current = true;

    try {
      console.log('🚀 [STOCKFISH] Getting singleton StockfishService');
      const service = getStockfishService();
      stockfishRef.current = service;
      
      // Always rebind handlers on mount (HMR safety)
      const handlers: StockfishHandlers = {
        onBestMove: (move: string) => {
          console.log('♟️ [HANDLER] Received best move:', move);
        },
        onInfo: (info: string) => {
          console.log('📊 [HANDLER] Engine info:', info);
        },
        onError: (error: string) => {
          console.error('❌ [HANDLER] Engine error:', error);
          setError(error);
        }
      };
      
      service.setHandlers(handlers);
      
      // Poll for readiness (handles both fresh init and HMR)
      const checkReady = setInterval(() => {
        if (service.isEngineReady()) {
          setIsReady(true);
          clearInterval(checkReady);
        }
      }, 100);

      // Cleanup timeout
      const timeout = setTimeout(() => {
        clearInterval(checkReady);
        if (!service.isEngineReady()) {
          setError('Stockfish initialization timeout');
        }
      }, 5000);

      return () => {
        clearInterval(checkReady);
        clearTimeout(timeout);
      };
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize Stockfish');
    }
  }, []); // No dependencies - always run on mount

  // Cleanup on unmount - only destroy in production
  useEffect(() => {
    return () => {
      if (stockfishRef.current) {
        console.log('🔄 [STOCKFISH] Hook cleanup - clearing handlers');
        stockfishRef.current.clearHandlers();
        
        // Only destroy in production
        if (import.meta.env.PROD) {
          console.log('🔥 [STOCKFISH] Production cleanup - destroying service');
          stockfishRef.current.destroy();
        } else {
          console.log('🔄 [STOCKFISH] Dev cleanup - keeping service alive for HMR');
        }
      }
    };
  }, []);

  const setSkillLevel = useCallback(async (level: number): Promise<void> => {
    if (!stockfishRef.current || !isReady) {
      setError('Stockfish not ready');
      return;
    }

    try {
      setError(null);
      await stockfishRef.current.setSkillLevel(level);
      setSkillLevelState(level);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to set skill level');
    }
  }, [isReady]);

  const requestMove = useCallback(async (
    fen: string, 
    timeLimit: number = 1000
  ): Promise<string | null> => {
    if (!stockfishRef.current || !isReady) {
      setError('Stockfish not ready');
      return null;
    }

    setError(null);
    setIsThinking(true);

    try {
      console.log('🎯 [STOCKFISH] Requesting move (service has single-flight protection)');
      // Service-level single-flight protection handles duplicates
      const move = await stockfishRef.current.getBestMoveWithPosition(fen, skillLevel, timeLimit);
      
      console.log(`✅ [STOCKFISH] Received move: ${move}`);
      return move;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get computer move');
      return null;
    } finally {
      setIsThinking(false);
    }
  }, [isReady, skillLevel]);

  const evaluatePosition = useCallback(async (fen: string): Promise<number> => {
    if (!stockfishRef.current || !isReady) {
      setError('Stockfish not ready');
      return 0;
    }

    try {
      setError(null);
      return await stockfishRef.current.evaluatePosition(fen);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to evaluate position');
      return 0;
    }
  }, [isReady]);

  return {
    isReady,
    isThinking,
    skillLevel,
    setSkillLevel,
    requestMove,
    evaluatePosition,
    error
  };
};