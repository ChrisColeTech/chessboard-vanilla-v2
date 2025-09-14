// Generated service for Puzzle

class PuzzleService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createPuzzle(data: any) {
    const response = await fetch(`${this.baseUrl}/puzzles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getPuzzleById(id: string) {
    const response = await fetch(`${this.baseUrl}/puzzles/${id}`);
    return response.json();
  }

  async updatePuzzle(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/puzzles/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deletePuzzle(id: string) {
    const response = await fetch(`${this.baseUrl}/puzzles/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listPuzzles() {
    const response = await fetch(`${this.baseUrl}/puzzles`);
    return response.json();
  }
}

export const puzzlesService = new PuzzleService();
export default puzzlesService;
