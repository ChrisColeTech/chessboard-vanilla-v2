// Generated service for HistoricGame

class HistoricGameService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createHistoricGame(data: any) {
    const response = await fetch(`${this.baseUrl}/historic_games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getHistoricGameById(id: string) {
    const response = await fetch(`${this.baseUrl}/historic_games/${id}`);
    return response.json();
  }

  async updateHistoricGame(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/historic_games/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deleteHistoricGame(id: string) {
    const response = await fetch(`${this.baseUrl}/historic_games/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listHistoricGames() {
    const response = await fetch(`${this.baseUrl}/historic_games`);
    return response.json();
  }
}

export const historic_gamesService = new HistoricGameService();
export default historic_gamesService;
