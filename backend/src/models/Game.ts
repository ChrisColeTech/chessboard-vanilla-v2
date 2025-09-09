export interface GameResponse {
  id: string;
  user_id: string;
  ai_level: number;
  user_color: string;
  current_fen: string;
  pgn: string;
  status: string;
  result: string;
  time_control: string;
  started_at: string;
  completed_at: string;
}

export interface CreateGameRequest {
  user_id: string;
  ai_level: number;
  user_color: string;
  current_fen: string;
  pgn: string;
  status: string;
  result: string;
  time_control: string;
  started_at: string;
  completed_at: string;
}

export interface UpdateGameRequest {
  user_id?: string;
  ai_level?: number;
  user_color?: string;
  current_fen?: string;
  pgn?: string;
  status?: string;
  result?: string;
  time_control?: string;
  started_at?: string;
  completed_at?: string;
}