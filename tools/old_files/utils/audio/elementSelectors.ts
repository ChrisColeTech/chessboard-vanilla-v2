// elementSelectors.ts - Pre-defined selectors for common UI elements

import type { UIElementSelector } from '../../types/audio/ui-audio.types';

/**
 * Default UI selectors for automatic audio detection
 * Higher priority numbers take precedence over lower ones
 */
export const DEFAULT_UI_SELECTORS: UIElementSelector[] = [
  // Standard HTML buttons
  {
    selector: 'button',
    interactionType: 'click',
    priority: 10
  },
  
  // Elements with button role
  {
    selector: '[role="button"]',
    interactionType: 'click',
    priority: 10
  },
  
  // Tab elements (higher priority for specialized behavior)
  {
    selector: '[role="tab"]',
    interactionType: 'click',
    priority: 15
  },
  
  // Links with href (clickable links)
  {
    selector: 'a[href]',
    interactionType: 'click',
    priority: 8
  },
  
  // Input elements (submit buttons, checkboxes, radio buttons)
  {
    selector: 'input[type="submit"]',
    interactionType: 'click',
    priority: 12
  },
  {
    selector: 'input[type="button"]',
    interactionType: 'click',
    priority: 12
  },
  {
    selector: 'input[type="checkbox"]',
    interactionType: 'click',
    priority: 9
  },
  {
    selector: 'input[type="radio"]',
    interactionType: 'click',
    priority: 9
  },
  
  // Custom clickable class (for elements made clickable with CSS/JS)
  {
    selector: '.clickable',
    interactionType: 'click',
    priority: 5
  },
  
  // Menu items and dropdowns
  {
    selector: '[role="menuitem"]',
    interactionType: 'click',
    priority: 11
  },
  {
    selector: '[role="option"]',
    interactionType: 'click',
    priority: 11
  },
  
  // Toggle switches and controls
  {
    selector: '[role="switch"]',
    interactionType: 'click',
    priority: 13
  }
];

/**
 * Default exclusion selectors - elements that should NOT play sounds
 */
export const DEFAULT_EXCLUSION_SELECTORS: string[] = [
  // Explicitly disabled elements
  '[data-no-sound]',
  '.no-sound',
  
  // Disabled form elements
  '[disabled]',
  '.disabled',
  
  // Chess-specific game elements (handled separately)
  '.chess-piece',
  '.chess-square',
  '.chess-board',
  
  // Elements that might have their own audio handling
  'video',
  'audio',
  
  // Hidden or invisible elements
  '[hidden]',
  '.hidden',
  '[style*="display: none"]',
  '[style*="visibility: hidden"]'
];

/**
 * Check if an element matches any exclusion selector
 */
export function isElementExcluded(element: Element): boolean {
  return DEFAULT_EXCLUSION_SELECTORS.some(selector => {
    try {
      return element.matches(selector);
    } catch {
      // Invalid selector, skip it
      return false;
    }
  });
}

/**
 * Find the best matching selector for an element
 * Returns the selector with the highest priority that matches
 */
export function findBestMatchingSelector(
  element: Element, 
  selectors: UIElementSelector[] = DEFAULT_UI_SELECTORS
): UIElementSelector | null {
  const matches: UIElementSelector[] = [];
  
  for (const selector of selectors) {
    try {
      if (element.matches(selector.selector)) {
        matches.push(selector);
      }
    } catch {
      // Invalid selector, skip it
      continue;
    }
  }
  
  // Return selector with highest priority
  return matches.length > 0 
    ? matches.reduce((best, current) => 
        current.priority > best.priority ? current : best
      )
    : null;
}

/**
 * Check if an element or any of its ancestors matches a selector
 * Useful for handling clicks on child elements of buttons
 */
export function findClickableAncestor(
  element: Element,
  selectors: UIElementSelector[] = DEFAULT_UI_SELECTORS
): { element: Element; selector: UIElementSelector } | null {
  let current: Element | null = element;
  
  while (current && current !== document.body) {
    // Check if this element is excluded first
    if (isElementExcluded(current)) {
      return null;
    }
    
    // Check if this element matches any selector
    const matchingSelector = findBestMatchingSelector(current, selectors);
    if (matchingSelector) {
      return { element: current, selector: matchingSelector };
    }
    
    current = current.parentElement;
  }
  
  return null;
}