// ThemeTypes.swift - Theme system definitions
import SwiftUI

enum ThemeID: String, CaseIterable, Codable, Hashable {
    case light = "light"
    case dark = "dark"
    case cyberNeon = "cyber-neon"
    case cyberNeonLight = "cyber-neon-light"
    case dragonGold = "dragon-gold"
    case dragonGoldLight = "dragon-gold-light"
    case shadowKnight = "shadow-knight"
    case shadowKnightLight = "shadow-knight-light"
    case forestMystique = "forest-mystique"
    case forestMystiqueLight = "forest-mystique-light"
    case royalPurple = "royal-purple"
    case royalPurpleLight = "royal-purple-light"
    
    var isLight: Bool {
        rawValue.contains("light") || self == .light
    }
    
    var baseTheme: BaseThemeID {
        if rawValue.contains("cyber-neon") { return .cyberNeon }
        if rawValue.contains("dragon-gold") { return .dragonGold }
        if rawValue.contains("shadow-knight") { return .shadowKnight }
        if rawValue.contains("forest-mystique") { return .forestMystique }
        if rawValue.contains("royal-purple") { return .royalPurple }
        return .default
    }
}

enum BaseThemeID: String, CaseIterable, Codable {
    case `default` = "default"
    case cyberNeon = "cyber-neon"
    case dragonGold = "dragon-gold"
    case shadowKnight = "shadow-knight"
    case forestMystique = "forest-mystique"
    case royalPurple = "royal-purple"
}

struct ChessThemeColors {
    let background: Color
    let foreground: Color
    let primary: Color
    let primaryForeground: Color
    let secondary: Color
    let secondaryForeground: Color
    let accent: Color
    let accentForeground: Color
    let muted: Color
    let mutedForeground: Color
    let border: Color
    let card: Color
    let cardForeground: Color
    let destructive: Color
    let destructiveForeground: Color
    
    // Gaming-specific colors
    let gamingGradient: LinearGradient
    let floatingParticlePrimary: Color
    let floatingParticleSecondary: Color
    let sparkle: Color
    
