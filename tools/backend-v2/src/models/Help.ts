export interface HelpResponse {
  id: string;
  category: string;
  title: string;
  content: string;
  tags: string;
  created_at: string;
  updated_at: string;
}

export interface CreateHelpRequest {
  category: string;
  title: string;
  content: string;
  tags: string;
}

export interface UpdateHelpRequest {
  category?: string;
  title?: string;
  content?: string;
  tags?: string;
}