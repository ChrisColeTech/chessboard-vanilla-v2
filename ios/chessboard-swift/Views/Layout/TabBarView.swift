// TabBarView.swift - Bottom tab navigation matching React implementation
import SwiftUI

struct TabBarView: View {
    let currentTab: TabID
    let onTabChange: (TabID) -> Void
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        // React: w-full h-[84px] glass-layout border-t border-border/20 shadow-gaming
        HStack(spacing: 0) {
            ForEach(TabConfig.allTabs, id: \.id) { tab in
                TabBarButton(
                    tab: tab,
                    isActive: currentTab == tab.id,
                    onTap: { onTabChange(tab.id) }
                )
                .environmentObject(themeService)
            }
        }
        .frame(height: 84)
        .background(
            ZStack {
                BlurView(style: .systemUltraThinMaterial, alpha: 0.85)
                    .ignoresSafeArea(.all, edges: .bottom)
                themeService.current.colors.background.opacity(0.05)
                    .ignoresSafeArea(.all, edges: .bottom)
            }
        )
        .overlay(
            Rectangle()
                .fill(.white.opacity(0.1))
                .frame(height: 1),
            alignment: .top
        )
        .shadow(
            color: Color.black.opacity(0.15),
            radius: 8,
            x: 0,
            y: -4
        )
    }
}

struct TabBarButton: View {
    let tab: TabConfig
    let isActive: Bool
    let onTap: () -> Void
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        Button(action: onTap) {
            VStack(spacing: 4) {
                // Icon
                Image(systemName: tab.iconName)
                    .font(.system(size: 24, weight: .medium))
                    .foregroundColor(iconColor)
                    .scaleEffect(isActive ? 1.1 : 1.0)
                
                // Label
                Text(tab.label)
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(textColor)
                
                // Active description
                if isActive {
                    Text(tab.description)
                        .font(.system(size: 10, weight: .regular))
                        .foregroundColor(themeService.current.colors.mutedForeground.opacity(0.7))
                        .lineLimit(1)
                }
            }
            .padding(.vertical, 8)
        }
        .frame(maxWidth: .infinity)
        .background(backgroundOverlay)
        .scaleEffect(isActive ? 1.0 : 0.95)
        .offset(y: isActive ? -4 : 0)
        .overlay(
            Rectangle()
                .fill(isActive ? themeService.current.colors.primary : Color.clear)
                .frame(height: 4),
            alignment: .top
        )
        .animation(.easeInOut(duration: 0.3), value: isActive)
    }
    
    private var iconColor: Color {
        if isActive {
            return themeService.current.colors.primary
        } else {
            return themeService.current.colors.mutedForeground
        }
    }
    
    private var textColor: Color {
        if isActive {
            return themeService.current.colors.foreground
        } else {
            return themeService.current.colors.mutedForeground
        }
    }
    
    private var backgroundOverlay: some View {
        Group {
            if isActive {
                themeService.current.colors.foreground.opacity(0.1)
            } else {
                Color.clear
            }
        }
    }
}

struct TabConfig: Identifiable {
    let id: TabID
    let label: String
    let iconName: String
    let description: String
    
    static let allTabs: [TabConfig] = [
        TabConfig(
            id: .layout,
            label: "Layout",
            iconName: "paintbrush.pointed.fill",
            description: "Background Test"
        ),
        TabConfig(
            id: .worker,
            label: "Stockfish",
            iconName: "cpu.fill",
            description: "Engine Testing"
        ),
        TabConfig(
            id: .drag,
            label: "Drag Test",
            iconName: "target",
            description: "Drag & Drop"
        ),
        TabConfig(
            id: .slots,
            label: "Casino",
            iconName: "bitcoinsign.circle.fill",
            description: "Slot Machine"
        )
    ]
}

#Preview {
    VStack {
        Spacer()
        
        TabBarView(
            currentTab: .layout,
            onTabChange: { _ in }
        )
        .environmentObject(ThemeService())
    }
    .background(Color.gray)
}