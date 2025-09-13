// grid-generator.utils.ts - Dynamic grid cell generation utilities

import React from "react";

export interface GridCell {
  id: string;
  position: number;
  backgroundColor: string;
  displayText: string;
  element: React.ReactElement;
}

export interface ChessGridConfig {
  showCoordinates?: boolean;
  coordinateStyle?: "all" | "edges" | "none";
  showFiles?: boolean;
  showRanks?: boolean;
  overlayMode?: boolean; // New: generate overlay cells instead of chess squares
}

/**
 * Generates grid cells with alternating background colors
 * @param numCells - Total number of cells to generate
 * @param lightColor - Color for light squares (default: lightblue)
 * @param darkColor - Color for dark squares (default: lightcoral)
 * @returns Array of GridCell objects
 */
export function generateGridCells(
  numCells: number,
  lightColor: string = "lightblue",
  darkColor: string = "lightcoral"
): GridCell[] {
  const cells: GridCell[] = [];

  for (let i = 1; i <= numCells; i++) {
    // Alternating colors - odd positions get light color, even get dark color
    const isLight = i % 2 === 1;

    const cellElement = React.createElement(
      "div",
      {
        key: `cell-${i}`,
        style: {
          backgroundColor: isLight ? lightColor : darkColor,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
        },
      },
      i.toString()
    );

    cells.push({
      id: `cell-${i}`,
      position: i,
      backgroundColor: isLight ? lightColor : darkColor,
      displayText: i.toString(),
      element: cellElement,
    });
  }

  return cells;
}

/**
 * Chess-style alternating colors for square grids with configurable coordinate display
 * @param numCells - Total number of cells (should be perfect square: 4, 9, 16, etc.)
 * @param lightColor - Color for light squares
 * @param darkColor - Color for dark squares
 * @param config - Configuration for coordinate display
 * @returns Array of GridCell objects with chess-pattern coloring and configurable coordinates
 */
export function generateChessGridCells(
  numCells: number,
  _lightColor?: string, // eslint-disable-line @typescript-eslint/no-unused-vars
  _darkColor?: string, // eslint-disable-line @typescript-eslint/no-unused-vars
  config: ChessGridConfig = {}
): GridCell[] {
  const cells: GridCell[] = [];
  const gridSize = Math.sqrt(numCells);

  // Debug: Log that we're using CSS classes instead of inline colors
  console.log(
    "🎨 [DEBUG] generateChessGridCells using CSS classes for theme-aware colors"
  );

  if (gridSize !== Math.floor(gridSize)) {
    throw new Error(
      `numCells must be a perfect square (4, 9, 16, etc.), got ${numCells}`
    );
  }

  // Chess files (columns): a, b, c, d, e, f, g, h
  const files = ["a", "b", "c", "d", "e", "f", "g", "h"];

  for (let i = 1; i <= numCells; i++) {
    // Convert to row/column (0-indexed)
    const row = Math.floor((i - 1) / gridSize);
    const col = (i - 1) % gridSize;

    // Chess notation: file (a-h) + rank (1-8)
    // Note: Chess ranks go from 1-8, bottom to top, so we need to invert row
    const file = files[col];
    const rank = gridSize - row; // Invert: top row = highest rank
    const chessSquare = `${file}${rank}`;

    // Chess pattern: alternating based on row + column sum
    const isLight = (row + col) % 2 === 0;

    // Determine what text to display based on configuration
    let displayText = "";
    const {
      showCoordinates = true,
      coordinateStyle = "all",
      showFiles = true,
      showRanks = true,
      overlayMode = false,
    } = config;

    if (showCoordinates) {
      switch (coordinateStyle) {
        case "all":
          displayText = chessSquare;
          break;
        case "edges":
          // Show full coordinates on bottom row (rank 1) and rightmost column
          if (rank === 1 && showFiles) {
            displayText = chessSquare; // Show full coordinate like "a1", "b1", "c1", "d1"
          }
          // Show full coordinates on rightmost column (for 4x4 grid, rightmost is 'd')
          else if (file === files[gridSize - 1] && showRanks) {
            displayText = chessSquare; // Show full coordinate like "d1", "d2", "d3", "d4"
          }
          break;
        case "none":
          displayText = "";
          break;
      }
    }

    // Create different elements based on mode
    const cellElement = overlayMode
      ? React.createElement("div", {
          key: chessSquare,
          id: chessSquare,
          className: `overlay-cell ${
            isLight ? "overlay-light-square" : "overlay-dark-square"
          }`,
          style: {
            transition: "backdrop-filter 0.3s ease, background-color 0.3s ease",
            borderRadius: "4px",
            pointerEvents: "none", // Overlay doesn't interfere with interactions
          },
        })
      : React.createElement(
          "div",
          {
            key: chessSquare,
            id: chessSquare,
            className: `chess-square ${
              isLight ? "chess-light-square" : "chess-dark-square"
            }`,
            style: {
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              position: "relative",
            },
          },
          // Add coordinate label as a positioned child element if needed (only for chess squares, not overlay)
          displayText
            ? React.createElement(
                "span",
                {
                  style: {
                    position: "absolute",
                    fontSize: "10px",
                    fontWeight: "bold",
                    color: "#333",
                    // Position at bottom-right corner of every square
                    bottom: "2px",
                    right: "2px",
                  },
                },
                displayText
              )
            : null
        );

    cells.push({
      id: chessSquare,
      position: i,
      backgroundColor: "", // No longer used - using CSS classes instead
      displayText: displayText,
      element: cellElement,
    });
  }

  return cells;
}
