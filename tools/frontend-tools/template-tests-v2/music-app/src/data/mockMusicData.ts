import type { Track, Album, Artist, Playlist, Genre, MusicLibrary } from '../types/music/music.types';

// Mock album artwork URLs (using placeholder images)
const artworkUrl = (seed: string) => `https://picsum.photos/seed/${seed}/300/300`;

// Mock Tracks
export const mockTracks: Track[] = [
  {
    id: '1',
    title: 'Electric Dreams',
    artist: 'Neon Pulse',
    artistId: 'artist-1',
    album: 'Synthetic Horizons',
    albumId: 'album-1',
    duration: 234,
    genre: 'Electronic',
    year: 2023,
    artwork: artworkUrl('electric-dreams'),
    audioUrl: '', // Will be added when we implement audio
    plays: 1250000,
    liked: true,
    addedAt: '2023-06-15T10:30:00Z'
  },
  {
    id: '2',
    title: 'Midnight City',
    artist: 'Urban Echo',
    artistId: 'artist-2',
    album: 'City Lights',
    albumId: 'album-2',
    duration: 198,
    genre: 'Pop',
    year: 2023,
    artwork: artworkUrl('midnight-city'),
    audioUrl: '',
    plays: 980000,
    liked: false,
    addedAt: '2023-07-02T14:22:00Z'
  },
  {
    id: '3',
    title: 'Thunder Road',
    artist: 'Desert Kings',
    artistId: 'artist-3',
    album: 'Wasteland',
    albumId: 'album-3',
    duration: 312,
    genre: 'Rock',
    year: 2022,
    artwork: artworkUrl('thunder-road'),
    audioUrl: '',
    plays: 2100000,
    liked: true,
    addedAt: '2023-05-18T09:15:00Z'
  },
  {
    id: '4',
    title: 'Ocean Waves',
    artist: 'Coastal Breeze',
    artistId: 'artist-4',
    album: 'Serenity',
    albumId: 'album-4',
    duration: 267,
    genre: 'Ambient',
    year: 2023,
    artwork: artworkUrl('ocean-waves'),
    audioUrl: '',
    plays: 650000,
    liked: false,
    addedAt: '2023-08-10T16:45:00Z'
  },
  {
    id: '5',
    title: 'Funky Groove',
    artist: 'Bass Federation',
    artistId: 'artist-5',
    album: 'Groove Station',
    albumId: 'album-5',
    duration: 189,
    genre: 'Funk',
    year: 2023,
    artwork: artworkUrl('funky-groove'),
    audioUrl: '',
    plays: 850000,
    liked: true,
    addedAt: '2023-07-25T11:20:00Z'
  },
  {
    id: '6',
    title: 'Digital Horizon',
    artist: 'Neon Pulse',
    artistId: 'artist-1',
    album: 'Synthetic Horizons',
    albumId: 'album-1',
    duration: 278,
    genre: 'Electronic',
    year: 2023,
    artwork: artworkUrl('electric-dreams'),
    audioUrl: '',
    plays: 920000,
    liked: false,
    addedAt: '2023-06-15T10:35:00Z'
  },
  {
    id: '7',
    title: 'Neon Nights',
    artist: 'Urban Echo',
    artistId: 'artist-2',
    album: 'City Lights',
    albumId: 'album-2',
    duration: 205,
    genre: 'Pop',
    year: 2023,
    artwork: artworkUrl('midnight-city'),
    audioUrl: '',
    plays: 1100000,
    liked: true,
    addedAt: '2023-07-02T14:25:00Z'
  },
  {
    id: '8',
    title: 'Mountain High',
    artist: 'Desert Kings',
    artistId: 'artist-3',
    album: 'Wasteland',
    albumId: 'album-3',
    duration: 298,
    genre: 'Rock',
    year: 2022,
    artwork: artworkUrl('thunder-road'),
    audioUrl: '',
    plays: 1850000,
    liked: false,
    addedAt: '2023-05-18T09:20:00Z'
  }
];

