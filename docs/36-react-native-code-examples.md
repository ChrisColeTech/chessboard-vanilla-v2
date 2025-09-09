# Document 36: React Native Migration Code Examples

## Component Conversion Examples

### HTML to React Native Element Mapping

**Basic Element Conversions:**
```typescript
// Web HTML → React Native
<div>      → <View>
<button>   → <TouchableOpacity> or <Pressable>
<span>     → <Text>
<p>        → <Text>
<h1-h6>    → <Text>
<header>   → <View>
<section>  → <View>
```

**Event Handler Conversions:**
```typescript
// Web → React Native
onClick    → onPress
onMouseDown → onTouchStart
onMouseMove → onTouchMove
onMouseUp   → onTouchEnd
```

### Complete Component Conversion Example

**Before: Web Header Component**
```typescript
// src/components/layout/Header.tsx (Web)
import { Settings } from 'lucide-react'

export function Header({ onSettingsClick }: Props) {
  return (
    <header className="glass-layout border-b border-primary/20">
      <div className="flex items-center justify-between px-4 py-3">
        <h1 className="text-xl font-bold text-primary">Chessboard</h1>
        <button onClick={onSettingsClick}>
          <Settings className="w-6 h-6" />
        </button>
      </div>
    </header>
  )
}
```

**After: React Native Header Component**
```typescript
// src/components/layout/Header.tsx (React Native)
import { View, Text, TouchableOpacity } from 'react-native'
import { Settings } from 'lucide-react-native'

export function Header({ onSettingsClick }: Props) {
  return (
    <View className="glass-layout border-b border-primary/20">
      <View className="flex-row items-center justify-between px-4 py-3">
        <Text className="text-xl font-bold text-primary">Chessboard</Text>
        <TouchableOpacity onPress={onSettingsClick}>
          <Settings size={24} color="#fff" />
        </TouchableOpacity>
      </View>
    </View>
  )
}
```

### Icon Library Migration

**Web Version (lucide-react):**
```typescript
import { Settings, X, Sun, Moon, Layout, Target, Coins } from 'lucide-react'

// Usage in JSX
<Settings className="w-6 h-6 text-primary" />
<X className="w-4 h-4" />
```

**React Native Version (lucide-react-native):**
```typescript
import { Settings, X, Sun, Moon, Layout, Target, Coins } from 'lucide-react-native'

// Usage in JSX
<Settings size={24} color="#primaryColor" />
<X size={16} color="#textColor" />
```

### Touch and Gesture Handling

**Web Mouse Events:**
```typescript
<div 
  onMouseDown={handleMouseDown}
  onMouseMove={handleMouseMove}
  onMouseUp={handleMouseUp}
  className="draggable-piece"
>
  <ChessPiece />
</div>
```

**React Native Touch Events:**
```typescript
<View
  onTouchStart={handleTouchStart}
  onTouchMove={handleTouchMove} 
  onTouchEnd={handleTouchEnd}
  className="draggable-piece"
>
  <ChessPiece />
</View>
```

**React Native Gesture Handler (Advanced):**
```typescript
import { PanGestureHandler } from 'react-native-gesture-handler'
import Animated, { useAnimatedGestureHandler } from 'react-native-reanimated'

const gestureHandler = useAnimatedGestureHandler({
  onStart: (_, context) => {
    // Handle drag start
    context.startX = translateX.value
    context.startY = translateY.value
  },
  onActive: (event, context) => {
    // Handle drag move
    translateX.value = context.startX + event.translationX
    translateY.value = context.startY + event.translationY
  },
  onEnd: () => {
    // Handle drop
    translateX.value = withSpring(0)
    translateY.value = withSpring(0)
  }
})

<PanGestureHandler onGestureEvent={gestureHandler}>
  <Animated.View style={animatedStyle}>
    <ChessPiece />
  </Animated.View>
</PanGestureHandler>
```

## Installation Commands

### Required React Native Dependencies
```bash
# Core React Native libraries
npm install @react-native-async-storage/async-storage
npm install react-native-sound
npm install lucide-react-native
npx expo install expo-linear-gradient

# For advanced touch handling
npm install react-native-gesture-handler
npm install react-native-reanimated

# For navigation
npm install @react-navigation/native
npm install @react-navigation/bottom-tabs
npm install react-native-screens
npm install react-native-safe-area-context
```

### Component Directory Setup
```bash
# From React Native project root
mkdir -p src/components/layout
mkdir -p src/components/chess
mkdir -p src/components/features
mkdir -p src/components/modals

# Copy components from web version
cp -r ../chessboard-vanilla-v2/src/components/layout/* src/components/layout/
cp -r ../chessboard-vanilla-v2/src/components/TestBoard.tsx src/components/chess/
cp -r ../chessboard-vanilla-v2/src/components/DraggedPiece.tsx src/components/chess/
cp -r ../chessboard-vanilla-v2/src/components/SettingsPanel.tsx src/components/features/
cp -r ../chessboard-vanilla-v2/src/components/ThemeSwitcher.tsx src/components/features/
cp -r ../chessboard-vanilla-v2/src/components/SlotMachine.tsx src/components/features/
```

