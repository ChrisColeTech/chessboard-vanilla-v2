// Historic-games Domain Types

import type { DomainState } from '../common';

// HistoricGame types from backend
export interface HistoricGame {
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

// Response type (same as base entity)
export type HistoricGameResponse = HistoricGame;

// Create request omits auto-generated fields
export type CreateHistoricGameRequest = Omit<HistoricGame, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateHistoricGameRequest = Partial<CreateHistoricGameRequest>;

// Frontend-specific historic-games types
// Uses common DomainState interface from ../common
export type HistoricGamesState = DomainState<HistoricGameResponse>;
