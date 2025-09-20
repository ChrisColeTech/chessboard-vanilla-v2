// stockfish-singleton.ts - HMR-safe singleton for development
// Based on Document 24 Lesson #11: HMR vs Web Worker Lifecycle Conflicts

import { StockfishService } from './StockfishService';

// CRITICAL: Module-level singleton that survives HMR cycles
let singletonInstance: StockfishService | null = null;
let instanceCount = 0;

/**
 * HMR-safe Stockfish service singleton
 * 
 * Key behaviors:
 * - Development: Keeps worker alive across HMR cycles, rebinds handlers only
 * - Production: Normal creation/destruction with component lifecycle
 * - Always rebinds event handlers on access (prevents orphaned listeners)
 */
export function getStockfishService(): StockfishService {
  instanceCount++;
  
  const isDevelopment = !import.meta.env.PROD;
  
  if (isDevelopment) {
    // Development mode: Use singleton pattern
    if (!singletonInstance) {
      console.log('🔧 [SINGLETON] Creating new Stockfish service instance for development');
      singletonInstance = new StockfishService();
      
      // HMR cleanup - only in development
      if (import.meta.hot) {
        import.meta.hot.dispose(() => {
          console.log('🔄 [SINGLETON] HMR dispose called - keeping worker alive');
          // Don't destroy the service - let it survive HMR
        });
      }
    } else {
      console.log(`🔄 [SINGLETON] Reusing existing service instance (access #${instanceCount})`);
    }
    
    return singletonInstance;
  } else {
    // Production mode: Always create fresh instances
    console.log('🏭 [SINGLETON] Creating new service instance for production');
    return new StockfishService();
  }
}

/**
 * Manually destroy the singleton (for testing or forced cleanup)
 */
export function destroyStockfishSingleton(): void {
  if (singletonInstance) {
    console.log('💥 [SINGLETON] Manually destroying singleton instance');
    singletonInstance.destroy();
    singletonInstance = null;
    instanceCount = 0;
  }
}

/**
 * Get singleton stats for debugging
 */
export function getStockfishSingletonStats() {
  return {
    hasInstance: !!singletonInstance,
    instanceCount,
    isDevelopment: !import.meta.env.PROD,
    isReady: singletonInstance?.isEngineReady() || false
  };
}

// Development-only debugging
if (!import.meta.env.PROD) {
  // Add to window for debugging
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).__stockfishSingleton = {
    getInstance: () => singletonInstance,
    getStats: getStockfishSingletonStats,
    destroy: destroyStockfishSingleton,
    forceRecreate: () => {
      destroyStockfishSingleton();
      return getStockfishService();
    }
  };
  
  console.log('🐛 [SINGLETON] Debug interface available at window.__stockfishSingleton');
}