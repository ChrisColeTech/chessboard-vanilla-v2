import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { LearningpathService } from '../services/learningpathService';
import { CreateLearningpathRequest, UpdateLearningpathRequest } from '../models/Learningpath';

const router = Router();
const learningpathService = new LearningpathService();


// GET /paths
router.get('/paths', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.getLearningPaths();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /paths/:id
router.get('/paths/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.getLearningPathById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /paths/:id/enroll
router.post('/paths/:id/enroll', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.enrollInPath(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /paths/:id/progress
router.put('/paths/:id/progress', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.updateProgress(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.getAllLearning_paths();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.getLearningpathById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.createLearningpath(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.updateLearningpath(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.deleteLearningpath(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;