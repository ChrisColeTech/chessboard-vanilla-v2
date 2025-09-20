import React from 'react';
import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX, Shuffle, Repeat, Repeat1 } from 'lucide-react';
import { usePlayer, usePlayerActions } from '../../stores/musicStore';
import { formatDuration } from '../../data/mockMusicData';

interface PlayerControlsProps {
  compact?: boolean;
}

export const PlayerControls: React.FC<PlayerControlsProps> = ({ compact = false }) => {
  const player = usePlayer();
  const {
    togglePlayPause,
    nextTrack,
    previousTrack,
    setVolume,
    toggleMute,
    setCurrentTime,
    toggleShuffle,
    toggleRepeat,
  } = usePlayerActions();

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    setCurrentTime(time);
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const volume = parseFloat(e.target.value);
    setVolume(volume);
  };

  const getRepeatIcon = () => {
    switch (player.repeat) {
      case 'one':
        return <Repeat1 className="w-4 h-4" />;
      case 'all':
        return <Repeat className="w-4 h-4 text-primary" />;
      default:
        return <Repeat className="w-4 h-4" />;
    }
  };

  if (compact) {
    return (
      <div className="flex items-center gap-2">
        <button
          onClick={previousTrack}
          className="p-1 hover:bg-muted rounded-full transition-colors"
          disabled={!player.currentTrack}
        >
          <SkipBack className="w-4 h-4" />
        </button>
        
        <button
          onClick={togglePlayPause}
          className="p-2 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-colors"
          disabled={!player.currentTrack}
        >
          {player.isPlaying ? (
            <Pause className="w-4 h-4" />
          ) : (
            <Play className="w-4 h-4" />
          )}
        </button>
        
        <button
          onClick={nextTrack}
          className="p-1 hover:bg-muted rounded-full transition-colors"
          disabled={!player.currentTrack}
        >
          <SkipForward className="w-4 h-4" />
        </button>
      </div>
    );
  }

  return (
    <div className="text-center text-muted-foreground">
      <div className="text-sm">Player Controls</div>
      <div className="text-xs">Play • Pause • Skip • Volume</div>
    </div>
  );
};