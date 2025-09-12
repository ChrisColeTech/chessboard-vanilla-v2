import { useEffect } from 'react';

interface GlobalUIAudioConfig {
  enabled: boolean;
  autoDetection: boolean;
  excludeSelectors: string[];
}

interface UseGlobalUIAudioProps {
  autoInitialize: boolean;
  initialConfig: GlobalUIAudioConfig;
}

export const useGlobalUIAudio = ({ autoInitialize, initialConfig }: UseGlobalUIAudioProps) => {
  useEffect(() => {
    if (!autoInitialize) return;

    const handleClick = (event: Event) => {
      const target = event.target as HTMLElement;
      
      // Check if element should be excluded
      const shouldExclude = initialConfig.excludeSelectors.some(selector => {
        if (selector.startsWith('[') && selector.endsWith(']')) {
          const attr = selector.slice(1, -1);
          return target.hasAttribute(attr);
        }
        if (selector.startsWith('.')) {
          const className = selector.slice(1);
          return target.classList.contains(className);
        }
        return target.matches(selector);
      });

      if (!shouldExclude && initialConfig.enabled) {
        // Play UI sound (placeholder implementation)
        console.log('UI Sound: click');
      }
    };

    if (initialConfig.autoDetection) {
      document.addEventListener('click', handleClick);
    }

    return () => {
      document.removeEventListener('click', handleClick);
    };
  }, [autoInitialize, initialConfig]);

  return {
    playUISound: (soundType: string) => {
      console.log(`UI Sound: ${soundType}`);
    }
  };
};
