// MobileChessSquare.tsx - Individual chess square component
import React from "react";
import type { ChessPosition, ChessPiece } from "../../types";
import { getPieceImagePath } from "../../constants/pieces.constants";
import { useAppStore } from "../../stores/appStore";

interface MobileChessSquareProps {
  square: ChessPosition;
  piece: ChessPiece | null;
  isSelected: boolean;
  isValidMove: boolean;
  isInCheck: boolean;
  isLastMove: boolean;
  onSquareTap: (square: ChessPosition) => void;
}

export const MobileChessSquare: React.FC<MobileChessSquareProps> = ({
  square,
  piece,
  isSelected,
  isValidMove,
  isInCheck,
  isLastMove,
  onSquareTap,
}) => {
  // Get selected piece set from app store
  const selectedPieceSet = useAppStore((state) => state.selectedPieceSet);

  // Calculate square color (alternating pattern)
  const getSquareColor = (): string => {
    const file = square[0];
    const rank = parseInt(square[1]);
    const fileIndex = file.charCodeAt(0) - "a".charCodeAt(0);
    const isLight = (fileIndex + rank) % 2 === 0;
    return isLight ? "#F0D9B5" : "#B58863";
  };

  // Calculate modern visual styling with pure background-based highlighting
  const getSquareStyle = () => {
    let backgroundColor = getSquareColor();
    let backgroundOverlay = "";

    if (isInCheck) {
      // King in check - highest priority with red overlay
      backgroundOverlay = "linear-gradient(rgba(255, 0, 0, 0.4), rgba(255, 0, 0, 0.3))";
    } else if (isSelected) {
      // Selected square - clean background highlight only
      backgroundOverlay = "linear-gradient(rgba(74, 144, 226, 0.3), rgba(74, 144, 226, 0.2))";
    } else if (isLastMove) {
      // Last move - subtle gold overlay
      backgroundOverlay = "linear-gradient(rgba(255, 215, 0, 0.3), rgba(255, 215, 0, 0.2))";
    } else if (isValidMove) {
      // Valid move target - green overlay without borders
      backgroundOverlay = "linear-gradient(rgba(34, 197, 94, 0.25), rgba(34, 197, 94, 0.15))";
    }

    return {
      backgroundColor,
      backgroundImage: backgroundOverlay || "none",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      cursor: piece ? "grab" : "default",
      position: "relative" as const,
      userSelect: "none" as const,
      touchAction: "manipulation" as const,
      WebkitTapHighlightColor: "transparent",
      minHeight:
        window.matchMedia && window.matchMedia("(max-width: 768px)").matches
          ? "48px"
          : "44px",
      transition: "all 0.2s ease",
      border: "1px solid rgba(139, 69, 19, 0.1)", // Subtle border for square separation
    };
  };

  const handleClick = () => {
    console.log(`🟦 [MOBILE SQUARE] Click on ${square}`);
    onSquareTap(square);
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    console.log(`🟦 [MOBILE SQUARE] Touch end on ${square}`);
    e.preventDefault();
    e.stopPropagation();
    onSquareTap(square);
  };

  return (
    <div
      data-square={square}
      onClick={handleClick}
      onTouchEnd={handleTouchEnd}
      style={getSquareStyle()}
    >
      {piece && (
        <img
          src={getPieceImagePath(
            piece.color,
            piece.type,
            selectedPieceSet,
            square
          )}
          alt={`${piece.color} ${piece.type}`}
          draggable={false}
          style={{
            width:
              window.matchMedia &&
              window.matchMedia("(max-width: 768px)").matches
                ? "100%"
                : "88%",
            height:
              window.matchMedia &&
              window.matchMedia("(max-width: 768px)").matches
                ? "100%"
                : "88%",
            cursor: "grab",
            userSelect: "none",
            pointerEvents: "auto",
            minWidth: "40px",
            minHeight: "40px",
            // Mobile contrast enhancements
            ...(window.matchMedia &&
              window.matchMedia("(max-width: 768px)").matches && {
                filter:
                  "drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4)) contrast(1.15) brightness(1.05)",
                borderRadius: "4px",
                background: "rgba(255, 255, 255, 0.1)",
              }),
          }}
          onError={(e) => {
            console.log(
              `Failed to load piece image: ${getPieceImagePath(
                piece.color,
                piece.type,
                selectedPieceSet,
                square
              )}`
            );
            (e.target as HTMLImageElement).style.display = "none";
          }}
        />
      )}

      {/* Square labels - only on bottom and right edges */}
      {(square[1] === "1" || square[0] === "h") && (
        <div
          style={{
            position: "absolute",
            bottom: "1px",
            right: "2px",
            fontSize: "8px",
            fontWeight: "bold",
            color: getSquareColor() === "#F0D9B5" ? "#8B4513" : "#F0D9B5",
            pointerEvents: "none",
            opacity: 0.7,
          }}
        >
          {square}
        </div>
      )}

      {/* Modern valid move indicator */}
      {isValidMove && !piece && (
        <div
          style={{
            position: "absolute",
            width: "16px",
            height: "16px",
            backgroundColor: "rgba(34, 197, 94, 0.8)",
            borderRadius: "50%",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            pointerEvents: "none",
            zIndex: 1,
            boxShadow: "0 0 8px rgba(34, 197, 94, 0.4)",
          }}
        />
      )}
    </div>
  );
};
