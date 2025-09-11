// index.ts - UI tests utils barrel export

// Demo examples utilities
export {
  generateDemoButtons,
  generateExclusionExamples,
  generateCodeSnippets,
  formatCodeSnippet,
  getDemoButtonById,
  getExclusionExampleById
} from './demo-examples.utils';

// Pattern helpers utilities
export {
  generateInteractiveSelectors,
  generateExclusionSelectors,
  mapInteractionToSound,
  generateSelectorFromExample,
  matchesExclusionPattern,
  validateDemoConfiguration,
  generateImplementationTip,
  extractElementTypeFromSelector,
  isInteractiveSelector,
  groupExamplesByCategory,
  formatSelectorForDisplay
} from './pattern-helpers.utils';