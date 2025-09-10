export interface GamereviewResponse {
  id: string;
  game_id: string;
  reviewer_id: string;
  analysis: string;
  rating: number;
  key_moments: string;
  created_at: string;
}

export interface CreateGamereviewRequest {
  game_id: string;
  reviewer_id: string;
  analysis: string;
  rating: number;
  key_moments: string;
}

export interface UpdateGamereviewRequest {
  game_id?: string;
  reviewer_id?: string;
  analysis?: string;
  rating?: number;
  key_moments?: string;
}