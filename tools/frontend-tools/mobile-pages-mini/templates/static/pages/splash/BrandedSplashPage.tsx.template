import React from "react";
import { useSpring, animated } from '@react-spring/web';
import { useBrandedSplashActions } from '../../hooks/splash/useBrandedSplashActions';

interface BrandedSplashPageProps {
  variant?: 'in-app' | 'modal';
}

const BrandedSplashPage: React.FC<BrandedSplashPageProps> = ({ variant = 'in-app' }) => {
  const { animationKey } = useBrandedSplashActions();
  
  const containerClass = variant === 'modal' 
    ? 'splash-container splash-modal splash-fade-in'
    : 'splash-container splash-in-app splash-fade-in';

  // Dignified crown animation - slower, more refined
  const floatingCrown = useSpring({
    from: { transform: 'translateY(-2px)' },
    to: async (next) => {
      while (true) {
        await next({ transform: 'translateY(2px)' });
        await next({ transform: 'translateY(-2px)' });
      }
    },
    config: { tension: 80, friction: 30 }, // Slower, more dignified
    reset: animationKey > 0
  });

  return (
    <div className={containerClass}>
      <div className="splash-center-content">
        {/* Professional Crown - Primary institutional symbol */}
        <animated.div 
          style={floatingCrown}
          className="floating-crown floating-crown-glow"
        >
          ♔
        </animated.div>
        
        {/* Institutional Branding */}
        <div className="professional-branding">
          <h1 className="splash-title">Master Chess Training</h1>
          <div className="brand-divider"></div>
          <p className="splash-subtitle professional-tagline">Excellence in Chess Education</p>
        </div>
        
        {/* Credibility Indicators */}
        <div className="credibility-section">
          <p className="credibility-text">Professional Training Since 2020</p>
          <p className="credibility-text">Structured Learning Methods</p>
        </div>
      </div>
    </div>
  );
};

export { BrandedSplashPage };