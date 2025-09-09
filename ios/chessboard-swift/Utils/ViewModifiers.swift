// ViewModifiers.swift - Reusable styling system
import SwiftUI

// MARK: - Glassmorphism Modifiers

struct GlassLayoutModifier: ViewModifier {
    @EnvironmentObject var themeService: ThemeService
    
    func body(content: Content) -> some View {
        content
            .background(
                ZStack {
                    // Custom semitransparent blur
                    BlurView(style: .systemUltraThinMaterial, alpha: 0.8)
                    
                    // Slight tint to match theme
                    themeService.current.colors.background
                        .opacity(0.1)
                }
            )
            .shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 2)
    }
}

struct CardGamingModifier: ViewModifier {
    @EnvironmentObject var themeService: ThemeService
    
    func body(content: Content) -> some View {
        content
            .background(
                ZStack {
                    BlurView(style: .systemUltraThinMaterial, alpha: 0.85)
                    themeService.current.colors.background.opacity(0.05)
                }
            )
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(.white.opacity(0.2), lineWidth: 1)
            )
            .shadow(
                color: themeService.current.colors.primary.opacity(0.15),
                radius: 12,
                x: 0,
                y: 6
            )
    }
}

// MARK: - Button Styles

struct GamingButtonStyle: ButtonStyle {
    let variant: ButtonVariant
    @EnvironmentObject var themeService: ThemeService
    
    enum ButtonVariant {
        case primary, secondary, destructive, muted
        
        func colors(theme: any ChessTheme) -> (background: Color, foreground: Color, border: Color) {
            switch self {
            case .primary:
                return (theme.colors.primary, theme.colors.foreground, theme.colors.primary)
            case .secondary:
                return (theme.colors.secondary, theme.colors.foreground, theme.colors.secondary)
            case .destructive:
                return (theme.colors.destructive, theme.colors.destructiveForeground, theme.colors.destructive)
            case .muted:
                return (theme.colors.muted, theme.colors.mutedForeground, theme.colors.border)
            }
        }
    }
    
    func makeBody(configuration: Configuration) -> some View {
        let colors = variant.colors(theme: themeService.current)
        
        configuration.label
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
            .background(colors.background.opacity(configuration.isPressed ? 0.8 : 1.0))
            .foregroundColor(colors.foreground)
            .clipShape(RoundedRectangle(cornerRadius: 8))
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(colors.border.opacity(0.5), lineWidth: 1)
            )
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}

// MARK: - View Extensions

extension View {
    func glassLayout() -> some View {
        self.modifier(GlassLayoutModifier())
    }
    
    func cardGaming() -> some View {
        self.modifier(CardGamingModifier())
    }
    
    func gamingButton(_ variant: GamingButtonStyle.ButtonVariant = .primary) -> some View {
        self.buttonStyle(GamingButtonStyle(variant: variant))
    }
    
    func primaryButton() -> some View {
        self.gamingButton(.primary)
    }
    
    func secondaryButton() -> some View {
        self.gamingButton(.secondary)
    }
    
    func destructiveButton() -> some View {
        self.gamingButton(.destructive)
    }
    
    func mutedButton() -> some View {
        self.gamingButton(.muted)
    }
}