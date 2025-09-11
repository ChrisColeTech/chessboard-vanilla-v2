import React from 'react';

interface PokerOverlayProps {
  className?: string;
  style?: React.CSSProperties;
}

export const PokerOverlay: React.FC<PokerOverlayProps> = ({ className, style }) => {
  return (
    <div
      className={className}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        borderRadius: '20px',
        background: 'linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.05) 100%)',
        backdropFilter: 'blur(1px)',
        pointerEvents: 'none',
        zIndex: 1,
        ...style
      }}
    />
  );
};