import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { PuzzleService } from '../services/puzzleService';
import { CreatePuzzleRequest, UpdatePuzzleRequest } from '../models/Puzzle';

const router = Router();
const puzzleService = new PuzzleService();

// IMPORTANT: All specific routes MUST come before the /:id route
// Otherwise /:id will catch specific endpoints like /categories

// GET /random - Frontend expects this instead of /next
router.get('/random', async (req: any, res) => {
  try {
    const result = await puzzleService.getRandomPuzzle(req.query);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /themes - Frontend expects this instead of /categories
router.get('/themes', async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleThemes();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /stats - Puzzle statistics
router.get('/stats', async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /search - Search puzzles
router.get('/search', async (req: any, res) => {
  try {
    const result = await puzzleService.searchPuzzles(req.query);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /next - Must be before /:id route
router.get('/next', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getNextPuzzle(req.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /categories - Must be before /:id route
router.get('/categories', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleCategories();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /history - Must be before /:id route
router.get('/history', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleHistory(req.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /custom - Must be before /:id route
router.get('/custom', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getCustomPuzzles();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET / - Get multiple puzzles with filtering
router.get('/', async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzles(req.query);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id - Get specific puzzle by ID (MUST be last among GET routes)
router.get('/:id', async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /:id/solve
router.post('/:id/solve', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.solvePuzzle(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id/hint
router.get('/:id/hint', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleHint(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /custom
router.post('/custom', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.createCustomPuzzle(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;