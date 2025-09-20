import React, { useState } from 'react';
import { Play, MoreHorizontal, Edit, Trash2, Share, Music, Lock, Globe } from 'lucide-react';
import { AlbumArtwork } from '../player/AlbumArtwork';
import { useMusicStore } from '../../stores/musicStore';
import type { Playlist } from '../../types/music/music.types';
import { formatDuration, formatNumber } from '../../data/mockMusicData';

interface PlaylistCardProps {
  playlist: Playlist;
  size?: 'sm' | 'md' | 'lg';
  showMenu?: boolean;
  onEdit?: (playlist: Playlist) => void;
  onDelete?: (playlistId: string) => void;
  className?: string;
}

export const PlaylistCard: React.FC<PlaylistCardProps> = ({
  playlist,
  size = 'md',
  showMenu = true,
  onEdit,
  onDelete,
  className = '',
}) => {
  const { playTrack, deletePlaylist } = useMusicStore();
  const [showDropdown, setShowDropdown] = useState(false);

  const sizeConfig = {
    sm: { artwork: 'sm' as const, titleClass: 'text-sm', subtitleClass: 'text-xs' },
    md: { artwork: 'md' as const, titleClass: 'text-base', subtitleClass: 'text-sm' },
    lg: { artwork: 'lg' as const, titleClass: 'text-lg', subtitleClass: 'text-base' },
  };

  const config = sizeConfig[size];

  const handlePlay = () => {
    if (playlist.tracks.length > 0) {
      playTrack(playlist.tracks[0]);
    }
  };

  const handleEdit = () => {
    onEdit?.(playlist);
    setShowDropdown(false);
  };

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${playlist.name}"?`)) {
      deletePlaylist(playlist.id);
      onDelete?.(playlist.id);
    }
    setShowDropdown(false);
  };

  const totalDuration = playlist.tracks.reduce((total, track) => total + track.duration, 0);

  return (
    <div className={`group p-4 rounded-lg hover:bg-muted/50 transition-colors ${className}`}>
      {/* Playlist artwork */}
      <div className="relative mb-4">
        <AlbumArtwork
          src={playlist.artwork}
          alt={playlist.name}
          size={config.artwork}
          className="w-full aspect-square"
        />
        
        {/* Play button overlay */}
        <button
          onClick={handlePlay}
          disabled={playlist.tracks.length === 0}
          className="absolute bottom-2 right-2 w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-200 shadow-lg hover:bg-primary/90 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play className="w-5 h-5 ml-0.5" />
        </button>

        {/* Privacy indicator */}
        <div className="absolute top-2 left-2">
          {playlist.isPublic ? (
            <div className="flex items-center gap-1 px-2 py-1 bg-green-500/20 text-green-400 rounded-full text-xs">
              <Globe className="w-3 h-3" />
              Public
            </div>
          ) : (
            <div className="flex items-center gap-1 px-2 py-1 bg-muted/80 text-muted-foreground rounded-full text-xs">
              <Lock className="w-3 h-3" />
              Private
            </div>
          )}
        </div>
      </div>

      {/* Playlist info */}
      <div className="space-y-2">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0 flex-1">
            <h4 className={`font-semibold truncate hover:text-primary cursor-pointer transition-colors ${config.titleClass}`}>
              {playlist.name}
            </h4>
            {playlist.description && (
              <p className={`text-muted-foreground truncate ${config.subtitleClass}`}>
                {playlist.description}
              </p>
            )}
          </div>

          {/* More options menu */}
          {showMenu && (
            <div className="relative">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="p-1 rounded-full hover:bg-muted transition-colors opacity-0 group-hover:opacity-100"
              >
                <MoreHorizontal className="w-4 h-4" />
              </button>

              {showDropdown && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setShowDropdown(false)}
                  />
                  <div className="absolute right-0 top-full mt-1 w-48 bg-background border border-border rounded-lg shadow-lg z-20">
                    <div className="py-1">
                      <button
                        onClick={handleEdit}
                        className="flex items-center gap-2 w-full px-3 py-2 text-left hover:bg-muted transition-colors"
                      >
                        <Edit className="w-4 h-4" />
                        Edit details
                      </button>
                      <button
                        className="flex items-center gap-2 w-full px-3 py-2 text-left hover:bg-muted transition-colors"
                      >
                        <Share className="w-4 h-4" />
                        Share
                      </button>
                      <div className="border-t border-border my-1" />
                      <button
                        onClick={handleDelete}
                        className="flex items-center gap-2 w-full px-3 py-2 text-left hover:bg-destructive/10 text-destructive transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                        Delete playlist
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </div>

        {/* Playlist stats */}
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Music className="w-3 h-3" />
            {playlist.tracks.length} {playlist.tracks.length === 1 ? 'track' : 'tracks'}
          </div>
          {totalDuration > 0 && (
            <>
              <span>•</span>
              <span>{formatDuration(totalDuration)}</span>
            </>
          )}
          {playlist.followers > 0 && (
            <>
              <span>•</span>
              <span>{formatNumber(playlist.followers)} followers</span>
            </>
          )}
        </div>

        {/* Created date */}
        <p className="text-xs text-muted-foreground">
          Created {new Date(playlist.createdAt).toLocaleDateString()}
        </p>
      </div>
    </div>
  );
};