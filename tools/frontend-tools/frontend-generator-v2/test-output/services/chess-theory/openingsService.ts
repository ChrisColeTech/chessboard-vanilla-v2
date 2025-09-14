// Generated service for Opening

class OpeningService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createOpening(data: any) {
    const response = await fetch(`${this.baseUrl}/openings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getOpeningById(id: string) {
    const response = await fetch(`${this.baseUrl}/openings/${id}`);
    return response.json();
  }

  async updateOpening(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/openings/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteOpening(id: string) {
    const response = await fetch(`${this.baseUrl}/openings/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listOpenings() {
    const response = await fetch(`${this.baseUrl}/openings`);
    return response.json();
  }
}

export const openingsService = new OpeningService();
export default openingsService;
