export interface PuzzleResponse {
  id: string;
  fen: string;
  solution_moves: string;
  themes: string;
  rating: number;
  description: string;
  created_at: string;
}

export interface CreatePuzzleRequest {
  fen: string;
  solution_moves: string;
  themes: string;
  rating: number;
  description: string;
}

export interface UpdatePuzzleRequest {
  fen?: string;
  solution_moves?: string;
  themes?: string;
  rating?: number;
  description?: string;
}