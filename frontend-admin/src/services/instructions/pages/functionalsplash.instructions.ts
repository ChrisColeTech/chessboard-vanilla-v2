export const functionalSplashInstructions = {
  title: "Functional Splash Screen",
  instructions: [
    "🎯 **Real Asset Preloading**: This splash screen performs actual app initialization, not fake animations",
    "📊 **Live Progress Tracking**: Progress bar shows real loading stages (0-25% store, 25-65% pieces, 65-85% audio, 85-100% background)",
    "🎨 **User-Preference-Driven**: Loads your selected piece set first, then other sets in background",
    "🔊 **Smart Audio Loading**: Only preloads audio files if audio is enabled in settings",
    "⚡ **Modern React APIs**: Uses 2024 React preload API + custom Promise coordination",
    "🚫 **Error Handling**: Shows retry options and graceful degradation on loading failures",
    "⏭️ **Skip Option**: Power users can bypass loading for immediate app access",
    "📱 **Network Aware**: Adapts to connection speed with timeout handling",
    "🎮 **Test Actions**: Use action sheet to test loading states and navigation",
    "🔄 **Auto-Restart**: Changes to piece set or theme automatically trigger re-initialization"
  ]
}