// StockfishService.ts - Production-ready Stockfish Web Worker integration
// Complete rewrite based on Document 24 lessons learned

export interface StockfishHandlers {
  onBestMove?: (move: string) => void;
  onInfo?: (info: string) => void;
  onError?: (error: string) => void;
  onLog?: (message: string) => void;
}

interface SearchPromise {
  resolve: (value: string) => void;
  reject: (reason?: Error) => void;
  timeoutId?: NodeJS.Timeout;
  promise: Promise<string>;
}

export class StockfishService {
  private stockfish: Worker | null = null;
  private engineReady: boolean = false;
  private pendingCommands: Map<string, (response: string) => void> = new Map();
  private messageQueue: string[] = [];
  private workerState: 'initializing' | 'ready' | 'error' | 'destroyed' = 'initializing';
  private handlers: StockfishHandlers = {};
  private currentSearch?: SearchPromise;
  
  // Remove initPromise - we'll use the v1 pattern

  constructor() {
    this.initializeEngine();
  }

  private initializeEngine(): void {
    console.log('🧠 [STOCKFISH] Starting engine initialization...');
    try {
      // Use improved Stockfish worker with proper error handling (copied from working v1)
      const workerUrl = new URL('../../workers/stockfish-worker.js', import.meta.url);
      console.log('🧠 [STOCKFISH] Worker URL resolved:', workerUrl.href);
      
      // Use classic worker (not ES module) to support importScripts()
      console.log('🧠 [STOCKFISH] Creating new Worker...');
      this.stockfish = new Worker(workerUrl);
      this.stockfish.addEventListener('message', this.handleMessage.bind(this));
      this.stockfish.addEventListener('error', this.handleError.bind(this));
      console.log('🧠 [STOCKFISH] Worker created and event listeners attached');

      // Initialize UCI protocol (no response expected) - v1 pattern
      this.sendCommand('uci', false);
      
      // Wait for UCI initialization before checking readiness
      let uciInitialized = false;
      
      const checkReadiness = () => {
        if (!uciInitialized) {
          return;
        }
        this.sendCommand('isready').then(() => {
          clearTimeout(initTimeout);
          this.engineReady = true;
          this.workerState = 'ready';
          this.processMessageQueue();
        }).catch(error => {
          clearTimeout(initTimeout);
          console.error('❌ [STOCKFISH] Failed to initialize:', error);
          this.workerState = 'error';
        });
      };
      
      // Set up a flag to track UCI initialization - v1 pattern
      this.pendingCommands.set('uci_init', (response: string) => {
        if (response === 'uciok') {
          uciInitialized = true;
          this.pendingCommands.delete('uci_init');
          // Small delay to ensure engine is fully ready
          setTimeout(checkReadiness, 100);
        }
      });
      
      // Wait for readiness with timeout
      const initTimeout = setTimeout(() => {
        if (this.workerState === 'initializing') {
          console.error('⏰ [STOCKFISH] Worker initialization timeout - no response after 10 seconds');
          this.workerState = 'error';
        }
      }, 10000); // Increased timeout
      
    } catch (error) {
      console.error('❌ [STOCKFISH] Failed to initialize worker:', error);
      this.workerState = 'error';
      this.engineReady = false;
    }
  }

  private processMessageQueue(): void {
    while (this.messageQueue.length > 0 && this.workerState === 'ready') {
      const command = this.messageQueue.shift();
      if (command && this.stockfish) {
        this.stockfish.postMessage(command);
      }
    }
  }

