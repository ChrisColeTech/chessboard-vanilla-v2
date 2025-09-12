// Tutorials Domain Types

import type { DomainState } from '../common';

// Tutorial types from backend
export interface Tutorial {
  id: string;
  title: string;
  description: string;
  content: string;
  difficulty: string;
  duration: number;
  completed: boolean;
  created_at: string;
}

// Response type (same as base entity)
export type TutorialResponse = Tutorial;

// Create request omits auto-generated fields
export type CreateTutorialRequest = Omit<Tutorial, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateTutorialRequest = Partial<CreateTutorialRequest>;

// Frontend-specific tutorials types
// Uses common DomainState interface from ../common
export type TutorialsState = DomainState<TutorialResponse>;
