// Puzzle-sources Domain Types

import type { DomainState } from '../common';

// PuzzleSource types from backend
export interface PuzzleSource {
  id: string;
  name: string;
  description: string;
  url: string;
  puzzle_count: number;
  created_at: string;
}

// Response type (same as base entity)
export type PuzzleSourceResponse = PuzzleSource;

// Create request omits auto-generated fields
export type CreatePuzzleSourceRequest = Omit<PuzzleSource, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdatePuzzleSourceRequest = Partial<CreatePuzzleSourceRequest>;

// Frontend-specific puzzle-sources types
// Uses common DomainState interface from ../common
export type PuzzleSourcesState = DomainState<PuzzleSourceResponse>;