  private handleMessage(event: MessageEvent): void {
    const message = event.data;
    
    // Handle structured messages from our improved worker (copied from v1)
    if (typeof message === 'object' && message.type) {
      switch (message.type) {
        case 'log':
          return;
        case 'error':
          console.error('❌ [WORKER]', message.message);
          this.workerState = 'error';
          this.engineReady = false;
          return;
      }
    }
    
    // Handle string messages (UCI protocol) - copied from working v1
    const messageStr = typeof message === 'string' ? message : message.toString();
    
    // Filter out verbose engine analysis spam
    if (messageStr.startsWith('info depth') || 
        messageStr.startsWith('option name') || 
        messageStr.trim() === '') {
      return; // Skip noisy analysis output
    }
    

    // Handle UCI protocol responses (copied from v1)
    if (message === 'uciok') {
      const uciInitCommand = this.pendingCommands.get('uci_init');
      if (uciInitCommand) {
        uciInitCommand(message);
      }
      return;
    }

    if (message === 'readyok') {
      const readyCommand = this.pendingCommands.get('isready');
      if (readyCommand) {
        readyCommand(message);
        this.pendingCommands.delete('isready');
      }
      return;
    }

    // Handle bestmove responses
    if (messageStr.startsWith('bestmove')) {
      
      // Resolve current search promise
      if (this.currentSearch) {
        
        if (this.currentSearch.timeoutId) {
          clearTimeout(this.currentSearch.timeoutId);
        }
        
        this.currentSearch.resolve(messageStr);
        this.currentSearch = undefined;
      }
      
      // Notify handlers
      if (this.handlers.onBestMove) {
        const match = messageStr.match(/bestmove\s+([a-h][1-8][a-h][1-8][qrbn]?)/);
        if (match) {
          this.handlers.onBestMove(match[1]);
        }
      }
      return;
    }

    // Handle evaluation responses
    if (message.includes('cp ')) {
      const evalCommand = this.pendingCommands.get('evaluation');
      if (evalCommand) {
        evalCommand(message);
        this.pendingCommands.delete('evaluation');
      }
    }
  }


  private handleError(error: ErrorEvent): void {
    console.error('💥 [STOCKFISH] Worker error event:', error);
    this.workerState = 'error';
    this.engineReady = false;
    
    if (this.handlers.onError) {
      this.handlers.onError(`Worker error: ${error.message}`);
    }
  }

  // Public API

  /**
   * Set handlers for engine events (with atomic updates)
   */
  public setHandlers(handlers: StockfishHandlers): void {
    this.handlers = { ...handlers };
    
    // Verify handlers are properly set (Document 24 Lesson #14)
  }

  /**
   * Check if engine is ready
   */
  public isEngineReady(): boolean {
    return this.engineReady && this.workerState === 'ready';
  }

  /**
   * Wait for engine to be ready
   */
  public async waitForReady(): Promise<void> {
    if (this.isEngineReady()) {
      return;
    }
    
    // Since we removed initPromise, we need a different approach
    // Wait up to 10 seconds for engine to become ready
    const startTime = Date.now();
    const timeout = 10000;
    
    return new Promise((resolve, reject) => {
      const checkReady = () => {
        if (this.isEngineReady()) {
          resolve();
        } else if (this.workerState === 'error') {
          reject(new Error('Engine failed to initialize - worker in error state'));
        } else if (Date.now() - startTime > timeout) {
          reject(new Error('Engine initialization timeout'));
        } else {
          setTimeout(checkReady, 100);
        }
      };
      
      checkReady();
    });
  }

