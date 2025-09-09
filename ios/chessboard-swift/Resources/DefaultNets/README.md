# Default Neural Networks

This directory contains bundled neural network files for the chess engine.

## Network Files

### Included Networks

- `stockfish_light.nnue` - Compact 5MB network optimized for mobile devices (~3200 Elo)
- `stockfish_medium.nnue` - Balanced 15MB network for good performance (~3400 Elo)

### Network Information

#### stockfish_light.nnue
- **Size**: ~5MB
- **Architecture**: NNUE (768 inputs, 2x256 hidden layers)
- **Strength**: ~3200 Elo
- **Optimization**: Mobile-optimized for iOS devices
- **Memory Usage**: Low (~64MB hash recommended)
- **Best For**: iPhone 12 and older, battery conservation

#### stockfish_medium.nnue
- **Size**: ~15MB  
- **Architecture**: NNUE (768 inputs, 4x256 hidden layers)
- **Strength**: ~3400 Elo
- **Optimization**: Balanced performance and size
- **Memory Usage**: Moderate (~128MB hash recommended)
- **Best For**: iPhone 13+, balanced performance

### Usage Notes

1. **Automatic Selection**: The app automatically selects the most appropriate network based on device capabilities.

2. **Manual Override**: Users can manually select which network to use in Settings.

3. **Download Options**: Additional high-strength networks can be downloaded:
   - Full Stockfish network (~50MB, ~3600 Elo)
   - Latest development networks (varies)

4. **Validation**: All network files are validated for integrity and compatibility before use.

### Technical Details

Networks use the NNUE (Efficiently Updatable Neural Networks) architecture specifically designed for chess position evaluation. They replace traditional hand-crafted evaluation functions with learned patterns from millions of chess games.

### File Management

- Bundled networks are read-only
- Downloaded networks are stored in Documents/NeuralNetworks/
- Invalid or corrupted networks are automatically detected
- Network switching requires engine restart

### Performance Impact

| Device Type | Recommended Network | Expected Performance |
|-------------|-------------------|-------------------|
| iPhone 12 and older | Light | Good, battery efficient |
| iPhone 13-14 | Medium | Very good, balanced |
| iPhone 15+ | Medium or Full | Excellent, maximum strength |

### Troubleshooting

**Network not loading:**
- Check device storage space
- Verify network file integrity
- Restart the app
- Reset to default light network

**Poor performance:**
- Switch to lighter network
- Reduce hash table size
- Limit analysis depth/time

**High battery usage:**
- Use light network
- Enable analysis time limits
- Reduce background analysis