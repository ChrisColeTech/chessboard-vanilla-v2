// Generated service for Content

class ContentService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createContent(data: any) {
    const response = await fetch(`${this.baseUrl}/content`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getContentById(id: string) {
    const response = await fetch(`${this.baseUrl}/content/${id}`);
    return response.json();
  }

  async updateContent(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/content/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteContent(id: string) {
    const response = await fetch(`${this.baseUrl}/content/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listContents() {
    const response = await fetch(`${this.baseUrl}/content`);
    return response.json();
  }
}

export const contentService = new ContentService();
export default contentService;
