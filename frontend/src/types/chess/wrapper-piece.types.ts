// Shared WrapperPiece interface for chess board animations

export interface WrapperPiece {
  id: string;
  color: string;
  type: string;
  x: number; // Pixel position
  y: number; // Pixel position
  opacity: number;
  isAnimating: boolean;
  boardPosition: string; // Chess notation (e.g., 'a1', 'e4')
  scale: number; // Scale for capture animation
}