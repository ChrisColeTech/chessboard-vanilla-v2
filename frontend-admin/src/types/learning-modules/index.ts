// Learning-modules Domain Types

import type { DomainState } from '../common';

// LearningModule types from backend
export interface LearningModule {
  id: string;
  title: string;
  description: string;
  content: string;
  difficulty: string;
  order: number;
  learning_path_id: string;
  created_at: string;
}

// Response type (same as base entity)
export type LearningModuleResponse = LearningModule;

// Create request omits auto-generated fields
export type CreateLearningModuleRequest = Omit<LearningModule, 'id' | 'created_at'>;

// Update request makes create fields optional
export type UpdateLearningModuleRequest = Partial<CreateLearningModuleRequest>;

// Frontend-specific learning-modules types
// Uses common DomainState interface from ../common
export type LearningModulesState = DomainState<LearningModuleResponse>;
