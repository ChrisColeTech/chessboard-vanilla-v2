// useChessGrid.ts - Hook for generating chess board grid cells
import { useState, useEffect } from 'react';
import {
  generateChessGridCells,
  type GridCell,
} from "../../utils/grid-generator.utils";

interface UseChessGridOptions {
  showCoordinates?: boolean;
  coordinateStyle?: "all" | "edges" | "none";
  showFiles?: boolean;
  showRanks?: boolean;
}

export const useChessGrid = (
  gridSize: number,
  options: UseChessGridOptions = {
    showCoordinates: true,
    coordinateStyle: "edges",
    showFiles: true,
    showRanks: true,
  }
) => {
  const [gridCells, setGridCells] = useState<GridCell[]>([]);

  useEffect(() => {
    const cells = generateChessGridCells(gridSize * gridSize, "", "", options);
    setGridCells(cells);
  }, [gridSize, options.showCoordinates, options.coordinateStyle, options.showFiles, options.showRanks]);

  return { gridCells };
};