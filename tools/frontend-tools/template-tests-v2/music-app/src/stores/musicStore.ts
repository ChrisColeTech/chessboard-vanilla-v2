import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import type { Track, Playlist, MusicLibrary, PlayerState, SearchResults } from '../types/music/music.types';
import { musicLibrary } from '../data/mockMusicData';

interface MusicStore extends MusicLibrary {
  // Player state
  player: PlayerState;
  
  // Search state
  searchResults: SearchResults;
  searchQuery: string;
  
  // UI state
  isPlayerVisible: boolean;
  currentView: 'library' | 'discover' | 'search' | 'profile';
  
  // Actions
  // Player actions
  setCurrentTrack: (track: Track) => void;
  playTrack: (track: Track) => void;
  pauseTrack: () => void;
  resumeTrack: () => void;
  togglePlayPause: () => void;
  nextTrack: () => void;
  previousTrack: () => void;
  setVolume: (volume: number) => void;
  toggleMute: () => void;
  setCurrentTime: (time: number) => void;
  toggleShuffle: () => void;
  toggleRepeat: () => void;
  addToQueue: (track: Track) => void;
  removeFromQueue: (index: number) => void;
  clearQueue: () => void;
  
  // Library actions
  toggleLikeTrack: (trackId: string) => void;
  createPlaylist: (name: string, description?: string) => Playlist;
  addToPlaylist: (playlistId: string, trackId: string) => void;
  removeFromPlaylist: (playlistId: string, trackId: string) => void;
  deletePlaylist: (playlistId: string) => void;
  
  // Search actions
  searchMusic: (query: string) => void;
  clearSearch: () => void;
  
  // UI actions
  showPlayer: () => void;
  hidePlayer: () => void;
  setCurrentView: (view: 'library' | 'discover' | 'search' | 'profile') => void;
}

const initialPlayerState: PlayerState = {
  currentTrack: null,
  isPlaying: false,
  volume: 0.7,
  isMuted: false,
  currentTime: 0,
  duration: 0,
  queue: [],
  currentIndex: 0,
  shuffle: false,
  repeat: 'none',
  isLoading: false,
};

const initialSearchResults: SearchResults = {
  tracks: [],
  albums: [],
  artists: [],
  playlists: [],
  query: '',
};

