// useResponsiveBoard.ts - Responsive board sizing
import { useState, useEffect, useRef, useCallback } from 'react';

export interface UseResponsiveBoardHook {
  boardSize: { width: number; height: number };
  squareSize: number;
  containerRef: React.RefObject<HTMLDivElement | null>;
  isResizing: boolean;
}

export const useResponsiveBoard = (maxWidth?: number): UseResponsiveBoardHook => {
  const [boardSize, setBoardSize] = useState({ width: 0, height: 0 });
  const [isResizing, setIsResizing] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const resizeTimeoutRef = useRef<NodeJS.Timeout>(undefined);

  const calculateBoardSize = useCallback(() => {
    if (!containerRef.current) {
      return { width: 400, height: 400 };
    }

    const container = containerRef.current;
    const containerRect = container.getBoundingClientRect();
    const containerSize = Math.min(containerRect.width, containerRect.height);

    // Apply constraints
    const minSize = 200;
    const maxSize = maxWidth || 800;
    const size = Math.max(minSize, Math.min(maxSize, containerSize * 0.9));

    return { width: size, height: size };
  }, [maxWidth]);

  const updateBoardSize = useCallback(() => {
    setIsResizing(true);
    
    // Debounce resize updates
    if (resizeTimeoutRef.current) {
      clearTimeout(resizeTimeoutRef.current);
    }

    resizeTimeoutRef.current = setTimeout(() => {
      const newSize = calculateBoardSize();
      setBoardSize(newSize);
      setIsResizing(false);
    }, 100);
  }, [calculateBoardSize]);

  // Initial size calculation
  useEffect(() => {
    if (containerRef.current) {
      const initialSize = calculateBoardSize();
      setBoardSize(initialSize);
    }
  }, [calculateBoardSize]);

  // ResizeObserver for responsive updates
  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    const resizeObserver = new ResizeObserver(() => {
      updateBoardSize();
    });

    resizeObserver.observe(containerRef.current);

    // Fallback window resize listener
    const handleWindowResize = () => updateBoardSize();
    window.addEventListener('resize', handleWindowResize);

    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', handleWindowResize);
      if (resizeTimeoutRef.current) {
        clearTimeout(resizeTimeoutRef.current);
      }
    };
  }, [updateBoardSize]);

  const squareSize = boardSize.width / 8;

  return {
    boardSize,
    squareSize,
    containerRef,
    isResizing
  };
};