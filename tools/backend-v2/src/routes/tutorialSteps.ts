import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { TutorialstepService } from '../services/tutorialstepService';
import { CreateTutorialstepRequest, UpdateTutorialstepRequest } from '../models/Tutorialstep';

const router = Router();
const tutorialstepService = new TutorialstepService();


// GET /tutorial/:tutorialId
router.get('/tutorial/:tutorialId', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialstepService.getStepsByTutorial();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /:id/complete
router.post('/:id/complete', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialstepService.completeStep(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialstepService.getAllTutorial_steps();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialstepService.getTutorialstepById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialstepService.createTutorialstep(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialstepService.updateTutorialstep(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialstepService.deleteTutorialstep(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;