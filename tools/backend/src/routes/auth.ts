import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { AuthService } from '../services/authService';
import { LoginRequest, RegisterRequest } from '../models/Auth';

const router = Router();
const authService = new AuthService();


// POST /register
router.post('/register', async (req: any, res) => {
  try {
    const result = await authService.register(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /login
router.post('/login', async (req: any, res) => {
  try {
    const result = await authService.login(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /me
router.get('/me', authenticate, async (req: any, res) => {
  try {
    const result = await authService.getCurrentUser(req.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /profile
router.put('/profile', authenticate, async (req: any, res) => {
  try {
    const result = await authService.updateProfile(req.userId, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /change-password
router.post('/change-password', authenticate, async (req: any, res) => {
  try {
    const result = await authService.changePassword(req.userId, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /verify-token
router.post('/verify-token', async (req: any, res) => {
  try {
    const result = await authService.verifyToken(req.body.token);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /forgot-password
router.post('/forgot-password', async (req: any, res) => {
  try {
    const result = await authService.forgotPassword(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /reset-password
router.post('/reset-password', async (req: any, res) => {
  try {
    const result = await authService.resetPassword(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /logout
router.post('/logout', async (req: any, res) => {
  try {
    const result = await authService.logout();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /check-email
router.post('/check-email', async (req: any, res) => {
  try {
    const result = await authService.checkEmailAvailability(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// POST /check-username
router.post('/check-username', async (req: any, res) => {
  try {
    const result = await authService.checkUsernameAvailability(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /delete-account
router.delete('/delete-account', authenticate, async (req: any, res) => {
  try {
    const result = await authService.deleteAccount(req.userId);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /health
router.get('/health', async (req: any, res) => {
  try {
    const result = await authService.healthCheck();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;