## Component Priority Conversion List

### Phase 1: Layout Components
```bash
# Core layout foundation
src/components/layout/AppLayout.tsx     # Main app container
src/components/layout/Header.tsx        # Top navigation bar  
src/components/layout/TabBar.tsx        # Bottom tab navigation
src/components/layout/MainContent.tsx   # Content area wrapper
src/components/layout/BackgroundEffects.tsx # Animated backgrounds
```

### Phase 2: Chess Components  
```bash
# Chess game functionality
src/components/chess/TestBoard.tsx      # 3x3 interactive board
src/components/chess/DraggedPiece.tsx   # Drag & drop rendering
src/components/chess/CapturedPieces.tsx # Captured pieces display
```

### Phase 3: Feature Components
```bash
# Enhanced app features  
src/components/features/SettingsPanel.tsx   # Settings drawer
src/components/features/ThemeSwitcher.tsx   # Theme selection
src/components/features/SlotMachine.tsx     # Casino slot game
src/components/features/InstructionsFAB.tsx # Help floating button
```

### Phase 4: Modal Components
```bash
# Modal dialogs
src/components/modals/CheckmateModal.tsx     # Game end modal
src/components/modals/PromotionModal.tsx     # Piece promotion
src/components/modals/InstructionsModal.tsx  # Help modal
```

## Glassmorphism Effect Implementation

### CSS-Based (Web Version)
```css
.glass-layout {
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-gaming {
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### React Native Implementation
```typescript
import { LinearGradient } from 'expo-linear-gradient'
import { BlurView } from 'expo-blur'

// Method 1: Using LinearGradient
<LinearGradient
  colors={['rgba(255,255,255,0.1)', 'rgba(255,255,255,0.05)']}
  className="rounded-xl border border-white/10"
>
  {/* Content */}
</LinearGradient>

// Method 2: Using BlurView (iOS/Android)
<BlurView
  intensity={20}
  tint="dark"
  className="rounded-xl border border-white/10"
>
  {/* Content */}
</BlurView>
```

## Testing Commands

### Development Testing
```bash
# Test web platform
npm run dev
# Open http://localhost:8081 in browser

# Test iOS platform  
npm run ios

# Test Android platform
npm run android

# Clear cache if needed
npx expo start --clear
```

### Validation Checklist Per Component
```bash
# After each component conversion, verify:
- [ ] Component renders without errors
- [ ] Styling appears correct on web platform
- [ ] Touch interactions work on mobile
- [ ] No console warnings or errors
- [ ] Theme switching functions properly
- [ ] State management works correctly
- [ ] Icons display properly
- [ ] Animations are smooth
```

## File Structure After Migration

```
src/
├── components/
│   ├── layout/
│   │   ├── AppLayout.tsx       # Converted
│   │   ├── Header.tsx          # Converted  
│   │   ├── TabBar.tsx          # Converted
│   │   ├── MainContent.tsx     # Converted
│   │   └── BackgroundEffects.tsx # Converted
│   ├── chess/
│   │   ├── TestBoard.tsx       # Converted
│   │   ├── DraggedPiece.tsx    # Converted
│   │   └── CapturedPieces.tsx  # Converted
│   ├── features/
│   │   ├── SettingsPanel.tsx   # Converted
│   │   ├── ThemeSwitcher.tsx   # Converted  
│   │   ├── SlotMachine.tsx     # Converted
│   │   └── InstructionsFAB.tsx # Converted
│   └── modals/
│       ├── CheckmateModal.tsx  # Converted
│       ├── PromotionModal.tsx  # Converted
│       └── InstructionsModal.tsx # Converted
├── services/           # No changes needed
├── stores/            # No changes needed
├── hooks/             # No changes needed  
├── types/             # No changes needed
├── utils/             # Minor AsyncStorage updates
└── constants/         # No changes needed
```

## Common Conversion Patterns

### Button Conversion Pattern
```typescript
// Web
<button 
  onClick={handleClick}
  className="btn-primary"
  disabled={isLoading}
>
  {label}
</button>

// React Native  
<TouchableOpacity 
  onPress={handleClick}
  className="btn-primary"
  disabled={isLoading}
>
  <Text>{label}</Text>
</TouchableOpacity>
```

### List Conversion Pattern
```typescript
// Web
<div className="list-container">
  {items.map(item => (
    <div key={item.id} className="list-item">
      <span>{item.name}</span>
    </div>
  ))}
</div>

// React Native
<View className="list-container">
  {items.map(item => (
    <View key={item.id} className="list-item">
      <Text>{item.name}</Text>
    </View>
  ))}
</View>
```

### Input Conversion Pattern
```typescript
// Web
<input
  type="text"
  value={value}
  onChange={handleChange}
  className="input-field"
  placeholder="Enter text"
/>

// React Native
<TextInput
  value={value}
  onChangeText={handleChange}
  className="input-field" 
  placeholder="Enter text"
/>
```

This document provides all the specific code examples and commands needed to execute the migration strategy outlined in Document 35.