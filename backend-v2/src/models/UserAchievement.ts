export interface UserAchievementResponse {
  id: string;
  user_id: string;
  achievement_id: string;
  current_progress: number;
  target_progress: number;
  progress_percentage: number;
  is_completed: boolean;
  is_notified: boolean;
  started_at: string;
  completed_at: string;
}

export interface CreateUserAchievementRequest {
  user_id: string;
  achievement_id: string;
  current_progress: number;
  target_progress: number;
  progress_percentage: number;
  is_completed: boolean;
  is_notified: boolean;
  started_at: string;
  completed_at: string;
}

export interface UpdateUserAchievementRequest {
  user_id?: string;
  achievement_id?: string;
  current_progress?: number;
  target_progress?: number;
  progress_percentage?: number;
  is_completed?: boolean;
  is_notified?: boolean;
  started_at?: string;
  completed_at?: string;
}