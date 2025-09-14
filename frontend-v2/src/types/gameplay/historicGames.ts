// Generated types for HistoricGame

export interface HistoricGame {
  id: string;
  white_player: string;
  black_player: string;
  white_rating: number;
  black_rating: number;
  tournament_name: string;
  tournament_year: number;
  round_info: string;
  pgn: string;
  result: string;
  opening_eco: string;
  opening_name: string;
  game_significance: string;
  key_moments: any;
  game_date: string;
  created_at: string;
}

export interface HistoricGameCreate {
  // Properties needed for creating new HistoricGame
  id: string;
  white_player: string;
  black_player: string;
  white_rating: number;
  black_rating: number;
  tournament_name: string;
  tournament_year: number;
  round_info: string;
  pgn: string;
  result: string;
  opening_eco: string;
  opening_name: string;
  game_significance: string;
  key_moments: any;
  game_date: string;
  created_at: string;
}

export interface HistoricGameUpdate {
  // Properties that can be updated
  id: string;
  white_player: string;
  black_player: string;
  white_rating: number;
  black_rating: number;
  tournament_name: string;
  tournament_year: number;
  round_info: string;
  pgn: string;
  result: string;
  opening_eco: string;
  opening_name: string;
  game_significance: string;
  key_moments: any;
  game_date: string;
  created_at: string;
}

export interface HistoricGameFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
