// Analytics Domain Types

import type { DomainState } from '../common';

// Analytics types from backend
export interface Analytics {
  id: string;
  user_id: string;
  event_type: string;
  event_data: string;
  timestamp: string;
  session_id: string;
}

// Response type (same as base entity)
export type AnalyticsResponse = Analytics;

// Create request omits auto-generated fields
export type CreateAnalyticsRequest = Omit<Analytics, 'id'>;

// Update request makes create fields optional
export type UpdateAnalyticsRequest = Partial<CreateAnalyticsRequest>;

// Frontend-specific analytics types
// Uses common DomainState interface from ../common
export type AnalyticsState = DomainState<AnalyticsResponse>;
