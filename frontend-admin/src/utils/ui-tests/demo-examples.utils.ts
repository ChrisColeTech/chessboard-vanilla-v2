// demo-examples.utils.ts - Pure functions for generating demo examples

import type { 
  DemoButtonExample, 
  ExclusionExample, 
  CodeSnippet 
} from '../../types/ui/audio-demo.types';

/**
 * Generate demo buttons for UI audio testing
 */
export const generateDemoButtons = (): readonly DemoButtonExample[] => {
  return [
    {
      id: 'standard-button',
      label: 'Standard Button',
      element: 'button',
      description: 'Automatically gets uiClick sound via Global UI Audio',
      codeExample: '<button>Click me</button>'
    },
    {
      id: 'aria-button',
      label: 'ARIA Button',
      element: 'div',
      attributes: { role: 'button' },
      description: 'ARIA buttons automatically detected',
      codeExample: '<div role="button">ARIA Button</div>'
    },
    {
      id: 'link-button',
      label: 'Link Button',
      element: 'a',
      attributes: { href: '#demo' },
      description: 'Links with href automatically get click sounds',
      codeExample: '<a href="#demo">Link Button</a>'
    },
    {
      id: 'submit-input',
      label: 'Submit Input',
      element: 'input',
      attributes: { type: 'submit', value: 'Submit' },
      description: 'Submit inputs automatically detected',
      codeExample: '<input type="submit" value="Submit" />'
    },
    {
      id: 'button-input',
      label: 'Button Input',
      element: 'input',
      attributes: { type: 'button', value: 'Button Input' },
      description: 'Button inputs automatically detected',
      codeExample: '<input type="button" value="Button Input" />'
    }
  ];
};

/**
 * Generate examples of exclusion patterns
 */
export const generateExclusionExamples = (): readonly ExclusionExample[] => {
  return [
    {
      id: 'silent-button',
      label: 'Silent Button',
      element: 'button',
      attributes: { 'data-no-sound': '' },
      description: 'Use data-no-sound to exclude elements',
      codeExample: '<button data-no-sound>Silent Button</button>'
    },
    {
      id: 'no-sound-class',
      label: 'No Sound Class',
      element: 'button',
      attributes: { className: 'no-sound' },
      description: 'Use .no-sound class to exclude elements',
      codeExample: '<button class="no-sound">Silent Button</button>'
    },
    {
      id: 'chess-piece',
      label: 'Chess Element',
      element: 'div',
      attributes: { className: 'chess-piece' },
      description: 'Chess elements automatically excluded',
      codeExample: '<div class="chess-piece">♔</div>'
    },
    {
      id: 'disabled-button',
      label: 'Disabled Button',
      element: 'button',
      attributes: { disabled: 'true' },
      description: 'Disabled elements automatically excluded',
      codeExample: '<button disabled>Disabled Button</button>'
    }
  ];
};

/**
 * Generate code snippets for implementation examples
 */
export const generateCodeSnippets = (): readonly CodeSnippet[] => {
  return [
    {
      title: 'Global UI Audio Setup',
      language: 'typescript',
      code: `// In App.tsx
useGlobalUIAudio({
  autoInitialize: true,
  initialConfig: {
    enabled: true,
    excludeSelectors: ['.chess-piece', '[data-no-sound]']
  }
});`
    },
    {
      title: 'Manual Chess Audio',
      language: 'typescript',
      code: `// In chess components
const { playMove, playCapture, playCheck } = useChessAudio();

// Call manually for game events
playMove(isCapture);
playCheck();
playError();`
    },
    {
      title: 'Excluding Elements',
      language: 'html',
      code: `<!-- Manual exclusion -->
<button data-no-sound>Silent Button</button>
<div class="no-sound">Silent Element</div>

<!-- Automatic exclusions -->
<div class="chess-piece">Game Element</div>
<button disabled>Disabled Button</button>`
    },
    {
      title: 'Service Configuration',
      language: 'typescript',
      code: `// Runtime configuration changes
const { configure } = useGlobalUIAudio();

configure({
  enabled: false,  // Temporarily disable
  excludeSelectors: [
    ...existingSelectors,
    '.my-custom-exclusion'
  ]
});`
    }
  ];
};

/**
 * Format code snippet for display
 */
export const formatCodeSnippet = (snippet: CodeSnippet): string => {
  const lines = snippet.code.split('\n');
  const trimmedLines = lines.map(line => line.trim()).filter(line => line.length > 0);
  return trimmedLines.join('\n');
};

/**
 * Get demo button by ID
 */
export const getDemoButtonById = (id: string): DemoButtonExample | null => {
  const demoButtons = generateDemoButtons();
  return demoButtons.find(button => button.id === id) || null;
};

/**
 * Get exclusion example by ID
 */
export const getExclusionExampleById = (id: string): ExclusionExample | null => {
  const exclusionExamples = generateExclusionExamples();
  return exclusionExamples.find(example => example.id === id) || null;
};