    static let defaultDark = ChessThemeColors(
        background: Color(red: 0.06, green: 0.09, blue: 0.16), // #0f172a
        foreground: Color(red: 0.97, green: 0.98, blue: 0.99), // #f8fafc
        primary: Color(red: 0.39, green: 0.46, blue: 0.55), // #64748b
        primaryForeground: Color(red: 0.97, green: 0.98, blue: 0.99), // #f8fafc
        secondary: Color(red: 0.58, green: 0.64, blue: 0.72), // #94a3b8
        secondaryForeground: Color(red: 0.06, green: 0.09, blue: 0.16), // #0f172a
        accent: Color(red: 0.28, green: 0.33, blue: 0.41), // #475569
        accentForeground: Color(red: 0.97, green: 0.98, blue: 0.99), // #f8fafc
        muted: Color(red: 0.20, green: 0.26, blue: 0.33), // #334155
        mutedForeground: Color(red: 0.58, green: 0.64, blue: 0.72), // #94a3b8
        border: Color(red: 0.20, green: 0.26, blue: 0.33), // #334155
        card: Color(red: 0.12, green: 0.16, blue: 0.23), // #1e293b
        cardForeground: Color(red: 0.97, green: 0.98, blue: 0.99), // #f8fafc
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 0.97, green: 0.98, blue: 0.99), // #f8fafc
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.06, green: 0.09, blue: 0.16),
                Color(red: 0.12, green: 0.16, blue: 0.23)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.39, green: 0.46, blue: 0.55).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.28, green: 0.33, blue: 0.41).opacity(0.4),
        sparkle: Color(red: 0.39, green: 0.46, blue: 0.55)
    )
    
    static let defaultLight = ChessThemeColors(
        background: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        foreground: Color(red: 0.06, green: 0.09, blue: 0.16), // #0f172a
        primary: Color(red: 0.20, green: 0.26, blue: 0.33), // #334155
        primaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        secondary: Color(red: 0.39, green: 0.46, blue: 0.55), // #64748b
        secondaryForeground: Color(red: 0.97, green: 0.98, blue: 0.99), // #f8fafc
        accent: Color(red: 0.28, green: 0.33, blue: 0.41), // #475569
        accentForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        muted: Color(red: 0.95, green: 0.96, blue: 0.98), // #f1f5f9
        mutedForeground: Color(red: 0.39, green: 0.46, blue: 0.55), // #64748b
        border: Color(red: 0.89, green: 0.91, blue: 0.94), // #e2e8f0
        card: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        cardForeground: Color(red: 0.06, green: 0.09, blue: 0.16), // #0f172a
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 1.0, green: 1.0, blue: 1.0),
                Color(red: 0.95, green: 0.96, blue: 0.98)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.20, green: 0.26, blue: 0.33).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.28, green: 0.33, blue: 0.41).opacity(0.4),
        sparkle: Color(red: 0.20, green: 0.26, blue: 0.33)
    )
    
    // MARK: - Cyber Neon Themes
    
    static let cyberNeonDark = ChessThemeColors(
        background: Color(red: 0.04, green: 0.04, blue: 0.04), // #0a0a0a
        foreground: Color(red: 1.0, green: 0.0, blue: 0.5), // #ff0080
        primary: Color(red: 1.0, green: 0.0, blue: 0.5), // #ff0080
        primaryForeground: Color(red: 0.0, green: 0.0, blue: 0.0), // #000000
        secondary: Color(red: 0.0, green: 1.0, blue: 0.25), // #00ff41
        secondaryForeground: Color(red: 0.0, green: 0.0, blue: 0.0), // #000000
        accent: Color(red: 0.0, green: 0.75, blue: 1.0), // #00bfff
        accentForeground: Color(red: 0.0, green: 0.0, blue: 0.0), // #000000
        muted: Color(red: 0.16, green: 0.10, blue: 0.16), // #2a1a2a
        mutedForeground: Color(red: 1.0, green: 0.0, blue: 0.5), // #ff0080
        border: Color(red: 1.0, green: 0.0, blue: 0.5), // #ff0080
        card: Color(red: 0.10, green: 0.04, blue: 0.10), // #1a0a1a
        cardForeground: Color(red: 1.0, green: 0.0, blue: 0.5), // #ff0080
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.04, green: 0.04, blue: 0.04),
                Color(red: 0.10, green: 0.04, blue: 0.10)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 1.0, green: 0.0, blue: 0.5).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.0, green: 1.0, blue: 0.25).opacity(0.4),
        sparkle: Color(red: 0.0, green: 0.75, blue: 1.0)
    )
    
    static let cyberNeonLight = ChessThemeColors(
        background: Color(red: 0.97, green: 0.94, blue: 1.0), // #f8f0ff
        foreground: Color(red: 0.5, green: 0.0, blue: 0.25), // #800040
        primary: Color(red: 0.75, green: 0.0, blue: 0.5), // #c0007f
        primaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        secondary: Color(red: 0.0, green: 0.70, blue: 0.25), // #00b341
        secondaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        accent: Color(red: 0.0, green: 0.50, blue: 0.80), // #0080cc
        accentForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        muted: Color(red: 0.90, green: 0.80, blue: 1.0), // #e6ccff
        mutedForeground: Color(red: 0.38, green: 0.0, blue: 0.19), // #600030
        border: Color(red: 0.75, green: 0.0, blue: 0.5), // #c0007f
        card: Color(red: 0.94, green: 0.90, blue: 1.0), // #f0e6ff
        cardForeground: Color(red: 0.5, green: 0.0, blue: 0.25), // #800040
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.97, green: 0.94, blue: 1.0),
                Color(red: 0.94, green: 0.90, blue: 1.0)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.75, green: 0.0, blue: 0.5).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.0, green: 0.70, blue: 0.25).opacity(0.4),
        sparkle: Color(red: 0.0, green: 0.50, blue: 0.80)
    )
    
    // MARK: - Dragon Gold Themes
    
    static let dragonGoldDark = ChessThemeColors(
        background: Color(red: 0.10, green: 0.06, blue: 0.04), // #1a0f0a
        foreground: Color(red: 1.0, green: 0.96, blue: 0.90), // #fff4e6
        primary: Color(red: 1.0, green: 0.84, blue: 0.0), // #ffd700
        primaryForeground: Color(red: 0.0, green: 0.0, blue: 0.0), // #000000
        secondary: Color(red: 0.86, green: 0.15, blue: 0.15), // #dc2626
        secondaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        accent: Color(red: 0.96, green: 0.62, blue: 0.04), // #f59e0b
        accentForeground: Color(red: 0.0, green: 0.0, blue: 0.0), // #000000
        muted: Color(red: 0.29, green: 0.17, blue: 0.10), // #4a2c1a
        mutedForeground: Color(red: 0.85, green: 0.47, blue: 0.02), // #d97706
        border: Color(red: 0.86, green: 0.15, blue: 0.15), // #dc2626
        card: Color(red: 0.18, green: 0.10, blue: 0.06), // #2d1a0f
        cardForeground: Color(red: 1.0, green: 0.96, blue: 0.90), // #fff4e6
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.10, green: 0.06, blue: 0.04),
                Color(red: 0.18, green: 0.10, blue: 0.06)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 1.0, green: 0.84, blue: 0.0).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.86, green: 0.15, blue: 0.15).opacity(0.4),
        sparkle: Color(red: 0.96, green: 0.62, blue: 0.04)
    )
    
    static let dragonGoldLight = ChessThemeColors(
        background: Color(red: 1.0, green: 0.97, blue: 0.94), // #fff8f0
        foreground: Color(red: 0.49, green: 0.18, blue: 0.07), // #7c2d12
        primary: Color(red: 0.85, green: 0.47, blue: 0.02), // #d97706
        primaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        secondary: Color(red: 0.73, green: 0.11, blue: 0.11), // #b91c1c
        secondaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        accent: Color(red: 0.96, green: 0.62, blue: 0.04), // #f59e0b
        accentForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        muted: Color(red: 1.0, green: 0.84, blue: 0.67), // #fed7aa
        mutedForeground: Color(red: 0.49, green: 0.18, blue: 0.07), // #7c2d12
        border: Color(red: 0.73, green: 0.11, blue: 0.11), // #b91c1c
        card: Color(red: 1.0, green: 0.95, blue: 0.89), // #fef3e2
        cardForeground: Color(red: 0.49, green: 0.18, blue: 0.07), // #7c2d12
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 1.0, green: 0.97, blue: 0.94),
                Color(red: 1.0, green: 0.95, blue: 0.89)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.85, green: 0.47, blue: 0.02).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.73, green: 0.11, blue: 0.11).opacity(0.4),
        sparkle: Color(red: 0.96, green: 0.62, blue: 0.04)
    )
    
    // MARK: - Shadow Knight Themes
    
    static let shadowKnightDark = ChessThemeColors(
        background: Color(red: 0.0, green: 0.0, blue: 0.0), // #000000
        foreground: Color(red: 0.75, green: 0.75, blue: 0.75), // #c0c0c0
        primary: Color(red: 0.28, green: 0.51, blue: 0.71), // #4682b4
        primaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        secondary: Color(red: 0.18, green: 0.31, blue: 0.31), // #2f4f4f
        secondaryForeground: Color(red: 0.75, green: 0.75, blue: 0.75), // #c0c0c0
        accent: Color(red: 0.44, green: 0.50, blue: 0.56), // #708090
        accentForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        muted: Color(red: 0.11, green: 0.11, blue: 0.11), // #1c1c1c
        mutedForeground: Color(red: 0.47, green: 0.53, blue: 0.60), // #778899
        border: Color(red: 0.28, green: 0.51, blue: 0.71), // #4682b4
        card: Color(red: 0.06, green: 0.08, blue: 0.10), // #0f1419
        cardForeground: Color(red: 0.75, green: 0.75, blue: 0.75), // #c0c0c0
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.0, green: 0.0, blue: 0.0),
                Color(red: 0.06, green: 0.08, blue: 0.10)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.28, green: 0.51, blue: 0.71).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.18, green: 0.31, blue: 0.31).opacity(0.4),
        sparkle: Color(red: 0.44, green: 0.50, blue: 0.56)
    )
    
    static let shadowKnightLight = ChessThemeColors(
        background: Color(red: 0.94, green: 0.97, blue: 1.0), // #f0f8ff
        foreground: Color(red: 0.18, green: 0.31, blue: 0.31), // #2f4f4f
        primary: Color(red: 0.28, green: 0.51, blue: 0.71), // #4682b4
        primaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        secondary: Color(red: 0.44, green: 0.50, blue: 0.56), // #708090
        secondaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        accent: Color(red: 0.53, green: 0.81, blue: 0.92), // #87ceeb
        accentForeground: Color(red: 0.18, green: 0.31, blue: 0.31), // #2f4f4f
        muted: Color(red: 0.87, green: 0.93, blue: 1.0), // #ddeeff
        mutedForeground: Color(red: 0.18, green: 0.31, blue: 0.31), // #2f4f4f
        border: Color(red: 0.28, green: 0.51, blue: 0.71), // #4682b4
        card: Color(red: 0.90, green: 0.95, blue: 1.0), // #e6f3ff
        cardForeground: Color(red: 0.18, green: 0.31, blue: 0.31), // #2f4f4f
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.94, green: 0.97, blue: 1.0),
                Color(red: 0.90, green: 0.95, blue: 1.0)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.28, green: 0.51, blue: 0.71).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.44, green: 0.50, blue: 0.56).opacity(0.4),
        sparkle: Color(red: 0.53, green: 0.81, blue: 0.92)
    )
    
    // MARK: - Forest Mystique Themes
    
    static let forestMystiqueDark = ChessThemeColors(
        background: Color(red: 0.06, green: 0.10, blue: 0.06), // #0f1a0f
        foreground: Color(red: 0.96, green: 0.98, blue: 0.96), // #f5fbf5
        primary: Color(red: 0.20, green: 0.82, blue: 0.35), // #34d058
        primaryForeground: Color(red: 0.06, green: 0.10, blue: 0.06), // #0f1a0f
        secondary: Color(red: 0.10, green: 0.20, blue: 0.10), // #1a331a
        secondaryForeground: Color(red: 0.96, green: 0.98, blue: 0.96), // #f5fbf5
        accent: Color(red: 0.13, green: 0.77, blue: 0.37), // #22c55e
        accentForeground: Color(red: 0.06, green: 0.10, blue: 0.06), // #0f1a0f
        muted: Color(red: 0.18, green: 0.29, blue: 0.18), // #2d4a2d
        mutedForeground: Color(red: 0.58, green: 0.64, blue: 0.58), // #94a394
        border: Color(red: 0.29, green: 0.40, blue: 0.25), // #4a6741
        card: Color(red: 0.10, green: 0.20, blue: 0.10), // #1a331a
        cardForeground: Color(red: 0.96, green: 0.98, blue: 0.96), // #f5fbf5
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.06, green: 0.10, blue: 0.06),
                Color(red: 0.10, green: 0.20, blue: 0.10)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.20, green: 0.82, blue: 0.35).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.13, green: 0.77, blue: 0.37).opacity(0.4),
        sparkle: Color(red: 0.29, green: 0.40, blue: 0.25)
    )
    
    static let forestMystiqueLight = ChessThemeColors(
        background: Color(red: 0.96, green: 0.98, blue: 0.96), // #f5fbf5
        foreground: Color(red: 0.06, green: 0.10, blue: 0.06), // #0f1a0f
        primary: Color(red: 0.08, green: 0.50, blue: 0.24), // #15803d
        primaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        secondary: Color(red: 0.06, green: 0.10, blue: 0.06), // #0f1a0f
        secondaryForeground: Color(red: 0.96, green: 0.98, blue: 0.96), // #f5fbf5
        accent: Color(red: 0.09, green: 0.64, blue: 0.29), // #16a34a
        accentForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        muted: Color(red: 0.80, green: 0.84, blue: 0.80), // #cbd5cb
        mutedForeground: Color(red: 0.28, green: 0.33, blue: 0.28), // #475547
        border: Color(red: 0.58, green: 0.64, blue: 0.58), // #94a394
        card: Color(red: 0.94, green: 0.97, blue: 0.94), // #f0f8f0
        cardForeground: Color(red: 0.06, green: 0.10, blue: 0.06), // #0f1a0f
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.96, green: 0.98, blue: 0.96),
                Color(red: 0.94, green: 0.97, blue: 0.94)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.08, green: 0.50, blue: 0.24).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.09, green: 0.64, blue: 0.29).opacity(0.4),
        sparkle: Color(red: 0.58, green: 0.64, blue: 0.58)
    )
    
    // MARK: - Royal Purple Themes
    
    static let royalPurpleDark = ChessThemeColors(
        background: Color(red: 0.10, green: 0.06, blue: 0.10), // #1a0f1a
        foreground: Color(red: 0.98, green: 0.96, blue: 0.98), // #fbf5fb
        primary: Color(red: 0.66, green: 0.33, blue: 0.97), // #a855f7
        primaryForeground: Color(red: 0.10, green: 0.06, blue: 0.10), // #1a0f1a
        secondary: Color(red: 0.16, green: 0.10, blue: 0.20), // #2a1a33
        secondaryForeground: Color(red: 0.98, green: 0.96, blue: 0.98), // #fbf5fb
        accent: Color(red: 0.75, green: 0.52, blue: 0.99), // #c084fc
        accentForeground: Color(red: 0.10, green: 0.06, blue: 0.10), // #1a0f1a
        muted: Color(red: 0.24, green: 0.18, blue: 0.29), // #3d2d4a
        mutedForeground: Color(red: 0.64, green: 0.58, blue: 0.64), // #a394a3
        border: Color(red: 0.35, green: 0.25, blue: 0.40), // #5a4167
        card: Color(red: 0.16, green: 0.10, blue: 0.20), // #2a1a33
        cardForeground: Color(red: 0.98, green: 0.96, blue: 0.98), // #fbf5fb
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.10, green: 0.06, blue: 0.10),
                Color(red: 0.16, green: 0.10, blue: 0.20)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.66, green: 0.33, blue: 0.97).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.75, green: 0.52, blue: 0.99).opacity(0.4),
        sparkle: Color(red: 0.35, green: 0.25, blue: 0.40)
    )
    
    static let royalPurpleLight = ChessThemeColors(
        background: Color(red: 0.98, green: 0.96, blue: 0.98), // #fbf5fb
        foreground: Color(red: 0.10, green: 0.06, blue: 0.10), // #1a0f1a
        primary: Color(red: 0.49, green: 0.23, blue: 0.93), // #7c3aed
        primaryForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        secondary: Color(red: 0.10, green: 0.06, blue: 0.10), // #1a0f1a
        secondaryForeground: Color(red: 0.98, green: 0.96, blue: 0.98), // #fbf5fb
        accent: Color(red: 0.55, green: 0.36, blue: 0.96), // #8b5cf6
        accentForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        muted: Color(red: 0.84, green: 0.80, blue: 0.84), // #d5cbd5
        mutedForeground: Color(red: 0.33, green: 0.28, blue: 0.33), // #554755
        border: Color(red: 0.64, green: 0.58, blue: 0.64), // #a394a3
        card: Color(red: 0.96, green: 0.94, blue: 0.97), // #f5f0f8
        cardForeground: Color(red: 0.10, green: 0.06, blue: 0.10), // #1a0f1a
        destructive: Color(red: 0.94, green: 0.27, blue: 0.27), // #ef4444
        destructiveForeground: Color(red: 1.0, green: 1.0, blue: 1.0), // #ffffff
        gamingGradient: LinearGradient(
            gradient: Gradient(colors: [
                Color(red: 0.98, green: 0.96, blue: 0.98),
                Color(red: 0.96, green: 0.94, blue: 0.97)
            ]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        ),
        floatingParticlePrimary: Color(red: 0.49, green: 0.23, blue: 0.93).opacity(0.6),
        floatingParticleSecondary: Color(red: 0.55, green: 0.36, blue: 0.96).opacity(0.4),
        sparkle: Color(red: 0.64, green: 0.58, blue: 0.64)
    )
}

