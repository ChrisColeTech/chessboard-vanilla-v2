// UIDemoService.ts - Business logic for UI demonstration functionality

import type {
  AudioDemoConfiguration,
  DragTestConfiguration,
  DemoButtonExample,
  ExclusionExample,
  CodeSnippet,
  UITestRoute
} from '../../types';
import {
  generateDemoButtons,
  generateExclusionExamples,
  generateCodeSnippets,
  generateInteractiveSelectors,
  generateExclusionSelectors,
  validateDemoConfiguration,
  groupExamplesByCategory
} from '../../utils';
import {
  DEFAULT_AUDIO_DEMO_CONFIG,
  DEFAULT_DRAG_TEST_CONFIG,
  UI_TEST_ROUTES,
  STANDARD_UI_INTERACTIONS,
  STANDARD_INTERACTIVE_SELECTORS,
  STANDARD_EXCLUSIONS
} from '../../constants';

/**
 * Service class for managing UI demo functionality
 */
export class UIDemoService {
  private static instance: UIDemoService | null = null;

  /**
   * Get singleton instance of UIDemoService
   */
  public static getInstance(): UIDemoService {
    if (!UIDemoService.instance) {
      UIDemoService.instance = new UIDemoService();
    }
    return UIDemoService.instance;
  }

  private constructor() {
    // Private constructor for singleton pattern
  }

  /**
   * Get demo button examples for UI testing
   */
  public getDemoButtons(): readonly DemoButtonExample[] {
    return generateDemoButtons();
  }

  /**
   * Get exclusion pattern examples
   */
  public getExclusionExamples(): readonly ExclusionExample[] {
    return generateExclusionExamples();
  }

  /**
   * Get implementation code snippets
   */
  public getCodeSnippets(): readonly CodeSnippet[] {
    return generateCodeSnippets();
  }

  /**
   * Get demo button by ID with error handling
   */
  public getDemoButtonById(id: string): DemoButtonExample | null {
    const buttons = this.getDemoButtons();
    return buttons.find(button => button.id === id) || null;
  }

  /**
   * Get exclusion example by ID with error handling
   */
  public getExclusionExampleById(id: string): ExclusionExample | null {
    const examples = this.getExclusionExamples();
    return examples.find(example => example.id === id) || null;
  }

  /**
   * Validate and normalize audio demo configuration
   */
  public validateAudioDemoConfig(config: Partial<AudioDemoConfiguration>): AudioDemoConfiguration {
    const mergedConfig = { ...DEFAULT_AUDIO_DEMO_CONFIG, ...config };
    
    if (!validateDemoConfiguration(mergedConfig)) {
      console.warn('Invalid demo configuration provided, using defaults');
      return DEFAULT_AUDIO_DEMO_CONFIG;
    }
    
    return mergedConfig;
  }

  /**
   * Validate and normalize drag test configuration
   */
  public validateDragTestConfig(config: Partial<DragTestConfiguration>): DragTestConfiguration {
    return { ...DEFAULT_DRAG_TEST_CONFIG, ...config };
  }

  /**
   * Get organized demo sections based on configuration
   */
  public getOrganizedDemoSections(config: AudioDemoConfiguration): {
    globalUIExamples: DemoButtonExample[] | null;
    exclusionExamples: ExclusionExample[] | null;
    codeSnippets: CodeSnippet[] | null;
  } {
    return {
      globalUIExamples: config.showGlobalUIExamples ? [...this.getDemoButtons()] : null,
      exclusionExamples: config.showExclusionExamples ? [...this.getExclusionExamples()] : null,
      codeSnippets: config.showImplementationTips ? [...this.getCodeSnippets()] : null
    };
  }

  /**
   * Get grouped examples by category for organized display
   */
  public getGroupedExamples(): Record<string, (DemoButtonExample | ExclusionExample)[]> {
    const allExamples = [...this.getDemoButtons(), ...this.getExclusionExamples()];
    return groupExamplesByCategory(allExamples);
  }

  /**
   * Get UI test routes with metadata
   */
  public getUITestRoutes(): readonly UITestRoute[] {
    return UI_TEST_ROUTES;
  }

  /**
   * Find UI test route by path
   */
  public getRouteByPath(path: string): UITestRoute | null {
    return UI_TEST_ROUTES.find(route => route.path === path) || null;
  }

  /**
   * Find UI test route by ID
   */
  public getRouteById(id: string): UITestRoute | null {
    return UI_TEST_ROUTES.find(route => route.id === id) || null;
  }

  /**
   * Get interactive element selectors for pattern demonstration
   */
  public getInteractiveSelectors() {
    return generateInteractiveSelectors();
  }

  /**
   * Get exclusion selectors for pattern demonstration
   */
  public getExclusionSelectors() {
    return generateExclusionSelectors();
  }

  /**
   * Get standard configurations for demo setup
   */
  public getStandardConfigurations() {
    return {
      uiInteractions: STANDARD_UI_INTERACTIONS,
      interactiveSelectors: STANDARD_INTERACTIVE_SELECTORS,
      exclusions: STANDARD_EXCLUSIONS,
      audioDemoConfig: DEFAULT_AUDIO_DEMO_CONFIG,
      dragTestConfig: DEFAULT_DRAG_TEST_CONFIG
    };
  }

  /**
   * Generate demo data for a specific configuration
   */
  public generateDemoData(config: AudioDemoConfiguration) {
    const demoData = {
      buttons: config.showGlobalUIExamples ? this.getDemoButtons() : [],
      exclusions: config.showExclusionExamples ? this.getExclusionExamples() : [],
      codeSnippets: config.showImplementationTips ? this.getCodeSnippets() : [],
      chessExamples: config.showChessAudioExamples ? this.getChessAudioExamples() : []
    };

    return demoData;
  }

  /**
   * Get chess-specific audio examples (placeholder for future implementation)
   */
  private getChessAudioExamples() {
    // Placeholder for chess-specific examples
    return [
      {
        id: 'chess-move',
        title: 'Chess Move Sound',
        description: 'Audio feedback when making a chess move',
        example: 'playMove(isCapture);'
      },
      {
        id: 'chess-check',
        title: 'Check Alert Sound', 
        description: 'Audio alert when king is in check',
        example: 'playCheck();'
      }
    ];
  }

  /**
   * Reset service to initial state (useful for testing)
   */
  public reset(): void {
    // Reset any cached data or state if needed in the future
    console.log('UIDemoService reset');
  }

  /**
   * Get service health status
   */
  public getHealthStatus() {
    return {
      status: 'healthy',
      version: '1.0.0',
      lastAccessed: new Date().toISOString(),
      availableRoutes: this.getUITestRoutes().length,
      availableDemoButtons: this.getDemoButtons().length,
      availableExclusionExamples: this.getExclusionExamples().length
    };
  }
}