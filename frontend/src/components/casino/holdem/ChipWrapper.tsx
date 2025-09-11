import React from 'react';

interface Chip {
  id: string;
  value: number;
  color: string;
  x: number;
  y: number;
  stackIndex?: number;
}

interface ChipWrapperProps {
  chip: Chip;
  size: string;
  onDragStart?: (chip: Chip) => void;
  onChipClick?: (chip: Chip) => void;
  onDrop?: (chip: Chip) => void;
  setDraggedChip?: (chip: Chip | null) => void;
}

export const ChipWrapper: React.FC<ChipWrapperProps> = ({
  chip,
  size,
  onDragStart,
  onChipClick
}) => {
  const getChipColor = (value: number) => {
    switch (value) {
      case 1: return '#ffffff'; // White
      case 5: return '#ff0000'; // Red  
      case 10: return '#0000ff'; // Blue
      case 25: return '#008000'; // Green
      case 100: return '#000000'; // Black
      case 500: return '#800080'; // Purple
      default: return '#ffd700'; // Gold
    }
  };

  return (
    <div
      style={{
        position: 'absolute',
        left: `${chip.x}%`,
        top: `${chip.y}%`,
        width: size,
        height: size,
        transform: `translate(-50%, -50%) translateZ(${(chip.stackIndex || 0) * 2}px)`,
        pointerEvents: 'auto',
        cursor: 'pointer',
        zIndex: 3 + (chip.stackIndex || 0)
      }}
      onClick={() => onChipClick?.(chip)}
      onMouseDown={() => onDragStart?.(chip)}
    >
      <div
        style={{
          width: '100%',
          height: '100%',
          borderRadius: '50%',
          background: `radial-gradient(circle, ${getChipColor(chip.value)} 0%, ${chip.color} 100%)`,
          border: '3px solid rgba(255,255,255,0.3)',
          boxShadow: '0 2px 8px rgba(0,0,0,0.3), inset 0 1px 2px rgba(255,255,255,0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: `calc(${size} * 0.25)`,
          fontWeight: 'bold',
          color: chip.value === 1 ? '#000' : '#fff',
          textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
        }}
      >
        {chip.value}
      </div>
    </div>
  );
};