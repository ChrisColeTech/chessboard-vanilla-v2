# Chessboard Visual Enhancements Implementation Plan - Document 26

## Overview
Comprehensive implementation plan for modern, elegant chessboard visual enhancements based on Document 25 research findings. This plan maintains the existing clean architecture while adding sophisticated visual features through a props-based, toggleable system that prioritizes performance and accessibility.

---

## 📊 Implementation Progress Tracking

| Priority | Phase | Feature | Status | New Files | Integration Points | Notes |
|----------|-------|---------|--------|-----------|-------------------|-------|
| **HIGH** | **Phase 1** | **Foundation Enhancements** | ⏳ **Pending** | | | |
| HIGH | 1.1 | Theme System Architecture | ⏳ Pending | `hooks/useTheme.ts`<br>`services/ThemeService.ts`<br>`constants/themes.constants.ts`<br>`types/enhancement.types.ts`<br>`styles/themes/*.css` | `components/Chessboard.tsx`<br>`components/Board.tsx`<br>`types/component.types.ts`<br>`styles/chessboard.css` | Modern, elegant visual identity with lazy loading |
| HIGH | 1.2 | Enhanced Move Animation System | ⏳ Pending | `services/AnimationController.ts`<br>`hooks/useAnimation.ts`<br>`styles/animations.css` | `components/Piece.tsx`<br>`components/Square.tsx`<br>`hooks/useDragAndDrop.ts`<br>`styles/chessboard.css` | Time-control adaptive animations with GPU acceleration |
| HIGH | 1.3 | Focus Mode Implementation | ⏳ Pending | `components/FocusMode.tsx`<br>`hooks/useFocusMode.ts`<br>`constants/focus-modes.constants.ts` | `components/Chessboard.tsx`<br>`App.tsx`<br>`styles/chessboard.css` | Context-aware UI with progressive disclosure |
| HIGH | 1.4 | Coordinate Display Enhancement | ⏳ Pending | `components/CoordinateDisplay.tsx`<br>`hooks/useCoordinates.ts`<br>`styles/coordinates.css` | `components/Board.tsx`<br>`components/Square.tsx`<br>`types/component.types.ts` | Skill-adaptive coordinate positioning |
| **MEDIUM** | **Phase 2** | **Advanced Visual Features** | ⏳ **Pending** | | | |
| MEDIUM | 2.1 | Advanced Move Highlighting System | ⏳ Pending | `services/HighlightEngine.ts`<br>`hooks/useHighlight.ts`<br>`components/HighlightOverlay.tsx`<br>`styles/highlights.css` | `components/Square.tsx`<br>`components/Board.tsx`<br>`services/ChessGameService.ts`<br>`hooks/useChessGame.ts` | Chess-specific threat and pattern visualization |
| MEDIUM | 2.2 | Audio System Integration | ⏳ Pending | `services/AudioManager.ts`<br>`hooks/useAudio.ts`<br>`constants/audio-profiles.constants.ts`<br>`assets/audio/*.mp3` | `components/Chessboard.tsx`<br>`hooks/useChessGame.ts`<br>`App.tsx` | Context-aware audio with environmental adaptation |
| MEDIUM | 2.3 | Accessibility Enhancement Suite | ⏳ Pending | `hooks/useAccessibility.ts`<br>`components/ScreenReaderAnnouncements.tsx`<br>`styles/accessibility.css`<br>`utils/a11y.utils.ts` | `components/Chessboard.tsx`<br>`components/Square.tsx`<br>`components/Piece.tsx`<br>`styles/chessboard.css` | WCAG 2.1 AA compliance with cognitive support |

### **Status Legend**
- ⏳ **Pending** - Not started
- 🔄 **In Progress** - Currently being implemented
- ✅ **Completed** - Implementation finished
- 🧪 **Testing** - Under review/testing
- ❌ **Blocked** - Blocked by dependencies or issues

---

## 🎓 Lessons Learned During Implementation

### **React Hooks Compliance**
- **Issue**: React hooks order violations caused crashes when hooks were called after early returns
- **Solution**: All hooks must be called at the top of components before any conditional logic or early returns
- **Impact**: Required restructuring of Chessboard component to move all useMemo/useCallback calls before loading/error checks

### **Import/Export Management**  
- **Issue**: Missing exports in index files caused import errors during development
- **Solution**: Systematically added all new enhancement hooks and types to barrel exports
- **Files Updated**: `src/hooks/index.ts`, `src/types/index.ts`

