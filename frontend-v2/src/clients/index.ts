// Domain-specific API clients
export { BaseAPIClient } from './BaseAPIClient';
export { UsersAPIClient } from './UsersAPIClient';
export { PuzzlesAPIClient } from './PuzzlesAPIClient';
export { GamesAPIClient } from './GamesAPIClient';
export { StatsAPIClient } from './StatsAPIClient';
export { LearningAPIClient } from './LearningAPIClient';
export { TutorialsAPIClient } from './TutorialsAPIClient';
export { AuthAPIClient } from './AuthAPIClient';
export { SessionsAPIClient } from './SessionsAPIClient';
export { AchievementsAPIClient } from './AchievementsAPIClient';
export { ProgressAPIClient } from './ProgressAPIClient';
export { OpeningsAPIClient } from './OpeningsAPIClient';
export { AnalysisAPIClient } from './AnalysisAPIClient';
export { AiOpponentsAPIClient } from './AiOpponentsAPIClient';
export { AnalyticsAPIClient } from './AnalyticsAPIClient';
export { ProfilesAPIClient } from './ProfilesAPIClient';
export { EndgamesAPIClient } from './EndgamesAPIClient';
export { GameReviewsAPIClient } from './GameReviewsAPIClient';
export { HistoricGamesAPIClient } from './HistoricGamesAPIClient';
export { PuzzleAttemptsAPIClient } from './PuzzleAttemptsAPIClient';
export { PuzzleSourcesAPIClient } from './PuzzleSourcesAPIClient';
export { LearningModulesAPIClient } from './LearningModulesAPIClient';
export { TutorialStepsAPIClient } from './TutorialStepsAPIClient';
export { StudyPlansAPIClient } from './StudyPlansAPIClient';
export { HelpAPIClient } from './HelpAPIClient';
export { SubscriptionsAPIClient } from './SubscriptionsAPIClient';

// Unified client for convenience (optional)
import { UsersAPIClient } from './UsersAPIClient';
import { PuzzlesAPIClient } from './PuzzlesAPIClient';
import { GamesAPIClient } from './GamesAPIClient';
import { StatsAPIClient } from './StatsAPIClient';
import { LearningAPIClient } from './LearningAPIClient';
import { TutorialsAPIClient } from './TutorialsAPIClient';
import { AuthAPIClient } from './AuthAPIClient';
import { SessionsAPIClient } from './SessionsAPIClient';
import { AchievementsAPIClient } from './AchievementsAPIClient';
import { ProgressAPIClient } from './ProgressAPIClient';
import { OpeningsAPIClient } from './OpeningsAPIClient';
import { AnalysisAPIClient } from './AnalysisAPIClient';
import { AiOpponentsAPIClient } from './AiOpponentsAPIClient';
import { AnalyticsAPIClient } from './AnalyticsAPIClient';
import { ProfilesAPIClient } from './ProfilesAPIClient';
import { EndgamesAPIClient } from './EndgamesAPIClient';
import { GameReviewsAPIClient } from './GameReviewsAPIClient';
import { HistoricGamesAPIClient } from './HistoricGamesAPIClient';
import { PuzzleAttemptsAPIClient } from './PuzzleAttemptsAPIClient';
import { PuzzleSourcesAPIClient } from './PuzzleSourcesAPIClient';
import { LearningModulesAPIClient } from './LearningModulesAPIClient';
import { TutorialStepsAPIClient } from './TutorialStepsAPIClient';
import { StudyPlansAPIClient } from './StudyPlansAPIClient';
import { HelpAPIClient } from './HelpAPIClient';
import { SubscriptionsAPIClient } from './SubscriptionsAPIClient';

export class APIClient {
  public readonly users = new UsersAPIClient();
  public readonly puzzles = new PuzzlesAPIClient();
  public readonly games = new GamesAPIClient();
  public readonly stats = new StatsAPIClient();
  public readonly learning = new LearningAPIClient();
  public readonly tutorials = new TutorialsAPIClient();
  public readonly auth = new AuthAPIClient();
  public readonly sessions = new SessionsAPIClient();
  public readonly achievements = new AchievementsAPIClient();
  public readonly progress = new ProgressAPIClient();
  public readonly openings = new OpeningsAPIClient();
  public readonly analysis = new AnalysisAPIClient();
  public readonly aiOpponents = new AiOpponentsAPIClient();
  public readonly analytics = new AnalyticsAPIClient();
  public readonly profiles = new ProfilesAPIClient();
  public readonly endgames = new EndgamesAPIClient();
  public readonly gameReviews = new GameReviewsAPIClient();
  public readonly historicGames = new HistoricGamesAPIClient();
  public readonly puzzleAttempts = new PuzzleAttemptsAPIClient();
  public readonly puzzleSources = new PuzzleSourcesAPIClient();
  public readonly learningModules = new LearningModulesAPIClient();
  public readonly tutorialSteps = new TutorialStepsAPIClient();
  public readonly studyPlans = new StudyPlansAPIClient();
  public readonly help = new HelpAPIClient();
  public readonly subscriptions = new SubscriptionsAPIClient();
}

// Singleton instance for convenience
export const apiClient = new APIClient();
export default apiClient;
