// pattern-helpers.utils.ts - Pattern demonstration and helper utilities

import type { 
  UIInteractionType,
  UISoundType,
  UIElementSelector,
  DemoButtonExample,
  ExclusionExample 
} from '../../types';

/**
 * Generate interactive element selector patterns
 */
export const generateInteractiveSelectors = (): readonly UIElementSelector[] => {
  return [
    { selector: 'button', interactionType: 'click', priority: 1 },
    { selector: 'a[href]', interactionType: 'click', priority: 2 },
    { selector: '[role="button"]', interactionType: 'click', priority: 3 },
    { selector: 'input[type="submit"]', interactionType: 'click', priority: 4 },
    { selector: 'input[type="button"]', interactionType: 'click', priority: 5 },
    { selector: '[tabindex]:not([tabindex="-1"])', interactionType: 'focus', priority: 6 }
  ];
};

/**
 * Generate exclusion selector patterns
 */
export const generateExclusionSelectors = (): readonly string[] => {
  return [
    '[data-no-sound]',
    '.no-sound',
    '.chess-piece',
    '.chess-square',
    '[disabled]',
    '.disabled'
  ];
};

/**
 * Map interaction types to sound types for demonstration
 */
export const mapInteractionToSound = (interaction: UIInteractionType): UISoundType => {
  switch (interaction) {
    case 'click':
      return 'uiClick';
    case 'hover':
      return 'uiHover';
    case 'focus':
      return 'uiSelect';
    case 'select':
      return 'uiSelect';
    default:
      return 'uiClick';
  }
};

/**
 * Generate CSS selector from demo button example
 */
export const generateSelectorFromExample = (example: DemoButtonExample): string => {
  let selector = example.element;
  
  if (example.attributes) {
    Object.entries(example.attributes).forEach(([key, value]) => {
      if (key === 'className' || key === 'class') {
        selector += `.${value.split(' ').join('.')}`;
      } else if (key === 'role') {
        selector += `[role="${value}"]`;
      } else if (key === 'type') {
        selector += `[type="${value}"]`;
      } else if (key === 'href') {
        selector += `[href="${value}"]`;
      } else {
        selector += `[${key}="${value}"]`;
      }
    });
  }
  
  return selector;
};

/**
 * Check if element matches exclusion patterns
 */
export const matchesExclusionPattern = (
  element: HTMLElement, 
  exclusionSelectors: readonly string[]
): boolean => {
  return exclusionSelectors.some(selector => {
    try {
      return element.matches(selector);
    } catch {
      return false;
    }
  });
};

/**
 * Validate demo configuration for completeness
 */
export const validateDemoConfiguration = (config: {
  showGlobalUIExamples?: boolean;
  showExclusionExamples?: boolean;
  showChessAudioExamples?: boolean;
  showImplementationTips?: boolean;
}): boolean => {
  return Object.values(config).some(value => value === true);
};

/**
 * Generate implementation tip based on example type
 */
export const generateImplementationTip = (
  example: DemoButtonExample | ExclusionExample
): string => {
  if ('codeExample' in example) {
    if (example.id.includes('silent') || example.id.includes('no-sound')) {
      return `Exclusion Pattern: ${example.element} elements with these attributes are automatically excluded from UI sounds.`;
    }
    
    if (example.id.includes('disabled')) {
      return 'Accessibility Pattern: Disabled elements are automatically excluded to prevent confusing audio feedback.';
    }
    
    if (example.id.includes('chess')) {
      return 'Game-Specific Pattern: Chess elements use manual audio calls instead of global UI sounds for game-specific feedback.';
    }
    
    return `Interactive Pattern: ${example.element} elements are automatically detected and enhanced with UI sounds.`;
  }
  
  return 'Standard interactive element with automatic sound integration.';
};

/**
 * Extract element type from selector
 */
export const extractElementTypeFromSelector = (selector: string): string => {
  const match = selector.match(/^([a-zA-Z]+)/);
  return match ? match[1] : 'element';
};

/**
 * Check if selector targets interactive element
 */
export const isInteractiveSelector = (
  selector: string,
  interactiveSelectors: readonly UIElementSelector[]
): boolean => {
  return interactiveSelectors.some(pattern => {
    try {
      // Simple pattern matching for demonstration
      if (pattern.selector === selector) return true;
      if (pattern.selector.includes('[') && selector.includes('[')) {
        return pattern.selector.split('[')[0] === selector.split('[')[0];
      }
      return false;
    } catch {
      return false;
    }
  });
};

/**
 * Group examples by category for organized display
 */
export const groupExamplesByCategory = (
  examples: readonly (DemoButtonExample | ExclusionExample)[]
): Record<string, (DemoButtonExample | ExclusionExample)[]> => {
  return examples.reduce((groups, example) => {
    let category = 'Other';
    
    if (example.id.includes('button')) {
      category = 'Buttons';
    } else if (example.id.includes('input')) {
      category = 'Inputs';
    } else if (example.id.includes('link')) {
      category = 'Links';
    } else if (example.id.includes('aria')) {
      category = 'ARIA Elements';
    } else if (example.id.includes('silent') || example.id.includes('no-sound')) {
      category = 'Exclusions';
    } else if (example.id.includes('chess')) {
      category = 'Game Elements';
    }
    
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(example);
    
    return groups;
  }, {} as Record<string, (DemoButtonExample | ExclusionExample)[]>);
};

/**
 * Format selector for display in documentation
 */
export const formatSelectorForDisplay = (selector: string): string => {
  return selector
    .replace(/\[([^\]]+)\]/g, '[$1]')  // Keep attribute selectors readable
    .replace(/:/g, ':')                 // Keep pseudo selectors readable
    .trim();
};