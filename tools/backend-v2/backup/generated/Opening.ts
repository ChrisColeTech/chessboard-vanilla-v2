export interface OpeningResponse {
  id: string;
  name: string;
  eco_code: string;
  moves: string;
  description: string;
  popularity: number;
  created_at: string;
}

export interface CreateOpeningRequest {
  name: string;
  eco_code: string;
  moves: string;
  description: string;
  popularity: number;
}

export interface UpdateOpeningRequest {
  name?: string;
  eco_code?: string;
  moves?: string;
  description?: string;
  popularity?: number;
}