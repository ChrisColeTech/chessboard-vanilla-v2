export interface AiopponentResponse {
  id: string;
  name: string;
  difficulty: number;
  elo_rating: number;
  personality: string;
  description: string;
  created_at: string;
}

export interface CreateAiopponentRequest {
  name: string;
  difficulty: number;
  elo_rating: number;
  personality: string;
  description: string;
}

export interface UpdateAiopponentRequest {
  name?: string;
  difficulty?: number;
  elo_rating?: number;
  personality?: string;
  description?: string;
}