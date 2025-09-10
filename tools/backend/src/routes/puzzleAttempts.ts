import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { PuzzleattemptService } from '../services/puzzleattemptService';
import { CreatePuzzleattemptRequest, UpdatePuzzleattemptRequest } from '../models/Puzzleattempt';

const router = Router();
const puzzleattemptService = new PuzzleattemptService();


// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleattemptService.recordAttempt(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /user/:userId
router.get('/user/:userId', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleattemptService.getUserAttempts();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /puzzle/:puzzleId
router.get('/puzzle/:puzzleId', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleattemptService.getPuzzleAttempts();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleattemptService.getAllPuzzle_attempts();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleattemptService.getPuzzleattemptById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleattemptService.updatePuzzleattempt(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await puzzleattemptService.deletePuzzleattempt(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;