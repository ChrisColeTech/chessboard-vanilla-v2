// Simple test worker to verify worker creation and stockfish.js loading
console.log('[TEST WORKER] Worker started');

// Test basic functionality
self.postMessage({ type: 'log', message: 'Test worker is alive' });

// Test stockfish.js loading
try {
  const baseUrl = self.location.origin;
  const stockfishUrl = new URL('/stockfish/stockfish.js', baseUrl).href;
  console.log(`[TEST WORKER] Attempting to load: ${stockfishUrl}`);
  
  // Test if we can fetch the stockfish file first
  fetch(stockfishUrl)
    .then(response => {
      console.log(`[TEST WORKER] Fetch response status: ${response.status}`);
      self.postMessage({ 
        type: 'log', 
        message: `Stockfish fetch status: ${response.status}` 
      });
      
      if (response.ok) {
        // Try importing if fetch works
        try {
          self.importScripts(stockfishUrl);
          self.postMessage({ type: 'log', message: 'Stockfish import SUCCESS' });
        } catch (importError) {
          self.postMessage({ 
            type: 'error', 
            message: `Stockfish import FAILED: ${importError.message}` 
          });
        }
      }
    })
    .catch(fetchError => {
      console.error(`[TEST WORKER] Fetch failed: ${fetchError.message}`);
      self.postMessage({ 
        type: 'error', 
        message: `Stockfish fetch FAILED: ${fetchError.message}` 
      });
    });

} catch (error) {
  console.error(`[TEST WORKER] General error: ${error.message}`);
  self.postMessage({ type: 'error', message: `General error: ${error.message}` });
}