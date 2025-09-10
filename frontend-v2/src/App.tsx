import './App.css'
import { useState, useEffect } from 'react';
import { AuthAPIClient } from './clients/AuthAPIClient';

// Import our generated components
import { AchievementComponent } from './components/achievements'
import { AIOpponentComponent } from './components/ai-opponents'
import { AnalysisComponent } from './components/analysis'
import { AnalyticsComponent } from './components/analytics'
import { AuthComponent } from './components/auth'
import { EndgameComponent } from './components/endgames'
import { GameReviewComponent } from './components/game-reviews'
import { GameComponent } from './components/games'
import { HelpComponent } from './components/help'
import { HistoricGameComponent } from './components/historic-games'
import { LearningPathComponent } from './components/learning'
import { LearningModuleComponent } from './components/learning-modules'
import { OpeningComponent } from './components/openings'
import { ProfileComponent } from './components/profiles'
import { ProgressComponent } from './components/progress'
import { PuzzleAttemptComponent } from './components/puzzle-attempts'
import { PuzzleSourceComponent } from './components/puzzle-sources'
import { PuzzleComponent } from './components/puzzles'
import { SessionComponent } from './components/sessions'
import { StatsComponent } from './components/stats'
import { StudyPlanComponent } from './components/study-plans'
import { SubscriptionComponent } from './components/subscriptions'
import { TutorialStepComponent } from './components/tutorial-steps'
import { TutorialComponent } from './components/tutorials'
import { UserComponent } from './components/users'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<any>(null);
  const authClient = new AuthAPIClient();

  // Check if user is already logged in on app start
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      setIsLoggedIn(true);
      // Optionally fetch user info
      authClient.getCurrentUser().then(response => {
        if (response.success) {
          setUser(response.data);
        }
      }).catch(() => {
        // Token might be invalid, clear it
        localStorage.removeItem('auth_token');
        setIsLoggedIn(false);
      });
    }
  }, []);

  const handleLogin = async () => {
    setLoading(true);
    try {
      // Login with demo credentials - try admin first, then test user
      let response;
      try {
        response = await authClient.login({
          email: 'admin@admin.com',
          password: 'admin'
        });
      } catch (err) {
        // Fallback to test user
        response = await authClient.login({
          email: 'test3@example.com',
          password: 'password123'
        });
      }
      
      if (response.success && response.data?.token) {
        localStorage.setItem('auth_token', response.data.token);
        setIsLoggedIn(true);
        setUser(response.data.user);
        console.log('Login successful:', response.data);
      } else {
        console.error('Login failed:', response);
        alert('Login failed. Please check your credentials.');
      }
    } catch (error: any) {
      console.error('Login error:', error);
      alert('Login error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    setIsLoggedIn(false);
    setUser(null);
  };

  if (!isLoggedIn) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Chess Platform - Login Required</h1>
          <p>Please log in to access the application</p>
          <div style={{ marginTop: '2rem' }}>
            <button 
              onClick={handleLogin}
              disabled={loading}
              style={{
                padding: '12px 24px',
                fontSize: '16px',
                backgroundColor: loading ? '#ccc' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'default' : 'pointer'
              }}
            >
              {loading ? 'Logging in...' : 'Login with Demo Account'}
            </button>
            <p style={{ fontSize: '14px', color: '#666', marginTop: '1rem' }}>
              Demo credentials: admin@admin.com / admin (or test3@example.com / password123)
            </p>
          </div>
        </header>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chess Platform - Domain-Driven Frontend</h1>
        <p>Generated frontend with complete API contract coverage</p>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
          <span>Welcome{user ? `, ${user.name || user.email}` : ''}!</span>
          <button 
            onClick={handleLogout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Logout
          </button>
        </div>
      </header>
      
      <main className="App-main">
        <div className="domain-section">
          <h2>Achievements Domain</h2>
                    <AchievementComponent />
        </div>
        <div className="domain-section">
          <h2>AiOpponents Domain</h2>
                    <AIOpponentComponent />
        </div>
        <div className="domain-section">
          <h2>Analysis Domain</h2>
                    <AnalysisComponent />
        </div>
        <div className="domain-section">
          <h2>Analytics Domain</h2>
                    <AnalyticsComponent />
        </div>
        <div className="domain-section">
          <h2>Auth Domain</h2>
                    <AuthComponent />
        </div>
        <div className="domain-section">
          <h2>Endgames Domain</h2>
                    <EndgameComponent />
        </div>
        <div className="domain-section">
          <h2>GameReviews Domain</h2>
                    <GameReviewComponent />
        </div>
        <div className="domain-section">
          <h2>Games Domain</h2>
                    <GameComponent />
        </div>
        <div className="domain-section">
          <h2>Help Domain</h2>
                    <HelpComponent />
        </div>
        <div className="domain-section">
          <h2>HistoricGames Domain</h2>
                    <HistoricGameComponent />
        </div>
        <div className="domain-section">
          <h2>Learning Domain</h2>
                    <LearningPathComponent />
        </div>
        <div className="domain-section">
          <h2>LearningModules Domain</h2>
                    <LearningModuleComponent />
        </div>
        <div className="domain-section">
          <h2>Openings Domain</h2>
                    <OpeningComponent />
        </div>
        <div className="domain-section">
          <h2>Profiles Domain</h2>
                    <ProfileComponent />
        </div>
        <div className="domain-section">
          <h2>Progress Domain</h2>
                    <ProgressComponent />
        </div>
        <div className="domain-section">
          <h2>PuzzleAttempts Domain</h2>
                    <PuzzleAttemptComponent />
        </div>
        <div className="domain-section">
          <h2>PuzzleSources Domain</h2>
                    <PuzzleSourceComponent />
        </div>
        <div className="domain-section">
          <h2>Puzzles Domain</h2>
                    <PuzzleComponent />
        </div>
        <div className="domain-section">
          <h2>Sessions Domain</h2>
                    <SessionComponent />
        </div>
        <div className="domain-section">
          <h2>Stats Domain</h2>
                    <StatsComponent />
        </div>
        <div className="domain-section">
          <h2>StudyPlans Domain</h2>
                    <StudyPlanComponent />
        </div>
        <div className="domain-section">
          <h2>Subscriptions Domain</h2>
                    <SubscriptionComponent />
        </div>
        <div className="domain-section">
          <h2>TutorialSteps Domain</h2>
                    <TutorialStepComponent />
        </div>
        <div className="domain-section">
          <h2>Tutorials Domain</h2>
                    <TutorialComponent />
        </div>
        <div className="domain-section">
          <h2>Users Domain</h2>
                    <UserComponent />
        </div>
      </main>
    </div>
  )
}

export default App