### **Vite Dynamic Import Compatibility**
- **Issue**: Dynamic imports using template literals caused Vite warnings and potential build issues
- **Solution**: Replaced dynamic imports with explicit switch statements for better static analysis
- **File**: `src/services/ThemeService.ts` - switched from `import(\`../styles/themes/\${file}\`)` to explicit case statements

### **Variable Naming Conflicts**
- **Issue**: Multiple hooks returning same-named properties (e.g., `isAnimating`) caused identifier conflicts
- **Solution**: Use destructuring aliases to avoid conflicts: `isAnimating: isDragAnimating`
- **Pattern**: Consistently prefix hook return values when conflicts arise

### **CSS Integration Strategy**
- **Issue**: Enhancement CSS files needed to be properly imported and integrated
- **Solution**: Import all theme CSS files directly in Chessboard component for immediate availability
- **Performance**: Lazy loading still maintained through ThemeService for optimization

### **Type Safety Maintenance**
- **Issue**: Complex type intersections and optional properties required careful handling
- **Solution**: Extended base interfaces rather than creating completely new ones to maintain compatibility
- **Pattern**: `extends Partial<ChessboardEnhancements>` for backward compatibility

### **Props Architecture**
- **Working Pattern**: 
  - Enhancement bundle prop (`enhancements?: ChessboardEnhancements`)
  - Individual override props with fallback to bundle
  - Event handler props for each enhancement category
- **Result**: Clean, backward-compatible API that supports both simple and advanced usage

---

## 🏗️ Current Architecture Analysis

### **Existing Foundation**
- **Clean Architecture**: Foundation → Services → Hooks → Components
- **TypeScript**: Full type safety with strict mode
- **Vanilla CSS**: CSS custom properties for theming (`--chessboard-light-square`, `--chessboard-dark-square`)
- **Props-Based Design**: `ChessboardProps` interface with optional configurations
- **Performance-Optimized**: React.memo, stable keys, ResizeObserver

### **Current Customization Points**
```typescript
interface ChessboardProps {
  pieceSet?: 'classic' | 'modern' | 'tournament' | 'executive' | 'conqueror';
  showCoordinates?: boolean;
  allowDragAndDrop?: boolean;
  orientation?: PieceColor;
  maxWidth?: number;
  className?: string;
  style?: React.CSSProperties;
}
```

### **Architecture Strengths for Enhancement**
- CSS custom properties already established for theming
- Component isolation allows for enhancement without breaking changes
- Hook-based state management enables complex feature addition
- Service layer separation supports audio and performance enhancements

---

## 🎯 Enhancement Architecture Strategy

### **Core Design Principles**
1. **Props-Based Configuration**: All enhancements controlled via optional props
2. **Zero Breaking Changes**: Existing API remains identical
3. **Performance First**: <200KB bundle impact, <16ms frame times
4. **Progressive Enhancement**: Features gracefully degrade if disabled
5. **Modern CSS**: Use latest CSS features for elegant animations and effects

### **Enhanced Props Interface Design**
```typescript
interface ChessboardEnhancements {
  // Theme System
  theme?: 'classic' | 'modern' | 'tournament' | 'executive' | 'conqueror' | 'elegant' | 'minimal';
  boardMaterial?: 'wood' | 'marble' | 'glass' | 'metal' | 'fabric';
  
  // Visual Feedback
  highlightStyle?: 'subtle' | 'standard' | 'vivid' | 'minimal';
  moveAnimation?: 'none' | 'fast' | 'smooth' | 'adaptive';
  
  // Focus Modes
  focusMode?: 'casual' | 'tournament' | 'analysis' | 'learning';
  
  // Audio System
  audioProfile?: 'silent' | 'subtle' | 'standard' | 'rich';
  
  // Accessibility
  highContrast?: boolean;
  reducedMotion?: boolean;
  
  // Advanced Features
  showThreats?: boolean;
  showLastMove?: boolean;
  coordinateStyle?: 'corner' | 'edge' | 'overlay' | 'hidden';
}

interface ChessboardProps extends ChessboardEnhancements {
  // ... existing props remain unchanged
  enhancements?: ChessboardEnhancements; // Optional enhancement bundle
}
```

---

## 📋 Implementation Phases

### **Phase 1: Foundation Enhancements (High Priority)**

#### **1.1 Theme System Architecture**
**Target**: Modern, elegant visual identity with performance focus

**Implementation**:
- Create `ThemeProvider` hook for centralized theme management
- Extend CSS custom properties for theme variations
- Implement theme lazy loading to minimize bundle impact

