// Generated service for UserProfile

class UserProfileService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createUserProfile(data: any) {
    const response = await fetch(`${this.baseUrl}/user_profiles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getUserProfileById(id: string) {
    const response = await fetch(`${this.baseUrl}/user_profiles/${id}`);
    return response.json();
  }

  async updateUserProfile(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/user_profiles/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteUserProfile(id: string) {
    const response = await fetch(`${this.baseUrl}/user_profiles/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listUserProfiles() {
    const response = await fetch(`${this.baseUrl}/user_profiles`);
    return response.json();
  }
}

export const user_profilesService = new UserProfileService();
export default user_profilesService;
