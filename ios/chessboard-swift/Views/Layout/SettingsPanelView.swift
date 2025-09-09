// SettingsPanelView.swift - Theme and settings configuration panel
import SwiftUI

struct SettingsPanelView: View {
    @EnvironmentObject private var themeService: ThemeService
    @EnvironmentObject private var appViewModel: AppViewModel
    
    var body: some View {
        // Settings panel only - overlay is handled by parent
        VStack(alignment: .leading, spacing: 0) {
            // Header with close button
            SettingsPanelHeader()
                .environmentObject(themeService)
                .environmentObject(appViewModel)
            
            // Content
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    ThemeSelectionSection()
                        .environmentObject(themeService)
                }
                .padding(20)
            }
        }
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 0))
        .overlay(
            Rectangle()
                .fill(themeService.current.colors.border.opacity(0.2))
                .frame(width: 1),
            alignment: .leading
        )
    }
}

struct SettingsPanelHeader: View {
    @EnvironmentObject private var themeService: ThemeService
    @EnvironmentObject private var appViewModel: AppViewModel
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text("Settings")
                    .font(.system(size: 24, weight: .semibold, design: .rounded))
                    .foregroundColor(themeService.current.colors.foreground)
                
                Text("Theme & Preferences")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(themeService.current.colors.mutedForeground)
            }
            
            Spacer()
            
            Button(action: {
                withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
                    appViewModel.closeSettingsPanel()
                }
            }) {
                Image(systemName: "xmark")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundColor(themeService.current.colors.foreground)
            }
            .frame(width: 36, height: 36)
            .background(themeService.current.colors.card.opacity(0.8))
            .clipShape(Circle())
            .overlay(
                Circle()
                    .stroke(themeService.current.colors.border.opacity(0.3), lineWidth: 1)
            )
        }
        .padding(20)
        .background(themeService.current.colors.card.opacity(0.5))
        .overlay(
            Rectangle()
                .fill(themeService.current.colors.border.opacity(0.2))
                .frame(height: 1),
            alignment: .bottom
        )
    }
}

struct ThemeSelectionSection: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            // Light/Dark mode toggle
            HStack {
                Text("Dark Mode")
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(themeService.current.colors.foreground)
                
                Spacer()
                
                Toggle("", isOn: Binding(
                    get: { themeService.isDarkMode },
                    set: { _ in themeService.toggleMode() }
                ))
                .toggleStyle(SwitchToggleStyle(tint: themeService.current.colors.primary))
            }
            .padding(.vertical, 8)
            
            // Theme grid
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 16), count: 2), spacing: 16) {
                ForEach(themeService.getAvailableBaseThemes(), id: \.id) { baseTheme in
                    EnhancedThemePreviewCard(baseTheme: baseTheme)
                        .environmentObject(themeService)
                }
            }
        }
    }
}

struct EnhancedThemePreviewCard: View {
    let baseTheme: BaseThemeConfig
    @EnvironmentObject private var themeService: ThemeService
    @State private var isPressed = false
    
    var isSelected: Bool {
        themeService.selectedBaseTheme == baseTheme.id
    }
    
    var currentThemeColors: ChessThemeColors {
        baseTheme.theme(isDark: themeService.isDarkMode).colors
    }
    
    var body: some View {
        VStack(spacing: 12) {
            // Theme icon and colors
            VStack(spacing: 8) {
                Image(systemName: baseTheme.icon)
                    .font(.system(size: 20, weight: .semibold))
                    .foregroundColor(currentThemeColors.primary)
                    .scaleEffect(isSelected ? 1.1 : 1.0)
                    .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isSelected)
                
                // Color palette preview
                HStack(spacing: 6) {
                    Circle()
                        .fill(currentThemeColors.primary)
                        .frame(width: 14, height: 14)
                    Circle()
                        .fill(currentThemeColors.secondary)
                        .frame(width: 12, height: 12)
                    Circle()
                        .fill(currentThemeColors.accent)
                        .frame(width: 10, height: 10)
                }
            }
            
            VStack(spacing: 4) {
                Text(baseTheme.name)
                    .font(.system(size: 14, weight: .bold, design: .rounded))
                    .foregroundColor(themeService.current.colors.foreground)
                    .lineLimit(1)
                
                Text(baseTheme.description)
                    .font(.system(size: 11, weight: .medium))
                    .foregroundColor(themeService.current.colors.mutedForeground)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
            }
            
            // Selection indicator
            if isSelected {
                HStack(spacing: 4) {
                    Image(systemName: "checkmark.circle.fill")
                        .font(.system(size: 12, weight: .bold))
                        .foregroundColor(themeService.current.colors.primary)
                    
                    Text("ACTIVE")
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(themeService.current.colors.primary)
                }
                .transition(.scale.combined(with: .opacity))
            }
        }
        .padding(16)
        .frame(height: 120)
        .frame(maxWidth: .infinity)
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(isSelected ? 
                      currentThemeColors.card.opacity(0.8) : 
                      themeService.current.colors.card.opacity(0.4))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(
                            isSelected ? currentThemeColors.primary : themeService.current.colors.border.opacity(0.3),
                            lineWidth: isSelected ? 2.5 : 1
                        )
                )
        )
        .scaleEffect(isPressed ? 0.95 : 1.0)
        .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isPressed)
        .animation(.spring(response: 0.4, dampingFraction: 0.7), value: isSelected)
        .onTapGesture {
            withAnimation(.spring(response: 0.4, dampingFraction: 0.6)) {
                themeService.setBaseTheme(baseTheme.id)
            }
        }
        .onLongPressGesture(minimumDuration: 0) { pressing in
            withAnimation(.easeInOut(duration: 0.1)) {
                isPressed = pressing
            }
        } perform: {
            // Long press action handled by tap gesture
        }
    }
}

