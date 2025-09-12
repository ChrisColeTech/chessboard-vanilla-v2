import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { LearningPathService } from '../services/learningpathService';
import { CreateLearningPathRequest, UpdateLearningPathRequest } from '../models/LearningPath';

const router = Router();
const learningpathService = new LearningPathService();


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
    const result = await learningpathService.enrollInPath(req.params.id, req.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /paths/:id/progress
router.put('/paths/:id/progress', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.updateProgress(req.params.id, req.userId, req.body);
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
    const result = await learningpathService.getLearningPathById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.createLearningPath(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.updateLearningPath(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningpathService.deleteLearningPath(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;