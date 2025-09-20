import { useMusicStore } from '../../stores/musicStore';
import type { Track } from '../../types/music/music.types';

class MusicAudioService {
  private audio: HTMLAudioElement | null = null;
  private updateInterval: NodeJS.Timeout | null = null;
  private fadeInterval: NodeJS.Timeout | null = null;
  
  constructor() {
    this.setupAudio();
  }

  private setupAudio() {
    if (typeof window === 'undefined') return;
    
    this.audio = new Audio();
    this.audio.preload = 'metadata';
    
    // Audio event listeners
    this.audio.addEventListener('loadstart', this.handleLoadStart);
    this.audio.addEventListener('loadedmetadata', this.handleLoadedMetadata);
    this.audio.addEventListener('canplay', this.handleCanPlay);
    this.audio.addEventListener('play', this.handlePlay);
    this.audio.addEventListener('pause', this.handlePause);
    this.audio.addEventListener('ended', this.handleEnded);
    this.audio.addEventListener('error', this.handleError);
    this.audio.addEventListener('timeupdate', this.handleTimeUpdate);
    this.audio.addEventListener('volumechange', this.handleVolumeChange);
  }

  private handleLoadStart = () => {
    const { player } = useMusicStore.getState();
    useMusicStore.setState({
      player: { ...player, isLoading: true }
    });
  };

  private handleLoadedMetadata = () => {
    if (!this.audio) return;
    
    const { player } = useMusicStore.getState();
    useMusicStore.setState({
      player: {
        ...player,
        duration: this.audio.duration,
        isLoading: false
      }
    });
  };

  private handleCanPlay = () => {
    const { player } = useMusicStore.getState();
    useMusicStore.setState({
      player: { ...player, isLoading: false }
    });
  };

  private handlePlay = () => {
    this.startTimeUpdates();
  };

  private handlePause = () => {
    this.stopTimeUpdates();
  };

  private handleEnded = () => {
    const { nextTrack } = useMusicStore.getState();
    const { player } = useMusicStore.getState();
    
    if (player.repeat === 'one') {
      this.seekTo(0);
      this.play();
    } else {
      nextTrack();
    }
  };

  private handleError = (e: Event) => {
    console.error('Audio playback error:', e);
    const { player } = useMusicStore.getState();
    useMusicStore.setState({
      player: { ...player, isLoading: false, isPlaying: false }
    });
  };

  private handleTimeUpdate = () => {
    if (!this.audio) return;
    
    const { setCurrentTime } = useMusicStore.getState();
    setCurrentTime(this.audio.currentTime);
  };

  private handleVolumeChange = () => {
    // Handle external volume changes if needed
  };

  private startTimeUpdates() {
    if (this.updateInterval) return;
    
    this.updateInterval = setInterval(() => {
      if (this.audio && !this.audio.paused) {
        this.handleTimeUpdate();
      }
    }, 100);
  }