  /**
   * Get best move with single-flight protection and position resyncing
   */
  public async getBestMove(fen: string, skillLevel: number = 8, timeLimit: number = 2000): Promise<string | null> {
    if (!this.isEngineReady() || !this.stockfish) {
      console.warn('⚠️ [STOCKFISH] Engine not ready for move calculation');
      return null;
    }

    try {
      
      // Single-flight protection (Document 24 Lesson #13)
      if (this.currentSearch) {
        return await this.currentSearch.promise;
      }

      // Position resyncing (Document 24 Lesson #3: Position Representation)
      // Always send full position to avoid HMR state issues
      await this.sendCommand(`ucinewgame`, false); // No response expected
      await this.sendCommand(`position fen ${fen}`, false); // No response expected
      
      // Set skill level
      await this.sendCommand(`setoption name Skill Level value ${Math.max(0, Math.min(20, skillLevel))}`, false); // No response expected
      
      // Create search promise
      this.currentSearch = {} as SearchPromise;
      this.currentSearch.promise = new Promise<string>((resolve, reject) => {
        this.currentSearch!.resolve = resolve;
        this.currentSearch!.reject = reject;
        
        // Timeout protection (3x movetime + buffer)
        const timeoutMs = timeLimit * 3 + 2000;
        this.currentSearch!.timeoutId = setTimeout(() => {
          console.error('⏰ [STOCKFISH] Move calculation timeout');
          this.currentSearch = undefined;
          reject(new Error(`Search timeout after ${timeoutMs}ms`));
        }, timeoutMs);
      });

      // Start search
      this.stockfish.postMessage(`go movetime ${timeLimit}`);
      
      const result = await this.currentSearch.promise;
      this.currentSearch = undefined;
      
      return result;
      
    } catch (error) {
      console.error('❌ [STOCKFISH] Error calculating best move:', error);
      if (this.currentSearch) {
        if (this.currentSearch.timeoutId) {
          clearTimeout(this.currentSearch.timeoutId);
        }
        this.currentSearch = undefined;
      }
      return null;
    }
  }

  private sendCommand(command: string, expectResponse: boolean = true): Promise<string> {
    return new Promise((resolve, reject) => {
      if (!this.stockfish) {
        reject(new Error('Stockfish not initialized'));
        return;
      }

      if (!expectResponse) {
        this.stockfish.postMessage(command);
        resolve('');
        return;
      }

      const commandType = command.startsWith('go') ? 'bestmove' : 
                         command.startsWith('isready') ? 'isready' :
                         command.startsWith('position') ? 'position' :
                         command.split(' ')[0];
      
      // Clear any existing pending command of the same type to prevent conflicts
      if (this.pendingCommands.has(commandType)) {
        this.pendingCommands.delete(commandType);
      }
      
      this.pendingCommands.set(commandType, resolve);

      // Only log important commands, not routine ones
      if (!command.startsWith('setoption') && !command.startsWith('position')) {
      }
      
      // Allow isready command during initialization (needed for two-stage init)
      if (this.workerState === 'ready' || (this.workerState === 'initializing' && command === 'isready')) {
        this.stockfish.postMessage(command);
      } else if (this.workerState === 'initializing') {
        this.messageQueue.push(command);
      } else {
        reject(new Error(`Cannot send command - worker state: ${this.workerState}`));
        return;
      }

      // Set timeout for commands
      setTimeout(() => {
        if (this.pendingCommands.has(commandType)) {
          console.error(`⏰ [STOCKFISH] TIMEOUT: Command '${command}' never resolved`);
          this.pendingCommands.delete(commandType);
          reject(new Error(`Command timeout: ${command}`));
        }
      }, 15000); // 15 second timeout
    });
  }

