import React from 'react';
import { Play, Pause, Heart, MoreHorizontal } from 'lucide-react';
import type { Track } from '../../types/music/music.types';
import { useMusicStore, usePlayer } from '../../stores/musicStore';
import { AlbumArtwork } from '../player/AlbumArtwork';
import { formatDuration, formatNumber } from '../../data/mockMusicData';

interface TrackListProps {
  tracks: Track[];
  showArtwork?: boolean;
  showAlbum?: boolean;
  showPlays?: boolean;
  compact?: boolean;
}

export const TrackList: React.FC<TrackListProps> = ({
  tracks,
  showArtwork = true,
  showAlbum = true,
  showPlays = true,
  compact = false,
}) => {
  const player = usePlayer();
  const { playTrack, toggleLikeTrack, pauseTrack, resumeTrack } = useMusicStore();

  const handlePlayTrack = (track: Track) => {
    if (player.currentTrack?.id === track.id) {
      // Same track - toggle play/pause
      if (player.isPlaying) {
        pauseTrack();
      } else {
        resumeTrack();
      }
    } else {
      // Different track - play it
      playTrack(track);
    }
  };

  const isCurrentTrack = (track: Track) => player.currentTrack?.id === track.id;
  const isPlaying = (track: Track) => isCurrentTrack(track) && player.isPlaying;

  if (compact) {
    return (
      <div className="space-y-1">
        {tracks.map((track, _index) => (
          <div
            key={track.id}
            className={`flex items-center gap-3 p-2 rounded-lg hover:bg-muted/50 transition-colors group ${
              isCurrentTrack(track) ? 'bg-primary/10' : ''
            }`}
          >
            {/* Play button */}
            <button
              onClick={() => handlePlayTrack(track)}
              className="p-1 rounded-full bg-primary text-primary-foreground hover:bg-primary/90 transition-colors opacity-0 group-hover:opacity-100"
            >
              {isPlaying(track) ? (
                <Pause className="w-3 h-3" />
              ) : (
                <Play className="w-3 h-3" />
              )}
            </button>

            {/* Track info */}
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{track.title}</p>
              <p className="text-xs text-muted-foreground truncate">{track.artist}</p>
            </div>

            {/* Duration */}
            <span className="text-xs text-muted-foreground">
              {formatDuration(track.duration)}
            </span>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {tracks.map((track, index) => (
        <div
          key={track.id}
          className={`flex items-center gap-4 p-3 rounded-lg hover:bg-muted/50 transition-colors group ${
            isCurrentTrack(track) ? 'bg-primary/10' : ''
          }`}
        >
          {/* Index/Play button */}
          <div className="w-8 flex justify-center">
            <button
              onClick={() => handlePlayTrack(track)}
              className="relative group/play"
            >
              <span className="text-sm text-muted-foreground group-hover/play:opacity-0 transition-opacity">
                {index + 1}
              </span>
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover/play:opacity-100 transition-opacity">
                {isPlaying(track) ? (
                  <Pause className="w-4 h-4" />
                ) : (
                  <Play className="w-4 h-4" />
                )}
              </div>
            </button>
          </div>

          {/* Artwork */}
          {showArtwork && (
            <AlbumArtwork
              src={track.artwork}
              alt={track.title}
              size="sm"
              showVisualizer={false}
              className="flex-shrink-0"
            />
          )}

          {/* Track info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h4 className={`font-medium truncate ${isCurrentTrack(track) ? 'text-primary' : ''}`}>
                {track.title}
              </h4>
              {track.liked && (
                <Heart className="w-4 h-4 text-red-500 fill-current flex-shrink-0" />
              )}
            </div>
            <p className="text-sm text-muted-foreground truncate">{track.artist}</p>
          </div>

          {/* Album */}
          {showAlbum && (
            <div className="hidden md:block w-32 lg:w-48">
              <p className="text-sm text-muted-foreground truncate">{track.album}</p>
            </div>
          )}

          {/* Plays */}
          {showPlays && (
            <div className="hidden lg:block w-20">
              <p className="text-sm text-muted-foreground">{formatNumber(track.plays)}</p>
            </div>
          )}

          {/* Duration & Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => toggleLikeTrack(track.id)}
              className={`p-1 rounded transition-colors opacity-0 group-hover:opacity-100 ${
                track.liked
                  ? 'text-red-500 opacity-100'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              <Heart className={`w-4 h-4 ${track.liked ? 'fill-current' : ''}`} />
            </button>

            <span className="text-sm text-muted-foreground w-12 text-right">
              {formatDuration(track.duration)}
            </span>

            <button className="p-1 text-muted-foreground hover:text-foreground rounded transition-colors opacity-0 group-hover:opacity-100">
              <MoreHorizontal className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};