  private stopTimeUpdates() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
      this.updateInterval = null;
    }
  }

  // Public methods
  async loadTrack(track: Track): Promise<void> {
    if (!this.audio) return;
    
    try {
      // For demo purposes, we'll use a placeholder audio URL
      // In a real app, this would be the actual audio file URL
      const audioUrl = track.audioUrl || this.getPlaceholderAudioUrl(track);
      
      if (this.audio.src !== audioUrl) {
        this.audio.src = audioUrl;
      }
      
      // Set volume from store
      const { player } = useMusicStore.getState();
      this.audio.volume = player.isMuted ? 0 : player.volume;
      
    } catch (error) {
      console.error('Error loading track:', error);
      throw error;
    }
  }

  async play(): Promise<void> {
    if (!this.audio) return;
    
    try {
      await this.audio.play();
    } catch (error) {
      console.error('Error playing audio:', error);
      throw error;
    }
  }

  pause(): void {
    if (!this.audio) return;
    this.audio.pause();
  }

  seekTo(time: number): void {
    if (!this.audio) return;
    this.audio.currentTime = Math.max(0, Math.min(time, this.audio.duration || 0));
  }

  setVolume(volume: number): void {
    if (!this.audio) return;
    this.audio.volume = Math.max(0, Math.min(1, volume));
  }

  mute(): void {
    if (!this.audio) return;
    this.audio.muted = true;
  }

  unmute(): void {
    if (!this.audio) return;
    this.audio.muted = false;
  }

  fadeOut(duration: number = 1000): Promise<void> {
    return new Promise((resolve) => {
      if (!this.audio) {
        resolve();
        return;
      }

      const startVolume = this.audio.volume;
      const steps = duration / 50; // Update every 50ms
      const volumeStep = startVolume / steps;
      let currentStep = 0;

      this.fadeInterval = setInterval(() => {
        if (!this.audio) {
          clearInterval(this.fadeInterval!);
          resolve();
          return;
        }

        currentStep++;
        const newVolume = Math.max(0, startVolume - (volumeStep * currentStep));
        this.audio.volume = newVolume;

        if (newVolume <= 0 || currentStep >= steps) {
          clearInterval(this.fadeInterval!);
          this.pause();
          resolve();
        }
      }, 50);
    });
  }

  fadeIn(targetVolume: number, duration: number = 1000): Promise<void> {
    return new Promise((resolve) => {
      if (!this.audio) {
        resolve();
        return;
      }

      this.audio.volume = 0;
      this.play();

      const steps = duration / 50; // Update every 50ms
      const volumeStep = targetVolume / steps;
      let currentStep = 0;

      this.fadeInterval = setInterval(() => {
        if (!this.audio) {
          clearInterval(this.fadeInterval!);
          resolve();
          return;
        }

        currentStep++;
        const newVolume = Math.min(targetVolume, volumeStep * currentStep);
        this.audio.volume = newVolume;

        if (newVolume >= targetVolume || currentStep >= steps) {
          clearInterval(this.fadeInterval!);
          resolve();
        }
      }, 50);
    });
  }

  getCurrentTime(): number {
    return this.audio?.currentTime || 0;
  }

  getDuration(): number {
    return this.audio?.duration || 0;
  }

  getIsPlaying(): boolean {
    return this.audio ? !this.audio.paused : false;
  }

  // For demo purposes - generates placeholder audio URLs
  private getPlaceholderAudioUrl(_track: Track): string {
    // In a real app, this would return the actual audio file URL
    // For demo, we return a data URL that represents silence
    return 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEUOX0fPJdykGImPH8N2QQAoUXrTp66hVFApGn+XgpF4dEU=';
  }

  destroy(): void {
    this.stopTimeUpdates();
    
    if (this.fadeInterval) {
      clearInterval(this.fadeInterval);
    }
    
    if (this.audio) {
      this.audio.removeEventListener('loadstart', this.handleLoadStart);
      this.audio.removeEventListener('loadedmetadata', this.handleLoadedMetadata);
      this.audio.removeEventListener('canplay', this.handleCanPlay);
      this.audio.removeEventListener('play', this.handlePlay);
      this.audio.removeEventListener('pause', this.handlePause);
      this.audio.removeEventListener('ended', this.handleEnded);
      this.audio.removeEventListener('error', this.handleError);
      this.audio.removeEventListener('timeupdate', this.handleTimeUpdate);
      this.audio.removeEventListener('volumechange', this.handleVolumeChange);
      
      this.audio.pause();
      this.audio.src = '';
      this.audio = null;
    }
  }
}

// Singleton instance
export const musicAudioService = new MusicAudioService();

// React hook for audio service integration
export const useMusicAudioService = () => {
  const player = useMusicStore((state) => state.player);
  const { 
    playTrack, 
    pauseTrack, 
    resumeTrack, 
    setCurrentTime: storeSetCurrentTime,
    setVolume: storeSetVolume,
    toggleMute
  } = useMusicStore();

  // Enhanced actions that integrate with audio service
  const enhancedActions = {
    async playTrack(track: Track) {
      try {
        playTrack(track);
        await musicAudioService.loadTrack(track);
        await musicAudioService.play();
      } catch (error) {
        console.error('Failed to play track:', error);
        pauseTrack();
      }
    },

    pauseTrack() {
      pauseTrack();
      musicAudioService.pause();
    },

    resumeTrack() {
      resumeTrack();
      musicAudioService.play();
    },

    setCurrentTime(time: number) {
      storeSetCurrentTime(time);
      musicAudioService.seekTo(time);
    },

    setVolume(volume: number) {
      storeSetVolume(volume);
      musicAudioService.setVolume(volume);
    },

    toggleMute() {
      toggleMute();
      const { player: currentPlayer } = useMusicStore.getState();
      if (currentPlayer.isMuted) {
        musicAudioService.mute();
      } else {
        musicAudioService.unmute();
        musicAudioService.setVolume(currentPlayer.volume);
      }
    },
  };

  return {
    player,
    audioService: musicAudioService,
    ...enhancedActions,
  };
};