// Sessions Domain Types

import type { DomainState } from '../common';

// Session types from backend
export interface Session {
  id: string;
  user_id: string;
  refresh_token: string;
  session_token: string;
  expires_at: string;
  created_at: string;
  last_accessed: string;
}

// Response type (same as base entity)
export type SessionResponse = Session;

// Create request omits auto-generated fields
export type CreateSessionRequest = Omit<Session, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateSessionRequest = Partial<CreateSessionRequest>;

// Frontend-specific sessions types
// Uses common DomainState interface from ../common
export type SessionsState = DomainState<SessionResponse>;
