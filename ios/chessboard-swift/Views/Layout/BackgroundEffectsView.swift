// BackgroundEffectsView.swift - Gaming background effects matching React implementation
import SwiftUI

struct BackgroundEffectsView: View {
    @EnvironmentObject private var themeService: ThemeService
    @State private var mounted = false
    
    var body: some View {
        ZStack {
            if mounted {
                // Full-screen theme gradient background
                GamingGradientBackground()
                    .environmentObject(themeService)
                
                // Floating orbs - gaming style (matching React positions)
                FloatingOrbsExact()
                    .environmentObject(themeService)
                
                // Chess pieces (matching React positions and Unicode)
                ChessSymbolsExact()
                    .environmentObject(themeService)
                
                // Sparkle effects (matching React positions)
                SparkleEffectsExact()
                    .environmentObject(themeService)
            }
        }
        .onAppear {
            mounted = true
        }
    }
}

struct GamingGradientBackground: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        LinearGradient(
            gradient: Gradient(colors: [
                themeService.current.colors.primary.opacity(0.3),
                themeService.current.colors.secondary.opacity(0.25),
                themeService.current.colors.accent.opacity(0.2)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
    }
}

struct FloatingOrbsExact: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Orb 1 - top-20 left-20
                FloatingOrb(
                    colors: [themeService.current.colors.primary, themeService.current.colors.accent],
                    size: CGSize(width: 64, height: 64), // w-16 h-16, responsive to lg:w-32 lg:h-32
                    animation: .pulseGlow,
                    delay: 0.5
                )
                .position(x: 80, y: 80) // top-20 left-20
                
                // Orb 2 - top-40 right-32
                FloatingOrb(
                    colors: [themeService.current.colors.secondary, themeService.current.colors.muted],
                    size: CGSize(width: 48, height: 48), // w-12 h-12, responsive to lg:w-24 lg:h-24
                    animation: .hover,
                    delay: 1.0
                )
                .position(x: geometry.size.width - 128, y: 160) // top-40 right-32
                
                // Orb 3 - bottom-32 left-40
                FloatingOrb(
                    colors: [themeService.current.colors.primary, themeService.current.colors.accent],
                    size: CGSize(width: 40, height: 40), // w-10 h-10, responsive to lg:w-20 lg:h-20
                    animation: .float,
                    delay: 2.0
                )
                .position(x: 160, y: geometry.size.height - 128) // bottom-32 left-40
                
                // Orb 4 - bottom-20 right-20
                FloatingOrb(
                    colors: [themeService.current.colors.secondary, themeService.current.colors.muted],
                    size: CGSize(width: 56, height: 56), // w-14 h-14, responsive to lg:w-28 lg:h-28
                    animation: .drift,
                    delay: 0.0
                )
                .position(x: geometry.size.width - 80, y: geometry.size.height - 80) // bottom-20 right-20
                
                // Additional ambient orbs for depth
                FloatingOrb(
                    colors: [themeService.current.colors.primary, themeService.current.colors.accent],
                    size: CGSize(width: 32, height: 32), // w-8 h-8, responsive to lg:w-16 lg:h-16
                    animation: .hover,
                    delay: 1.5
                )
                .position(x: geometry.size.width / 6, y: geometry.size.height / 2) // top-1/2 left-1/6
                
                FloatingOrb(
                    colors: [themeService.current.colors.secondary, themeService.current.colors.muted],
                    size: CGSize(width: 24, height: 24), // w-6 h-6, responsive to lg:w-12 lg:h-12
                    animation: .drift,
                    delay: 0.8
                )
                .position(x: geometry.size.width * 5/6, y: geometry.size.height * 3/4) // top-3/4 right-1/6
            }
        }
    }
}

struct FloatingOrb: View {
    let colors: [Color]
    let size: CGSize
    let animation: OrbAnimation
    let delay: Double
    
    @State private var animationOffset: CGFloat = 0
    @State private var scale: CGFloat = 1.0
    @State private var opacity: Double = 0.2
    
    enum OrbAnimation {
        case pulseGlow, hover, float, drift
    }
    
    var body: some View {
        Circle()
            .fill(
                RadialGradient(
                    gradient: Gradient(colors: colors.map { $0.opacity(0.3) }),
                    center: .center,
                    startRadius: 0,
                    endRadius: size.width / 2
                )
            )
            .frame(width: size.width, height: size.height)
            .blur(radius: 3)
            .scaleEffect(scale)
            .opacity(opacity)
            .onAppear {
                startAnimation()
            }
    }
    
    private func startAnimation() {
        switch animation {
        case .pulseGlow:
            withAnimation(.easeInOut(duration: 4.0).repeatForever(autoreverses: true).delay(delay)) {
                scale = 1.05
                opacity = 0.8
            }
        case .hover:
            withAnimation(.easeInOut(duration: 3.0).repeatForever(autoreverses: true).delay(delay)) {
                scale = 1.05
                opacity = 0.6
            }
        case .float:
            withAnimation(.easeInOut(duration: 5.0).repeatForever(autoreverses: true).delay(delay)) {
                animationOffset = -30
                scale = 1.2
            }
        case .drift:
            withAnimation(.linear(duration: 8.0).repeatForever(autoreverses: false).delay(delay)) {
                animationOffset = 40
                scale = 1.02
            }
        }
    }
}

