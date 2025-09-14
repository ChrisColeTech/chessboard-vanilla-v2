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
  // Properties needed for creating new Achievement
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

export interface AchievementUpdate {
  // Properties that can be updated
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

export interface AchievementFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
