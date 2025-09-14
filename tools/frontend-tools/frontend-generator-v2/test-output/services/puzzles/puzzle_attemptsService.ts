// Generated service for PuzzleAttempt

class PuzzleAttemptService {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async createPuzzleAttempt(data: any) {
    const response = await fetch(`${this.baseUrl}/puzzle_attempts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async getPuzzleAttemptById(id: string) {
    const response = await fetch(`${this.baseUrl}/puzzle_attempts/${id}`);
    return response.json();
  }

  async updatePuzzleAttempt(id: string, data: any) {
    const response = await fetch(`${this.baseUrl}/puzzle_attempts/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async deletePuzzleAttempt(id: string) {
    const response = await fetch(`${this.baseUrl}/puzzle_attempts/${id}`, {
      method: 'DELETE'
    });
    return response.json();
  }

  async listPuzzleAttempts() {
    const response = await fetch(`${this.baseUrl}/puzzle_attempts`);
    return response.json();
  }
}

export const puzzle_attemptsService = new PuzzleAttemptService();
export default puzzle_attemptsService;
