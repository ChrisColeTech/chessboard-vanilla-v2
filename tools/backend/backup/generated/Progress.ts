import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { ProgressService } from '../services/progressService';
import { CreateProgressRequest, UpdateProgressRequest } from '../models/Progress';

const router = Router();
const progressService = new ProgressService();


// GET /user/:userId
router.get('/user/:userId', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.getUserProgress();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /update
router.put('/update', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.updateProgress(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /stats/:userId
router.get('/stats/:userId', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.getProgressStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.getAllProgress();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.getProgressById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.createProgress(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.updateProgress(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await progressService.deleteProgress(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;