export const useMusicStore = create<MusicStore>()(
  subscribeWithSelector((set, get) => ({
    // Initial state from mock data
    ...musicLibrary,
    
    // Player state
    player: initialPlayerState,
    
    // Search state
    searchResults: initialSearchResults,
    searchQuery: '',
    
    // UI state
    isPlayerVisible: false,
    currentView: 'discover',
    
    // Player actions
    setCurrentTrack: (track: Track) => {
      set((state) => ({
        player: {
          ...state.player,
          currentTrack: track,
          duration: track.duration,
          currentTime: 0,
        },
      }));
    },
    
    playTrack: (track: Track) => {
      const state = get();
      
      set({
        player: {
          ...state.player,
          currentTrack: track,
          isPlaying: true,
          duration: track.duration,
          currentTime: 0,
          queue: state.player.queue.length === 0 ? [track] : state.player.queue,
          currentIndex: state.player.queue.findIndex(t => t.id === track.id) || 0,
        },
        isPlayerVisible: true,
      });
      
      // Add to recently played
      const recentlyPlayed = [track, ...state.recentlyPlayed.filter(t => t.id !== track.id)].slice(0, 20);
      set({ recentlyPlayed });
    },
    
    pauseTrack: () => {
      set((state) => ({
        player: { ...state.player, isPlaying: false },
      }));
    },
    
    resumeTrack: () => {
      set((state) => ({
        player: { ...state.player, isPlaying: true },
      }));
    },
    
    togglePlayPause: () => {
      const { player } = get();
      if (player.isPlaying) {
        get().pauseTrack();
      } else {
        get().resumeTrack();
      }
    },
    
    nextTrack: () => {
      const { player } = get();
      if (player.queue.length === 0) return;
      
      let nextIndex = player.currentIndex + 1;
      
      if (player.shuffle) {
        nextIndex = Math.floor(Math.random() * player.queue.length);
      } else if (nextIndex >= player.queue.length) {
        if (player.repeat === 'all') {
          nextIndex = 0;
        } else {
          return; // End of queue
        }
      }
      
      const nextTrack = player.queue[nextIndex];
      if (nextTrack) {
        set((state) => ({
          player: {
            ...state.player,
            currentTrack: nextTrack,
            currentIndex: nextIndex,
            currentTime: 0,
            duration: nextTrack.duration,
          },
        }));
      }
    },
    
    previousTrack: () => {
      const { player } = get();
      if (player.queue.length === 0) return;
      
      // If current time > 3 seconds, restart current track
      if (player.currentTime > 3) {
        set((state) => ({
          player: { ...state.player, currentTime: 0 },
        }));
        return;
      }
      
      let prevIndex = player.currentIndex - 1;
      
      if (player.shuffle) {
        prevIndex = Math.floor(Math.random() * player.queue.length);
      } else if (prevIndex < 0) {
        if (player.repeat === 'all') {
          prevIndex = player.queue.length - 1;
        } else {
          return; // Beginning of queue
        }
      }
      
      const prevTrack = player.queue[prevIndex];
      if (prevTrack) {
        set((state) => ({
          player: {
            ...state.player,
            currentTrack: prevTrack,
            currentIndex: prevIndex,
            currentTime: 0,
            duration: prevTrack.duration,
          },
        }));
      }
    },
    
    setVolume: (volume: number) => {
      set((state) => ({
        player: { ...state.player, volume: Math.max(0, Math.min(1, volume)) },
      }));
    },
    
    toggleMute: () => {
      set((state) => ({
        player: { ...state.player, isMuted: !state.player.isMuted },
      }));
    },
    
    setCurrentTime: (time: number) => {
      set((state) => ({
        player: { ...state.player, currentTime: time },
      }));
    },
    
    toggleShuffle: () => {
      set((state) => ({
        player: { ...state.player, shuffle: !state.player.shuffle },
      }));
    },
    
    toggleRepeat: () => {
      const { player } = get();
      const repeatModes: Array<'none' | 'one' | 'all'> = ['none', 'one', 'all'];
      const currentIndex = repeatModes.indexOf(player.repeat);
      const nextRepeat = repeatModes[(currentIndex + 1) % repeatModes.length];
      
      set((state) => ({
        player: { ...state.player, repeat: nextRepeat },
      }));
    },
    
    addToQueue: (track: Track) => {
      set((state) => ({
        player: {
          ...state.player,
          queue: [...state.player.queue, track],
        },
      }));
    },
    
    removeFromQueue: (index: number) => {
      set((state) => ({
        player: {
          ...state.player,
          queue: state.player.queue.filter((_, i) => i !== index),
        },
      }));
    },
    
    clearQueue: () => {
      set((state) => ({
        player: { ...state.player, queue: [], currentIndex: 0 },
      }));
    },
    
    // Library actions
    toggleLikeTrack: (trackId: string) => {
      set((state) => ({
        tracks: state.tracks.map(track =>
          track.id === trackId ? { ...track, liked: !track.liked } : track
        ),
      }));
    },
    
    createPlaylist: (name: string, description = '') => {
      const newPlaylist: Playlist = {
        id: `playlist-${Date.now()}`,
        name,
        description,
        artwork: `https://picsum.photos/seed/playlist-${Date.now()}/300/300`,
        tracks: [],
        duration: 0,
        isPublic: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        createdBy: 'user-1',
        followers: 0,
      };
      
      set((state) => ({
        playlists: [...state.playlists, newPlaylist],
      }));
      
      return newPlaylist;
    },
    
    addToPlaylist: (playlistId: string, trackId: string) => {
      const { tracks } = get();
      const track = tracks.find(t => t.id === trackId);
      if (!track) return;
      
      set((state) => ({
        playlists: state.playlists.map(playlist =>
          playlist.id === playlistId
            ? {
                ...playlist,
                tracks: [...playlist.tracks, track],
                duration: playlist.duration + track.duration,
                updatedAt: new Date().toISOString(),
              }
            : playlist
        ),
      }));
    },
    
    removeFromPlaylist: (playlistId: string, trackId: string) => {
      set((state) => ({
        playlists: state.playlists.map(playlist =>
          playlist.id === playlistId
            ? {
                ...playlist,
                tracks: playlist.tracks.filter(track => track.id !== trackId),
                duration: playlist.tracks
                  .filter(track => track.id !== trackId)
                  .reduce((total, track) => total + track.duration, 0),
                updatedAt: new Date().toISOString(),
              }
            : playlist
        ),
      }));
    },
    
    deletePlaylist: (playlistId: string) => {
      set((state) => ({
        playlists: state.playlists.filter(playlist => playlist.id !== playlistId),
      }));
    },
    
    // Search actions
    searchMusic: (query: string) => {
      const { tracks, albums, artists, playlists } = get();
      const lowerQuery = query.toLowerCase();
      
      const searchResults: SearchResults = {
        tracks: tracks.filter(track =>
          track.title.toLowerCase().includes(lowerQuery) ||
          track.artist.toLowerCase().includes(lowerQuery) ||
          track.album.toLowerCase().includes(lowerQuery)
        ),
        albums: albums.filter(album =>
          album.title.toLowerCase().includes(lowerQuery) ||
          album.artist.toLowerCase().includes(lowerQuery)
        ),
        artists: artists.filter(artist =>
          artist.name.toLowerCase().includes(lowerQuery)
        ),
        playlists: playlists.filter(playlist =>
          playlist.name.toLowerCase().includes(lowerQuery) ||
          playlist.description.toLowerCase().includes(lowerQuery)
        ),
        query,
      };
      
      set({ searchResults, searchQuery: query });
    },
    
    clearSearch: () => {
      set({ searchResults: initialSearchResults, searchQuery: '' });
    },
    
    // UI actions
    showPlayer: () => {
      set({ isPlayerVisible: true });
    },
    
    hidePlayer: () => {
      set({ isPlayerVisible: false });
    },
    
    setCurrentView: (view) => {
      set({ currentView: view });
    },
  }))
);

