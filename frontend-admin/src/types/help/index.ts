// Help Domain Types

import type { DomainState } from '../common';

// Help types from backend
export interface Help {
  id: string;
  category: string;
  title: string;
  content: string;
  tags: string;
  created_at: string;
  updated_at: string;
}

// Response type (same as base entity)
export type HelpResponse = Help;

// Create request omits auto-generated fields
export type CreateHelpRequest = Omit<Help, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateHelpRequest = Partial<CreateHelpRequest>;

// Frontend-specific help types
// Uses common DomainState interface from ../common
export type HelpState = DomainState<HelpResponse>;
