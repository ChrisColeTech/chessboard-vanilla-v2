export interface PuzzleattemptResponse {
  id: string;
  user_id: string;
  puzzle_id: string;
  correct: boolean;
  time_spent: number;
  moves_made: string;
  completed_at: string;
}

export interface CreatePuzzleattemptRequest {
  user_id: string;
  puzzle_id: string;
  correct: boolean;
  time_spent: number;
  moves_made: string;
  completed_at: string;
}

export interface UpdatePuzzleattemptRequest {
  user_id?: string;
  puzzle_id?: string;
  correct?: boolean;
  time_spent?: number;
  moves_made?: string;
  completed_at?: string;
}