// Generated service for Game

class GameService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createGame(data: any) {
    const response = await fetch(`${this.baseUrl}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getGameById(id: string) {
    const response = await fetch(`${this.baseUrl}/games/${id}`);
    return response.json();
  }

  async updateGame(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/games/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteGame(id: string) {
    const response = await fetch(`${this.baseUrl}/games/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listGames() {
    const response = await fetch(`${this.baseUrl}/games`);
    return response.json();
  }
}

export const gamesService = new GameService();
export default gamesService;
