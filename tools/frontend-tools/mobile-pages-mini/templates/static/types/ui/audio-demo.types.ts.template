// audio-demo.types.ts - Audio demo type definitions

/**
 * Configuration for audio demo sections
 */
export interface AudioDemoConfiguration {
  readonly showGlobalUIExamples: boolean;
  readonly showExclusionExamples: boolean;
  readonly showChessAudioExamples: boolean;
  readonly showImplementationTips: boolean;
}

/**
 * Represents a demo section on the audio page
 */
export interface DemoSection {
  readonly id: string;
  readonly title: string;
  readonly description: string;
  readonly codeExample?: string;
  readonly enabled: boolean;
}

/**
 * Demo button example for UI testing
 */
export interface DemoButtonExample {
  readonly id: string;
  readonly label: string;
  readonly element: string;
  readonly attributes?: Record<string, string>;
  readonly description: string;
  readonly codeExample: string;
}

/**
 * Exclusion pattern example
 */
export interface ExclusionExample {
  readonly id: string;
  readonly label: string;
  readonly element: string;
  readonly attributes: Record<string, string>;
  readonly description: string;
  readonly codeExample: string;
}

/**
 * Code snippet for implementation examples
 */
export interface CodeSnippet {
  readonly title: string;
  readonly code: string;
  readonly language?: string;
}

/**
 * Audio demo hook state
 */
export interface AudioDemoState {
  readonly config: AudioDemoConfiguration;
  readonly demoButtons: readonly DemoButtonExample[];
  readonly exclusionExamples: readonly ExclusionExample[];
  readonly codeSnippets: readonly CodeSnippet[];
  readonly isLoading: boolean;
  readonly selectedExample: string | null;
  readonly expandedSections: Record<string, boolean>;
  readonly hasContent: boolean;
  readonly activeExamplesCount: number;
  readonly enabledSectionsCount: number;
  readonly activeSections: Record<string, boolean>;
}

/**
 * Audio demo hook actions
 */
export interface AudioDemoActions {
  readonly updateConfig: (updates: Partial<AudioDemoConfiguration>) => void;
  readonly resetConfig: () => void;
  readonly toggleSection: (sectionKey: string) => void;
  readonly selectExample: (exampleId: string) => void;
  readonly clearSelection: () => void;
  readonly getSelectedExample: () => DemoButtonExample | ExclusionExample | null;
  readonly expandSection: (sectionId: string) => void;
  readonly collapseSection: (sectionId: string) => void;
  readonly toggleSectionExpansion: (sectionId: string) => void;
  readonly expandAllSections: () => void;
  readonly collapseAllSections: () => void;
  readonly refreshContent: () => void;
  readonly getGroupedExamples: () => Record<string, (DemoButtonExample | ExclusionExample)[]>;
  readonly validateCurrentConfig: () => AudioDemoConfiguration;
}

/**
 * Complete audio demo hook return type
 */
export interface AudioDemoHook extends AudioDemoState, AudioDemoActions {}