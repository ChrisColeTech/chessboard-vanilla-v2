interface PageInstructions {
  id: string;
  title: string;
  instructions: string[];
}

interface PageInstructionsModule {
  pageInstructions: PageInstructions;
}

class DynamicInstructionsService {
  private instructionsCache: Map<string, PageInstructions> = new Map();
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // Use import.meta.glob to dynamically import all instruction files
      const instructionModules = import.meta.glob('./pages/*.ts', { eager: true }) as Record<string, PageInstructionsModule>;
      
      for (const [, module] of Object.entries(instructionModules)) {
        if (module.pageInstructions) {
          this.instructionsCache.set(module.pageInstructions.id, module.pageInstructions);
        }
      }
      
      this.initialized = true;
      console.log(`🔄 [DYNAMIC INSTRUCTIONS] Loaded ${this.instructionsCache.size} instruction files`);
    } catch (error) {
      console.error('❌ [DYNAMIC INSTRUCTIONS] Failed to load instruction files:', error);
    }
  }

  getInstructions(pageId: string): PageInstructions | null {
    if (!this.initialized) {
      // Synchronously initialize if not already done
      this.initialize();
    }
    
    const instructions = this.instructionsCache.get(pageId);
    if (!instructions) {
      console.warn(`⚠️ [DYNAMIC INSTRUCTIONS] No instructions found for page: ${pageId}`);
      return null;
    }
    
    return instructions;
  }

  listAvailablePages(): string[] {
    return Array.from(this.instructionsCache.keys());
  }

  reload(): void {
    this.instructionsCache.clear();
    this.initialized = false;
    this.initialize();
  }
}

export const dynamicInstructionsService = new DynamicInstructionsService();