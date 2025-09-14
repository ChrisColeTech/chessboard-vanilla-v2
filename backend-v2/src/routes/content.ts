import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { ContentService } from '../services/contentService';
import { ContentResponse, CreateContentRequest, UpdateContentRequest } from '../models/Content';

const router = Router();
const contentService = new ContentService();

// POST /
router.post('/', authenticate, async (req: any, res) => {
  try {
    const result = await contentService.createContent(req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id
router.get('/:id', async (req: any, res) => {
  try {
    const result = await contentService.getContentById(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// PUT /:id
router.put('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await contentService.updateContent(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// DELETE /:id
router.delete('/:id', authenticate, async (req: any, res) => {
  try {
    const result = await contentService.deleteContent(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /
router.get('/', async (req: any, res) => {
  try {
    const result = await contentService.listContent();
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /type/:type
router.get('/type/:type', async (req: any, res) => {
  try {
    const result = await contentService.getContentByType(req.params.type);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /category/:category
router.get('/category/:category', async (req: any, res) => {
  try {
    const result = await contentService.getContentByCategory(req.params.category);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// GET /:id/children
router.get('/:id/children', async (req: any, res) => {
  try {
    const result = await contentService.getChildContent(req.params.id);
    res.json({ success: true, data: result });
  } catch (error: any) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default router;