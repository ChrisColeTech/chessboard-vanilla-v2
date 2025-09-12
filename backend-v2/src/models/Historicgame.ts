export interface HistoricgameResponse {
  id: string;
  white_player: string;
  black_player: string;
  white_rating: number;
  black_rating: number;
  result: string;
  pgn: string;
  event: string;
  date: string;
  eco: string;
  tournament_name: string;
  tournament_year: number;
  opening_name: string;
  opening_eco: string;
  created_at: string;
}

export interface CreateHistoricgameRequest {
  white_player: string;
  black_player: string;
  white_rating: number;
  black_rating: number;
  result: string;
  pgn: string;
  event: string;
  date: string;
  eco: string;
  tournament_name: string;
  tournament_year: number;
  opening_name: string;
  opening_eco: string;
}

export interface UpdateHistoricgameRequest {
  white_player?: string;
  black_player?: string;
  white_rating?: number;
  black_rating?: number;
  result?: string;
  pgn?: string;
  event?: string;
  date?: string;
  eco?: string;
  tournament_name?: string;
  tournament_year?: number;
  opening_name?: string;
  opening_eco?: string;
}