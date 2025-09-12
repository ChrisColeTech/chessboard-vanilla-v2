// Openings Domain Types

import type { DomainState } from '../common';

// Opening types from backend
export interface Opening {
  id: string;
  name: string;
  eco_code: string;
  moves: string;
  description: string;
  popularity: number;
  created_at: string;
}

// Response type (same as base entity)
export type OpeningResponse = Opening;

// Create request omits auto-generated fields
export type CreateOpeningRequest = Omit<Opening, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateOpeningRequest = Partial<CreateOpeningRequest>;

// Frontend-specific openings types
// Uses common DomainState interface from ../common
export type OpeningsState = DomainState<OpeningResponse>;
