import { Howl } from 'howler';

export type SoundEffect = 'move' | 'capture' | 'check' | 'gameStart' | 'gameEnd' | 'error' | 'uiClick';

interface AudioSettings {
  enabled: boolean;
  volume: number; // 0-1
  moveSound: boolean;
  captureSound: boolean;
  checkSound: boolean;
  uiSounds: boolean;
}

class ChessAudioService {
  private sounds: Map<SoundEffect, Howl> = new Map();
  private audioContext: AudioContext | null = null;
  private settings: AudioSettings = {
    enabled: true,
    volume: 0.7,
    moveSound: true,
    captureSound: true,
    checkSound: true,
    uiSounds: true,
  };
  private initialized = false;

  constructor() {
    this.initializeSounds();
  }

  private initializeSounds() {
    // Try to use file-based sounds first, fallback to generated sounds
    const soundDefinitions: Record<SoundEffect, { src: string[]; volume: number; fallback: () => void }> = {
      move: {
        src: ['/sounds/move.mp3', '/sounds/move.wav'],
        volume: 0.6,
        fallback: () => this.generateTone(800, 0.1, 'sine'),
      },
      capture: {
        src: ['/sounds/capture.mp3', '/sounds/capture.wav'],
        volume: 0.8,
        fallback: () => this.generateTone(400, 0.2, 'sawtooth'),
      },
      check: {
        src: ['/sounds/check.mp3', '/sounds/check.wav'],
        volume: 0.9,
        fallback: () => this.generateBeep([800, 600], 0.15),
      },
      gameStart: {
        src: ['/sounds/game-start.mp3', '/sounds/game-start.wav'],
        volume: 0.7,
        fallback: () => this.generateBeep([523, 659, 784], 0.3),
      },
      gameEnd: {
        src: ['/sounds/game-end.mp3', '/sounds/game-end.wav'],
        volume: 0.7,
        fallback: () => this.generateBeep([784, 659, 523], 0.3),
      },
      error: {
        src: ['/sounds/error.mp3', '/sounds/error.wav'],
        volume: 0.5,
        fallback: () => this.generateTone(200, 0.3, 'square'),
      },
      uiClick: {
        src: ['/sounds/ui-click.mp3', '/sounds/ui-click.wav'],
        volume: 0.4,
        fallback: () => this.generateTone(1000, 0.05, 'sine'),
      },
    };

    // Create Howl instances for each sound
    Object.entries(soundDefinitions).forEach(([key, config]) => {
      const sound = new Howl({
        src: config.src,
        volume: config.volume * this.settings.volume,
        preload: false, // Don't preload files that might not exist
        html5: false, // Use Web Audio API when possible
        onloaderror: () => {
          console.warn(`Sound file not found: ${key}, using generated fallback`);
          // Store the fallback function for this sound
          (this.sounds.get(key as SoundEffect) as any)._fallback = config.fallback;
        },
        onload: () => {
          console.log(`✅ Sound file loaded: ${key}`);
        },
      });

      this.sounds.set(key as SoundEffect, sound);
    });

    this.initialized = true;
    console.log('🔊 Audio service initialized with fallbacks');
  }

