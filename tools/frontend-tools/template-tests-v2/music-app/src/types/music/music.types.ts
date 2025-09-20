export interface Track {
  id: string;
  title: string;
  artist: string;
  artistId: string;
  album: string;
  albumId: string;
  duration: number; // in seconds
  genre: string;
  year: number;
  artwork: string;
  audioUrl: string;
  plays: number;
  liked: boolean;
  addedAt: string;
}

export interface Album {
  id: string;
  title: string;
  artist: string;
  artistId: string;
  year: number;
  genre: string;
  artwork: string;
  tracks: Track[];
  duration: number; // total duration in seconds
  plays: number;
}

export interface Artist {
  id: string;
  name: string;
  bio: string;
  genre: string[];
  avatar: string;
  albums: Album[];
  topTracks: Track[];
  followers: number;
  verified: boolean;
}

export interface Playlist {
  id: string;
  name: string;
  description: string;
  artwork: string;
  tracks: Track[];
  duration: number; // total duration in seconds
  isPublic: boolean;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  followers: number;
}

export interface Genre {
  id: string;
  name: string;
  description: string;
  artwork: string;
  color: string;
  tracks: Track[];
  topArtists: Artist[];
}

export interface MusicLibrary {
  tracks: Track[];
  albums: Album[];
  artists: Artist[];
  playlists: Playlist[];
  genres: Genre[];
  recentlyPlayed: Track[];
  topTracks: Track[];
  newReleases: Album[];
}

export interface PlayerState {
  currentTrack: Track | null;
  isPlaying: boolean;
  volume: number;
  isMuted: boolean;
  currentTime: number;
  duration: number;
  queue: Track[];
  currentIndex: number;
  shuffle: boolean;
  repeat: 'none' | 'one' | 'all';
  isLoading: boolean;
}

export interface SearchResults {
  tracks: Track[];
  albums: Album[];
  artists: Artist[];
  playlists: Playlist[];
  query: string;
}