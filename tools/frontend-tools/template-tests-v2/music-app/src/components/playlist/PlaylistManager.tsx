import React, { useState } from 'react';
import { Plus, Grid, List as ListIcon, Search } from 'lucide-react';
import { PlaylistCard } from './PlaylistCard';
import { CreatePlaylistModal } from './CreatePlaylistModal';
import { useMusicLibrary } from '../../stores/musicStore';
import type { Playlist } from '../../types/music/music.types';

type ViewMode = 'grid' | 'list';

export const PlaylistManager: React.FC = () => {
  const { playlists } = useMusicLibrary();
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedPlaylist, setSelectedPlaylist] = useState<Playlist | null>(null);

  // Filter playlists based on search query
  const filteredPlaylists = playlists.filter(playlist =>
    playlist.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    playlist.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCreatePlaylist = () => {
    setShowCreateModal(true);
  };

  const handleEditPlaylist = (playlist: Playlist) => {
    setSelectedPlaylist(playlist);
    // In a real app, this would open an edit modal
    console.log('Edit playlist:', playlist);
  };

  const handlePlaylistCreated = (playlistId: string) => {
    console.log('Playlist created:', playlistId);
    // Optionally scroll to the new playlist or show a success message
  };

  const EmptyState = () => (
    <div className="text-center py-12">
      <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-full flex items-center justify-center">
        <Plus className="w-10 h-10 text-primary" />
      </div>
      <h3 className="text-xl font-semibold mb-2">Create your first playlist</h3>
      <p className="text-muted-foreground mb-6 max-w-md mx-auto">
        Organize your favorite songs into personalized playlists. Start by creating your first one!
      </p>
      <button
        onClick={handleCreatePlaylist}
        className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
      >
        <Plus className="w-5 h-5" />
        Create Playlist
      </button>
    </div>
  );

  const NoResults = () => (
    <div className="text-center py-12">
      <div className="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
        <Search className="w-8 h-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold mb-2">No playlists found</h3>
      <p className="text-muted-foreground">
        Try searching for something else or create a new playlist
      </p>
    </div>
  );

  if (playlists.length === 0) {
    return (
      <div className="space-y-6">
        <EmptyState />
        <CreatePlaylistModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onSuccess={handlePlaylistCreated}
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">Your Playlists</h2>
          <p className="text-muted-foreground">
            {playlists.length} {playlists.length === 1 ? 'playlist' : 'playlists'}
          </p>
        </div>
        
        <button
          onClick={handleCreatePlaylist}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Create Playlist
        </button>
      </div>

      {/* Search and view controls */}
      <div className="flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search playlists..."
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          />
        </div>

        <div className="flex items-center gap-1 p-1 bg-muted rounded-lg">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded-md transition-colors ${
              viewMode === 'grid'
                ? 'bg-background text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <Grid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-2 rounded-md transition-colors ${
              viewMode === 'list'
                ? 'bg-background text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <ListIcon className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Playlists */}
      {filteredPlaylists.length === 0 ? (
        <NoResults />
      ) : (
        <div className={
          viewMode === 'grid'
            ? 'grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4'
            : 'space-y-2'
        }>
          {filteredPlaylists.map((playlist) => (
            <PlaylistCard
              key={playlist.id}
              playlist={playlist}
              size={viewMode === 'grid' ? 'md' : 'sm'}
              onEdit={handleEditPlaylist}
              className={viewMode === 'list' ? 'flex items-center gap-4 p-3' : ''}
            />
          ))}
        </div>
      )}

      {/* Create playlist modal */}
      <CreatePlaylistModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSuccess={handlePlaylistCreated}
      />
    </div>
  );
};