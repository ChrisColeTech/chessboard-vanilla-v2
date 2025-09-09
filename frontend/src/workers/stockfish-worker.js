// stockfish-worker.js - Copy of working v1 approach (JavaScript, not TypeScript)
// The key insight: stockfish.js is ALREADY a complete worker

// Send structured messages back to main thread
function log(message) {
  console.log(`[WORKER] ${message}`);
  self.postMessage({
    type: 'log',
    message: `[WORKER] ${message}`,
    timestamp: new Date().toISOString()
  });
}

function reportError(error) {
  console.error(`[WORKER ERROR] ${error.message || error}`);
  self.postMessage({
    type: 'error',
    message: error.message || error,
    timestamp: new Date().toISOString()
  });
}

// Initialize Stockfish
try {
  log('Loading Stockfish.js...');
  
  // Import the stockfish.js script - this creates a Module with built-in worker handling
  self.importScripts('/stockfish/stockfish.js');
  log('Stockfish.js loaded successfully');
  
  // The stockfish.js file we have is already a complete worker implementation
  // It sets up onmessage handlers and communication automatically
  // We just need to let our main thread know it's ready
  
  // Check if Module is available and properly configured
  if (typeof self.Module !== 'undefined') {
    log('Stockfish Module loaded successfully');
    
    // Override Module.print to intercept UCI responses and send them properly
    const originalPrint = self.Module.print;
    self.Module.print = function(stdout) {
      console.log(`[STOCKFISH OUTPUT] ${stdout}`);
      log(`Stockfish output: ${stdout}`);
      // Forward UCI messages to main thread
      self.postMessage(stdout);
      // Also call original print if it exists
      if (originalPrint) originalPrint(stdout);
    };
    
    // Override Module.postRun to know when engine is fully initialized
    const originalPostRun = self.Module.postRun;
    self.Module.postRun = function() {
      log('Stockfish Module postRun called - engine should be ready');
      if (originalPostRun) originalPostRun();
    };
    
    log('Stockfish worker ready and configured');
  } else {
    reportError('Module not found after loading stockfish.js');
  }
  
} catch (error) {
  reportError(`Failed to initialize Stockfish: ${error}`);
}

// The stockfish.js Module handles messages automatically
// We just need to make sure readyok gets through properly
log('Worker setup complete - stockfish.js Module will handle messages');

self.onerror = function(error) {
  reportError(`Worker error: ${error.message}`);
};