export interface ProgressResponse {
  id: string;
  user_id: string;
  puzzles_solved: number;
  puzzles_correct: number;
  current_streak: number;
  best_streak: number;
  total_time_spent: number;
  achievements_unlocked: string;
  last_puzzle_date: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProgressRequest {
  user_id: string;
  puzzles_solved: number;
  puzzles_correct: number;
  current_streak: number;
  best_streak: number;
  total_time_spent: number;
  achievements_unlocked: string;
  last_puzzle_date: string;
}

export interface UpdateProgressRequest {
  user_id?: string;
  puzzles_solved?: number;
  puzzles_correct?: number;
  current_streak?: number;
  best_streak?: number;
  total_time_spent?: number;
  achievements_unlocked?: string;
  last_puzzle_date?: string;
}