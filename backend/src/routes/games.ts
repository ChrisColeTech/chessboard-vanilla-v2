import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { GameService } from '../services/gameService';
import { CreateGameRequest, UpdateGameRequest } from '../models/Game';

const router = Router();
const gameService = new GameService();


// GET /reviews - Must be before /:id route
router.get('/reviews', authenticate, async (req: any, res) => {
  try {
    const result = await gameService.getGameReviews();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await gameService.getGames();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id - Must be after specific routes
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await gameService.getGameById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await gameService.createGame(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await gameService.updateGame(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /:id/analyze
router.post('/:id/analyze', authenticate, async (req: any, res) => {
  try {
    const result = await gameService.analyzeGame(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id/analysis
router.get('/:id/analysis', authenticate, async (req: any, res) => {
  try {
    const result = await gameService.getGameAnalysis(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;