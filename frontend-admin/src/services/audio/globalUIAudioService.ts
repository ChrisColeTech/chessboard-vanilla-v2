// globalUIAudioService.ts - Main service class for global UI audio detection and playback

import type { 
  GlobalUIAudioService as IGlobalUIAudioService, 
  GlobalUIAudioConfig, 
  GlobalUIAudioConfigUpdate,
  ElementDetectionResult,
  GlobalClickHandler 
} from '../../types/audio/global-audio.types';
import type { UIElementSelector } from '../../types/audio/ui-audio.types';
import { audioService } from './audioService';
import { 
  DEFAULT_UI_SELECTORS,
  findClickableAncestor,
  isElementExcluded 
} from '../../utils/audio/elementSelectors';
import { 
  getSoundForInteraction,
  isInteractionAudioEnabled 
} from '../../utils/audio/soundMapping';

/**
 * Default configuration for Global UI Audio Service
 */
const DEFAULT_CONFIG: GlobalUIAudioConfig = {
  enabled: true,
  autoDetection: true,
  customSelectors: [],
  excludeSelectors: [
    '[data-no-sound]',
    '.no-sound',
    '[disabled]',
    '.disabled',
    '.chess-piece', // Exclude chess game elements
    '.chess-square',
    'audio',
    'video'
  ],
  exclusions: []
};

/**
 * Global UI Audio Service Implementation
 * Provides automatic audio feedback for all UI interactions using event delegation
 */
export class GlobalUIAudioService implements IGlobalUIAudioService {
  private config: GlobalUIAudioConfig;
  private initialized = false;
  private globalClickHandler: GlobalClickHandler;
  private globalHoverHandler: (event: Event) => void;
  private lastHoveredElementId: string | null = null; // More robust element tracking
  private lastHoverSoundTime = 0;
  private readonly HOVER_SOUND_COOLDOWN_MS = 300; // Increased cooldown to prevent retriggering

  constructor(initialConfig: Partial<GlobalUIAudioConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...initialConfig };
    
    // Bind the event handlers to maintain 'this' context
    this.globalClickHandler = this.handleGlobalClick.bind(this);
    this.globalHoverHandler = this.handleGlobalHover.bind(this);
    
