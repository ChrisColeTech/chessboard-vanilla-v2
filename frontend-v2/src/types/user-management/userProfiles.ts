// Generated types for UserProfile

export interface UserProfile {
  id: string;
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  timezone: string;
  board_preferences: any;
  profile_visibility: string;
  show_rating: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserProfileCreate {
  // Properties needed for creating new UserProfile
  id: string;
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  timezone: string;
  board_preferences: any;
  profile_visibility: string;
  show_rating: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserProfileUpdate {
  // Properties that can be updated
  id: string;
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  timezone: string;
  board_preferences: any;
  profile_visibility: string;
  show_rating: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserProfileFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
