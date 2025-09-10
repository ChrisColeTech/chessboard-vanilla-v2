import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { PuzzleService } from '../services/puzzleService';
import { CreatePuzzleRequest, UpdatePuzzleRequest } from '../models/Puzzle';

const router = Router();
const puzzleService = new PuzzleService();


// GET /next
router.get('/next', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getNextPuzzle(req.userId);
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

// GET /categories
router.get('/categories', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleCategories();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /history
router.get('/history', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleHistory(req.userId);
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

// GET /custom
router.get('/custom', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getCustomPuzzles();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getAllPuzzles();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.getPuzzleById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.createPuzzle(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.updatePuzzle(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleService.deletePuzzle(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;