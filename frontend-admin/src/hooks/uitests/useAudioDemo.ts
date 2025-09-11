// useAudioDemo.ts - Hook for managing audio demo functionality

import { useState, useCallback, useMemo, useEffect } from 'react';
import type {
  AudioDemoState,
  AudioDemoActions,
  AudioDemoHook,
  AudioDemoConfiguration,
  DemoButtonExample,
  ExclusionExample,
  CodeSnippet
} from '../../types';
import { UIDemoService } from '../../services';
import { DEFAULT_AUDIO_DEMO_CONFIG } from '../../constants';

/**
 * Hook for managing audio demo state and functionality
 */
export const useAudioDemo = (
  initialConfig?: Partial<AudioDemoConfiguration>
): AudioDemoHook => {
  const demoService = useMemo(() => UIDemoService.getInstance(), []);

  // Initialize configuration
  const [config, setConfig] = useState<AudioDemoConfiguration>(() => {
    return demoService.validateAudioDemoConfig(initialConfig || {});
  });

  // Demo content state
  const [demoButtons, setDemoButtons] = useState<readonly DemoButtonExample[]>([]);
  const [exclusionExamples, setExclusionExamples] = useState<readonly ExclusionExample[]>([]);
  const [codeSnippets, setCodeSnippets] = useState<readonly CodeSnippet[]>([]);

  // UI state
  const [isLoading, setIsLoading] = useState(false);
  const [selectedExample, setSelectedExample] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    globalUI: true,
    exclusions: false,
    implementation: false,
    chessAudio: false
  });

  // Load demo content based on configuration
  const loadDemoContent = useCallback(() => {
    setIsLoading(true);
    
    try {
      const { globalUIExamples, exclusionExamples: exclusions, codeSnippets: snippets } = 
        demoService.getOrganizedDemoSections(config);

      setDemoButtons(globalUIExamples || []);
      setExclusionExamples(exclusions || []);
      setCodeSnippets(snippets || []);
    } catch (error) {
      console.error('Failed to load demo content:', error);
    } finally {
      setIsLoading(false);
    }
  }, [config, demoService]);

  // Load content when config changes
  useEffect(() => {
    loadDemoContent();
  }, [loadDemoContent]);

  // Configuration actions
  const updateConfig = useCallback((updates: Partial<AudioDemoConfiguration>) => {
    const newConfig = demoService.validateAudioDemoConfig({ ...config, ...updates });
    setConfig(newConfig);
  }, [config, demoService]);

  const resetConfig = useCallback(() => {
    setConfig(DEFAULT_AUDIO_DEMO_CONFIG);
  }, []);

  const toggleSection = useCallback((sectionKey: string) => {
    updateConfig({ [sectionKey]: !config[sectionKey as keyof AudioDemoConfiguration] });
  }, [config, updateConfig]);

  // Example selection actions
  const selectExample = useCallback((exampleId: string) => {
    setSelectedExample(exampleId);
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedExample(null);
  }, []);

  const getSelectedExample = useCallback((): DemoButtonExample | ExclusionExample | null => {
    if (!selectedExample) return null;
    
    return demoService.getDemoButtonById(selectedExample) || 
           demoService.getExclusionExampleById(selectedExample);
  }, [selectedExample, demoService]);

  // Section expansion actions
  const expandSection = useCallback((sectionId: string) => {
    setExpandedSections(prev => ({ ...prev, [sectionId]: true }));
  }, []);

  const collapseSection = useCallback((sectionId: string) => {
    setExpandedSections(prev => ({ ...prev, [sectionId]: false }));
  }, []);

  const toggleSectionExpansion = useCallback((sectionId: string) => {
    setExpandedSections(prev => ({ ...prev, [sectionId]: !prev[sectionId] }));
  }, []);

  const expandAllSections = useCallback(() => {
    setExpandedSections({
      globalUI: true,
      exclusions: true,
      implementation: true,
      chessAudio: true
    });
  }, []);

  const collapseAllSections = useCallback(() => {
    setExpandedSections({
      globalUI: false,
      exclusions: false,
      implementation: false,
      chessAudio: false
    });
  }, []);

  // Utility actions
  const refreshContent = useCallback(() => {
    loadDemoContent();
  }, [loadDemoContent]);

  const getGroupedExamples = useCallback(() => {
    return demoService.getGroupedExamples();
  }, [demoService]);

  const validateCurrentConfig = useCallback(() => {
    return demoService.validateAudioDemoConfig(config);
  }, [config, demoService]);

  // Computed values
  const hasContent = demoButtons.length > 0 || exclusionExamples.length > 0 || codeSnippets.length > 0;
  const activeExamplesCount = demoButtons.length + exclusionExamples.length;
  const enabledSectionsCount = Object.values(config).filter(Boolean).length;
  
  const activeSections = useMemo(() => {
    return {
      globalUI: config.showGlobalUIExamples,
      exclusions: config.showExclusionExamples,
      implementation: config.showImplementationTips,
      chessAudio: config.showChessAudioExamples
    };
  }, [config]);

  // State object
  const state: AudioDemoState = {
    config,
    demoButtons,
    exclusionExamples,
    codeSnippets,
    isLoading,
    selectedExample,
    expandedSections,
    hasContent,
    activeExamplesCount,
    enabledSectionsCount,
    activeSections
  };

  // Actions object  
  const actions: AudioDemoActions = {
    updateConfig,
    resetConfig,
    toggleSection,
    selectExample,
    clearSelection,
    getSelectedExample,
    expandSection,
    collapseSection,
    toggleSectionExpansion,
    expandAllSections,
    collapseAllSections,
    refreshContent,
    getGroupedExamples,
    validateCurrentConfig
  };

  // Return hook interface
  return {
    ...state,
    ...actions
  };
};