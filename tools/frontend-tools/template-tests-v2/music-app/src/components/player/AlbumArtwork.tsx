import React, { useState, useEffect } from 'react';
import { usePlayer } from '../../stores/musicStore';

interface AlbumArtworkProps {
  src: string;
  alt: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  showVisualizer?: boolean;
}

export const AlbumArtwork: React.FC<AlbumArtworkProps> = ({
  src,
  alt,
  size = 'md',
  className = '',
  showVisualizer = false,
}) => {
  const player = usePlayer();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const sizeClasses = {
    sm: 'w-12 h-12',
    md: 'w-16 h-16',
    lg: 'w-24 h-24',
    xl: 'w-32 h-32',
  };

  const handleImageLoad = () => {
    setImageLoaded(true);
    setImageError(false);
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(false);
  };

  const FallbackArtwork = () => (
    <div className="w-full h-full bg-gradient-to-br from-primary/30 to-secondary/30 flex items-center justify-center">
      <div className="w-1/2 h-1/2 rounded-full bg-white/20 flex items-center justify-center">
        <svg 
          className="w-1/2 h-1/2 text-white/60" 
          fill="currentColor" 
          viewBox="0 0 20 20"
        >
          <path fillRule="evenodd" d="M18 3a1 1 0 00-1.447-.894L8.763 6H5a3 3 0 000 6h.28l1.771 5.316A1 1 0 008 18h1a1 1 0 001-1v-4.382l6.553 3.276A1 1 0 0018 15V3z" clipRule="evenodd" />
        </svg>
      </div>
    </div>
  );

  const AudioVisualizer = () => {
    const [bars, setBars] = useState<number[]>([]);

    useEffect(() => {
      if (!player.isPlaying) {
        setBars(Array(8).fill(0.1));
        return;
      }

      const interval = setInterval(() => {
        setBars(Array(8).fill(0).map(() => Math.random() * 0.8 + 0.2));
      }, 150);

      return () => clearInterval(interval);
    }, [player.isPlaying]);

    return (
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="flex items-end gap-0.5 h-6">
          {bars.map((height, index) => (
            <div
              key={index}
              className="w-1 bg-white/40 rounded-sm transition-all duration-150"
              style={{ 
                height: `${height * 100}%`,
                animationDelay: `${index * 50}ms`
              }}
            />
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className={`${sizeClasses[size]} ${className} relative group`}>
      {/* Main artwork container with glow effect */}
      <div className="relative w-full h-full rounded-xl overflow-hidden bg-gradient-to-br from-primary/20 to-secondary/20 ring-1 ring-white/10">
        {imageError ? (
          <FallbackArtwork />
        ) : (
          <>
            <img
              src={src}
              alt={alt}
              className={`w-full h-full object-cover transition-all duration-300 ${
                imageLoaded 
                  ? 'opacity-100 group-hover:scale-105' 
                  : 'opacity-0'
              }`}
              onLoad={handleImageLoad}
              onError={handleImageError}
            />
            {!imageLoaded && !imageError && (
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20 animate-pulse" />
            )}
          </>
        )}

        {/* Visualizer overlay */}
        {showVisualizer && player.isPlaying && (
          <div className="absolute inset-0 bg-black/30 backdrop-blur-sm">
            <AudioVisualizer />
          </div>
        )}

        {/* Playing indicator */}
        {player.isPlaying && player.currentTrack && (
          <div className="absolute bottom-1 right-1">
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
          </div>
        )}
      </div>

      {/* Glow effect when playing */}
      {player.isPlaying && player.currentTrack && (
        <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-xl blur-sm opacity-60 animate-pulse" />
      )}

      {/* Reflection effect */}
      <div className="absolute -bottom-2 left-0 right-0 h-2 bg-gradient-to-b from-black/10 to-transparent rounded-b-xl opacity-30" />
    </div>
  );
};