import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { EndgameService } from '../services/endgameService';
import { CreateEndgameRequest, UpdateEndgameRequest } from '../models/Endgame';

const router = Router();
const endgameService = new EndgameService();


// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await endgameService.getAllEndgames();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await endgameService.getEndgameById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /category/:category
router.get('/category/:category', authenticate, async (req: any, res) => {
  try {
    const result = await endgameService.getEndgamesByCategory();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await endgameService.createEndgame(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await endgameService.updateEndgame(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await endgameService.deleteEndgame(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;