**New Files**:
```
src/
├── hooks/useTheme.ts                 # Theme management hook
├── services/ThemeService.ts          # Theme loading and caching
├── constants/themes.constants.ts     # Theme definitions
├── styles/themes/                    # Theme-specific CSS files
│   ├── classic.css
│   ├── modern.css
│   ├── tournament.css
│   ├── executive.css
│   ├── conqueror.css
│   ├── elegant.css
│   └── minimal.css
└── types/enhancement.types.ts        # Enhancement type definitions
```

**Integration Points**:
```
src/
├── components/Chessboard.tsx         # Add theme prop support and provider
├── components/Board.tsx              # Apply theme CSS variables
├── types/component.types.ts          # Extend props with theme options
└── styles/chessboard.css            # Extend with theme custom properties
```

**Technical Approach**:
```typescript
// Theme service with lazy loading
export class ThemeService {
  private static loadedThemes = new Set<string>();
  
  static async loadTheme(theme: string): Promise<void> {
    if (this.loadedThemes.has(theme)) return;
    
    const themeModule = await import(`../styles/themes/${theme}.css`);
    this.loadedThemes.add(theme);
  }
}

// Enhanced CSS custom properties
:root[data-theme="elegant"] {
  --chessboard-light-square: linear-gradient(135deg, #f4f1e8, #e8e2d5);
  --chessboard-dark-square: linear-gradient(135deg, #8b7355, #6d5a42);
  --chessboard-border: linear-gradient(45deg, #5a4a37, #3e342a);
  --board-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
```

#### **1.2 Enhanced Move Animation System**
**Target**: Time-control adaptive animations with 60fps performance

**Implementation**:
- Create `AnimationController` for managing piece movement
- Implement adaptive timing based on game context
- Use CSS transforms and transitions for GPU acceleration

**New Files**:
```
src/
├── services/AnimationController.ts   # Animation timing and context management
├── hooks/useAnimation.ts             # Animation state and controls
└── styles/animations.css            # Animation classes and transitions
```

**Integration Points**:
```
src/
├── components/Piece.tsx              # Add animation classes and timing
├── components/Square.tsx             # Apply animation states
├── hooks/useDragAndDrop.ts          # Integrate animation timing
└── styles/chessboard.css            # Extend with animation variables
```

**Technical Approach**:
```typescript
// Animation service
export class AnimationController {
  static getAnimationConfig(context: GameContext): AnimationConfig {
    switch (context.timeControl) {
      case 'bullet': return { duration: 0, easing: 'none' };
      case 'blitz': return { duration: 150, easing: 'ease-out' };
      case 'rapid': return { duration: 300, easing: 'ease-in-out' };
      default: return { duration: 400, easing: 'cubic-bezier(0.4, 0, 0.2, 1)' };
    }
  }
}

// CSS animation classes
.piece-move-smooth {
  transition: transform var(--move-duration) var(--move-easing);
  will-change: transform;
}
```

#### **1.3 Focus Mode Implementation**
**Target**: Context-aware UI that adapts to different play styles

**Implementation**:
- Create `FocusMode` component wrapper
- Implement progressive UI disclosure
- Design tournament-appropriate minimal interface

**New Files**:
```
src/
├── components/FocusMode.tsx          # Focus mode wrapper component
├── hooks/useFocusMode.ts             # Focus mode state management
└── constants/focus-modes.constants.ts # Focus mode configurations
```

**Integration Points**:
```
src/
├── components/Chessboard.tsx         # Apply focus mode wrapper
├── App.tsx                           # Add focus mode controls
└── styles/chessboard.css            # Add focus mode CSS variables
```

**Technical Approach**:
```typescript
// Focus mode configurations
const FOCUS_MODES: Record<FocusMode, FocusModeConfig> = {
  casual: { 
    showCoordinates: true, 
    showControls: true, 
    allowCustomization: true 
  },
  tournament: { 
    showCoordinates: false, 
    showControls: false, 
    allowCustomization: false 
  },
  analysis: { 
    showCoordinates: true, 
    showControls: true, 
    showAnalysisTools: true 
  },
  learning: { 
    showCoordinates: true, 
    showHints: true, 
    showPatterns: true 
  }
};
```

#### **1.4 Coordinate Display Enhancement**
**Target**: Skill-adaptive coordinate display with multiple positioning options

**Implementation**:
- Enhance existing coordinate system with new positioning modes
- Add contextual display logic based on skill level and game mode
- Implement typography optimization for different screen sizes

