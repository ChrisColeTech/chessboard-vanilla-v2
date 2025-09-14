// Generated service for Achievement

class AchievementService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createAchievement(data: any) {
    const response = await fetch(`${this.baseUrl}/achievements`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getAchievementById(id: string) {
    const response = await fetch(`${this.baseUrl}/achievements/${id}`);
    return response.json();
  }

  async updateAchievement(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/achievements/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteAchievement(id: string) {
    const response = await fetch(`${this.baseUrl}/achievements/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listAchievements() {
    const response = await fetch(`${this.baseUrl}/achievements`);
    return response.json();
  }
}

export const achievementsService = new AchievementService();
export default achievementsService;
