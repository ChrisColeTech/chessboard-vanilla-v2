// Game-reviews Domain Types

import type { DomainState } from '../common';

// GameReview types from backend
export interface GameReview {
  id: string;
  game_id: string;
  reviewer_id: string;
  analysis: string;
  rating: number;
  key_moments: string;
  created_at: string;
}

// Response type (same as base entity)
export type GameReviewResponse = GameReview;

// Create request omits auto-generated fields
export type CreateGameReviewRequest = Omit<GameReview, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateGameReviewRequest = Partial<CreateGameReviewRequest>;

// Frontend-specific game-reviews types
// Uses common DomainState interface from ../common
export type GameReviewsState = DomainState<GameReviewResponse>;