**New Files**:
```
src/
├── components/CoordinateDisplay.tsx  # Enhanced coordinate component
├── hooks/useCoordinates.ts           # Coordinate display logic
└── styles/coordinates.css           # Coordinate styling and positioning
```

**Integration Points**:
```
src/
├── components/Board.tsx              # Apply coordinate enhancements
├── components/Square.tsx             # Add coordinate positioning logic
└── types/component.types.ts          # Extend with coordinate options
```

### **Phase 2: Advanced Visual Features (Medium Priority)**

#### **2.1 Advanced Move Highlighting System**
**Target**: Chess-specific visual feedback for threats, patterns, and analysis

**Implementation**:
- Create `HighlightEngine` for managing complex visual states
- Implement threat detection visualization
- Add pattern recognition highlighting (pins, forks, skewers)

**New Files**:
```
src/
├── services/HighlightEngine.ts       # Chess pattern and threat detection
├── hooks/useHighlight.ts             # Highlight state management
├── components/HighlightOverlay.tsx   # Visual highlight components
└── styles/highlights.css            # Highlight styling and animations
```

**Integration Points**:
```
src/
├── components/Square.tsx             # Apply highlight overlays
├── components/Board.tsx              # Coordinate highlight display
├── services/ChessGameService.ts      # Extend with threat detection
└── hooks/useChessGame.ts            # Integrate highlight state
```

**Technical Approach**:
```typescript
// Highlight engine
export class HighlightEngine {
  static generateHighlights(gameState: ChessGameState, config: HighlightConfig): HighlightMap {
    const highlights = new Map();
    
    if (config.showThreats) {
      highlights.set('threats', this.calculateThreats(gameState));
    }
    
    if (config.showPatterns) {
      highlights.set('pins', this.detectPins(gameState));
      highlights.set('forks', this.detectForks(gameState));
    }
    
    return highlights;
  }
}
```

#### **2.2 Audio System Integration**
**Target**: Chess-specific audio design with environmental adaptation

**Implementation**:
- Create `AudioManager` service for sound management
- Implement context-aware audio profiles
- Add lazy loading for audio assets

**New Files**:
```
src/
├── services/AudioManager.ts          # Audio context and sound management
├── hooks/useAudio.ts                 # Audio state and profile management
├── constants/audio-profiles.constants.ts # Audio profile configurations
└── assets/audio/                     # Audio asset files
    ├── subtle/
    ├── standard/
    └── rich/
        ├── move.mp3
        ├── capture.mp3
        ├── check.mp3
        └── checkmate.mp3
```

**Integration Points**:
```
src/
├── components/Chessboard.tsx         # Add audio prop support
├── hooks/useChessGame.ts            # Trigger audio events on game actions
└── App.tsx                           # Add audio profile controls
```

**Technical Approach**:
```typescript
// Audio manager with context awareness
export class AudioManager {
  private static audioContext?: AudioContext;
  private static loadedSounds = new Map<string, AudioBuffer>();
  
  static async playSound(event: ChessAudioEvent, profile: AudioProfile): Promise<void> {
    const config = AUDIO_PROFILES[profile][event];
    if (!config.enabled) return;
    
    const sound = await this.loadSound(config.file);
    this.playWithVolume(sound, config.volume);
  }
}

// Audio profiles
const AUDIO_PROFILES = {
  silent: { move: { enabled: false } },
  subtle: { move: { enabled: true, file: 'soft-click.mp3', volume: 0.3 } },
  standard: { move: { enabled: true, file: 'wood-click.mp3', volume: 0.6 } },
  rich: { move: { enabled: true, file: 'premium-move.mp3', volume: 0.8 } }
};
```

#### **2.3 Accessibility Enhancement Suite**
**Target**: WCAG 2.1 AA compliance with cognitive support features

**Implementation**:
- Add high contrast mode with customizable color schemes
- Implement motion reduction support
- Create keyboard navigation enhancement
- Add screen reader support for game state

**New Files**:
```
src/
├── hooks/useAccessibility.ts         # Accessibility state and preferences
├── components/ScreenReaderAnnouncements.tsx # Screen reader integration
├── styles/accessibility.css         # High contrast and a11y styles
└── utils/a11y.utils.ts              # Accessibility utility functions
```

**Integration Points**:
```
src/
├── components/Chessboard.tsx         # Add accessibility wrapper and props
├── components/Square.tsx             # Add keyboard navigation and ARIA
├── components/Piece.tsx              # Add screen reader descriptions
└── styles/chessboard.css            # Extend with accessibility variables
```



