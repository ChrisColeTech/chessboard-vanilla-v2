// Learning Domain Types

// LearningPath types from backend
export interface LearningPath {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  modules: string;
  progress: number;
  created_at: string;
  updated_at: string;
}

// Response type (same as base entity)
export type LearningPathResponse = LearningPath;

// Create request omits auto-generated fields
export type CreateLearningPathRequest = Omit<LearningPath, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateLearningPathRequest = Partial<CreateLearningPathRequest>;

// Frontend-specific learning types
export interface LearningProgress {
  completedModules: number;
  totalModules: number;
  currentLevel: string;
  skillPoints: number;
}

export interface CourseEnrollment {
  courseId: string;
  enrolledAt: string;
  progress: number;
  status: 'active' | 'completed' | 'paused';
}
