// Generated service for PuzzleSource

class PuzzleSourceService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createPuzzleSource(data: any) {
    const response = await fetch(`${this.baseUrl}/puzzle_sources`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getPuzzleSourceById(id: string) {
    const response = await fetch(`${this.baseUrl}/puzzle_sources/${id}`);
    return response.json();
  }

  async updatePuzzleSource(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/puzzle_sources/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deletePuzzleSource(id: string) {
    const response = await fetch(`${this.baseUrl}/puzzle_sources/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listPuzzleSources() {
    const response = await fetch(`${this.baseUrl}/puzzle_sources`);
    return response.json();
  }
}

export const puzzle_sourcesService = new PuzzleSourceService();
export default puzzle_sourcesService;
