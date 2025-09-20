import React, { useState } from 'react';
import { Music, Disc, Users, List, Play } from 'lucide-react';
import { TrackList } from '../music/TrackList';
import { AlbumArtwork } from '../player/AlbumArtwork';
import { useSearch, useMusicStore } from '../../stores/musicStore';
import type { Album, Artist, Playlist } from '../../types/music/music.types';

type SearchCategory = 'all' | 'tracks' | 'albums' | 'artists' | 'playlists';

export const SearchResults: React.FC = () => {
  const { searchResults, searchQuery } = useSearch();
  const { playTrack } = useMusicStore();
  const [activeCategory, setActiveCategory] = useState<SearchCategory>('all');

  if (!searchQuery) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
          <Music className="w-8 h-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold mb-2">Start searching</h3>
        <p className="text-muted-foreground">Find your favorite songs, albums, and artists</p>
      </div>
    );
  }

  const hasResults = searchResults.tracks.length > 0 || 
                   searchResults.albums.length > 0 || 
                   searchResults.artists.length > 0 || 
                   searchResults.playlists.length > 0;

  if (!hasResults) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
          <Music className="w-8 h-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold mb-2">No results found</h3>
        <p className="text-muted-foreground">
          Try searching for something else or check your spelling
        </p>
      </div>
    );
  }

  const categories = [
    { key: 'all' as const, label: 'All', icon: Music, count: null },
    { key: 'tracks' as const, label: 'Songs', icon: Music, count: searchResults.tracks.length },
    { key: 'albums' as const, label: 'Albums', icon: Disc, count: searchResults.albums.length },
    { key: 'artists' as const, label: 'Artists', icon: Users, count: searchResults.artists.length },
    { key: 'playlists' as const, label: 'Playlists', icon: List, count: searchResults.playlists.length },
  ];

  const AlbumCard: React.FC<{ album: Album }> = ({ album }) => (
    <div className="p-4 rounded-lg hover:bg-muted/50 transition-colors group cursor-pointer">
      <div className="relative mb-3">
        <AlbumArtwork
          src={album.artwork}
          alt={album.title}
          size="lg"
          className="w-full aspect-square"
        />
        <button 
          onClick={() => album.tracks.length > 0 && playTrack(album.tracks[0])}
          className="absolute bottom-2 right-2 w-10 h-10 bg-primary text-primary-foreground rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-lg hover:bg-primary/90"
        >
          <Play className="w-4 h-4 ml-0.5" />
        </button>
      </div>
      <h4 className="font-semibold truncate">{album.title}</h4>
      <p className="text-sm text-muted-foreground truncate">{album.artist}</p>
      <p className="text-xs text-muted-foreground">{album.year} • {album.tracks.length} tracks</p>
    </div>
  );

  const ArtistCard: React.FC<{ artist: Artist }> = ({ artist }) => (
    <div className="p-4 rounded-lg hover:bg-muted/50 transition-colors group cursor-pointer">
      <div className="relative mb-3">
        <div className="w-full aspect-square rounded-full overflow-hidden bg-gradient-to-br from-primary/20 to-secondary/20">
          <img
            src={artist.image}
            alt={artist.name}
            className="w-full h-full object-cover"
          />
        </div>
        <button className="absolute bottom-2 right-2 w-10 h-10 bg-primary text-primary-foreground rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-lg hover:bg-primary/90">
          <Play className="w-4 h-4 ml-0.5" />
        </button>
      </div>
      <h4 className="font-semibold truncate">{artist.name}</h4>
      <p className="text-sm text-muted-foreground">Artist</p>
      <p className="text-xs text-muted-foreground">{artist.followers.toLocaleString()} followers</p>
    </div>
  );

  const PlaylistCard: React.FC<{ playlist: Playlist }> = ({ playlist }) => (
    <div className="p-4 rounded-lg hover:bg-muted/50 transition-colors group cursor-pointer">
      <div className="relative mb-3">
        <AlbumArtwork
          src={playlist.artwork}
          alt={playlist.name}
          size="lg"
          className="w-full aspect-square"
        />
        <button 
          onClick={() => playlist.tracks.length > 0 && playTrack(playlist.tracks[0])}
          className="absolute bottom-2 right-2 w-10 h-10 bg-primary text-primary-foreground rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-lg hover:bg-primary/90"
        >
          <Play className="w-4 h-4 ml-0.5" />
        </button>
      </div>
      <h4 className="font-semibold truncate">{playlist.name}</h4>
      <p className="text-sm text-muted-foreground truncate">{playlist.description}</p>
      <p className="text-xs text-muted-foreground">{playlist.tracks.length} tracks</p>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Category Tabs */}
      <div className="flex items-center gap-1 p-1 bg-muted rounded-lg">
        {categories.map((category) => {
          const Icon = category.icon;
          return (
            <button
              key={category.key}
              onClick={() => setActiveCategory(category.key)}
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeCategory === category.key
                  ? 'bg-background text-foreground shadow-sm'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              <Icon className="w-4 h-4" />
              {category.label}
              {category.count !== null && category.count > 0 && (
                <span className="text-xs bg-primary/20 text-primary px-1.5 py-0.5 rounded-full">
                  {category.count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Results */}
      <div className="space-y-8">
        {(activeCategory === 'all' || activeCategory === 'tracks') && searchResults.tracks.length > 0 && (
          <section>
            <h3 className="text-xl font-bold mb-4">Songs</h3>
            <TrackList tracks={activeCategory === 'all' ? searchResults.tracks.slice(0, 5) : searchResults.tracks} />
            {activeCategory === 'all' && searchResults.tracks.length > 5 && (
              <button 
                onClick={() => setActiveCategory('tracks')}
                className="mt-4 text-sm text-primary hover:underline"
              >
                Show all {searchResults.tracks.length} songs
              </button>
            )}
          </section>
        )}

        {(activeCategory === 'all' || activeCategory === 'albums') && searchResults.albums.length > 0 && (
          <section>
            <h3 className="text-xl font-bold mb-4">Albums</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {(activeCategory === 'all' ? searchResults.albums.slice(0, 5) : searchResults.albums).map((album) => (
                <AlbumCard key={album.id} album={album} />
              ))}
            </div>
            {activeCategory === 'all' && searchResults.albums.length > 5 && (
              <button 
                onClick={() => setActiveCategory('albums')}
                className="mt-4 text-sm text-primary hover:underline"
              >
                Show all {searchResults.albums.length} albums
              </button>
            )}
          </section>
        )}

        {(activeCategory === 'all' || activeCategory === 'artists') && searchResults.artists.length > 0 && (
          <section>
            <h3 className="text-xl font-bold mb-4">Artists</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {(activeCategory === 'all' ? searchResults.artists.slice(0, 5) : searchResults.artists).map((artist) => (
                <ArtistCard key={artist.id} artist={artist} />
              ))}
            </div>
            {activeCategory === 'all' && searchResults.artists.length > 5 && (
              <button 
                onClick={() => setActiveCategory('artists')}
                className="mt-4 text-sm text-primary hover:underline"
              >
                Show all {searchResults.artists.length} artists
              </button>
            )}
          </section>
        )}

        {(activeCategory === 'all' || activeCategory === 'playlists') && searchResults.playlists.length > 0 && (
          <section>
            <h3 className="text-xl font-bold mb-4">Playlists</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {(activeCategory === 'all' ? searchResults.playlists.slice(0, 5) : searchResults.playlists).map((playlist) => (
                <PlaylistCard key={playlist.id} playlist={playlist} />
              ))}
            </div>
            {activeCategory === 'all' && searchResults.playlists.length > 5 && (
              <button 
                onClick={() => setActiveCategory('playlists')}
                className="mt-4 text-sm text-primary hover:underline"
              >
                Show all {searchResults.playlists.length} playlists
              </button>
            )}
          </section>
        )}
      </div>
    </div>
  );
};