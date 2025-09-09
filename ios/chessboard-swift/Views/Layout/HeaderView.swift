// HeaderView.swift - Top navigation header
import SwiftUI

struct HeaderView: View {
    @EnvironmentObject private var appViewModel: AppViewModel
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        HStack(spacing: 0) {
            // Logo and title section
            HStack(spacing: 16) {
                // Crown logo with theme colors
                ZStack {
                    Circle()
                        .fill(themeService.current.colors.primary.opacity(0.12))
                        .frame(width: 44, height: 44)
                    
                    Circle()
                        .stroke(themeService.current.colors.primary.opacity(0.25), lineWidth: 1.5)
                        .frame(width: 44, height: 44)
                    
                    Image(systemName: "crown.fill")
                        .font(.system(size: 20, weight: .bold))
                        .foregroundColor(themeService.current.colors.primary)
                }
                
                // Title
                Text("Chess Training")
                    .font(.system(size: 16, weight: .semibold, design: .rounded))
                    .foregroundColor(themeService.current.colors.foreground)
                    .lineLimit(1)
            }
            
            Spacer(minLength: 20)
            
            // Right side controls
            HStack(spacing: 16) {
                // Coin balance display
                CoinBalanceView(balance: appViewModel.coinBalance)
                
                // Theme/Settings button - hide when settings panel is open
                if !appViewModel.isSettingsPanelOpen {
                    ThemeSwitcherButtonView {
                        appViewModel.toggleSettingsPanel()
                    }
                    .transition(.opacity.combined(with: .scale))
                }
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 14)
        .background(
            ZStack {
                BlurView(style: .systemUltraThinMaterial, alpha: 0.85)
                    .ignoresSafeArea(.all, edges: .top)
                themeService.current.colors.background.opacity(0.05)
                    .ignoresSafeArea(.all, edges: .top)
            }
        )
    }
}

struct CoinBalanceView: View {
    let balance: Int
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "circle.fill")
                .font(.system(size: 12, weight: .medium))
                .foregroundColor(Color.yellow.opacity(0.9))
            
            Text(balance.formatted())
                .font(.system(size: 16, weight: .bold, design: .rounded))
                .foregroundColor(themeService.current.colors.foreground)
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
        .background(
            RoundedRectangle(cornerRadius: 10)
                .fill(.thinMaterial)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(.white.opacity(0.2), lineWidth: 1)
                )
        )
    }
}

struct ThemeSwitcherButtonView: View {
    let action: () -> Void
    @EnvironmentObject private var themeService: ThemeService
    @State private var isPressed = false
    
    var body: some View {
        Button(action: action) {
            Image(systemName: "gearshape.fill")
                .font(.system(size: 18, weight: .medium))
                .foregroundColor(themeService.current.colors.primary)
                .scaleEffect(isPressed ? 0.95 : 1.0)
                .animation(.easeInOut(duration: 0.1), value: isPressed)
        }
        .frame(width: 44, height: 44)
        .background(
            Circle()
                .fill(.thinMaterial)
                .overlay(
                    Circle()
                        .stroke(.white.opacity(0.2), lineWidth: 1)
                )
        )
        .scaleEffect(isPressed ? 0.98 : 1.0)
        .animation(.easeInOut(duration: 0.1), value: isPressed)
        .onTapGesture {
            isPressed = true
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                isPressed = false
            }
            action()
        }
    }
}

#Preview {
    HeaderView()
        .environmentObject(AppViewModel())
        .environmentObject(ThemeService())
}