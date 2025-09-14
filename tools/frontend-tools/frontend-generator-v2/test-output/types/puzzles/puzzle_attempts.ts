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
  // Add creation properties here
}

export interface PuzzleAttemptUpdate {
  // Add update properties here  
}

export interface PuzzleAttemptFilter {
  // Add filter properties here
}
