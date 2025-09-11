// Users Domain Types

import type { DomainState } from '../common';

// User types from backend
export interface User {
  id: string;
  username: string;
  email: string;
  password_hash: string;
  chess_elo: number;
  puzzle_rating: number;
  preferences: string;
  created_at: string;
  updated_at: string;
}

// Response type (same as base entity)
export type UserResponse = User;

// Create request omits auto-generated fields
export type CreateUserRequest = Omit<User, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateUserRequest = Partial<CreateUserRequest>;

// Frontend-specific users types
// Uses common DomainState interface from ../common
export type UsersState = DomainState<UserResponse>;
