import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { Database } from './utils/database';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet({
  contentSecurityPolicy: false,
  crossOriginEmbedderPolicy: false
}));

app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://localhost:5175'
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.path}`);
  next();
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '2.0.0'
  });
});

// API info
app.get('/api', (req, res) => {
  res.json({
    success: true,
    name: 'Chessboard Vanilla Backend V2',
    version: '2.0.0',
    description: 'Backend API with PostgreSQL and Generated Architecture',
    endpoints: {
      health: '/api/health'
    }
  });
});

// Test database connection
app.get('/api/test-db', async (req, res) => {
  try {
    const { Database } = require('./utils/database');
    const db = Database.getInstance();
    
    // Test basic connection
    const result = await db.query('SELECT COUNT(*) as puzzle_count FROM puzzles LIMIT 1');
    
    res.json({
      success: true,
      database_connected: true,
      puzzle_count: result.rows[0]?.puzzle_count || 0,
      timestamp: new Date().toISOString()
    });
  } catch (error: any) {
    res.json({
      success: false,
      database_connected: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Routes
import authRoutes from './routes/auth';
import puzzleRoutes from './routes/puzzles';
import gameRoutes from './routes/games';
import userRoutes from './routes/users';
import statsRoutes from './routes/stats';
import learningPathRoutes from './routes/learning_paths';
import tutorialRoutes from './routes/tutorials';

app.use('/api/auth', authRoutes);
app.use('/api/puzzles', puzzleRoutes);
app.use('/api/games', gameRoutes);
app.use('/api/users', userRoutes);
app.use('/api/stats', statsRoutes);
app.use('/api/learning', learningPathRoutes);
app.use('/api/tutorials', tutorialRoutes);

// Serve built frontend (for Railway deployment)
import path from 'path';
const frontendPath = path.join(__dirname, '../../frontend/dist');
app.use(express.static(frontendPath));

// Frontend routing fallback (must come after API routes)
app.get('*', (req, res) => {
  // Don't serve index.html for API routes that return 404
  if (req.path.startsWith('/api/')) {
    return res.status(404).json({
      success: false,
      error: 'API endpoint not found'
    });
  }
  // Serve React app for all other routes
  res.sendFile(path.join(frontendPath, 'index.html'));
});

// 404 handler for API routes only
app.use('/api/*', (req, res) => {
  res.status(404).json({
    success: false,
    error: 'API endpoint not found'
  });
});

// Error handler
app.use((err: any, req: any, res: any, next: any) => {
  console.error('Error:', err);
  
  if (!res.headersSent) {
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      timestamp: new Date().toISOString()
    });
  }
});

// Start server
async function startServer() {
  try {
    console.log('Starting Chessboard Vanilla Backend V2...');
    
    // Initialize database
    const db = Database.getInstance();
    await db.connect();
    console.log('✓ Database connected');

    // Start server
    const server = app.listen(PORT, () => {
      console.log(`✓ Server running on port ${PORT}`);
      console.log(`✓ Health check: http://localhost:${PORT}/api/health`);
      console.log(`✓ API info: http://localhost:${PORT}/api`);
    });

    // Graceful shutdown
    process.on('SIGTERM', async () => {
      console.log('SIGTERM received, shutting down gracefully...');
      server.close(async () => {
        await db.close();
        process.exit(0);
      });
    });

    process.on('SIGINT', async () => {
      console.log('SIGINT received, shutting down gracefully...');
      server.close(async () => {
        await db.close();
        process.exit(0);
      });
    });

  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();

export default app;