// Analysis Domain Types

import type { DomainState } from '../common';

// Analysis types from backend
export interface Analysis {
  id: string;
  position_fen: string;
  analysis_data: string;
  best_move: string;
  evaluation: number;
  depth: number;
  created_at: string;
}

// Response type (same as base entity)
export type AnalysisResponse = Analysis;

// Create request omits auto-generated fields
export type CreateAnalysisRequest = Omit<Analysis, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateAnalysisRequest = Partial<CreateAnalysisRequest>;

// Frontend-specific analysis types
// Uses common DomainState interface from ../common
export type AnalysisState = DomainState<AnalysisResponse>;
