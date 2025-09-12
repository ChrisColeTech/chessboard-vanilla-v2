// Puzzles Domain Types

import type { DomainState } from '../common';

// Puzzle types from backend
export interface Puzzle {
  id: string;
  fen: string;
  solution_moves: string;
  themes: string;
  rating: number;
  description: string;
  created_at: string;
}

// Response type (same as base entity)
export type PuzzleResponse = Puzzle;

// Create request omits auto-generated fields
export type CreatePuzzleRequest = Omit<Puzzle, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdatePuzzleRequest = Partial<CreatePuzzleRequest>;

// Frontend-specific puzzles types
// Uses common DomainState interface from ../common
export type PuzzlesState = DomainState<PuzzleResponse>;
