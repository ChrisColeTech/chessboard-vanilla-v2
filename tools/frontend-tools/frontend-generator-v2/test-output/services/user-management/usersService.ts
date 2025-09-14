// Generated service for User

class UserService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createUser(data: any) {
    const response = await fetch(`${this.baseUrl}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getUserById(id: string) {
    const response = await fetch(`${this.baseUrl}/users/${id}`);
    return response.json();
  }

  async updateUser(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteUser(id: string) {
    const response = await fetch(`${this.baseUrl}/users/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listUsers() {
    const response = await fetch(`${this.baseUrl}/users`);
    return response.json();
  }

  async updateUser(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }
}

export const usersService = new UserService();
export default usersService;