struct ChessSymbolsExact: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Chess pieces matching React positions exactly
                ChessPieceSymbol(
                    symbol: "♛",
                    fontSize: 80, // text-5xl lg:text-8xl
                    color: themeService.current.colors.foreground.opacity(0.15),
                    animationDelay: 0.1
                )
                .position(x: geometry.size.width / 4, y: geometry.size.height / 4) // top-1/4 left-1/4
                
                ChessPieceSymbol(
                    symbol: "♔",
                    fontSize: 64, // text-4xl lg:text-7xl
                    color: themeService.current.colors.primary.opacity(0.3),
                    animationDelay: 0.5
                )
                .position(x: geometry.size.width * 2/3, y: geometry.size.height / 3) // top-1/3 right-1/3
                
                ChessPieceSymbol(
                    symbol: "♝",
                    fontSize: 64, // text-4xl lg:text-7xl
                    color: themeService.current.colors.foreground.opacity(0.15),
                    animationDelay: 1.0
                )
                .position(x: geometry.size.width * 3/4, y: geometry.size.height * 3/4) // bottom-1/4 right-1/4
                
                ChessPieceSymbol(
                    symbol: "♞",
                    fontSize: 64, // text-4xl lg:text-7xl
                    color: themeService.current.colors.primary.opacity(0.2),
                    animationDelay: 1.5
                )
                .position(x: geometry.size.width / 3, y: geometry.size.height * 2/3) // bottom-1/3 left-1/3
                
                ChessPieceSymbol(
                    symbol: "♜",
                    fontSize: 64, // text-4xl lg:text-7xl
                    color: themeService.current.colors.foreground.opacity(0.15),
                    animationDelay: 2.0
                )
                .position(x: geometry.size.width / 5, y: geometry.size.height * 2/3) // top-2/3 left-1/5
                
                ChessPieceSymbol(
                    symbol: "♟",
                    fontSize: 48, // text-3xl lg:text-6xl
                    color: themeService.current.colors.primary.opacity(0.2),
                    animationDelay: 0.8
                )
                .position(x: geometry.size.width * 4/5, y: geometry.size.height / 3) // bottom-2/3 right-1/5
                
                // Additional pieces for richness
                ChessPieceSymbol(
                    symbol: "♕",
                    fontSize: 48, // text-3xl lg:text-6xl
                    color: themeService.current.colors.accent.opacity(0.2),
                    animationDelay: 0.3
                )
                .position(x: geometry.size.width * 4/5, y: geometry.size.height / 5) // top-1/5 right-1/5
                
                ChessPieceSymbol(
                    symbol: "♗",
                    fontSize: 48, // text-3xl lg:text-6xl
                    color: themeService.current.colors.accent.opacity(0.2),
                    animationDelay: 1.8
                )
                .position(x: geometry.size.width / 5, y: geometry.size.height * 4/5) // bottom-1/5 left-1/5
            }
        }
    }
}

struct ChessPieceSymbol: View {
    let symbol: String
    let fontSize: CGFloat
    let color: Color
    let animationDelay: Double
    
    @State private var yOffset: CGFloat = 0
    @State private var scale: CGFloat = 1.0
    
    var body: some View {
        Text(symbol)
            .font(.system(size: fontSize, weight: .light))
            .foregroundColor(color)
            .scaleEffect(scale)
            .offset(y: yOffset)
            .onAppear {
                withAnimation(.easeInOut(duration: 6.0).repeatForever(autoreverses: true).delay(animationDelay)) {
                    yOffset = -30
                    scale = 1.2
                }
            }
    }
}

struct SparkleEffectsExact: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Sparkles matching React positions exactly
                SparkleEffect(
                    color: themeService.current.colors.primary,
                    size: 8, // w-2 h-2
                    animationDelay: 0.1
                )
                .position(x: geometry.size.width * 3/4, y: geometry.size.height / 4) // top-1/4 right-1/4
                
                SparkleEffect(
                    color: themeService.current.colors.accent,
                    size: 6, // w-1.5 h-1.5
                    animationDelay: 0.5
                )
                .position(x: geometry.size.width / 3, y: geometry.size.height / 3) // top-1/3 left-1/3
                
                SparkleEffect(
                    color: themeService.current.colors.primary,
                    size: 8, // w-2 h-2
                    animationDelay: 1.0
                )
                .position(x: geometry.size.width / 4, y: geometry.size.height * 3/4) // bottom-1/4 left-1/4
                
                SparkleEffect(
                    color: themeService.current.colors.accent,
                    size: 6, // w-1.5 h-1.5
                    animationDelay: 0.2
                )
                .position(x: geometry.size.width * 2/3, y: geometry.size.height * 2/3) // bottom-1/3 right-1/3
                
                SparkleEffect(
                    color: themeService.current.colors.primary,
                    size: 4, // w-1 h-1
                    animationDelay: 2.0
                )
                .position(x: geometry.size.width * 4/5, y: geometry.size.height * 2/3) // top-2/3 right-1/5
                
                SparkleEffect(
                    color: themeService.current.colors.accent,
                    size: 4, // w-1 h-1
                    animationDelay: 1.5
                )
                .position(x: geometry.size.width / 5, y: geometry.size.height / 3) // bottom-2/3 left-1/5
            }
        }
    }
}

struct SparkleEffect: View {
    let color: Color
    let size: CGFloat
    let animationDelay: Double
    
    @State private var scale: CGFloat = 0.8
    @State private var opacity: Double = 0.2
    
    var body: some View {
        Circle()
            .fill(color.opacity(0.6))
            .frame(width: size, height: size)
            .scaleEffect(scale)
            .opacity(opacity)
            .onAppear {
                withAnimation(.easeInOut(duration: 3.0).repeatForever(autoreverses: true).delay(animationDelay)) {
                    scale = 1.2
                    opacity = 1.0
                }
            }
    }
}

#Preview {
    BackgroundEffectsView()
        .environmentObject(ThemeService())
}