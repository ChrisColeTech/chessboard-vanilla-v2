// Progress Domain Types

import type { DomainState } from '../common';

// Progress types from backend
export interface Progress {
  id: string;
  user_id: string;
  puzzles_solved: number;
  puzzles_correct: number;
  current_streak: number;
  best_streak: number;
  total_time_spent: number;
  achievements_unlocked: string;
  last_puzzle_date: string;
  created_at: string;
  updated_at: string;
}

// Response type (same as base entity)
export type ProgressResponse = Progress;

// Create request omits auto-generated fields
export type CreateProgressRequest = Omit<Progress, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateProgressRequest = Partial<CreateProgressRequest>;

// Frontend-specific progress types
// Uses common DomainState interface from ../common
export type ProgressState = DomainState<ProgressResponse>;
