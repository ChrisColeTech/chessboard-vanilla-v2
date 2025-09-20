import React, { useState } from 'react';
import { Heart, MoreHorizontal, Shuffle, Repeat, Repeat1, List, X, Clock, Play, Pause } from 'lucide-react';
import { AlbumArtwork } from './AlbumArtwork';
import { MusicVisualizer } from './MusicVisualizer';
import { TrackList } from '../music/TrackList';
import { usePlayer, useMusicStore, usePlayerActions } from '../../stores/musicStore';
import { formatDuration } from '../../data/mockMusicData';
import type { Track } from '../../types/music/music.types';

interface NowPlayingProps {
  isOpen: boolean;
  onClose: () => void;
}

export const NowPlaying: React.FC<NowPlayingProps> = ({ isOpen, onClose }) => {
  const player = usePlayer();
  const { toggleLikeTrack, clearQueue, removeFromQueue } = useMusicStore();
  const { toggleShuffle, toggleRepeat, playTrack, pauseTrack, resumeTrack } = usePlayerActions();
  const [activeTab, setActiveTab] = useState<'queue' | 'lyrics'>('queue');

  if (!isOpen || !player.currentTrack) return null;

  const { currentTrack } = player;

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

  const handleTrackSelect = (track: Track) => {
    playTrack(track);
  };

  const handleRemoveFromQueue = (index: number) => {
    removeFromQueue(index);
  };

  const QueueList = () => (
    <div className="space-y-1">
      {player.queue.length === 0 ? (
        <div className="text-center py-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
            <List className="w-8 h-8 text-muted-foreground" />
          </div>
          <h3 className="font-semibold mb-2">Your queue is empty</h3>
          <p className="text-sm text-muted-foreground">Add songs to see them here</p>
        </div>
      ) : (
        <>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Queue ({player.queue.length})</h3>
            <button
              onClick={clearQueue}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Clear queue
            </button>
          </div>
          <div className="space-y-1">
            {player.queue.map((track, index) => (
              <div
                key={`${track.id}-${index}`}
                className={`flex items-center gap-3 p-2 rounded-lg hover:bg-muted/50 transition-colors group ${
                  index === player.currentIndex ? 'bg-primary/10' : ''
                }`}
              >
                {/* Track number/play indicator */}
                <div className="w-8 flex justify-center">
                  {index === player.currentIndex ? (
                    <button
                      onClick={() => player.isPlaying ? pauseTrack() : resumeTrack()}
                      className="text-primary"
                    >
                      {player.isPlaying ? (
                        <Pause className="w-4 h-4" />
                      ) : (
                        <Play className="w-4 h-4" />
                      )}
                    </button>
                  ) : (
                    <button
                      onClick={() => handleTrackSelect(track)}
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {index + 1}
                    </button>
                  )}
                </div>

                {/* Track info */}
                <div className="flex-1 min-w-0">
                  <h4 className={`font-medium text-sm truncate ${
                    index === player.currentIndex ? 'text-primary' : ''
                  }`}>
                    {track.title}
                  </h4>
                  <p className="text-xs text-muted-foreground truncate">{track.artist}</p>
                </div>

                {/* Duration */}
                <span className="text-xs text-muted-foreground">
                  {formatDuration(track.duration)}
                </span>

                {/* Remove button */}
                <button
                  onClick={() => handleRemoveFromQueue(index)}
                  className="p-1 text-muted-foreground hover:text-foreground rounded transition-colors opacity-0 group-hover:opacity-100"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );

  const LyricsView = () => (
    <div className="text-center py-8">
      <div className="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
        <MoreHorizontal className="w-8 h-8 text-muted-foreground" />
      </div>
      <h3 className="font-semibold mb-2">Lyrics not available</h3>
      <p className="text-sm text-muted-foreground">
        Lyrics for "{currentTrack.title}" are not available at this time
      </p>
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-background border border-border rounded-xl w-full max-w-4xl h-full max-h-[90vh] shadow-xl flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <h2 className="text-xl font-semibold">Now Playing</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-full hover:bg-muted transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Main content */}
        <div className="flex-1 overflow-hidden flex">
          {/* Left: Track info and visualizer */}
          <div className="flex-1 p-6 flex flex-col">
            <div className="flex-1 flex flex-col items-center justify-center text-center space-y-6">
              {/* Large album artwork */}
              <div className="relative">
                <AlbumArtwork
                  src={currentTrack.artwork}
                  alt={currentTrack.title}
                  size="xl"
                  className="w-80 h-80"
                />
              </div>

              {/* Track details */}
              <div className="space-y-2">
                <h1 className="text-3xl font-bold">{currentTrack.title}</h1>
                <p className="text-xl text-muted-foreground">{currentTrack.artist}</p>
                <p className="text-sm text-muted-foreground">{currentTrack.album}</p>
              </div>

              {/* Status indicator */}
              <div className="flex items-center gap-2 text-muted-foreground">
                {player.isPlaying ? (
                  <>
                    <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
                    <span className="text-sm">Now playing</span>
                  </>
                ) : (
                  <>
                    <div className="w-2 h-2 bg-muted-foreground rounded-full" />
                    <span className="text-sm">Paused</span>
                  </>
                )}
              </div>

              {/* Controls */}
              <div className="flex items-center gap-6">
                {/* Like button */}
                <button
                  onClick={() => toggleLikeTrack(currentTrack.id)}
                  className={`p-3 rounded-full transition-all duration-200 ${
                    currentTrack.liked
                      ? 'text-red-400 bg-red-400/10'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`}
                >
                  <Heart className={`w-6 h-6 ${currentTrack.liked ? 'fill-current' : ''}`} />
                </button>

                {/* Shuffle */}
                <button
                  onClick={toggleShuffle}
                  className={`p-3 rounded-full transition-all duration-200 ${
                    player.shuffle
                      ? 'text-primary bg-primary/20'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`}
                >
                  <Shuffle className="w-6 h-6" />
                </button>

                {/* Repeat */}
                <button
                  onClick={toggleRepeat}
                  className={`p-3 rounded-full transition-all duration-200 ${
                    player.repeat !== 'none'
                      ? 'text-primary bg-primary/20'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`}
                >
                  {getRepeatIcon()}
                </button>

                {/* More options */}
                <button className="p-3 rounded-full text-muted-foreground hover:text-foreground hover:bg-muted transition-all duration-200">
                  <MoreHorizontal className="w-6 h-6" />
                </button>
              </div>
            </div>
          </div>

          {/* Right: Queue and lyrics */}
          <div className="w-80 border-l border-border flex flex-col">
            {/* Tabs */}
            <div className="flex border-b border-border">
              <button
                onClick={() => setActiveTab('queue')}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'queue'
                    ? 'text-foreground border-b-2 border-primary'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                <div className="flex items-center gap-2 justify-center">
                  <List className="w-4 h-4" />
                  Queue
                </div>
              </button>
              <button
                onClick={() => setActiveTab('lyrics')}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'lyrics'
                    ? 'text-foreground border-b-2 border-primary'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                <div className="flex items-center gap-2 justify-center">
                  <Clock className="w-4 h-4" />
                  Lyrics
                </div>
              </button>
            </div>

            {/* Tab content */}
            <div className="flex-1 overflow-auto p-4">
              {activeTab === 'queue' ? <QueueList /> : <LyricsView />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};