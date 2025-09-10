export interface HistoricgameResponse {
  id: string;
  white_player: string;
  black_player: string;
  result: string;
  pgn: string;
  event: string;
  date: string;
  eco: string;
  created_at: string;
}

export interface CreateHistoricgameRequest {
  white_player: string;
  black_player: string;
  result: string;
  pgn: string;
  event: string;
  date: string;
  eco: string;
}

export interface UpdateHistoricgameRequest {
  white_player?: string;
  black_player?: string;
  result?: string;
  pgn?: string;
  event?: string;
  date?: string;
  eco?: string;
}