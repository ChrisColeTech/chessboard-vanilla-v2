export interface StudyplanResponse {
  id: string;
  user_id: string;
  title: string;
  goals: string;
  schedule: string;
  progress: number;
  created_at: string;
  updated_at: string;
}

export interface CreateStudyplanRequest {
  user_id: string;
  title: string;
  goals: string;
  schedule: string;
  progress: number;
}

export interface UpdateStudyplanRequest {
  user_id?: string;
  title?: string;
  goals?: string;
  schedule?: string;
  progress?: number;
}