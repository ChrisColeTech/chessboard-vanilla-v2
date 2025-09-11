import { Crown, RotateCcw } from 'lucide-react';
import { useUIClickSound } from '../../hooks/audio/useUIClickSound';

interface CheckmateModalProps {
  isOpen: boolean;
  winner: 'white' | 'black';
  onReset: () => void;
}

export function CheckmateModal({ isOpen, winner, onReset }: CheckmateModalProps) {
  const { playUIClick } = useUIClickSound();
  
  const handleReset = () => {
    playUIClick('Play Again');
    onReset();
  };
  
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop modal-backdrop-dark">
      <div className="modal-content modal-content-sm">
        <div className="text-center space-y-6">
          {/* Winner Crown */}
          <div className="flex justify-center">
            <div className="modal-icon-container-lg">
              <Crown className="w-8 h-8 text-primary" />
            </div>
          </div>

          {/* Title */}
          <div>
            <h2 className="text-2xl font-bold text-foreground mb-2">Checkmate!</h2>
            <p className="text-lg text-muted-foreground capitalize">
              {winner} wins the game
            </p>
          </div>

          {/* Reset Button */}
          <button
            onClick={handleReset}
            className="w-full flex items-center justify-center gap-3 px-6 py-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg font-semibold transition-colors"
          >
            <RotateCcw className="w-5 h-5" />
            Play Again
          </button>
        </div>
      </div>
    </div>
  );
}