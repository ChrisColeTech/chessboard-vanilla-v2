import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { TutorialService } from '../services/tutorialService';
import { CreateTutorialRequest, UpdateTutorialRequest } from '../models/Tutorial';

const router = Router();
const tutorialService = new TutorialService();


// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialService.getTutorials();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialService.getTutorialById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /:id/complete
router.post('/:id/complete', authenticate, async (req: any, res) => {
  try {
    const result = await tutorialService.completeTutorial(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;