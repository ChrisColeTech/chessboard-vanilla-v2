// Profiles Domain Types

import type { DomainState } from '../common';

// Profile types from backend
export interface Profile {
  id: string;
  user_id: string;
  display_name: string;
  avatar_url: string;
  bio: string;
  country: string;
  created_at: string;
  updated_at: string;
}

// Response type (same as base entity)
export type ProfileResponse = Profile;

// Create request omits auto-generated fields
export type CreateProfileRequest = Omit<Profile, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateProfileRequest = Partial<CreateProfileRequest>;

// Frontend-specific profiles types
// Uses common DomainState interface from ../common
export type ProfilesState = DomainState<ProfileResponse>;
