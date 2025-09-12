import type { ActionSheetAction } from '../../types/core/action-sheet.types';

interface PageActions {
  id: string;
  actions: ActionSheetAction[];
}

interface PageActionsModule {
  pageActions: PageActions;
}

class DynamicPageActionsService {
  private actionsCache: Map<string, ActionSheetAction[]> = new Map();
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // Use import.meta.glob to dynamically import all action files
      const actionModules = import.meta.glob('./pages/*.ts', { eager: true }) as Record<string, PageActionsModule>;
      
      for (const [, module] of Object.entries(actionModules)) {
        if (module.pageActions) {
          this.actionsCache.set(module.pageActions.id, module.pageActions.actions);
        }
      }
      
      this.initialized = true;
      console.log(`🔄 [DYNAMIC ACTIONS] Loaded ${this.actionsCache.size} action files`);
    } catch (error) {
      console.error('❌ [DYNAMIC ACTIONS] Failed to load action files:', error);
    }
  }

  getActions(pageId: string): ActionSheetAction[] {
    if (!this.initialized) {
      // Synchronously initialize if not already done
      this.initialize();
    }
    
    const actions = this.actionsCache.get(pageId);
    if (!actions) {
      console.warn(`⚠️ [DYNAMIC ACTIONS] No actions found for page: ${pageId}`);
      return [];
    }
    
    return actions;
  }

  listAvailablePages(): string[] {
    return Array.from(this.actionsCache.keys());
  }

  reload(): void {
    this.actionsCache.clear();
    this.initialized = false;
    this.initialize();
  }
}

const dynamicPageActionsService = new DynamicPageActionsService();

// Export as object matching the original PAGE_ACTIONS structure
export const DYNAMIC_PAGE_ACTIONS = new Proxy({}, {
  get(_, pageId: string | symbol) {
    if (typeof pageId === 'string') {
      return dynamicPageActionsService.getActions(pageId);
    }
    return undefined;
  }
}) as Record<string, ActionSheetAction[]>;