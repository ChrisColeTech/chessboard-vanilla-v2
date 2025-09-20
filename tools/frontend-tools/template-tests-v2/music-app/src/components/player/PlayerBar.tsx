import React, { useState } from 'react';
import { Heart, MoreHorizontal, ChevronUp, List } from 'lucide-react';
import { usePlayer, useMusicStore } from '../../stores/musicStore';
import { PlayerControls } from './PlayerControls';
import { NowPlaying } from './NowPlaying';
import { formatDuration } from '../../data/mockMusicData';

export const PlayerBar: React.FC = () => {
  const player = usePlayer();
  const { toggleLikeTrack } = useMusicStore();
  const isPlayerVisible = useMusicStore((state) => state.isPlayerVisible);
  const [isExpanded, setIsExpanded] = useState(false);
  const [showNowPlaying, setShowNowPlaying] = useState(false);

  if (!player.currentTrack || !isPlayerVisible) {
    return null;
  }

  const { currentTrack } = player;

  return (
    <>
      {/* Simple Player Bar */}
      <div className="fixed bottom-16 left-0 right-0 z-30">
        {/* Main Player Bar */}
        <div className="bg-background border-t border-border">
          <div className="px-4 py-3">
            {/* Mobile Layout */}
            <div className="md:hidden">
              <div className="flex items-center gap-3">
                {/* Album Art */}
                <button
                  onClick={() => setShowNowPlaying(true)}
                  className="cursor-pointer"
                >
                  <div className="w-10 h-10 rounded overflow-hidden">
                    <img
                      src={currentTrack.artwork}
                      alt={currentTrack.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                </button>
                
                {/* Track Info */}
                <button
                  onClick={() => setShowNowPlaying(true)}
                  className="flex-1 min-w-0 text-left"
                >
                  <h4 className="font-medium text-sm truncate hover:underline">{currentTrack.title}</h4>
                  <p className="text-xs text-muted-foreground truncate">{currentTrack.artist}</p>
                </button>
                
                {/* Mobile Controls */}
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => toggleLikeTrack(currentTrack.id)}
                    className={`p-2 rounded transition-colors ${
                      currentTrack.liked
                        ? 'text-red-500'
                        : 'text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    <Heart className={`w-4 h-4 ${currentTrack.liked ? 'fill-current' : ''}`} />
                  </button>
                  
                  <PlayerControls compact />
                  
                  <button 
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="p-2 rounded text-muted-foreground hover:text-foreground transition-colors"
                  >
                    <ChevronUp className={`w-4 h-4 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`} />
                  </button>
                </div>
              </div>

              {/* Expanded Mobile Controls */}
              {isExpanded && (
                <div className="mt-4 pt-4 border-t border-border space-y-4">
                  {/* Time Display */}
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>{formatDuration(Math.floor(player.currentTime))}</span>
                    <span>{formatDuration(Math.floor(player.duration))}</span>
                  </div>
                  
                  {/* Full Controls */}
                  <div className="flex justify-center">
                    <PlayerControls />
                  </div>
                </div>
              )}
            </div>

            {/* Desktop Layout */}
            <div className="hidden md:grid grid-cols-[1fr_2fr_1fr] items-center gap-6">
              {/* Left: Track Info */}
              <div className="flex items-center gap-4 min-w-0">
                <button
                  onClick={() => setShowNowPlaying(true)}
                  className="cursor-pointer"
                >
                  <div className="w-12 h-12 rounded overflow-hidden">
                    <img
                      src={currentTrack.artwork}
                      alt={currentTrack.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                </button>
                
                <button
                  onClick={() => setShowNowPlaying(true)}
                  className="min-w-0 flex-1 text-left"
                >
                  <h4 className="font-semibold truncate hover:underline">
                    {currentTrack.title}
                  </h4>
                  <p className="text-sm text-muted-foreground truncate hover:text-foreground transition-colors">
                    {currentTrack.artist}
                  </p>
                </button>
                
                <button
                  onClick={() => toggleLikeTrack(currentTrack.id)}
                  className={`p-2 rounded transition-colors ${
                    currentTrack.liked
                      ? 'text-red-500'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Heart className={`w-4 h-4 ${currentTrack.liked ? 'fill-current' : ''}`} />
                </button>
              </div>

              {/* Center: Player Controls */}
              <div className="flex justify-center">
                <PlayerControls />
              </div>

              {/* Right: More */}
              <div className="flex items-center justify-end gap-2">
                <button 
                  onClick={() => setShowNowPlaying(true)}
                  className="p-2 rounded text-muted-foreground hover:text-foreground transition-colors"
                  title="Show queue"
                >
                  <List className="w-4 h-4" />
                </button>
                
                <button className="p-2 rounded text-muted-foreground hover:text-foreground transition-colors">
                  <MoreHorizontal className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Now Playing Modal */}
      <NowPlaying 
        isOpen={showNowPlaying}
        onClose={() => setShowNowPlaying(false)}
      />
    </>
  );
};