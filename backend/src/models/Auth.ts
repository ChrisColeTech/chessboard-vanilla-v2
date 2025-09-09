export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  user: UserInfo;
  token: string;
}

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

export interface MeResponse {
  user: UserInfo;
  progress: UserProgress;
}

export interface UserProgress {
  id: string;
  user_id: string;
  puzzles_solved: number;
  puzzles_correct: number;
  current_streak: number;
  best_streak: number;
  total_time_spent: number;
  achievements_unlocked: string;
  last_puzzle_date?: string;
  created_at: string;
  updated_at: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  resetToken: string;
  password: string;
}

export interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

export interface UpdateProfileRequest {
  username?: string;
  email?: string;
  chess_elo?: number;
  puzzle_rating?: number;
  preferences?: string;
}

export interface TokenVerificationResponse {
  user: UserInfo;
  tokenValid: boolean;
}

export interface EmailCheckRequest {
  email: string;
}

export interface UsernameCheckRequest {
  username: string;
}

export interface AvailabilityResponse {
  available: boolean;
}

export interface AuthResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface CreateAuthRequest extends RegisterRequest {}
export interface UpdateAuthRequest extends UpdateProfileRequest {}