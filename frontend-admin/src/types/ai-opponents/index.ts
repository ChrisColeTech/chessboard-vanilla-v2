// Ai-opponents Domain Types

import type { DomainState } from '../common';

// AIOpponent types from backend
export interface AIOpponent {
  id: string;
  name: string;
  difficulty: number;
  elo_rating: number;
  personality: string;
  description: string;
  created_at: string;
}

// Response type (same as base entity)
export type AIOpponentResponse = AIOpponent;

// Create request omits auto-generated fields
export type CreateAIOpponentRequest = Omit<AIOpponent, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateAIOpponentRequest = Partial<CreateAIOpponentRequest>;

// Frontend-specific ai-opponents types
// Uses common DomainState interface from ../common
export type AiOpponentsState = DomainState<AIOpponentResponse>;
