// Endgames Domain Types

import type { DomainState } from '../common';

// Endgame types from backend
export interface Endgame {
  id: string;
  name: string;
  fen: string;
  category: string;
  difficulty: number;
  description: string;
  solution: string;
  created_at: string;
}

// Response type (same as base entity)
export type EndgameResponse = Endgame;

// Create request omits auto-generated fields
export type CreateEndgameRequest = Omit<Endgame, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateEndgameRequest = Partial<CreateEndgameRequest>;

// Frontend-specific endgames types
// Uses common DomainState interface from ../common
export type EndgamesState = DomainState<EndgameResponse>;
