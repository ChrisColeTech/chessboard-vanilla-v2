// Generated service for UserSession

class UserSessionService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createUserSession(data: any) {
    const response = await fetch(`${this.baseUrl}/user_sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getUserSessionById(id: string) {
    const response = await fetch(`${this.baseUrl}/user_sessions/${id}`);
    return response.json();
  }

  async updateUserSession(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/user_sessions/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteUserSession(id: string) {
    const response = await fetch(`${this.baseUrl}/user_sessions/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listUserSessions() {
    const response = await fetch(`${this.baseUrl}/user_sessions`);
    return response.json();
  }
}

export const user_sessionsService = new UserSessionService();
export default user_sessionsService;