---

## 🔧 Technical Implementation Details

### **Props Integration Strategy**

#### **Backward Compatibility**
```typescript
// Enhanced Chessboard component with full backward compatibility
export const Chessboard: React.FC<ChessboardProps> = ({
  // Existing props (unchanged)
  pieceSet = 'classic',
  showCoordinates = true,
  allowDragAndDrop = true,
  orientation = 'white',
  
  // New enhancement props (all optional)
  enhancements = {},
  
  // Individual enhancement props for convenience
  theme = enhancements.theme || 'classic',
  boardMaterial = enhancements.boardMaterial || 'wood',
  highlightStyle = enhancements.highlightStyle || 'standard',
  moveAnimation = enhancements.moveAnimation || 'smooth',
  focusMode = enhancements.focusMode || 'casual',
  audioProfile = enhancements.audioProfile || 'standard',
  
  ...rest
}) => {
  // Component implementation
};
```

#### **Enhancement Hook Architecture**
```typescript
// Central enhancement management hook
export const useEnhancements = (config: ChessboardEnhancements) => {
  const theme = useTheme(config.theme, config.boardMaterial);
  const animation = useAnimation(config.moveAnimation);
  const focus = useFocusMode(config.focusMode);
  const audio = useAudio(config.audioProfile);
  const highlight = useHighlight(config.highlightStyle);
  
  return {
    theme,
    animation,
    focus,
    audio,
    highlight,
    cssVariables: generateCSSVariables({ theme, animation, focus })
  };
};
```

### **CSS Architecture Enhancement**

#### **Advanced Custom Properties System**
```css
/* Enhanced CSS custom properties for themes */
:root {
  /* Base theme properties */
  --chessboard-theme: 'classic';
  --chessboard-material: 'wood';
  
  /* Dynamic color calculations */
  --light-base: hsl(39, 40%, 85%);
  --dark-base: hsl(39, 30%, 65%);
  
  /* Material-specific enhancements */
  --material-texture: none;
  --material-shine: 0;
  --material-depth: 0px;
  
  /* Animation properties */
  --move-duration: 300ms;
  --move-easing: cubic-bezier(0.4, 0, 0.2, 1);
  --hover-transition: 150ms ease-out;
  
  /* Focus mode adjustments */
  --ui-opacity: 1;
  --coordinate-visibility: visible;
  --control-display: flex;
}

/* Theme variations */
:root[data-theme="elegant"] {
  --material-texture: linear-gradient(135deg, transparent 25%, rgba(255,255,255,0.1) 50%, transparent 75%);
  --material-shine: 0.05;
  --material-depth: 2px;
  --board-shadow: 0 8px 32px rgba(0,0,0,0.15);
}

:root[data-theme="minimal"] {
  --chessboard-light-square: #fafafa;
  --chessboard-dark-square: #e0e0e0;
  --chessboard-border: #bdbdbd;
  --material-texture: none;
  --board-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

#### **Performance-Optimized Animations**
```css
/* GPU-accelerated piece movement */
.chessboard-piece {
  transform: translateZ(0); /* Force GPU layer */
  will-change: transform;
  backface-visibility: hidden;
}

.piece-moving {
  transition: transform var(--move-duration) var(--move-easing);
  z-index: 10;
}

/* Smooth highlight animations */
.square-highlight {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 200ms ease-in-out;
  pointer-events: none;
}

.square-highlight.active {
  opacity: 1;
}
```

### **Bundle Optimization Strategy**

#### **Lazy Loading Implementation**
```typescript
// Theme lazy loading with dynamic imports
const loadTheme = async (themeName: string) => {
  const themeModule = await import(`../styles/themes/${themeName}.css`);
  return themeModule.default;
};

// Audio lazy loading
const loadAudioProfile = async (profileName: string) => {
  const sounds = await Promise.all([
    import(`../assets/audio/${profileName}/move.mp3`),
    import(`../assets/audio/${profileName}/capture.mp3`),
    import(`../assets/audio/${profileName}/check.mp3`)
  ]);
  return sounds;
};
```

#### **Progressive Enhancement Detection**
```typescript
// Feature detection for progressive enhancement
const FEATURE_SUPPORT = {
  cssCustomProperties: CSS.supports('(--test: 0)'),
  webAudio: typeof AudioContext !== 'undefined',
  cssGrid: CSS.supports('display: grid'),
  resizeObserver: typeof ResizeObserver !== 'undefined',
  intersectionObserver: typeof IntersectionObserver !== 'undefined'
};

