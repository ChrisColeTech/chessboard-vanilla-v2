export interface UserResponse {
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

export interface CreateUserRequest {
  username: string;
  email: string;
  password_hash: string;
  chess_elo: number;
  puzzle_rating: number;
  preferences: string;
}

export interface UpdateUserRequest {
  username?: string;
  email?: string;
  password_hash?: string;
  chess_elo?: number;
  puzzle_rating?: number;
  preferences?: string;
}