export interface LearningpathResponse {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  modules: string;
  progress: number;
  created_at: string;
  updated_at: string;
}

export interface CreateLearningpathRequest {
  title: string;
  description: string;
  difficulty: string;
  modules: string;
  progress: number;
}

export interface UpdateLearningpathRequest {
  title?: string;
  description?: string;
  difficulty?: string;
  modules?: string;
  progress?: number;
}