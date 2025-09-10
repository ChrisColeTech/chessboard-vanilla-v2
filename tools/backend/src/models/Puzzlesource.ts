export interface PuzzlesourceResponse {
  id: string;
  name: string;
  description: string;
  url: string;
  puzzle_count: number;
  created_at: string;
}

export interface CreatePuzzlesourceRequest {
  name: string;
  description: string;
  url: string;
  puzzle_count: number;
}

export interface UpdatePuzzlesourceRequest {
  name?: string;
  description?: string;
  url?: string;
  puzzle_count?: number;
}