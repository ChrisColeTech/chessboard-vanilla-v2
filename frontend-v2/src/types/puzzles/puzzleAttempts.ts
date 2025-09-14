// Generated types for PuzzleAttempt

export interface PuzzleAttempt {
  id: string;
  user_id: string;
  puzzle_id: string;
  solved: boolean;
  user_moves: string;
  time_taken: number;
  hints_used: number;
  attempt_number: number;
  rating_before: number;
  rating_after: number;
  rating_change: number;
  attempted_at: string;
}

export interface PuzzleAttemptCreate {
  // Properties needed for creating new PuzzleAttempt
  id: string;
  user_id: string;
  puzzle_id: string;
  solved: boolean;
  user_moves: string;
  time_taken: number;
  hints_used: number;
  attempt_number: number;
  rating_before: number;
  rating_after: number;
  rating_change: number;
  attempted_at: string;
}

export interface PuzzleAttemptUpdate {
  // Properties that can be updated
  id: string;
  user_id: string;
  puzzle_id: string;
  solved: boolean;
  user_moves: string;
  time_taken: number;
  hints_used: number;
  attempt_number: number;
  rating_before: number;
  rating_after: number;
  rating_change: number;
  attempted_at: string;
}

export interface PuzzleAttemptFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
