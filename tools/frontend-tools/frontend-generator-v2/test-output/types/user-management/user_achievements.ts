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
  // Add creation properties here
}

export interface UserAchievementUpdate {
  // Add update properties here  
}

export interface UserAchievementFilter {
  // Add filter properties here
}
