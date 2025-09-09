import React, { useState, useEffect } from "react";
import { useSpring, animated, useTrail } from '@react-spring/web';
import { useAnimatedSplashActions } from '../../hooks/splash/useAnimatedSplashActions';

interface AnimatedSplashPageProps {
  variant?: 'in-app' | 'modal';
}

interface ChessPiece {
  symbol: string;
  category: 'royalty' | 'major' | 'minor';
  position: number; // 0-4 for circle positions
}

const AnimatedSplashPage: React.FC<AnimatedSplashPageProps> = ({ variant = 'in-app' }) => {
  const { animationKey } = useAnimatedSplashActions();
  const [visiblePieces, setVisiblePieces] = useState<number>(0);
  
  const containerClass = variant === 'modal' 
    ? 'splash-container splash-modal splash-fade-in'
    : 'splash-container splash-in-app splash-fade-in';

  const chessPieces: ChessPiece[] = [
    { symbol: '♕', category: 'royalty', position: 0 }, // Top
    { symbol: '♖', category: 'major', position: 1 },   // Top-right
    { symbol: '♗', category: 'major', position: 2 },   // Bottom-right
    { symbol: '♘', category: 'minor', position: 3 },   // Bottom-left
    { symbol: '♙', category: 'minor', position: 4 }    // Top-left
  ];

  // Floating crown animation
  const floatingCrown = useSpring({
    from: { transform: 'translateY(-3px)' },
    to: async (next) => {
      while (true) {
        await next({ transform: 'translateY(3px)' });
        await next({ transform: 'translateY(-3px)' });
      }
    },
    config: { tension: 120, friction: 20 },
    reset: animationKey > 0
  });

  // Progressive piece revelation
  useEffect(() => {
    setVisiblePieces(0);
    
    const timeouts: NodeJS.Timeout[] = [];
    
    chessPieces.forEach((_, index) => {
      const timeout = setTimeout(() => {
        setVisiblePieces(index + 1);
      }, 600 + (index * 400));
      timeouts.push(timeout);
    });
    
    return () => timeouts.forEach(clearTimeout);
  }, [animationKey]);

  // Staggered text animations
  const textItems = ['Master Chess Training', 'Elevate Your Game'];
  const textTrail = useTrail(textItems.length, {
    from: { opacity: 0, transform: 'translateY(20px)' },
    to: { opacity: 1, transform: 'translateY(0px)' },
    config: { tension: 280, friction: 60 },
    delay: 2800, // After all pieces appear
    reset: animationKey > 0
  });

  return (
    <div className={containerClass}>
      <div className="splash-center-content">
        {/* Floating Crown - Primary focal point */}
        <animated.div 
          style={floatingCrown}
          className="floating-crown floating-crown-glow"
        >
          ♔
        </animated.div>
        
        {/* Floating Assembly Pieces */}
        <div className="floating-pieces-container">
          {chessPieces.map((piece, index) => (
            <div 
              key={piece.symbol}
              className={`floating-piece piece-${index + 1} ${
                index < visiblePieces ? 'animate' : ''
              }`}
            >
              {piece.symbol}
            </div>
          ))}
        </div>
        
        {/* Staggered text after assembly completes */}
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

export { AnimatedSplashPage };