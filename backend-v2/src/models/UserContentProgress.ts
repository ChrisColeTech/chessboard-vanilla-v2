export interface UserContentProgressResponse {
  id: string;
  user_id: string;
  content_id: string;
  status: string;
  progress_percentage: number;
  time_spent: number;
  completion_score: number;
  started_at: string;
  completed_at: string;
  last_accessed: string;
  notes: string;
  bookmarked: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateUserContentProgressRequest {
  user_id: string;
  content_id: string;
  status: string;
  progress_percentage: number;
  time_spent: number;
  completion_score: number;
  started_at: string;
  completed_at: string;
  last_accessed: string;
  notes: string;
  bookmarked: boolean;
}

export interface UpdateUserContentProgressRequest {
  user_id?: string;
  content_id?: string;
  status?: string;
  progress_percentage?: number;
  time_spent?: number;
  completion_score?: number;
  started_at?: string;
  completed_at?: string;
  last_accessed?: string;
  notes?: string;
  bookmarked?: boolean;
}