// Convenience hooks for specific parts of the store
export const usePlayer = () => useMusicStore((state) => state.player);
export const usePlayerActions = () => {
  const playTrack = useMusicStore((state) => state.playTrack);
  const pauseTrack = useMusicStore((state) => state.pauseTrack);
  const resumeTrack = useMusicStore((state) => state.resumeTrack);
  const togglePlayPause = useMusicStore((state) => state.togglePlayPause);
  const nextTrack = useMusicStore((state) => state.nextTrack);
  const previousTrack = useMusicStore((state) => state.previousTrack);
  const setVolume = useMusicStore((state) => state.setVolume);
  const toggleMute = useMusicStore((state) => state.toggleMute);
  const setCurrentTime = useMusicStore((state) => state.setCurrentTime);
  const toggleShuffle = useMusicStore((state) => state.toggleShuffle);
  const toggleRepeat = useMusicStore((state) => state.toggleRepeat);
  
  return {
    playTrack,
    pauseTrack,
    resumeTrack,
    togglePlayPause,
    nextTrack,
    previousTrack,
    setVolume,
    toggleMute,
    setCurrentTime,
    toggleShuffle,
    toggleRepeat,
  };
};

export const useMusicLibrary = () => {
  const tracks = useMusicStore((state) => state.tracks);
  const albums = useMusicStore((state) => state.albums);
  const artists = useMusicStore((state) => state.artists);
  const playlists = useMusicStore((state) => state.playlists);
  const genres = useMusicStore((state) => state.genres);
  const recentlyPlayed = useMusicStore((state) => state.recentlyPlayed);
  const topTracks = useMusicStore((state) => state.topTracks);
  const newReleases = useMusicStore((state) => state.newReleases);
  
  return {
    tracks,
    albums,
    artists,
    playlists,
    genres,
    recentlyPlayed,
    topTracks,
    newReleases,
  };
};

export const useSearch = () => {
  const searchResults = useMusicStore((state) => state.searchResults);
  const searchQuery = useMusicStore((state) => state.searchQuery);
  const searchMusic = useMusicStore((state) => state.searchMusic);
  const clearSearch = useMusicStore((state) => state.clearSearch);
  
  return {
    searchResults,
    searchQuery,
    searchMusic,
    clearSearch,
  };
};