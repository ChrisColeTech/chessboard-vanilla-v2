// Generated types for Puzzle

export interface Puzzle {
  id: string;
  source_id: string;
  fen: string;
  moves: string;
  rating: number;
  themes: string;
  opening_family: string;
  game_phase: string;
  popularity: number;
  play_count: number;
  success_rate: number;
  created_at: string;
  updated_at: string;
}

export interface PuzzleCreate {
  // Properties needed for creating new Puzzle
  id: string;
  source_id: string;
  fen: string;
  moves: string;
  rating: number;
  themes: string;
  opening_family: string;
  game_phase: string;
  popularity: number;
  play_count: number;
  success_rate: number;
  created_at: string;
  updated_at: string;
}

export interface PuzzleUpdate {
  // Properties that can be updated
  id: string;
  source_id: string;
  fen: string;
  moves: string;
  rating: number;
  themes: string;
  opening_family: string;
  game_phase: string;
  popularity: number;
  play_count: number;
  success_rate: number;
  created_at: string;
  updated_at: string;
}

export interface PuzzleFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
