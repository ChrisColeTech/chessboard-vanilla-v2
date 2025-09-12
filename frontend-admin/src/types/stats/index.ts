// Stats Domain Types

import type { DomainState } from '../common';

// Stats types from backend
export interface Stats {
  user_id: string;
  total_puzzles: number;
  correct_puzzles: number;
  puzzle_accuracy: number;
  avg_solve_time: number;
  current_rating: number;
  games_played: number;
  games_won: number;
  win_rate: number;
}

// Response type (same as base entity)
export type StatsResponse = Stats;

// Create request omits auto-generated fields
export type CreateStatsRequest = Omit<Stats, 'id'>;

// Update request makes create fields optional
export type UpdateStatsRequest = Partial<CreateStatsRequest>;

// Frontend-specific stats types
// Uses common DomainState interface from ../common
export type StatsState = DomainState<StatsResponse>;
