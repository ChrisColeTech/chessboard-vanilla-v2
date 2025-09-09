// Puzzle types for database integration
export interface Puzzle {
  id: string;
  fen: string;
  solution_moves: string[]; // JSON parsed from DB
  themes: string[]; // JSON parsed from DB
  rating: number;
  description?: string;
  created_at: string;
}

export interface PuzzleAttempt {
  id: string;
  user_id: string;
  puzzle_id: string;
  moves: string[]; // JSON parsed from DB
  correct: boolean;
  time_taken: number; // in seconds
  hints_used: number;
  rating_change: number;
  attempted_at: string;
}

export interface PuzzleFilters {
  minRating?: number;
  maxRating?: number;
  themes?: string[];
  limit?: number;
  offset?: number;
}

export interface PuzzleProgress {
  currentMove: number;
  playerMoves: string[];
  isCorrect?: boolean;
  isComplete: boolean;
  hintsUsed: number;
  startTime: number;
}

export interface PuzzleStats {
  totalPuzzles: number;
  averageRating: number;
  minRating: number;
  maxRating: number;
}

export interface UserPuzzleStats {
  totalSolved: number;
  totalAttempted: number;
  accuracyRate: number;
  averageRating: number;
  currentStreak: number;
  bestStreak: number;
}

// Database raw types (before JSON parsing)
export interface PuzzleRaw {
  id: string;
  fen: string;
  solution_moves: string; // JSON string from DB
  themes: string; // JSON string from DB
  rating: number;
  description?: string;
  created_at: string;
}