protocol ChessTheme {
    var id: ThemeID { get }
    var name: String { get }
    var description: String { get }
    var isDark: Bool { get }
    var colors: ChessThemeColors { get }
    var icon: String { get }
}

struct DefaultDarkTheme: ChessTheme {
    let id: ThemeID = .dark
    let name = "Dark"
    let description = "Pure dark elegance"
    let isDark = true
    let colors = ChessThemeColors.defaultDark
    let icon = "moon.fill"
}

struct DefaultLightTheme: ChessTheme {
    let id: ThemeID = .light
    let name = "Light"
    let description = "Clean light elegance"
    let isDark = false
    let colors = ChessThemeColors.defaultLight
    let icon = "sun.max.fill"
}

// MARK: - Cyber Neon Themes

struct CyberNeonDarkTheme: ChessTheme {
    let id: ThemeID = .cyberNeon
    let name = "Cyber Neon"
    let description = "Electric neon glow"
    let isDark = true
    let colors = ChessThemeColors.cyberNeonDark
    let icon = "bolt.fill"
}

struct CyberNeonLightTheme: ChessTheme {
    let id: ThemeID = .cyberNeonLight
    let name = "Cyber Light"
    let description = "Bright neon colors"
    let isDark = false
    let colors = ChessThemeColors.cyberNeonLight
    let icon = "bolt.fill"
}

