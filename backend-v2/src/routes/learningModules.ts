import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { LearningmoduleService } from '../services/learningmoduleService';
import { CreateLearningmoduleRequest, UpdateLearningmoduleRequest } from '../models/Learningmodule';

const router = Router();
const learningmoduleService = new LearningmoduleService();


// GET /path/:pathId
router.get('/path/:pathId', authenticate, async (req: any, res) => {
  try {
    const result = await learningmoduleService.getModulesByPath();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningmoduleService.getModuleById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /:id/complete
router.post('/:id/complete', authenticate, async (req: any, res) => {
  try {
    const result = await learningmoduleService.completeModule(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await learningmoduleService.getAllLearning_modules();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await learningmoduleService.createLearningmodule(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningmoduleService.updateLearningmodule(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await learningmoduleService.deleteLearningmodule(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;