// Graceful degradation
export const useProgressiveEnhancement = () => {
  return {
    canUseAdvancedThemes: FEATURE_SUPPORT.cssCustomProperties,
    canUseAudio: FEATURE_SUPPORT.webAudio,
    canUseAnimations: !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  };
};
```

---

## 📊 Performance Targets & Metrics

### **Bundle Size Optimization**
- **Target**: <200KB additional for all enhancements
- **Strategy**: Lazy loading, tree shaking, asset compression
- **Measurement**: Bundle analyzer reports, performance budgets

### **Runtime Performance**
- **Target**: <16ms frame times during 60fps gameplay
- **Strategy**: GPU acceleration, efficient DOM updates, RAF optimization
- **Measurement**: Chrome DevTools performance profiling

### **Theme Switching Performance**
- **Target**: <100ms response time for theme changes
- **Strategy**: CSS custom property updates, cached theme data
- **Measurement**: Performance.mark() timing

### **Audio Performance**
- **Target**: <50ms audio loading for game events
- **Strategy**: Audio context management, buffer caching
- **Measurement**: AudioContext timing analysis

---

## 🎨 Modern Design Language

### **Visual Design Principles**
1. **Subtle Elegance**: Refined materials and lighting effects
2. **Contextual Adaptation**: UI adapts to game context and user skill
3. **Motion with Purpose**: Animations enhance understanding, not distraction
4. **Accessibility First**: High contrast, motion reduction, screen reader support
5. **Performance Transparency**: Visual quality never compromises responsiveness

### **Component Enhancement Examples**

#### **Enhanced Square Component**
```typescript
interface EnhancedSquareProps extends SquareProps {
  highlight?: HighlightType[];
  material?: MaterialType;
  animationContext?: AnimationContext;
  focusMode?: FocusMode;
}

export const EnhancedSquare: React.FC<EnhancedSquareProps> = ({
  // Standard props
  position, piece, isSelected, isValidDropTarget,
  
  // Enhancement props
  highlight = [],
  material = 'wood',
  animationContext = 'standard',
  focusMode = 'casual',
  
  ...rest
}) => {
  const { cssClasses, cssVariables } = useSquareEnhancements({
    highlight,
    material,
    animationContext,
    focusMode
  });
  
  return (
    <div 
      className={`chessboard-square ${cssClasses.join(' ')}`}
      style={cssVariables}
      {...rest}
    >
      {/* Enhanced square content */}
    </div>
  );
};
```

### **Accessibility Integration**
```typescript
// Screen reader integration for enhanced features
export const useScreenReaderEnhancements = (gameState: ChessGameState, highlights: HighlightMap) => {
  const announcements = useRef<string[]>([]);
  
  useEffect(() => {
    if (highlights.has('threats')) {
      const threatCount = highlights.get('threats').length;
      announcements.current.push(`${threatCount} pieces under threat`);
    }
    
    if (highlights.has('pins')) {
      announcements.current.push(`Pin detected on the board`);
    }
    
    // Announce changes to screen reader
    const message = announcements.current.join(', ');
    if (message) {
      announceToScreenReader(message);
      announcements.current = [];
    }
  }, [highlights]);
};
```

---

## ✅ Success Criteria

### **Technical Metrics**
- ✅ Bundle size increase <200KB
- ✅ Frame rates maintain >55fps during animations
- ✅ Theme switching <100ms response time
- ✅ Audio loading <50ms for game events
- ✅ Zero breaking changes to existing API

### **User Experience Metrics**
- ✅ WCAG 2.1 AA accessibility compliance
- ✅ 3-5 meaningful customization options
- ✅ Context-aware defaults
- ✅ Progressive enhancement graceful degradation

### **Code Quality Metrics**
- ✅ TypeScript strict mode compliance
- ✅ 90%+ test coverage for new features
- ✅ Clean architecture principles maintained
- ✅ Performance regression tests pass

---

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Review current codebase architecture for enhancement implementation", "status": "completed", "activeForm": "Reviewing current codebase architecture for enhancement implementation"}, {"content": "Analyze Document 25 research findings for implementation phases", "status": "completed", "activeForm": "Analyzing Document 25 research findings for implementation phases"}, {"content": "Create Document 26 implementation plan with modern design approach", "status": "completed", "activeForm": "Creating Document 26 implementation plan with modern design approach"}, {"content": "Design props-based architecture for toggleable enhancements", "status": "completed", "activeForm": "Designing props-based architecture for toggleable enhancements"}]