// Generated types for Content

export interface Content {
  id: string;
  title: string;
  content_type: string;
  parent_id: string;
  order_index: number;
  description: string;
  content_body: any;
  difficulty_level: string;
  estimated_duration: number;
  category: string;
  objectives: any;
  prerequisites: any;
  is_published: boolean;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface ContentCreate {
  // Properties needed for creating new Content
  id: string;
  title: string;
  content_type: string;
  parent_id: string;
  order_index: number;
  description: string;
  content_body: any;
  difficulty_level: string;
  estimated_duration: number;
  category: string;
  objectives: any;
  prerequisites: any;
  is_published: boolean;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface ContentUpdate {
  // Properties that can be updated
  id: string;
  title: string;
  content_type: string;
  parent_id: string;
  order_index: number;
  description: string;
  content_body: any;
  difficulty_level: string;
  estimated_duration: number;
  category: string;
  objectives: any;
  prerequisites: any;
  is_published: boolean;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface ContentFilter {
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}
