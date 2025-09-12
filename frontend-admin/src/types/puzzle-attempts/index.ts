// Puzzle-attempts Domain Types

import type { DomainState } from '../common';

// PuzzleAttempt types from backend
export interface PuzzleAttempt {
  id: string;
  user_id: string;
  puzzle_id: string;
  correct: boolean;
  time_spent: number;
  moves_made: string;
  completed_at: string;
}

// Response type (same as base entity)
export type PuzzleAttemptResponse = PuzzleAttempt;

// Create request omits auto-generated fields
export type CreatePuzzleAttemptRequest = Omit<PuzzleAttempt, 'id'>;

// Update request makes create fields optional
export type UpdatePuzzleAttemptRequest = Partial<CreatePuzzleAttemptRequest>;

// Frontend-specific puzzle-attempts types
// Uses common DomainState interface from ../common
export type PuzzleAttemptsState = DomainState<PuzzleAttemptResponse>;
