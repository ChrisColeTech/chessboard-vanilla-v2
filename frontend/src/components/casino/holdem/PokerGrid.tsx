import React from 'react';

interface PokerGridProps {
  // Add any props we might need later for interaction, styling, etc.
  className?: string;
  style?: React.CSSProperties;
}

export const PokerGrid: React.FC<PokerGridProps> = ({ className, style }) => {
  return (
    <div
      className={className}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'radial-gradient(ellipse at center, #0f5132 0%, #1a5c37 40%, #0d4a2b 100%)',
        border: '3px solid #8b4513',
        boxShadow: 'inset 0 0 20px rgba(0,0,0,0.3), 0 4px 20px rgba(0,0,0,0.2)',
        borderRadius: '0px',
        ...style
      }}
    />
  );
};