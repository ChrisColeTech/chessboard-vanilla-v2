// Hook for puzzle service operations
import { useCallback, useEffect } from 'react';
import { usePuzzleStore } from '../../stores/puzzleStore';
import { puzzleApiService } from '../../services/api/puzzleApiService';
import type { PuzzleFilters } from '../../types/puzzle.types';

export const usePuzzleService = () => {
  const {
    setCurrentPuzzle,
    setLoading,
    setError,
    setCurrentHint,
    setAvailableThemes,
    filters,
    initializePuzzleProgress,
    resetPuzzleProgress
  } = usePuzzleStore();

  // Load available themes on mount
  useEffect(() => {
    const loadThemes = async () => {
      const themes = await puzzleApiService.getAvailableThemes();
      setAvailableThemes(themes);
    };
    loadThemes();
  }, [setAvailableThemes]);

  /**
   * Load a random puzzle based on current filters
   */
  const loadRandomPuzzle = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Add a small delay to show loading state
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const puzzle = await puzzleApiService.getRandomPuzzle(filters);
      
      if (puzzle) {
        setCurrentPuzzle(puzzle);
        initializePuzzleProgress(puzzle);
      } else {
        setError('No puzzles found matching your criteria');
      }
    } catch (error) {
      console.error('Failed to load puzzle:', error);
      setError('Failed to load puzzle');
    } finally {
      setLoading(false);
    }
  }, [filters, setCurrentPuzzle, setLoading, setError, initializePuzzleProgress]);

  /**
   * Load a specific puzzle by ID
   */
  const loadPuzzleById = useCallback(async (puzzleId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const puzzle = await puzzleApiService.getPuzzleById(puzzleId);
      
      if (puzzle) {
        setCurrentPuzzle(puzzle);
        initializePuzzleProgress(puzzle);
      } else {
        setError('Puzzle not found');
      }
    } catch (error) {
      console.error('Failed to load puzzle:', error);
      setError('Failed to load puzzle');
    } finally {
      setLoading(false);
    }
  }, [setCurrentPuzzle, setLoading, setError, initializePuzzleProgress]);

  /**
   * Load multiple puzzles with filters
   */
  const loadPuzzles = useCallback(async (customFilters?: PuzzleFilters) => {
    setLoading(true);
    setError(null);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const puzzles = await puzzleApiService.getPuzzles(customFilters || filters);
      return puzzles;
    } catch (error) {
      console.error('Failed to load puzzles:', error);
      setError('Failed to load puzzles');
      return [];
    } finally {
      setLoading(false);
    }
  }, [filters, setLoading, setError]);

  /**
   * Search puzzles by description
   */
  const searchPuzzles = useCallback(async (searchTerm: string, limit = 10) => {
    setLoading(true);
    setError(null);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const puzzles = await puzzleApiService.searchPuzzles(searchTerm, limit);
      return puzzles;
    } catch (error) {
      console.error('Failed to search puzzles:', error);
      setError('Failed to search puzzles');
      return [];
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError]);

  /**
   * Get database statistics
   */
  const getPuzzleStats = useCallback(async () => {
    try {
      return await puzzleApiService.getPuzzleStats();
    } catch (error) {
      console.error('Failed to get puzzle stats:', error);
      return null;
    }
  }, []);

  /**
   * Start a new puzzle session
   */
  const startNewPuzzle = useCallback(async () => {
    resetPuzzleProgress();
    await loadRandomPuzzle();
  }, [resetPuzzleProgress, loadRandomPuzzle]);

  /**
   * Get the next hint for the current puzzle
   */
  const getHint = useCallback(() => {
    const { currentPuzzle, puzzleProgress, useHint } = usePuzzleStore.getState();
    
    if (!currentPuzzle || !puzzleProgress || puzzleProgress.isComplete) {
      setCurrentHint(null);
      return;
    }

    const currentMoveIndex = puzzleProgress.currentMove;
    const hint = currentPuzzle.solution_moves[currentMoveIndex];
    
    if (hint) {
      useHint();
      setCurrentHint(hint);
    } else {
      setCurrentHint(null);
    }
  }, [setCurrentHint]);

  return {
    // Core puzzle loading
    loadRandomPuzzle,
    loadPuzzleById,
    loadPuzzles,
    searchPuzzles,
    startNewPuzzle,
    
    // Utilities
    getPuzzleStats,
    getHint
  };
};