import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import swaggerUi from 'swagger-ui-express';
import * as fs from 'fs';
import * as path from 'path';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Request logging middleware
app.use((req, res, next) => {
  console.log(`📥 ${new Date().toISOString()} - ${req.method} ${req.path}`);
  if (req.body && Object.keys(req.body).length > 0) {
    console.log(`   Body:`, JSON.stringify(req.body, null, 2));
  }
  if (req.query && Object.keys(req.query).length > 0) {
    console.log(`   Query:`, JSON.stringify(req.query, null, 2));
  }
  next();
});

// CORS Configuration
const corsOptions = {
  origin: [
    'http://localhost:5173',
    'http://localhost:3000',
    'https://chessboard-vanilla-v2.onrender.com',
    // Add any other domains you need
  ],
  credentials: true,
  optionsSuccessStatus: 200
};

// Load comprehensive pre-generated OpenAPI specification
const generatedSpecPath = path.join(__dirname, '..', 'generated_swagger.json');
const generatedSpec = JSON.parse(fs.readFileSync(generatedSpecPath, 'utf8'));

// Configure the spec with correct server URLs
const specs = {
  ...generatedSpec,
  servers: [
    {
      url: process.env.NODE_ENV === 'production' 
        ? 'https://chessboard-vanilla-v2.onrender.com'
        : 'http://localhost:3001',
      description: process.env.NODE_ENV === 'production' ? 'Production server' : 'Development server'
    }
  ]
};

console.log(`📋 Loaded ${Object.keys(generatedSpec.paths || {}).length} endpoints from comprehensive spec`);

// Middleware
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Swagger Documentation Routes
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'Chessboard V2 API',
  swaggerOptions: {
    defaultModelsExpandDepth: -1,
    docExpansion: 'list',
    filter: true,
    showRequestDuration: true
  }
}));

// Swagger JSON endpoint  
app.get('/api-docs.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.send(specs);
});

// Redirect root to API documentation
app.get('/', (req, res) => {
  res.redirect('/api-docs');
});

// Health check endpoint
/**
 * @swagger
 * /health:
 *   get:
 *     tags: [System]
 *     summary: Health check endpoint
 *     description: Returns the current status and timestamp of the API
 *     responses:
 *       200:
 *         description: API is healthy
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: OK
 *                 timestamp:
 *                   type: string
 *                   format: date-time
 */
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Import route handlers
import UsersRouter from './routes/users';
import PuzzlesRouter from './routes/puzzles';
import GamesRouter from './routes/games';
import StatsRouter from './routes/stats';
import LearningRouter from './routes/learningPaths';
import TutorialsRouter from './routes/tutorials';
import AuthRouter from './routes/auth';
import SessionsRouter from './routes/sessions';
import AchievementsRouter from './routes/achievements';
import ProgressRouter from './routes/progress';
import OpeningsRouter from './routes/openings';
import AnalysisRouter from './routes/analysis';
import AiOpponentsRouter from './routes/aiOpponents';
import AnalyticsRouter from './routes/analytics';
import ProfilesRouter from './routes/profiles';
import EndgamesRouter from './routes/endgames';
import GameReviewsRouter from './routes/gameReviews';
import HistoricGamesRouter from './routes/historicGames';
import PuzzleAttemptsRouter from './routes/puzzleAttempts';
import PuzzleSourcesRouter from './routes/puzzleSources';
import LearningModulesRouter from './routes/learningModules';
import TutorialStepsRouter from './routes/tutorialSteps';
import StudyPlansRouter from './routes/studyPlans';
import HelpRouter from './routes/help';
import SubscriptionsRouter from './routes/subscriptions';

// Register API routes
app.use('/api/users', UsersRouter);
app.use('/api/puzzles', PuzzlesRouter);
app.use('/api/games', GamesRouter);
app.use('/api/stats', StatsRouter);
app.use('/api/learning', LearningRouter);
app.use('/api/tutorials', TutorialsRouter);
app.use('/api/auth', AuthRouter);
app.use('/api/sessions', SessionsRouter);
app.use('/api/achievements', AchievementsRouter);
app.use('/api/progress', ProgressRouter);
app.use('/api/openings', OpeningsRouter);
app.use('/api/analysis', AnalysisRouter);
app.use('/api/aiOpponents', AiOpponentsRouter);
app.use('/api/analytics', AnalyticsRouter);
app.use('/api/profiles', ProfilesRouter);
app.use('/api/endgames', EndgamesRouter);
app.use('/api/gameReviews', GameReviewsRouter);
app.use('/api/historicGames', HistoricGamesRouter);
app.use('/api/puzzleAttempts', PuzzleAttemptsRouter);
app.use('/api/puzzleSources', PuzzleSourcesRouter);
app.use('/api/learningModules', LearningModulesRouter);
app.use('/api/tutorialSteps', TutorialStepsRouter);
app.use('/api/studyPlans', StudyPlansRouter);
app.use('/api/help', HelpRouter);
app.use('/api/subscriptions', SubscriptionsRouter);

// Response logging middleware
app.use((req, res, next) => {
  const originalSend = res.send;
  res.send = function(data) {
    console.log(`📤 ${new Date().toISOString()} - ${req.method} ${req.path} - ${res.statusCode}`);
    if (res.statusCode >= 400) {
      console.log(`   Error Response:`, data);
    }
    return originalSend.call(this, data);
  };
  next();
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('❌ Internal Error:', err);
  console.error('   Stack:', err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
  });
}

export default app;