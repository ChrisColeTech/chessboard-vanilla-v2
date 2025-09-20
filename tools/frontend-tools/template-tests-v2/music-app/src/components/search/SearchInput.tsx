import React, { useState, useEffect } from 'react';
import { Search, X, Music, Disc, Users, List } from 'lucide-react';
import { useSearch } from '../../stores/musicStore';

interface SearchInputProps {
  placeholder?: string;
  autoFocus?: boolean;
  onFocus?: () => void;
  onBlur?: () => void;
  className?: string;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  placeholder = "Search songs, artists, albums...",
  autoFocus = false,
  onFocus,
  onBlur,
  className = '',
}) => {
  const { searchQuery, searchMusic, clearSearch } = useSearch();
  const [localQuery, setLocalQuery] = useState(searchQuery);
  const [isFocused, setIsFocused] = useState(false);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (localQuery.trim()) {
        searchMusic(localQuery.trim());
      } else {
        clearSearch();
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [localQuery, searchMusic, clearSearch]);

  // Sync with external search query changes
  useEffect(() => {
    setLocalQuery(searchQuery);
  }, [searchQuery]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalQuery(e.target.value);
  };

  const handleClear = () => {
    setLocalQuery('');
    clearSearch();
  };

  const handleFocus = () => {
    setIsFocused(true);
    onFocus?.();
  };

  const handleBlur = () => {
    setIsFocused(false);
    onBlur?.();
  };

  const QuickFilters = () => (
    <div className="flex items-center gap-2 mt-3">
      <span className="text-xs text-muted-foreground">Quick filters:</span>
      <button
        onClick={() => setLocalQuery('genre:rock')}
        className="flex items-center gap-1 px-2 py-1 text-xs bg-muted rounded-full hover:bg-muted/80 transition-colors"
      >
        <Music className="w-3 h-3" />
        Rock
      </button>
      <button
        onClick={() => setLocalQuery('genre:jazz')}
        className="flex items-center gap-1 px-2 py-1 text-xs bg-muted rounded-full hover:bg-muted/80 transition-colors"
      >
        <Disc className="w-3 h-3" />
        Jazz
      </button>
      <button
        onClick={() => setLocalQuery('artist:')}
        className="flex items-center gap-1 px-2 py-1 text-xs bg-muted rounded-full hover:bg-muted/80 transition-colors"
      >
        <Users className="w-3 h-3" />
        Artists
      </button>
    </div>
  );

  return (
    <div className={`relative ${className}`}>
      <div className={`relative transition-all duration-200 ${
        isFocused ? 'ring-2 ring-primary ring-opacity-50' : ''
      }`}>
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className={`h-4 w-4 transition-colors ${
            isFocused ? 'text-primary' : 'text-muted-foreground'
          }`} />
        </div>
        
        <input
          type="text"
          value={localQuery}
          onChange={handleInputChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          placeholder={placeholder}
          autoFocus={autoFocus}
          className={`
            block w-full pl-10 pr-10 py-3 
            border border-border rounded-xl
            bg-background/50 backdrop-blur-sm
            text-foreground placeholder-muted-foreground
            focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent
            transition-all duration-200
            ${isFocused ? 'bg-background' : ''}
          `}
        />
        
        {localQuery && (
          <button
            onClick={handleClear}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Search suggestions or quick filters */}
      {isFocused && !localQuery && (
        <div className="absolute top-full left-0 right-0 mt-2 p-4 bg-background border border-border rounded-xl shadow-lg z-10">
          <h4 className="text-sm font-medium mb-2">Popular searches</h4>
          <div className="space-y-2">
            {['The Weeknd', 'Billie Eilish', 'Daft Punk', 'Radiohead'].map((term) => (
              <button
                key={term}
                onClick={() => setLocalQuery(term)}
                className="flex items-center gap-2 w-full p-2 text-left hover:bg-muted rounded-lg transition-colors"
              >
                <Search className="w-3 h-3 text-muted-foreground" />
                <span className="text-sm">{term}</span>
              </button>
            ))}
          </div>
          <QuickFilters />
        </div>
      )}

      {/* Search status */}
      {localQuery && (
        <div className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            Searching for "{localQuery}"
          </div>
        </div>
      )}
    </div>
  );
};