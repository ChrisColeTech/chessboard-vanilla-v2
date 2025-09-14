// Generated types for UserAchievement

export interface UserAchievement {
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

export interface UserAchievementCreate {
  // Properties needed for creating new UserAchievement
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

export interface UserAchievementUpdate {
  // Properties that can be updated
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

export interface UserAchievementFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
