// CRITICAL: StrictMode temporarily disabled for Web Worker compatibility
// Based on Document 24 Lesson #2: React StrictMode vs Workers
// StrictMode causes double-mounting in development, destroying workers before init
import { createRoot } from 'react-dom/client'
import './index.css'
// Import theme CSS files directly
import './styles/organized_themes/themes-base.css'
import './styles/organized_themes/themes-professional.css'
import './styles/organized_themes/themes-gaming.css'
import './styles/organized_themes/themes-effects.css'
// Import splash screen styles
import './styles/splash.css'
// Import background effects registry to initialize effects
import './services/core/backgroundEffectsRegistry'
import App from './App.tsx'
import withSplashScreen from './components/splash/withSplashScreen'

// Wrap App with splash screen HOC
const AppWithSplash = withSplashScreen(App);

createRoot(document.getElementById('root')!).render(
  // Temporarily disable StrictMode for Stockfish worker compatibility
  // <StrictMode>
    <AppWithSplash />
  // </StrictMode>
)
