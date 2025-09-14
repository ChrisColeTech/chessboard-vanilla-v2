import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { UserAchievementService } from '../services/user_achievementsService';
import { UserAchievementResponse, CreateUserAchievementRequest, UpdateUserAchievementRequest } from '../models/UserAchievement';

const router = Router();
const user_achievementsService = new UserAchievementService();

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await user_achievementsService.createUserAchievement(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_achievementsService.getUserAchievementById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_achievementsService.updateUserAchievement(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_achievementsService.deleteUserAchievement(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await user_achievementsService.listUserAchievements();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /user/:userId
router.get('/user/:userId', authenticate, async (req: any, res) => {
  try {
    const result = await user_achievementsService.getUserAchievementsByUser(req.params.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /achievement/:achievementId
router.get('/achievement/:achievementId', authenticate, async (req: any, res) => {
  try {
    const result = await user_achievementsService.getUserAchievementsByAchievement(req.params.achievementId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;