  /**
   * Get best move with position resyncing (HMR-safe)
   */
  public async getBestMoveWithPosition(fen: string, skillLevel: number = 8, timeLimit: number = 1000): Promise<string | null> {
    if (!this.isEngineReady() || !this.stockfish) {
      console.warn('⚠️ [STOCKFISH] Engine not ready for move calculation');
      return null;
    }

    try {
      console.log('🎯 [STOCKFISH] Requesting best move with position resync:', { fen, skillLevel, timeLimit });
      
      // Single-flight protection (Document 24 Lesson #13)
      if (this.currentSearch) {
        return await this.currentSearch.promise;
      }

      // Position resyncing (Document 24 Lesson #3: Position Representation)
      // Always send full position to avoid HMR state issues
      await this.sendCommand(`ucinewgame`, false); // No response expected
      await this.sendCommand(`position fen ${fen}`, false); // No response expected
      
      // Set skill level
      await this.sendCommand(`setoption name Skill Level value ${Math.max(0, Math.min(20, skillLevel))}`, false); // No response expected
      
      // Create search promise
      this.currentSearch = {} as SearchPromise;
      this.currentSearch.promise = new Promise<string>((resolve, reject) => {
        this.currentSearch!.resolve = resolve;
        this.currentSearch!.reject = reject;
        
        // Timeout protection (3x movetime + buffer)
        const timeoutMs = timeLimit * 3 + 2000;
        this.currentSearch!.timeoutId = setTimeout(() => {
          console.error('⏰ [STOCKFISH] Move calculation timeout');
          this.currentSearch = undefined;
          reject(new Error(`Search timeout after ${timeoutMs}ms`));
        }, timeoutMs);
      });

      // Start search
      this.stockfish.postMessage(`go movetime ${timeLimit}`);
      
      const result = await this.currentSearch.promise;
      this.currentSearch = undefined;
      
      // Parse bestmove response
      const match = result.match(/bestmove\s+([a-h][1-8][a-h][1-8][qrbn]?)/);
      if (match) {
        const move = match[1];
        return move;
      }
      
      console.warn('⚠️ [STOCKFISH] Could not parse move from response:', result);
      return null;
      
    } catch (error) {
      console.error('❌ [STOCKFISH] Error calculating best move:', error);
      if (this.currentSearch) {
        if (this.currentSearch.timeoutId) {
          clearTimeout(this.currentSearch.timeoutId);
        }
        this.currentSearch = undefined;
      }
      return null;
    }
  }

  /**
   * Evaluate position and return centipawn score
   */
  public async evaluatePosition(fen: string, depth: number = 15): Promise<number> {
    if (!this.isEngineReady() || !this.stockfish) {
      console.warn('⚠️ [STOCKFISH] Engine not ready for position evaluation');
      return 0;
    }

    try {
      
      // Set position
      await this.sendCommand(`position fen ${fen}`);
      
      // Request evaluation - register handler for evaluation responses
      let finalEvaluation = 0;
      this.pendingCommands.set('evaluation', (response: string) => {
        // Parse centipawn evaluation from the response
        const cpMatch = response.match(/cp\s+(-?\d+)/);
        if (cpMatch) {
          finalEvaluation = parseInt(cpMatch[1]);
        }
      });
      
      await this.sendCommand(`go depth ${depth}`);
      
      return finalEvaluation;
      
    } catch (error) {
      console.error('❌ [STOCKFISH] Error evaluating position:', error);
      return 0;
    }
  }

  /**
   * Set skill level (0-20, where 20 is strongest)
   */
  public async setSkillLevel(level: number): Promise<void> {
    if (!this.isEngineReady()) {
      console.warn('⚠️ [STOCKFISH] Cannot set skill level - engine not ready');
      return;
    }

    const clampedLevel = Math.max(0, Math.min(20, level));
    await this.sendCommand(`setoption name Skill Level value ${clampedLevel}`, false);
  }

  /**
   * Destroy the service and cleanup resources
   */
  public destroy(): void {
    if (this.workerState === 'destroyed') {
      return;
    }

    
    this.workerState = 'destroyed';
    this.engineReady = false;
    
    // Clean up current search
    if (this.currentSearch) {
      if (this.currentSearch.timeoutId) {
        clearTimeout(this.currentSearch.timeoutId);
      }
      this.currentSearch.reject(new Error('Service destroyed'));
      this.currentSearch = undefined;
    }
    
    // Terminate worker
    if (this.stockfish) {
      this.stockfish.terminate();
      this.stockfish = null;
    }
    
    // Clear handlers
    this.handlers = {};
    
  }

  /**
   * Clear all handlers
   */
  public clearHandlers(): void {
    this.handlers = {};
  }

  /**
   * Get service stats for debugging
   */
  public getStats() {
    return {
      workerState: this.workerState,
      isEngineReady: this.engineReady,
      hasWorker: !!this.stockfish,
      hasCurrentSearch: !!this.currentSearch,
      handlerCount: Object.keys(this.handlers).length
    };
  }
}