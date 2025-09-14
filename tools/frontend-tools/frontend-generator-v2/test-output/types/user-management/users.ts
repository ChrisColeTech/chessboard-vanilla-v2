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
  // Add creation properties here
}

export interface UserUpdate {
  // Add update properties here  
}

export interface UserFilter {
  // Add filter properties here
}
