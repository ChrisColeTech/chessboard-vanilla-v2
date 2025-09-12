// global-audio.types.ts - Type definitions for global UI audio (stub implementation)

import type { UIElementSelector } from './ui-audio.types';

export interface GlobalUIAudioConfig {
  enabled: boolean;
  autoDetection: boolean;
  customSelectors: UIElementSelector[];
  excludeSelectors: string[];
  exclusions: string[];
}

export type GlobalUIAudioConfigUpdate = Partial<GlobalUIAudioConfig>;

export interface ElementDetectionResult {
  shouldPlaySound: boolean;
  element: Element;
  matchedSelector?: string;
  priority?: number;
}

export type GlobalClickHandler = (event: Event) => void;

export interface GlobalUIAudioService {
  initialize(): void;
  destroy(): void;
  configure(configUpdate: GlobalUIAudioConfigUpdate): void;
  addCustomSelector(selector: UIElementSelector): void;
  removeCustomSelector(selectorString: string): void;
  getConfig(): GlobalUIAudioConfig;
  isInitialized(): boolean;
}