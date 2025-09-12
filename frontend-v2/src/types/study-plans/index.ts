// Study-plans Domain Types

import type { DomainState } from '../common';

// StudyPlan types from backend
export interface StudyPlan {
  id: string;
  user_id: string;
  title: string;
  goals: string;
  schedule: string;
  progress: number;
  created_at: string;
  updated_at: string;
}

// Response type (same as base entity)
export type StudyPlanResponse = StudyPlan;

// Create request omits auto-generated fields
export type CreateStudyPlanRequest = Omit<StudyPlan, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateStudyPlanRequest = Partial<CreateStudyPlanRequest>;

// Frontend-specific study-plans types
// Uses common DomainState interface from ../common
export type StudyPlansState = DomainState<StudyPlanResponse>;
