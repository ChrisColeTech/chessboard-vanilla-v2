export interface ProfileResponse {
  id: string;
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProfileRequest {
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  timezone: string;
}

export interface UpdateProfileRequest {
  user_id?: string;
  display_name?: string;
  avatar_url?: string;
  bio?: string;
  country?: string;
  timezone?: string;
}