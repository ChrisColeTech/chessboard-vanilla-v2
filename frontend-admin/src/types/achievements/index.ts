// Achievements Domain Types

import type { DomainState } from '../common';

// Achievement types from backend
export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  points: number;
  criteria: string;
  created_at: string;
}

// Response type (same as base entity)
export type AchievementResponse = Achievement;

// Create request omits auto-generated fields
export type CreateAchievementRequest = Omit<Achievement, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateAchievementRequest = Partial<CreateAchievementRequest>;

// Frontend-specific achievements types
// Uses common DomainState interface from ../common
export type AchievementsState = DomainState<AchievementResponse>;
