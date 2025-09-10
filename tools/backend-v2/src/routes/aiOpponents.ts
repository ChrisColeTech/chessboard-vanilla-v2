import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { AiopponentService } from '../services/aiopponentService';
import { CreateAiopponentRequest, UpdateAiopponentRequest } from '../models/Aiopponent';

const router = Router();
const aiopponentService = new AiopponentService();


// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await aiopponentService.getAllOpponents();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await aiopponentService.getOpponentById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /difficulty/:level
router.get('/difficulty/:level', authenticate, async (req: any, res) => {
  try {
    const result = await aiopponentService.getOpponentsByDifficulty();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await aiopponentService.createAiopponent(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await aiopponentService.updateAiopponent(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await aiopponentService.deleteAiopponent(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;