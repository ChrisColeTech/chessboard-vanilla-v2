import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { UserProfileService } from '../services/user_profilesService';
import { UserProfileResponse, CreateUserProfileRequest, UpdateUserProfileRequest } from '../models/UserProfile';

const router = Router();
const user_profilesService = new UserProfileService();

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await user_profilesService.createUserProfile(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_profilesService.getUserProfileById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_profilesService.updateUserProfile(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await user_profilesService.deleteUserProfile(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', authenticate, async (req: any, res) => {
  try {
    const result = await user_profilesService.listUserProfiles();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /user/:userId
router.get('/user/:userId', authenticate, async (req: any, res) => {
  try {
    const result = await user_profilesService.getUserProfileByUserId(req.params.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;