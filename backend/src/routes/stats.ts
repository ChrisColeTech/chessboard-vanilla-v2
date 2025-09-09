import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { StatsService } from '../services/statsService';
import { CreateStatsRequest, UpdateStatsRequest } from '../models/Stats';

const router = Router();
const statsService = new StatsService();


// GET /overview
router.get('/overview', authenticate, async (req: any, res) => {
  try {
    const result = await statsService.getOverviewStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /puzzles
router.get('/puzzles', authenticate, async (req: any, res) => {
  try {
    const result = await statsService.getPuzzleStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /games
router.get('/games', authenticate, async (req: any, res) => {
  try {
    const result = await statsService.getGameStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /progress
router.get('/progress', authenticate, async (req: any, res) => {
  try {
    const result = await statsService.getProgressStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /performance
router.get('/performance', authenticate, async (req: any, res) => {
  try {
    const result = await statsService.getPerformanceStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /ratings
router.get('/ratings', authenticate, async (req: any, res) => {
  try {
    const result = await statsService.getRatingStats();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;