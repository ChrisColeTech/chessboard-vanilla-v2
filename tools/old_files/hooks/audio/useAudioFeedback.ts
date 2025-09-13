// useAudioFeedback.ts - Generic audio feedback patterns and decision logic

import { useState, useCallback, useRef } from 'react';
import type { 
  AudioFeedbackPattern, 
  AudioFeedbackContext, 
  AudioFeedbackDecision,
  ComponentAudioConfig
} from '../../types/audio/audio-feedback.types';

/**
 * Generic audio feedback hook for components
 * Provides decision logic and timing for audio feedback
 */
export const useAudioFeedback = (config: ComponentAudioConfig) => {
  const [isEnabled, setIsEnabled] = useState(config.enabled);
  const [currentVolume, setCurrentVolume] = useState(config.defaultVolume);
  const lastFeedbackTime = useRef<number>(0);

  /**
   * Evaluate whether audio feedback should be played
   * @param context - Context information for the feedback decision
   * @returns Decision result with pattern and settings
   */
  const evaluateFeedback = useCallback((context: AudioFeedbackContext): AudioFeedbackDecision => {
    // Quick exit if disabled
    if (!isEnabled) {
      return {
        shouldPlay: false,
        reason: 'Audio feedback disabled'
      };
    }

    // Check for user preferences
    if (context.reducedAudio) {
      return {
        shouldPlay: false,
        reason: 'User prefers reduced audio'
      };
    }

    // Find appropriate pattern
    const pattern = config.patterns.find(p => 
      p.enabled && p.id === context.interactionType
    ) || config.patterns.find(p => 
      p.enabled && p.id === config.defaultPattern
    );

    if (!pattern) {
      return {
        shouldPlay: false,
        reason: 'No suitable pattern found'
      };
    }

    // Check timing constraints
    const now = Date.now();
    const timeSinceLastFeedback = now - lastFeedbackTime.current;
    const minInterval = pattern.timing.duration || 100;

    if (timeSinceLastFeedback < minInterval && !pattern.timing.interrupt) {
      return {
        shouldPlay: false,
        reason: 'Too soon since last feedback',
        pattern
      };
    }

    // Calculate adjusted volume
    const contextVolume = context.currentVolume || currentVolume;
    const adjustedVolume = contextVolume * pattern.volumeMultiplier;

    return {
      shouldPlay: true,
      pattern,
      adjustedVolume,
      reason: `Playing ${pattern.name} at ${Math.round(adjustedVolume * 100)}% volume`
    };
  }, [isEnabled, currentVolume, config.patterns, config.defaultPattern]);

  /**
   * Execute audio feedback with timing and volume control
   * @param decision - Result from evaluateFeedback
   * @param playFunction - Function to actually play the audio
   */
  const executeFeedback = useCallback((
    decision: AudioFeedbackDecision, 
    playFunction: (volume?: number) => void
  ) => {
    if (!decision.shouldPlay || !decision.pattern) {
      return;
    }

    const pattern = decision.pattern;
    const now = Date.now();

    // Update last feedback time
    lastFeedbackTime.current = now;

    // Apply delay if specified
    const delay = pattern.timing.delay || 0;
    
    if (delay > 0) {
      setTimeout(() => {
        playFunction(decision.adjustedVolume);
      }, delay);
    } else {
      playFunction(decision.adjustedVolume);
    }

    // Log feedback for debugging
    console.log(`🔊 [AudioFeedback] ${decision.reason}`);
  }, []);

  /**
   * Convenience method to evaluate and execute feedback in one call
   * @param context - Context for the feedback
   * @param playFunction - Function to play the audio
   */
  const playFeedback = useCallback((
    context: AudioFeedbackContext,
    playFunction: (volume?: number) => void
  ) => {
    const decision = evaluateFeedback(context);
    executeFeedback(decision, playFunction);
  }, [evaluateFeedback, executeFeedback]);

  /**
   * Get pattern by interaction type
   * @param interactionType - Type of interaction to get pattern for
   * @returns Pattern if found, undefined otherwise
   */
  const getPattern = useCallback((interactionType: string): AudioFeedbackPattern | undefined => {
    return config.patterns.find(p => p.id === interactionType);
  }, [config.patterns]);

  /**
   * Update volume level
   * @param volume - New volume level (0-1)
   */
  const updateVolume = useCallback((volume: number) => {
    setCurrentVolume(Math.max(0, Math.min(1, volume)));
  }, []);

  /**
   * Toggle audio feedback enabled state
   */
  const toggleEnabled = useCallback(() => {
    setIsEnabled(prev => !prev);
  }, []);

  return {
    // Core methods
    evaluateFeedback,
    executeFeedback,
    playFeedback,
    getPattern,
    
    // State management
    isEnabled,
    setIsEnabled: setIsEnabled,
    toggleEnabled,
    currentVolume,
    updateVolume,
    
    // Utilities
    timeSinceLastFeedback: () => Date.now() - lastFeedbackTime.current,
    resetFeedbackTimer: () => { lastFeedbackTime.current = 0; }
  };
};