// Mock Artists
export const mockArtists: Artist[] = [
  {
    id: 'artist-1',
    name: 'Neon Pulse',
    bio: 'Electronic music producer known for atmospheric synthwave and ambient soundscapes.',
    genre: ['Electronic', 'Synthwave', 'Ambient'],
    avatar: artworkUrl('neon-pulse-artist'),
    albums: [],
    topTracks: [],
    followers: 450000,
    verified: true
  },
  {
    id: 'artist-2',
    name: 'Urban Echo',
    bio: 'Pop artist blending modern beats with classic melodies from the urban landscape.',
    genre: ['Pop', 'Urban', 'Electronic'],
    avatar: artworkUrl('urban-echo-artist'),
    albums: [],
    topTracks: [],
    followers: 680000,
    verified: true
  },
  {
    id: 'artist-3',
    name: 'Desert Kings',
    bio: 'Rock band delivering powerful anthems inspired by the vast desert landscapes.',
    genre: ['Rock', 'Alternative', 'Indie'],
    avatar: artworkUrl('desert-kings-artist'),
    albums: [],
    topTracks: [],
    followers: 920000,
    verified: true
  },
  {
    id: 'artist-4',
    name: 'Coastal Breeze',
    bio: 'Ambient musician creating peaceful soundscapes inspired by ocean waves.',
    genre: ['Ambient', 'Chill', 'Nature'],
    avatar: artworkUrl('coastal-breeze-artist'),
    albums: [],
    topTracks: [],
    followers: 280000,
    verified: false
  },
  {
    id: 'artist-5',
    name: 'Bass Federation',
    bio: 'Funk collective bringing groovy basslines and infectious rhythms.',
    genre: ['Funk', 'Jazz', 'Electronic'],
    avatar: artworkUrl('bass-federation-artist'),
    albums: [],
    topTracks: [],
    followers: 340000,
    verified: true
  }
];

// Mock Albums
export const mockAlbums: Album[] = [
  {
    id: 'album-1',
    title: 'Synthetic Horizons',
    artist: 'Neon Pulse',
    artistId: 'artist-1',
    year: 2023,
    genre: 'Electronic',
    artwork: artworkUrl('electric-dreams'),
    tracks: [],
    duration: 0,
    plays: 2170000
  },
  {
    id: 'album-2',
    title: 'City Lights',
    artist: 'Urban Echo',
    artistId: 'artist-2',
    year: 2023,
    genre: 'Pop',
    artwork: artworkUrl('midnight-city'),
    tracks: [],
    duration: 0,
    plays: 2080000
  },
  {
    id: 'album-3',
    title: 'Wasteland',
    artist: 'Desert Kings',
    artistId: 'artist-3',
    year: 2022,
    genre: 'Rock',
    artwork: artworkUrl('thunder-road'),
    tracks: [],
    duration: 0,
    plays: 3950000
  },
  {
    id: 'album-4',
    title: 'Serenity',
    artist: 'Coastal Breeze',
    artistId: 'artist-4',
    year: 2023,
    genre: 'Ambient',
    artwork: artworkUrl('ocean-waves'),
    tracks: [],
    duration: 0,
    plays: 650000
  },
  {
    id: 'album-5',
    title: 'Groove Station',
    artist: 'Bass Federation',
    artistId: 'artist-5',
    year: 2023,
    genre: 'Funk',
    artwork: artworkUrl('funky-groove'),
    tracks: [],
    duration: 0,
    plays: 850000
  }
];

