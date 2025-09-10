import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { HistoricgameService } from '../services/historicgameService';
import { CreateHistoricgameRequest, UpdateHistoricgameRequest } from '../models/Historicgame';

const router = Router();
const historicgameService = new HistoricgameService();


// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await historicgameService.getAllHistoricGames();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await historicgameService.getGameById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /search
router.get('/search', authenticate, async (req: any, res) => {
  try {
    const result = await historicgameService.searchGames();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /player/:player
router.get('/player/:player', authenticate, async (req: any, res) => {
  try {
    const result = await historicgameService.getGamesByPlayer();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await historicgameService.createHistoricgame(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await historicgameService.updateHistoricgame(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await historicgameService.deleteHistoricgame(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;