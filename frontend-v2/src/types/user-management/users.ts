// Generated types for User

export interface User {
  id: string;
  username: string;
  email: string;
  password_hash: string;
  email_verified: boolean;
  chess_elo: number;
  puzzle_rating: number;
  games_played: number;
  games_won: number;
  games_lost: number;
  games_drawn: number;
  created_at: string;
  updated_at: string;
  last_login: string;
}

export interface UserCreate {
  // Properties needed for creating new User
  id: string;
  username: string;
  email: string;
  password_hash: string;
  email_verified: boolean;
  chess_elo: number;
  puzzle_rating: number;
  games_played: number;
  games_won: number;
  games_lost: number;
  games_drawn: number;
  created_at: string;
  updated_at: string;
  last_login: string;
}

export interface UserUpdate {
  // Properties that can be updated
  id: string;
  username: string;
  email: string;
  password_hash: string;
  email_verified: boolean;
  chess_elo: number;
  puzzle_rating: number;
  games_played: number;
  games_won: number;
  games_lost: number;
  games_drawn: number;
  created_at: string;
  updated_at: string;
  last_login: string;
}

export interface UserFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
