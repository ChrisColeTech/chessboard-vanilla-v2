// Auth Domain Types

// Auth types from backend
export interface Auth {
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
export type AuthResponse = Auth;

// Create request omits auto-generated fields
export type CreateAuthRequest = Omit<Auth, 'id' | 'created_at' | 'updated_at'>;

// Update request makes create fields optional
export type UpdateAuthRequest = Partial<CreateAuthRequest>;

// Frontend-specific auth types
export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated' | 'error';

export interface UserInfo {
  id: string;
  username: string;
  email: string;
  chess_elo: number;
  puzzle_rating: number;
  preferences: string;
  created_at: string;
  updated_at: string;
}

export interface AuthState {
  status: AuthStatus;
  user: UserInfo | null;
  token: string | null;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}
