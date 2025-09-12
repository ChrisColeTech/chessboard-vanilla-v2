import React from "react";
import { useSpring, animated, useTrail } from '@react-spring/web';
import { useMinimalSplashActions } from '../../hooks/splash/useMinimalSplashActions';

interface MinimalSplashPageProps {
  variant?: 'in-app' | 'modal';
}

const MinimalSplashPage: React.FC<MinimalSplashPageProps> = ({ variant = 'in-app' }) => {
  const { animationKey } = useMinimalSplashActions();
  
  const containerClass = variant === 'modal' 
    ? 'splash-container splash-modal splash-fade-in'
    : 'splash-container splash-in-app splash-fade-in';

  // Floating crown animation - simple and always visible
  const floatingCrown = useSpring({
    from: { transform: 'translateY(-4px)' },
    to: async (next) => {
      while (true) {
        await next({ transform: 'translateY(4px)' });
        await next({ transform: 'translateY(-4px)' });
      }
    },
    config: { tension: 150, friction: 25 },
    reset: animationKey > 0
  });

  // Staggered text animations using useTrail (modern 2024 approach)
  const textItems = ['Master Chess Training', 'Elevate Your Game'];
  const textTrail = useTrail(textItems.length, {
    from: { opacity: 0, transform: 'translateY(20px)' },
    to: { opacity: 1, transform: 'translateY(0px)' },
    config: { tension: 280, friction: 60 },
    delay: 300,
    reset: animationKey > 0
  });

  return (
    <div className={containerClass}>
      <div className="splash-center-content">
        {/* Floating Crown - Core concept element with crown glow */}
        <animated.div 
          style={floatingCrown}
          className="floating-crown-minimal floating-crown-glow"
        >
          ♔
        </animated.div>
        
        {/* Staggered text using useTrail */}
        {textTrail.map((style, index) => (
          <animated.div key={index} style={style}>
            {index === 0 ? (
              <h1 className="splash-title">{textItems[index]}</h1>
            ) : (
              <p className="splash-subtitle">{textItems[index]}</p>
            )}
          </animated.div>
        ))}
      </div>
    </div>
  );
};

export { MinimalSplashPage };