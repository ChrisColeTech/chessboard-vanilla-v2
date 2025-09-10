export interface TutorialResponse {
  id: string;
  title: string;
  description: string;
  content: string;
  difficulty: string;
  duration: number;
  completed: boolean;
  created_at: string;
}

export interface CreateTutorialRequest {
  title: string;
  description: string;
  content: string;
  difficulty: string;
  duration: number;
  completed: boolean;
}

export interface UpdateTutorialRequest {
  title?: string;
  description?: string;
  content?: string;
  difficulty?: string;
  duration?: number;
  completed?: boolean;
}