struct ThemePreviewCard: View {
    let baseTheme: BaseThemeConfig
    @EnvironmentObject private var themeService: ThemeService
    
    var isSelected: Bool {
        themeService.selectedBaseTheme == baseTheme.id
    }
    
    var body: some View {
        VStack(spacing: 8) {
            // Theme preview
            HStack(spacing: 4) {
                Circle()
                    .fill(baseTheme.theme(isDark: themeService.isDarkMode).colors.primary)
                    .frame(width: 16, height: 16)
                Circle()
                    .fill(baseTheme.theme(isDark: themeService.isDarkMode).colors.secondary)
                    .frame(width: 12, height: 12)
                Circle()
                    .fill(baseTheme.theme(isDark: themeService.isDarkMode).colors.accent)
                    .frame(width: 10, height: 10)
            }
            .padding(.top, 8)
            
            Text(baseTheme.name)
                .font(.system(size: 12, weight: .medium))
                .foregroundColor(themeService.current.colors.foreground)
            
            Text(baseTheme.description)
                .font(.system(size: 10))
                .foregroundColor(themeService.current.colors.mutedForeground)
                .multilineTextAlignment(.center)
                .lineLimit(2)
        }
        .frame(height: 80)
        .frame(maxWidth: .infinity)
        .background(isSelected ? themeService.current.colors.primary.opacity(0.1) : themeService.current.colors.card.opacity(0.5))
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(
                    isSelected ? themeService.current.colors.primary : themeService.current.colors.border.opacity(0.3),
                    lineWidth: isSelected ? 2 : 1
                )
        )
        .onTapGesture {
            themeService.setBaseTheme(baseTheme.id)
        }
    }
}

struct AppearanceSection: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Appearance")
                .font(.system(size: 18, weight: .semibold))
                .foregroundColor(themeService.current.colors.foreground)
            
            HStack {
                Text("Dark Mode")
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(themeService.current.colors.foreground)
                
                Spacer()
                
                Toggle("", isOn: Binding(
                    get: { themeService.isDarkMode },
                    set: { _ in themeService.toggleMode() }
                ))
                .toggleStyle(SwitchToggleStyle(tint: themeService.current.colors.primary))
            }
            .padding(.vertical, 8)
        }
    }
}

struct AboutSection: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("About")
                .font(.system(size: 18, weight: .semibold))
                .foregroundColor(themeService.current.colors.foreground)
            
            VStack(alignment: .leading, spacing: 8) {
                Text("Responsive Chessboard")
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(themeService.current.colors.foreground)
                
                Text("SwiftUI POC Implementation")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(themeService.current.colors.mutedForeground)
                
                Text("A proof-of-concept implementation showcasing responsive layout, theme management, and interactive components in SwiftUI.")
                    .font(.system(size: 12))
                    .foregroundColor(themeService.current.colors.mutedForeground)
                    .lineLimit(nil)
                    .multilineTextAlignment(.leading)
            }
            .padding(12)
            .background(themeService.current.colors.muted)
            .clipShape(RoundedRectangle(cornerRadius: 8))
        }
    }
}

#Preview {
    ZStack {
        Color.gray.ignoresSafeArea()
        
        SettingsPanelView()
            .environmentObject(ThemeService())
            .environmentObject(AppViewModel())
    }
}