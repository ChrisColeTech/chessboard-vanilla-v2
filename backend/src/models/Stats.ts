export interface StatsResponse {
  user_id: string;
  total_puzzles: number;
  correct_puzzles: number;
  puzzle_accuracy: number;
  avg_solve_time: number;
  current_rating: number;
  games_played: number;
  games_won: number;
  win_rate: number;
}

export interface CreateStatsRequest {
  user_id: string;
  total_puzzles: number;
  correct_puzzles: number;
  puzzle_accuracy: number;
  avg_solve_time: number;
  current_rating: number;
  games_played: number;
  games_won: number;
  win_rate: number;
}

export interface UpdateStatsRequest {
  user_id?: string;
  total_puzzles?: number;
  correct_puzzles?: number;
  puzzle_accuracy?: number;
  avg_solve_time?: number;
  current_rating?: number;
  games_played?: number;
  games_won?: number;
  win_rate?: number;
}