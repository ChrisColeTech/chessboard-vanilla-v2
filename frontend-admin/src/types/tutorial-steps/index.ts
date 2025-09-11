// Tutorial-steps Domain Types

import type { DomainState } from '../common';

// TutorialStep types from backend
export interface TutorialStep {
  id: string;
  tutorial_id: string;
  step_number: number;
  title: string;
  content: string;
  action_required: string;
  completed: boolean;
}

// Response type (same as base entity)
export type TutorialStepResponse = TutorialStep;

// Create request omits auto-generated fields
export type CreateTutorialStepRequest = Omit<TutorialStep, 'id'>;

// Update request makes create fields optional
export type UpdateTutorialStepRequest = Partial<CreateTutorialStepRequest>;

// Frontend-specific tutorial-steps types
// Uses common DomainState interface from ../common
export type TutorialStepsState = DomainState<TutorialStepResponse>;
