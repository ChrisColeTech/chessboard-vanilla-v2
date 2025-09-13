import React from 'react'
import { useSpring, animated } from '@react-spring/web'
import { useAppInitialization } from '../../hooks/core/useAppInitialization'

interface FunctionalSplashPageProps {
  variant?: 'in-app' | 'modal'
}

export const FunctionalSplashPage: React.FC<FunctionalSplashPageProps> = ({ 
  variant = 'in-app' 
}) => {
  const {
    progress,
    status,
    stage,
    error,
    isInitializing,
    skipInitialization,
    retryInitialization,
    initializationTime
  } = useAppInitialization()

  // Container class based on variant
  const containerClass = variant === 'modal' 
    ? 'splash-container splash-modal splash-fade-in'
    : 'splash-container splash-in-app splash-fade-in'

  // Crown floating animation
  const crownAnimation = useSpring({
    transform: 'translateY(-20px)',
    from: { transform: 'translateY(0px)' },
    config: { tension: 120, friction: 50 },
    loop: { reverse: true }
  })

  // Progress bar animation
  const progressAnimation = useSpring({
    width: `${progress}%`,
    from: { width: '0%' },
    config: { tension: 180, friction: 20 }
  })

  // Status text animation - changes based on stage
  const statusAnimation = useSpring({
    opacity: isInitializing ? 1 : 0.7,
    transform: isInitializing ? 'translateY(0px)' : 'translateY(5px)',
    config: { tension: 200, friction: 25 }
  })

  // Error state animation
  const errorAnimation = useSpring({
    opacity: error ? 1 : 0,
    transform: error ? 'scale(1)' : 'scale(0.95)',
    config: { tension: 300, friction: 30 }
  })

  // Get stage-specific styling
  const getStageColor = () => {
    switch (stage) {
      case 'critical': return 'text-amber-400'
      case 'important': return 'text-blue-400'
      case 'background': return 'text-green-400'
      case 'completed': return 'text-green-500'
      case 'error': return 'text-red-400'
      case 'skipped': return 'text-gray-400'
      default: return 'text-white'
    }
  }

  const getProgressColor = () => {
    if (error) return 'bg-red-500'
    if (progress >= 100) return 'bg-green-500'
    if (stage === 'critical') return 'bg-amber-500'
    if (stage === 'important') return 'bg-blue-500'
    if (stage === 'background') return 'bg-green-400'
    return 'bg-white'
  }

  return (
    <div className={containerClass}>
      <div className="splash-center-content">
        {/* Floating Crown */}
        <animated.div style={crownAnimation} className="text-center mb-8">
          <div className="text-8xl crown-glow">♔</div>
        </animated.div>

        {/* Brand Title */}
        <h1 className="splash-title text-center mb-2">
          Master Chess Training
        </h1>
        
        <p className="splash-subtitle text-center mb-8 opacity-80">
          Professional Chess Education Platform
        </p>

        {/* Real Progress Section */}
        <div className="w-full max-w-md mx-auto">
          {/* Progress Bar */}
          <div className="bg-white/10 rounded-full h-2 mb-4 overflow-hidden">
            <animated.div 
              style={progressAnimation}
              className={`h-full rounded-full transition-colors duration-500 ${getProgressColor()}`}
            />
          </div>

          {/* Status Text */}
          <animated.div style={statusAnimation}>
            <p className={`text-center text-sm transition-colors duration-300 ${getStageColor()}`}>
              {status}
            </p>
            
            {/* Progress Percentage */}
            <p className="text-center text-xs opacity-60 mt-1">
              {Math.round(progress)}% • Stage: {stage}
            </p>

            {/* Timing Info (dev mode) */}
            {initializationTime > 0 && (
              <p className="text-center text-xs opacity-40 mt-1">
                Completed in {initializationTime}ms
              </p>
            )}
          </animated.div>

          {/* Error State */}
          {error && (
            <animated.div style={errorAnimation} className="mt-6">
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                <p className="text-red-400 text-sm text-center mb-3">
                  {error}
                </p>
                <div className="flex gap-2 justify-center">
                  <button
                    onClick={retryInitialization}
                    className="px-4 py-2 bg-red-500 text-white text-xs rounded-md hover:bg-red-600 transition-colors"
                  >
                    Retry Loading
                  </button>
                  <button
                    onClick={skipInitialization}
                    className="px-4 py-2 bg-gray-600 text-white text-xs rounded-md hover:bg-gray-700 transition-colors"
                  >
                    Continue Anyway
                  </button>
                </div>
              </div>
            </animated.div>
          )}

          {/* Skip Option (for power users) */}
          {isInitializing && !error && progress < 50 && (
            <div className="mt-6 text-center">
              <button
                onClick={skipInitialization}
                className="text-xs opacity-50 hover:opacity-80 transition-opacity underline"
              >
                Skip loading (advanced users)
              </button>
            </div>
          )}
        </div>

        {/* Real Loading Stages Indicator */}
        <div className="mt-8 flex justify-center gap-2">
          {['initialization', 'critical', 'important', 'background'].map((stageName, index) => (
            <div
              key={stageName}
              className={`w-2 h-2 rounded-full transition-all duration-500 ${
                stage === stageName 
                  ? 'bg-white scale-125' 
                  : progress > (index * 25) 
                    ? 'bg-white/60' 
                    : 'bg-white/20'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}