// Mock Playlists
export const mockPlaylists: Playlist[] = [
  {
    id: 'playlist-1',
    name: 'Chill Vibes',
    description: 'Perfect tracks for relaxation and focus',
    artwork: artworkUrl('chill-vibes'),
    tracks: [],
    duration: 0,
    isPublic: true,
    createdAt: '2023-06-01T00:00:00Z',
    updatedAt: '2023-08-15T14:30:00Z',
    createdBy: 'user-1',
    followers: 1250
  },
  {
    id: 'playlist-2',
    name: 'Workout Energy',
    description: 'High-energy tracks to power your workout',
    artwork: artworkUrl('workout-energy'),
    tracks: [],
    duration: 0,
    isPublic: true,
    createdAt: '2023-07-10T00:00:00Z',
    updatedAt: '2023-08-20T09:15:00Z',
    createdBy: 'user-1',
    followers: 890
  },
  {
    id: 'playlist-3',
    name: 'My Favorites',
    description: 'All-time favorite tracks',
    artwork: artworkUrl('my-favorites'),
    tracks: [],
    duration: 0,
    isPublic: false,
    createdAt: '2023-05-15T00:00:00Z',
    updatedAt: '2023-08-25T18:45:00Z',
    createdBy: 'user-1',
    followers: 0
  }
];

// Mock Genres
export const mockGenres: Genre[] = [
  {
    id: 'genre-1',
    name: 'Electronic',
    description: 'Digital beats and synthesized sounds',
    artwork: artworkUrl('genre-electronic'),
    color: '#00D4FF',
    tracks: [],
    topArtists: []
  },
  {
    id: 'genre-2',
    name: 'Pop',
    description: 'Popular music with catchy melodies',
    artwork: artworkUrl('genre-pop'),
    color: '#FF6B9D',
    tracks: [],
    topArtists: []
  },
  {
    id: 'genre-3',
    name: 'Rock',
    description: 'Powerful guitars and driving rhythms',
    artwork: artworkUrl('genre-rock'),
    color: '#FF4E3E',
    tracks: [],
    topArtists: []
  },
  {
    id: 'genre-4',
    name: 'Ambient',
    description: 'Atmospheric and peaceful soundscapes',
    artwork: artworkUrl('genre-ambient'),
    color: '#4ECDC4',
    tracks: [],
    topArtists: []
  },
  {
    id: 'genre-5',
    name: 'Funk',
    description: 'Groovy basslines and infectious rhythms',
    artwork: artworkUrl('genre-funk'),
    color: '#FFD93D',
    tracks: [],
    topArtists: []
  }
];

// Build relationships between data
function buildMusicLibrary(): MusicLibrary {
  // Assign tracks to albums
  mockAlbums.forEach(album => {
    album.tracks = mockTracks.filter(track => track.albumId === album.id);
    album.duration = album.tracks.reduce((total, track) => total + track.duration, 0);
  });

  // Assign albums and top tracks to artists
  mockArtists.forEach(artist => {
    artist.albums = mockAlbums.filter(album => album.artistId === artist.id);
    artist.topTracks = mockTracks.filter(track => track.artistId === artist.id).slice(0, 5);
  });

  // Assign tracks to genres
  mockGenres.forEach(genre => {
    genre.tracks = mockTracks.filter(track => track.genre === genre.name);
    genre.topArtists = mockArtists.filter(artist => artist.genre.includes(genre.name)).slice(0, 6);
  });

  // Assign tracks to playlists
  mockPlaylists[0].tracks = [mockTracks[3], mockTracks[0], mockTracks[5]]; // Chill Vibes
  mockPlaylists[1].tracks = [mockTracks[2], mockTracks[4], mockTracks[7]]; // Workout Energy
  mockPlaylists[2].tracks = mockTracks.filter(track => track.liked); // My Favorites

  // Calculate playlist durations
  mockPlaylists.forEach(playlist => {
    playlist.duration = playlist.tracks.reduce((total, track) => total + track.duration, 0);
  });

  return {
    tracks: mockTracks,
    albums: mockAlbums,
    artists: mockArtists,
    playlists: mockPlaylists,
    genres: mockGenres,
    recentlyPlayed: mockTracks.slice(0, 5),
    topTracks: mockTracks.sort((a, b) => b.plays - a.plays).slice(0, 10),
    newReleases: mockAlbums.filter(album => album.year === 2023)
  };
}

export const musicLibrary = buildMusicLibrary();

// Helper functions
export const formatDuration = (seconds: number): string => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};