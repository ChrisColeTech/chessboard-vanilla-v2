import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

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

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
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
app.use('/api/learningPaths', LearningRouter);
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