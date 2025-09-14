// Generated types for Opening

export interface Opening {
  id: string;
  eco_code: string;
  name: string;
  moves: string;
  fen: string;
  popularity: number;
  difficulty_level: string;
  created_at: string;
  updated_at: string;
}

export interface OpeningCreate {
  // Properties needed for creating new Opening
  id: string;
  eco_code: string;
  name: string;
  moves: string;
  fen: string;
  popularity: number;
  difficulty_level: string;
  created_at: string;
  updated_at: string;
}

export interface OpeningUpdate {
  // Properties that can be updated
  id: string;
  eco_code: string;
  name: string;
  moves: string;
  fen: string;
  popularity: number;
  difficulty_level: string;
  created_at: string;
  updated_at: string;
}

export interface OpeningFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
