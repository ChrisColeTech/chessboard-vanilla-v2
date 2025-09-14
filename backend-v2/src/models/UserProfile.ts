export interface UserProfileResponse {
  id: string;
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  timezone: string;
  board_preferences: object;
  profile_visibility: string;
  show_rating: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateUserProfileRequest {
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  timezone: string;
  board_preferences: object;
  profile_visibility: string;
  show_rating: boolean;
}

export interface UpdateUserProfileRequest {
  user_id?: string;
  display_name?: string;
  avatar_url?: string;
  bio?: string;
  country?: string;
  timezone?: string;
  board_preferences?: object;
  profile_visibility?: string;
  show_rating?: boolean;
}