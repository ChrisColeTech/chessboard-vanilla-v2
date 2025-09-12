// Games Domain Types

import type { DomainState } from '../common';

// Game types from backend
export interface Game {
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

// Response type (same as base entity)
export type GameResponse = Game;

// Create request omits auto-generated fields
export type CreateGameRequest = Omit<Game, 'id'>;

// Update request makes create fields optional
export type UpdateGameRequest = Partial<CreateGameRequest>;

// Frontend-specific games types
// Uses common DomainState interface from ../common
export type GamesState = DomainState<GameResponse>;
