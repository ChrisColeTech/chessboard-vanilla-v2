// Generated types for UserContentProgress

export interface UserContentProgress {
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

export interface UserContentProgressCreate {
  // Add creation properties here
}

export interface UserContentProgressUpdate {
  // Add update properties here  
}

export interface UserContentProgressFilter {
  // Add filter properties here
}
