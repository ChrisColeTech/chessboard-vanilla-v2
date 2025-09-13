import React from "react";
import { useSpring, animated } from '@react-spring/web';
import { useLoadingProgressActions } from '../../hooks/splash/useLoadingProgressActions';

interface LoadingProgressPageProps {
  variant?: 'in-app' | 'modal';
}

const LoadingProgressPage: React.FC<LoadingProgressPageProps> = ({ variant = 'in-app' }) => {
  const { animationKey, overallProgress, currentStatus } = useLoadingProgressActions();
  
  const containerClass = variant === 'modal' 
    ? 'splash-container splash-modal splash-fade-in'
    : 'splash-container splash-in-app splash-fade-in';

  // Floating crown animation
  const floatingCrown = useSpring({
    from: { transform: 'translateY(-3px)' },
    to: async (next) => {
      while (true) {
        await next({ transform: 'translateY(3px)' });
        await next({ transform: 'translateY(-3px)' });
      }
    },
    config: { tension: 140, friction: 22 },
    reset: animationKey > 0
  });

  return (
    <div className={containerClass}>
      <div className="splash-center-content">
        {/* Floating Crown - Primary focal element */}
        <animated.div 
          style={floatingCrown}
          className="floating-crown floating-crown-glow"
        >
          ♔
        </animated.div>
        
        {/* App Title - Below crown */}
        <h1 className="splash-title">Master Chess Training</h1>
        
        {/* Loading Status */}
        <div className="loading-status">
          {currentStatus}
        </div>
        
        {/* Single Progress Bar */}
        <div className="progress-container">
          <div 
            className="progress-bar"
            style={{ width: `${overallProgress}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export { LoadingProgressPage };