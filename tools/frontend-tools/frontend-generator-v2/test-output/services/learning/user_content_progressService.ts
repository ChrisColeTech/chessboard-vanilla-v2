// Generated service for UserContentProgress

class UserContentProgressService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createUserContentProgress(data: any) {
    const response = await fetch(`${this.baseUrl}/user_content_progress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getUserContentProgressById(id: string) {
    const response = await fetch(`${this.baseUrl}/user_content_progress/${id}`);
    return response.json();
  }

  async updateUserContentProgress(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/user_content_progress/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteUserContentProgress(id: string) {
    const response = await fetch(`${this.baseUrl}/user_content_progress/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listUserContentProgresss() {
    const response = await fetch(`${this.baseUrl}/user_content_progress`);
    return response.json();
  }
}

export const user_content_progressService = new UserContentProgressService();
export default user_content_progressService;
