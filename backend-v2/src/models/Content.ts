export interface ContentResponse {
  id: string;
  title: string;
  content_type: string;
  parent_id: string;
  order_index: number;
  description: string;
  content_body: object;
  difficulty_level: string;
  estimated_duration: number;
  category: string;
  objectives: object;
  prerequisites: object;
  is_published: boolean;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface CreateContentRequest {
  title: string;
  content_type: string;
  parent_id: string;
  order_index: number;
  description: string;
  content_body: object;
  difficulty_level: string;
  estimated_duration: number;
  category: string;
  objectives: object;
  prerequisites: object;
  is_published: boolean;
  version: number;
}

export interface UpdateContentRequest {
  title?: string;
  content_type?: string;
  parent_id?: string;
  order_index?: number;
  description?: string;
  content_body?: object;
  difficulty_level?: string;
  estimated_duration?: number;
  category?: string;
  objectives?: object;
  prerequisites?: object;
  is_published?: boolean;
  version?: number;
}