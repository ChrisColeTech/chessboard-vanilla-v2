// Generated types for Achievement

export interface Achievement {
  id: string;
  key: string;
  name: string;
  description: string;
  category: string;
  tier: string;
  requirements: any;
  points: number;
  badge_icon: string;
  difficulty: string;
  is_secret: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AchievementCreate {
  // Add creation properties here
}

export interface AchievementUpdate {
  // Add update properties here  
}

export interface AchievementFilter {
  // Add filter properties here
}
