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
  // Add creation properties here
}

export interface PuzzleUpdate {
  // Add update properties here  
}

export interface PuzzleFilter {
  // Add filter properties here
}
