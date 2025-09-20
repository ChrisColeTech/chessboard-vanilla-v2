import React, { useState } from 'react';
import { X, Music, Globe, Lock, Image } from 'lucide-react';
import { useMusicStore } from '../../stores/musicStore';

interface CreatePlaylistModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (playlistId: string) => void;
}

export const CreatePlaylistModal: React.FC<CreatePlaylistModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const { createPlaylist } = useMusicStore();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    isPublic: false,
  });
  const [isCreating, setIsCreating] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name.trim()) return;

    setIsCreating(true);
    
    try {
      const playlist = createPlaylist(formData.name.trim(), formData.description.trim());
      
      // Reset form
      setFormData({ name: '', description: '', isPublic: false });
      
      // Call success callback
      onSuccess?.(playlist.id);
      
      // Close modal
      onClose();
    } catch (error) {
      console.error('Failed to create playlist:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleInputChange = (field: keyof typeof formData, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={handleOverlayClick}
    >
      <div className="bg-background border border-border rounded-xl w-full max-w-md shadow-xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <h2 className="text-xl font-semibold">Create New Playlist</h2>
          <button
            onClick={onClose}
            className="p-1 rounded-full hover:bg-muted transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Artwork placeholder */}
          <div className="flex justify-center">
            <div className="w-32 h-32 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-xl flex items-center justify-center border-2 border-dashed border-border">
              <div className="text-center">
                <Image className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
                <p className="text-xs text-muted-foreground">Add artwork</p>
              </div>
            </div>
          </div>

          {/* Name input */}
          <div>
            <label htmlFor="playlist-name" className="block text-sm font-medium mb-2">
              Playlist name *
            </label>
            <input
              id="playlist-name"
              type="text"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              placeholder="My awesome playlist"
              className="w-full px-3 py-2 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              maxLength={100}
              required
            />
            <p className="text-xs text-muted-foreground mt-1">
              {formData.name.length}/100 characters
            </p>
          </div>

          {/* Description input */}
          <div>
            <label htmlFor="playlist-description" className="block text-sm font-medium mb-2">
              Description
            </label>
            <textarea
              id="playlist-description"
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              placeholder="Tell people what this playlist is about..."
              className="w-full px-3 py-2 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
              rows={3}
              maxLength={300}
            />
            <p className="text-xs text-muted-foreground mt-1">
              {formData.description.length}/300 characters
            </p>
          </div>

          {/* Privacy setting */}
          <div>
            <label className="block text-sm font-medium mb-3">Privacy</label>
            <div className="space-y-3">
              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="radio"
                  name="privacy"
                  checked={!formData.isPublic}
                  onChange={() => handleInputChange('isPublic', false)}
                  className="mt-1"
                />
                <div>
                  <div className="flex items-center gap-2 font-medium">
                    <Lock className="w-4 h-4" />
                    Private
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Only you can see this playlist
                  </p>
                </div>
              </label>

              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="radio"
                  name="privacy"
                  checked={formData.isPublic}
                  onChange={() => handleInputChange('isPublic', true)}
                  className="mt-1"
                />
                <div>
                  <div className="flex items-center gap-2 font-medium">
                    <Globe className="w-4 h-4" />
                    Public
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Anyone can search for and view this playlist
                  </p>
                </div>
              </label>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!formData.name.trim() || isCreating}
              className="flex items-center gap-2 px-6 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isCreating ? (
                <>
                  <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <Music className="w-4 h-4" />
                  Create Playlist
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};