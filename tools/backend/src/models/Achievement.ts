export interface AchievementResponse {
  id: string;
  title: string;
  description: string;
  icon: string;
  points: number;
  criteria: string;
  created_at: string;
}

export interface CreateAchievementRequest {
  title: string;
  description: string;
  icon: string;
  points: number;
  criteria: string;
}

export interface UpdateAchievementRequest {
  title?: string;
  description?: string;
  icon?: string;
  points?: number;
  criteria?: string;
}