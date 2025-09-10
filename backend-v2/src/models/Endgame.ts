export interface EndgameResponse {
  id: string;
  name: string;
  fen: string;
  category: string;
  difficulty: number;
  description: string;
  solution: string;
  created_at: string;
}

export interface CreateEndgameRequest {
  name: string;
  fen: string;
  category: string;
  difficulty: number;
  description: string;
  solution: string;
}

export interface UpdateEndgameRequest {
  name?: string;
  fen?: string;
  category?: string;
  difficulty?: number;
  description?: string;
  solution?: string;
}