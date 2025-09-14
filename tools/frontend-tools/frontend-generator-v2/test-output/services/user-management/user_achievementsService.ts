// Generated service for UserAchievement

class UserAchievementService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createUserAchievement(data: any) {
    const response = await fetch(`${this.baseUrl}/user_achievements`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getUserAchievementById(id: string) {
    const response = await fetch(`${this.baseUrl}/user_achievements/${id}`);
    return response.json();
  }

  async updateUserAchievement(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/user_achievements/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteUserAchievement(id: string) {
    const response = await fetch(`${this.baseUrl}/user_achievements/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listUserAchievements() {
    const response = await fetch(`${this.baseUrl}/user_achievements`);
    return response.json();
  }
}

export const user_achievementsService = new UserAchievementService();
export default user_achievementsService;