    console.log('🔊 [GLOBAL UI AUDIO] Service created with config:', this.config);
  }

  /**
   * Initialize the service and start listening for global click events
   */
  public initialize(): void {
    if (this.initialized) {
      console.log('🔊 [GLOBAL UI AUDIO] Service already initialized, skipping...');
      return;
    }

    if (!this.config.enabled) {
      console.log('🔊 [GLOBAL UI AUDIO] Service disabled, not initializing event listeners');
      return;
    }

    // Use event delegation on window with capture phase (avoids React conflicts)
    window.addEventListener('click', this.globalClickHandler, true);
    window.addEventListener('mouseover', this.globalHoverHandler, true);
    window.addEventListener('mouseout', this.resetHoverState.bind(this), true);
    console.log('🔊 [GLOBAL UI AUDIO] Event listeners attached to window (click, hover, mouseout) with capture phase');
    
    this.initialized = true;
    console.log('🔊 [GLOBAL UI AUDIO] Service initialized and listening for click and hover events');
  }

  /**
   * Destroy the service and clean up event listeners
   */
  public destroy(): void {
    if (!this.initialized) {
      console.log('🔊 [GLOBAL UI AUDIO] Service not initialized, nothing to destroy');
      return;
    }

    // Clean up event listeners
    window.removeEventListener('click', this.globalClickHandler, true);
    window.removeEventListener('mouseover', this.globalHoverHandler, true);
    window.removeEventListener('mouseout', this.resetHoverState.bind(this), true);
    
    this.initialized = false;
    console.log('🔊 [GLOBAL UI AUDIO] Service destroyed, event listener removed from window');
  }

  /**
   * Configure the service with new settings
   */
  public configure(configUpdate: GlobalUIAudioConfigUpdate): void {
    const wasEnabled = this.config.enabled;
    
    // Update configuration
    this.config = { ...this.config, ...configUpdate };
    
    console.log('🔊 [GLOBAL UI AUDIO] Configuration updated:', configUpdate);
    
    // Handle enable/disable state changes
    if (wasEnabled && !this.config.enabled && this.initialized) {
      this.destroy();
    } else if (!wasEnabled && this.config.enabled && !this.initialized) {
      this.initialize();
    }
  }

  /**
   * Add a custom element selector for audio detection
   */
  public addCustomSelector(selector: UIElementSelector): void {
    const existingIndex = this.config.customSelectors.findIndex(
      s => s.selector === selector.selector
    );
    
    if (existingIndex >= 0) {
      // Update existing selector - create new array with updated selector
      const newSelectors = [...this.config.customSelectors];
      newSelectors[existingIndex] = selector;
      this.config = { ...this.config, customSelectors: newSelectors };
      console.log('🔊 [GLOBAL UI AUDIO] Updated custom selector:', selector.selector);
    } else {
      // Add new selector - create new array with added selector
      this.config = {
        ...this.config,
        customSelectors: [...this.config.customSelectors, selector]
      };
      console.log('🔊 [GLOBAL UI AUDIO] Added custom selector:', selector.selector);
    }
  }

  /**
   * Remove a custom element selector
   */
  public removeCustomSelector(selectorString: string): void {
    const originalLength = this.config.customSelectors.length;
    const newSelectors = this.config.customSelectors.filter(
      s => s.selector !== selectorString
    );
    
    this.config = { ...this.config, customSelectors: newSelectors };
    
    const removed = originalLength - newSelectors.length;
    if (removed > 0) {
      console.log('🔊 [GLOBAL UI AUDIO] Removed custom selector:', selectorString);
    } else {
      console.log('🔊 [GLOBAL UI AUDIO] Custom selector not found:', selectorString);
    }
  }

  /**
   * Get current configuration
   */
  public getConfig(): GlobalUIAudioConfig {
    return { ...this.config };
  }

  /**
   * Check if service is initialized
   */
  public isInitialized(): boolean {
    return this.initialized;
  }

  /**
   * Global hover event handler for UI audio feedback
   */
  private handleGlobalHover(event: Event): void {
    const target = event.target as HTMLElement;
    
    // Create a unique identifier for the element to prevent repeated sounds
    const elementId = this.createElementIdentifier(target);
    
    // Prevent repeated sounds for the same element (mouseover fires repeatedly)
    if (this.lastHoveredElementId === elementId) {
      return;
    }
    
    this.lastHoveredElementId = elementId;
    
    if (!this.config.enabled || !this.config.autoDetection) {
      return;
    }

    if (!target) {
      return;
    }

    try {
      // Detect if this hover should trigger audio
      const detectionResult = this.detectClickableElement(target);
      
      if (detectionResult.shouldPlaySound) {
        // Play the UI hover sound
        this.playAudioForInteraction('hover');
      }
    } catch (error) {
      console.error('🔊 [GLOBAL UI AUDIO] Error in hover handler:', error);
    }
  }

  /**
   * Global click event handler - the core of the audio detection system
   */
  private handleGlobalClick(event: Event): void {
    const target = event.target as HTMLElement;
    console.log('🔊 [GLOBAL UI AUDIO] Click detected:', {
      tagName: target?.tagName,
      className: target?.className || '',
      id: target?.id || ''
    });
    
    if (!this.config.enabled || !this.config.autoDetection) {
      console.log('🔊 [GLOBAL UI AUDIO] Disabled - enabled:', this.config.enabled, 'autoDetection:', this.config.autoDetection);
      return;
    }

    if (!target) {
      console.log('🔊 [GLOBAL UI AUDIO] No target');
      return;
    }

    try {
      // Detect if this click should trigger audio
      const detectionResult = this.detectClickableElement(target);
      console.log('🔊 [GLOBAL UI AUDIO] Detection result:', {
        shouldPlaySound: detectionResult.shouldPlaySound,
        elementTag: detectionResult.element?.tagName,
        matchedSelector: detectionResult.matchedSelector,
        priority: detectionResult.priority
      });
      
      if (detectionResult.shouldPlaySound) {
        console.log(
          `🔊 [GLOBAL UI AUDIO] Playing click sound for element:`, 
          detectionResult.element.tagName,
          detectionResult.matchedSelector ? `(${detectionResult.matchedSelector})` : ''
        );
        
        // Play the UI click sound
        this.playAudioForInteraction('click');
      } else {
        console.log('🔊 [GLOBAL UI AUDIO] Not playing sound - element excluded or not clickable');
      }
    } catch (error) {
      console.error('🔊 [GLOBAL UI AUDIO] Error in click handler:', {
        message: error instanceof Error ? error.message : String(error),
        stack: error instanceof Error ? error.stack : undefined,
        target: target ? { tagName: target.tagName, className: target.className, id: target.id } : null
      });
    }
  }

  /**
   * Detect if a clicked element should trigger audio feedback
   */
  private detectClickableElement(target: Element): ElementDetectionResult {
    // First check if the element is explicitly excluded
    if (this.isElementExcludedByConfig(target)) {
      return {
        shouldPlaySound: false,
        element: target
      };
    }

    // Combine default selectors with custom selectors
    const allSelectors = [
      ...DEFAULT_UI_SELECTORS,
      ...this.config.customSelectors
    ];

    // Find the best matching clickable element (might be an ancestor)
    const result = findClickableAncestor(target, allSelectors);
    
    if (result) {
      return {
        shouldPlaySound: true,
        element: result.element,
        matchedSelector: result.selector.selector,
        priority: result.selector.priority
      };
    }

    return {
      shouldPlaySound: false,
      element: target
    };
  }

  /**
   * Check if an element is excluded by configuration
   */
  private isElementExcludedByConfig(element: Element): boolean {
    // Check built-in exclusions
    if (isElementExcluded(element)) {
      return true;
    }

    // Check config-specific exclusions
    for (const excludeSelector of this.config.excludeSelectors) {
      try {
        if (element.matches(excludeSelector)) {
          return true;
        }
      } catch {
        // Invalid selector, skip
        continue;
      }
    }

    return false;
  }

  /**
   * Create a unique identifier for an element to prevent duplicate sounds
   */
  private createElementIdentifier(element: Element): string {
    // Use a stable combination of tag, id, class, and position (exclude textContent which can vary)
    const tagName = element.tagName.toLowerCase();
    const id = element.id || '';
    const className = element.className || '';
    
    // Get element's position in DOM tree for uniqueness
    let position = '';
    let parent = element.parentElement;
    if (parent) {
      const siblings = Array.from(parent.children);
      position = siblings.indexOf(element).toString();
    }
    
    // Create a stable identifier without textContent to prevent rapid-fire sounds
    return `${tagName}#${id}.${className}[${position}]`;
  }

  /**
   * Reset hover state to allow new hover sounds (called on mouseleave-like events)
   */
  private resetHoverState(): void {
    this.lastHoveredElementId = null;
  }

  /**
   * Play audio for a specific interaction type
   */
  private playAudioForInteraction(interactionType: 'click' | 'hover' | 'focus' | 'select'): void {
    // Check if this interaction type should play audio
    if (!isInteractionAudioEnabled(interactionType)) {
      return;
    }

    // Apply cooldown specifically for hover sounds to prevent rapid-fire
    if (interactionType === 'hover') {
      const now = Date.now();
      const timeSinceLastHover = now - this.lastHoverSoundTime;
      
      if (timeSinceLastHover < this.HOVER_SOUND_COOLDOWN_MS) {
        console.log(`🔊 [GLOBAL UI AUDIO] Hover sound skipped (cooldown: ${timeSinceLastHover}ms < ${this.HOVER_SOUND_COOLDOWN_MS}ms)`);
        return;
      }
      
      this.lastHoverSoundTime = now;
    }

    try {
      // Get the appropriate sound effect for this interaction
      const soundEffect = getSoundForInteraction(interactionType);
      
      // Play the sound through the audio service
      audioService.play(soundEffect);
      console.log(`🔊 [GLOBAL UI AUDIO] Playing ${interactionType} sound: ${soundEffect}`);
    } catch (error) {
      console.error(`🔊 [GLOBAL UI AUDIO] Error playing audio for ${interactionType}:`, error);
    }
  }
}