// Generated types for Game

export interface Game {
  id: string;
  white_player_id: string;
  black_player_id: string;
  time_control: string;
  ai_level: number;
  initial_fen: string;
  current_fen: string;
  pgn: string;
  result: string;
  termination: string;
  opening_eco: string;
  opening_name: string;
  move_count: number;
  white_elo_before: number;
  white_elo_after: number;
  black_elo_before: number;
  black_elo_after: number;
  started_at: string;
  completed_at: string;
}

export interface GameCreate {
  // Properties needed for creating new Game
  id: string;
  white_player_id: string;
  black_player_id: string;
  time_control: string;
  ai_level: number;
  initial_fen: string;
  current_fen: string;
  pgn: string;
  result: string;
  termination: string;
  opening_eco: string;
  opening_name: string;
  move_count: number;
  white_elo_before: number;
  white_elo_after: number;
  black_elo_before: number;
  black_elo_after: number;
  started_at: string;
  completed_at: string;
}

export interface GameUpdate {
  // Properties that can be updated
  id: string;
  white_player_id: string;
  black_player_id: string;
  time_control: string;
  ai_level: number;
  initial_fen: string;
  current_fen: string;
  pgn: string;
  result: string;
  termination: string;
  opening_eco: string;
  opening_name: string;
  move_count: number;
  white_elo_before: number;
  white_elo_after: number;
  black_elo_before: number;
  black_elo_after: number;
  started_at: string;
  completed_at: string;
}

export interface GameFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