// MARK: - Dragon Gold Themes

struct DragonGoldDarkTheme: ChessTheme {
    let id: ThemeID = .dragonGold
    let name = "Dragon Gold"
    let description = "Medieval dragon theme"
    let isDark = true
    let colors = ChessThemeColors.dragonGoldDark
    let icon = "crown.fill"
}

struct DragonGoldLightTheme: ChessTheme {
    let id: ThemeID = .dragonGoldLight
    let name = "Gold Light"
    let description = "Light dragon theme"
    let isDark = false
    let colors = ChessThemeColors.dragonGoldLight
    let icon = "crown.fill"
}

// MARK: - Shadow Knight Themes

struct ShadowKnightDarkTheme: ChessTheme {
    let id: ThemeID = .shadowKnight
    let name = "Shadow Knight"
    let description = "Dark steel armor"
    let isDark = true
    let colors = ChessThemeColors.shadowKnightDark
    let icon = "shield.fill"
}

struct ShadowKnightLightTheme: ChessTheme {
    let id: ThemeID = .shadowKnightLight
    let name = "Knight Light"
    let description = "Polished steel"
    let isDark = false
    let colors = ChessThemeColors.shadowKnightLight
    let icon = "shield.fill"
}

// MARK: - Forest Mystique Themes

struct ForestMystiqueDarkTheme: ChessTheme {
    let id: ThemeID = .forestMystique
    let name = "Forest Mystique"
    let description = "Mystic forest theme"
    let isDark = true
    let colors = ChessThemeColors.forestMystiqueDark
    let icon = "tree.fill"
}

struct ForestMystiqueLightTheme: ChessTheme {
    let id: ThemeID = .forestMystiqueLight
    let name = "Forest Light"
    let description = "Light forest theme"
    let isDark = false
    let colors = ChessThemeColors.forestMystiqueLight
    let icon = "tree.fill"
}

// MARK: - Royal Purple Themes

struct RoyalPurpleDarkTheme: ChessTheme {
    let id: ThemeID = .royalPurple
    let name = "Royal Purple"
    let description = "Majestic purple theme"
    let isDark = true
    let colors = ChessThemeColors.royalPurpleDark
    let icon = "gem.fill"
}

struct RoyalPurpleLightTheme: ChessTheme {
    let id: ThemeID = .royalPurpleLight
    let name = "Purple Light"
    let description = "Lavender royalty"
    let isDark = false
    let colors = ChessThemeColors.royalPurpleLight
    let icon = "gem.fill"
}