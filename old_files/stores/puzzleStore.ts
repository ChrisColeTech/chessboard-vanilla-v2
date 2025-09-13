// Zustand store for puzzle state management
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { Puzzle, PuzzleProgress, PuzzleFilters, PuzzleStats } from '../types/puzzle.types';

interface PuzzleStore {
  // Current puzzle state
  currentPuzzle: Puzzle | null;
  puzzleProgress: PuzzleProgress | null;
  isLoading: boolean;
  error: string | null;
  currentHint: string | null;

  // Puzzle collection state
  availableThemes: string[];
  filters: PuzzleFilters;
  stats: PuzzleStats | null;

  // Actions
  setCurrentPuzzle: (puzzle: Puzzle | null) => void;
  setPuzzleProgress: (progress: PuzzleProgress | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setCurrentHint: (hint: string | null) => void;
  setAvailableThemes: (themes: string[]) => void;
  setFilters: (filters: Partial<PuzzleFilters>) => void;
  setStats: (stats: PuzzleStats | null) => void;

  // Puzzle progress actions
  initializePuzzleProgress: (puzzle: Puzzle) => void;
  addPlayerMove: (move: string) => void;
  useHint: () => void;
  markPuzzleComplete: (correct: boolean) => void;
  resetPuzzleProgress: () => void;

  // Filter helpers
  updateRatingRange: (minRating: number, maxRating: number) => void;
  toggleTheme: (theme: string) => void;
  resetFilters: () => void;
}

const initialProgress = (): PuzzleProgress => ({
  currentMove: 0,
  playerMoves: [],
  isCorrect: undefined,
  isComplete: false,
  hintsUsed: 0,
  startTime: Date.now()
});

const defaultFilters: PuzzleFilters = {
  minRating: 1000,
  maxRating: 2000,
  themes: [],
  limit: 10,
  offset: 0
};

export const usePuzzleStore = create<PuzzleStore>()(
  devtools(
    (set, get) => ({
      // Initial state
      currentPuzzle: null,
      puzzleProgress: null,
      isLoading: false,
      error: null,
      currentHint: null,
      availableThemes: [],
      filters: defaultFilters,
      stats: null,

      // Basic setters
      setCurrentPuzzle: (puzzle) => set({ currentPuzzle: puzzle }),
      setPuzzleProgress: (progress) => set({ puzzleProgress: progress }),
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),
      setCurrentHint: (hint) => set({ currentHint: hint }),
      setAvailableThemes: (themes) => set({ availableThemes: themes }),
      setFilters: (newFilters) => set({ 
        filters: { ...get().filters, ...newFilters } 
      }),
      setStats: (stats) => set({ stats }),

      // Puzzle progress management
      initializePuzzleProgress: (_puzzle) => {
        set({ 
          puzzleProgress: initialProgress(),
          error: null 
        });
      },

      addPlayerMove: (move) => {
        const progress = get().puzzleProgress;
        const puzzle = get().currentPuzzle;
        
        if (!progress || !puzzle) return;

        const newPlayerMoves = [...progress.playerMoves, move];
        const currentMoveIndex = progress.currentMove;
        const expectedMove = puzzle.solution_moves[currentMoveIndex];
        
        // Check if the move is correct
        const isCorrectMove = move === expectedMove;
        const isLastMove = currentMoveIndex === puzzle.solution_moves.length - 1;
        
        set({
          puzzleProgress: {
            ...progress,
            playerMoves: newPlayerMoves,
            currentMove: isCorrectMove ? currentMoveIndex + 1 : currentMoveIndex,
            isCorrect: isCorrectMove,
            isComplete: isCorrectMove && isLastMove
          }
        });
      },

      useHint: () => {
        const progress = get().puzzleProgress;
        if (!progress) return;

        set({
          puzzleProgress: {
            ...progress,
            hintsUsed: progress.hintsUsed + 1
          }
        });
      },

      markPuzzleComplete: (correct) => {
        const progress = get().puzzleProgress;
        if (!progress) return;

        set({
          puzzleProgress: {
            ...progress,
            isComplete: true,
            isCorrect: correct
          }
        });
      },

      resetPuzzleProgress: () => {
        set({ puzzleProgress: null });
      },

      // Filter helpers
      updateRatingRange: (minRating, maxRating) => {
        set({
          filters: {
            ...get().filters,
            minRating,
            maxRating
          }
        });
      },

      toggleTheme: (theme) => {
        const currentThemes = get().filters.themes || [];
        const newThemes = currentThemes.includes(theme)
          ? currentThemes.filter(t => t !== theme)
          : [...currentThemes, theme];
        
        set({
          filters: {
            ...get().filters,
            themes: newThemes
          }
        });
      },

      resetFilters: () => {
        set({ filters: defaultFilters });
      }
    }),
    {
      name: 'puzzle-store'
    }
  )
);

// Selector hooks for common patterns
export const useCurrentPuzzle = () => usePuzzleStore(state => state.currentPuzzle);
export const usePuzzleProgress = () => usePuzzleStore(state => state.puzzleProgress);
export const usePuzzleFilters = () => usePuzzleStore(state => state.filters);
export const usePuzzleLoading = () => usePuzzleStore(state => state.isLoading);
export const usePuzzleError = () => usePuzzleStore(state => state.error);
export const useCurrentHint = () => usePuzzleStore(state => state.currentHint);
export const useAvailableThemes = () => usePuzzleStore(state => state.availableThemes);