export interface LearningmoduleResponse {
  id: string;
  title: string;
  description: string;
  content: string;
  difficulty: string;
  order: number;
  learning_path_id: string;
  created_at: string;
}

export interface CreateLearningmoduleRequest {
  title: string;
  description: string;
  content: string;
  difficulty: string;
  order: number;
  learning_path_id: string;
}

export interface UpdateLearningmoduleRequest {
  title?: string;
  description?: string;
  content?: string;
  difficulty?: string;
  order?: number;
  learning_path_id?: string;
}