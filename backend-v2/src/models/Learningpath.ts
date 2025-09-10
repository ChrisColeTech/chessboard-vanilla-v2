export interface LearningPathResponse {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  modules: string;
  progress: number;
  created_at: string;
  updated_at: string;
}

export interface CreateLearningPathRequest {
  title: string;
  description: string;
  difficulty: string;
  modules: string;
  progress: number;
}

export interface UpdateLearningPathRequest {
  title?: string;
  description?: string;
  difficulty?: string;
  modules?: string;
  progress?: number;
}