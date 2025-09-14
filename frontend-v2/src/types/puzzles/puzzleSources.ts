// Generated types for PuzzleSource

export interface PuzzleSource {
  id: string;
  name: string;
  description: string;
  attribution: string;
  license: string;
  source_url: string;
  total_puzzles: number;
  average_rating: number;
  is_active: boolean;
  last_imported: string;
  created_at: string;
  updated_at: string;
}

export interface PuzzleSourceCreate {
  // Properties needed for creating new PuzzleSource
  id: string;
  name: string;
  description: string;
  attribution: string;
  license: string;
  source_url: string;
  total_puzzles: number;
  average_rating: number;
  is_active: boolean;
  last_imported: string;
  created_at: string;
  updated_at: string;
}

export interface PuzzleSourceUpdate {
  // Properties that can be updated
  id: string;
  name: string;
  description: string;
  attribution: string;
  license: string;
  source_url: string;
  total_puzzles: number;
  average_rating: number;
  is_active: boolean;
  last_imported: string;
  created_at: string;
  updated_at: string;
}

export interface PuzzleSourceFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
