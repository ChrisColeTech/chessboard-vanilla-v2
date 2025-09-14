import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { UserContentProgressService } from '../services/user_content_progressService';
import { UserContentProgressResponse, CreateUserContentProgressRequest, UpdateUserContentProgressRequest } from '../models/UserContentProgress';

const router = Router();
const user_content_progressService = new UserContentProgressService();

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await user_content_progressService.createUserContentProgress(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_content_progressService.getUserContentProgressById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_content_progressService.updateUserContentProgress(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_content_progressService.deleteUserContentProgress(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await user_content_progressService.listUserContentProgress();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /user/:userId
router.get('/user/:userId', authenticate, async (req: any, res) => {
  try {
    const result = await user_content_progressService.getUserContentProgressByUser(req.params.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /content/:contentId
router.get('/content/:contentId', authenticate, async (req: any, res) => {
  try {
    const result = await user_content_progressService.getUserContentProgressByContent(req.params.contentId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;