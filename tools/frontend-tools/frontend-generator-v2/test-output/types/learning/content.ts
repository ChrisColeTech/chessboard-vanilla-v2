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
  // Add creation properties here
}

export interface ContentUpdate {
  // Add update properties here  
}

export interface ContentFilter {
  // Add filter properties here
}
