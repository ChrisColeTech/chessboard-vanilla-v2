# Chess Sound Effects

This directory contains sound effects for chess interactions.

## Current Files
- `move.mp3` - Standard piece movement sound
- `capture.mp3` - Piece capture sound (slightly more dramatic)
- `check.mp3` - King in check alert sound
- `error.mp3` - Invalid move attempt sound
- `game-start.mp3` - Game beginning sound
- `game-end.mp3` - Game conclusion sound

## Usage
These sounds are loaded by the `audioService.ts` and played during chess interactions:
- Move: Standard piece movement
- Capture: When a piece captures another piece
- Check: When the king is in check
- Error: Invalid moves or errors
- Game Start/End: Session boundary events

## Sound Specifications
- Format: MP3 (with WAV fallback support)
- Duration: 0.1-0.5 seconds for responsive feedback
- Volume: Pre-normalized to prevent audio spikes
- Quality: Optimized for web delivery

## Replacement
You can replace these placeholder files with professional chess sound effects.
Recommended sources:
- Freesound.org
- Chess.com sound assets
- Custom recordings
- Royalty-free sound libraries