  private createAudioContext(): AudioContext {
    if (!this.audioContext) {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    return this.audioContext;
  }

  private generateTone(frequency: number, duration: number, type: OscillatorType = 'sine'): void {
    try {
      const audioContext = this.createAudioContext();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
      oscillator.type = type;

      gainNode.gain.setValueAtTime(0, audioContext.currentTime);
      gainNode.gain.linearRampToValueAtTime(this.settings.volume * 0.3, audioContext.currentTime + 0.01);
      gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + duration);

      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + duration);
    } catch (error) {
      console.warn('Failed to generate tone:', error);
    }
  }

  private generateBeep(frequencies: number[], duration: number): void {
    frequencies.forEach((freq, index) => {
      setTimeout(() => {
        this.generateTone(freq, duration / frequencies.length);
      }, (duration * 1000 / frequencies.length) * index);
    });
  }

  public play(effect: SoundEffect): void {
    if (!this.initialized || !this.settings.enabled) {
      return;
    }

    // Check specific sound type settings
    switch (effect) {
      case 'move':
        if (!this.settings.moveSound) return;
        break;
      case 'capture':
        if (!this.settings.captureSound) return;
        break;
      case 'check':
        if (!this.settings.checkSound) return;
        break;
      case 'error':
      case 'gameStart':
      case 'gameEnd':
      case 'uiClick':
        if (!this.settings.uiSounds) return;
        break;
    }

    const sound = this.sounds.get(effect);
    if (sound) {
      try {
        // Check if user has interacted with the page (required for autoplay policies)
        if (this.canPlaySound()) {
          // Try to play the Howl sound first
          const playId = sound.play();
          
          // If play fails or sound wasn't loaded, use fallback
          if (!playId || sound.state() === 'unloaded') {
            const fallback = (sound as any)._fallback;
            if (fallback) {
              console.log(`🔊 Using generated sound fallback: ${effect}`);
              fallback();
            } else {
              console.log(`🔊 Playing sound: ${effect}`);
            }
          } else {
            console.log(`🔊 Playing sound file: ${effect}`);
          }
        } else {
          console.warn('🔊 Cannot play sound - user interaction required');
        }
      } catch (error) {
        console.error(`🔊 Error playing sound ${effect}:`, error);
        // Try fallback on error
        const fallback = (sound as any)._fallback;
        if (fallback) {
          console.log(`🔊 Using fallback due to error: ${effect}`);
          fallback();
        }
      }
    } else {
      console.warn(`🔊 Sound not found: ${effect}`);
    }
  }

  public playMove(wasCapture: boolean = false): void {
    this.play(wasCapture ? 'capture' : 'move');
  }

  public playCheck(): void {
    this.play('check');
  }

  public playError(): void {
    this.play('error');
  }

  public playGameStart(): void {
    this.play('gameStart');
  }

  public playGameEnd(): void {
    this.play('gameEnd');
  }

  public playUIClick(): void {
    this.play('uiClick');
  }

  public setVolume(volume: number): void {
    this.settings.volume = Math.max(0, Math.min(1, volume));
    
    // Update all sound volumes
    this.sounds.forEach((sound) => {
      sound.volume(this.settings.volume);
    });
    
    console.log(`🔊 Volume set to: ${this.settings.volume}`);
  }

  public toggleEnabled(): void {
    this.settings.enabled = !this.settings.enabled;
    console.log(`🔊 Audio ${this.settings.enabled ? 'enabled' : 'disabled'}`);
  }

  public setEnabled(enabled: boolean): void {
    this.settings.enabled = enabled;
    console.log(`🔊 Audio ${enabled ? 'enabled' : 'disabled'}`);
  }

  public setSoundType(type: keyof Omit<AudioSettings, 'enabled' | 'volume'>, enabled: boolean): void {
    this.settings[type] = enabled;
    console.log(`🔊 ${type} ${enabled ? 'enabled' : 'disabled'}`);
  }

  public getSettings(): AudioSettings {
    return { ...this.settings };
  }

  public updateSettings(newSettings: Partial<AudioSettings>): void {
    this.settings = { ...this.settings, ...newSettings };
    
    if (newSettings.volume !== undefined) {
      this.setVolume(newSettings.volume);
    }
  }

  private canPlaySound(): boolean {
    // Check if the document has focus and user has interacted
    return document.hasFocus() && this.hasUserInteracted();
  }

  private hasUserInteracted(): boolean {
    // Simple check - in a real app, you'd track user interactions
    // For now, assume interaction if the page is focused
    return document.hasFocus();
  }

  // Preload all sounds (call this on user's first interaction)
  public preloadSounds(): void {
    this.sounds.forEach((sound) => {
      sound.load();
    });
    console.log('🔊 All sounds preloaded');
  }

  // Cleanup method
  public destroy(): void {
    this.sounds.forEach((sound) => {
      sound.unload();
    });
    this.sounds.clear();
    console.log('🔊 Audio service destroyed');
  }
}

// Create singleton instance
export const audioService = new ChessAudioService();

// Hook for React components
export function useChessAudio() {
  return {
    playMove: (wasCapture: boolean = false) => audioService.playMove(wasCapture),
    playCheck: () => audioService.playCheck(),
    playError: () => audioService.playError(),
    playGameStart: () => audioService.playGameStart(),
    playGameEnd: () => audioService.playGameEnd(),
    playUIClick: () => audioService.playUIClick(),
    setVolume: (volume: number) => audioService.setVolume(volume),
    toggleEnabled: () => audioService.toggleEnabled(),
    setEnabled: (enabled: boolean) => audioService.setEnabled(enabled),
    getSettings: () => audioService.getSettings(),
    updateSettings: (settings: Partial<AudioSettings>) => audioService.updateSettings(settings),
    preloadSounds: () => audioService.preloadSounds(),
  };
}

export default audioService;