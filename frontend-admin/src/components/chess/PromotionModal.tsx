import { Crown, X } from 'lucide-react';
import { getPieceImagePath, DEFAULT_PIECE_SET } from '../../constants/pieces.constants';
import { useUIClickSound } from '../../hooks/audio/useUIClickSound';

type PromotionPiece = 'queen' | 'rook' | 'bishop' | 'knight';
type PieceColor = 'white' | 'black';

interface PromotionModalProps {
  isOpen: boolean;
  color: PieceColor;
  onSelect: (piece: PromotionPiece) => void;
  onCancel: () => void;
}

// Use the default piece set for stability
const STABLE_PIECE_SET = DEFAULT_PIECE_SET;

const promotionPieces: Array<{ type: PromotionPiece; name: string }> = [
  { type: 'queen', name: 'Queen' },
  { type: 'rook', name: 'Rook' },
  { type: 'bishop', name: 'Bishop' },
  { type: 'knight', name: 'Knight' }
];

export function PromotionModal({ isOpen, color, onSelect, onCancel }: PromotionModalProps) {
  const { playUIClick } = useUIClickSound();
  
  const handleSelect = (pieceType: PromotionPiece) => {
    playUIClick(`Promote to ${pieceType}`);
    onSelect(pieceType);
  };
  
  const handleCancel = () => {
    playUIClick('Promotion Cancel');
    onCancel();
  };
  
  if (!isOpen) return null;

  console.log(`🔍 [PROMOTION] Modal opened for ${color} pieces using piece set: ${STABLE_PIECE_SET}`);
  
  // Log all paths being generated for debugging
  promotionPieces.forEach(piece => {
    const path = getPieceImagePath(color, piece.type, STABLE_PIECE_SET);
    console.log(`🔍 [PROMOTION] Generated path for ${color} ${piece.type}: ${path}`);
  });

  return (
    <div className="modal-backdrop modal-backdrop-padding">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 modal-backdrop-dark"
        onClick={handleCancel}
      />
      
      {/* Modal Content */}
      <div className="modal-content modal-content-md">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="modal-icon-container">
              <Crown className="w-5 h-5 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">Pawn Promotion</h3>
          </div>
          <button
            onClick={handleCancel}
            className="p-1 hover:bg-muted rounded-lg transition-colors"
            aria-label="Cancel promotion"
          >
            <X className="w-5 h-5 text-muted-foreground" />
          </button>
        </div>
        
        <p className="text-sm text-muted-foreground mb-6 capitalize">
          Choose a piece for your {color} pawn
        </p>

        {/* Piece Selection Grid */}
        <div className="grid-settings mb-6">
          {promotionPieces.map((pieceOption) => (
            <button
              key={pieceOption.type}
              onClick={() => handleSelect(pieceOption.type)}
              className="flex flex-col items-center gap-3 p-4 rounded-lg border border-border hover:border-primary/50 hover:bg-muted/30 transition-all group"
            >
              {/* Piece SVG with background for visibility */}
              <div className="w-16 h-16 flex items-center justify-center rounded-lg border border-border/50 bg-accent">
                <img
                  src={getPieceImagePath(color, pieceOption.type, STABLE_PIECE_SET)}
                  alt={`${color} ${pieceOption.type}`}
                  className="w-12 h-12 object-contain group-hover:scale-110 transition-transform"
                  onError={(e) => {
                    const imagePath = getPieceImagePath(color, pieceOption.type, STABLE_PIECE_SET);
                    console.error(`❌ [PROMOTION] Failed to load piece image:`, imagePath);
                    console.error('Error target:', e.target);
                  }}
                  onLoad={() => {
                    const imagePath = getPieceImagePath(color, pieceOption.type, STABLE_PIECE_SET);
                    console.log(`✅ [PROMOTION] Successfully loaded piece image:`, imagePath);
                  }}
                />
              </div>
              
              {/* Piece Name */}
              <div className="text-sm font-semibold text-foreground">
                {pieceOption.name}
              </div>
            </button>
          ))}
        </div>

        {/* Cancel Button */}
        <button
          onClick={handleCancel}
          className="w-full px-4 py-2 text-sm text-muted-foreground hover:text-foreground border border-border rounded-lg hover:bg-muted/30 transition-colors"
        >
          Cancel Move
        </button>
      </div>
    </div>
  );
}