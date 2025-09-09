// AppLayoutView.swift - Main application layout
import SwiftUI

struct AppLayoutView: View {
    @StateObject private var appViewModel = AppViewModel()
    @StateObject private var themeService = ThemeService()
    
    var body: some View {
        // React structure: relative min-h-screen bg-background text-foreground
        GeometryReader { geometry in
            let isLandscape = geometry.size.width > geometry.size.height
            let headerHeight: CGFloat = isLandscape ? 50 : 64
            let tabBarHeight: CGFloat = isLandscape ? 60 : 84
            
            ZStack {
                // Background effects layer - absolute inset-0
                BackgroundEffectsView()
                    .environmentObject(themeService)
                    .ignoresSafeArea()
                
                // Fixed header - fixed top-0 left-0 right-0 z-20
                VStack(spacing: 0) {
                    HeaderView()
                        .environmentObject(appViewModel)
                        .environmentObject(themeService)
                        .frame(height: headerHeight)
                    
                    Spacer()
                    
                    // Fixed TabBar - fixed bottom-0 left-0 right-0 z-20
                    TabBarView(
                        currentTab: appViewModel.selectedTab,
                        onTabChange: { tab in
                            appViewModel.setSelectedTab(tab)
                        }
                    )
                    .environmentObject(themeService)
                    .frame(height: tabBarHeight)
                }
                
                // Main Content Area - absolute top-16 bottom-[84px] left-0 right-0 z-10
                VStack(spacing: 0) {
                    Spacer().frame(height: headerHeight) // dynamic offset
                    
                    // Primary Content - w-full h-full overflow-auto
                    ScrollView {
                        VStack(spacing: 0) {
                            // Container mx-auto px-6 py-8
                            Group {
                                switch appViewModel.selectedTab {
                                case .layout:
                                    LayoutTestPageView()
                                case .worker:
                                    WorkerTestPageView()
                                case .drag:
                                    DragTestPageView()
                                case .slots:
                                    SlotMachinePageView()
                                }
                            }
                            .padding(.horizontal, 24) // px-6
                            .padding(.vertical, 32) // py-8
                        }
                    }
                    
                    Spacer().frame(height: tabBarHeight) // dynamic bottom offset
                }
                
                // Instructions FAB - positioned within main content area
                VStack {
                    Spacer()
                    HStack {
                        Spacer()
                        InstructionsFABView {
                            appViewModel.showInstructions()
                        }
                        .environmentObject(themeService)
                        .padding(.trailing, 24)
                        .padding(.bottom, tabBarHeight + 16) // Above TabBar with margin
                    }
                }
                
                // Settings Panel Overlay System - within main content area only
                if appViewModel.isSettingsPanelOpen {
                    // Backdrop overlay covering only main content area
                    VStack(spacing: 0) {
                        Spacer().frame(height: 64) // Don't overlap header
                        
                        Color.black.opacity(0.4)
                            .onTapGesture {
                                appViewModel.closeSettingsPanel()
                            }
                        
                        Spacer().frame(height: tabBarHeight) // Don't overlap TabBar
                    }
                    .zIndex(20)
                    
                    // Settings Panel - slides from right, 65% width
                    VStack(spacing: 0) {
                        Spacer().frame(height: headerHeight) // Don't overlap header
                        
                        HStack(spacing: 0) {
                            Spacer()
                            
                            SettingsPanelView()
                                .environmentObject(themeService)
                                .environmentObject(appViewModel)
                                .frame(width: geometry.size.width * 0.65) // 65% of screen width
                        }
                        
                        Spacer().frame(height: tabBarHeight) // Don't overlap TabBar
                    }
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .trailing).combined(with: .opacity)
                    ))
                    .zIndex(30)
                }
                
                // Global Instructions Modal
                if appViewModel.showingInstructions {
                    InstructionsModalView(
                        isVisible: appViewModel.showingInstructions,
                        title: appViewModel.instructionsTitle,
                        instructions: appViewModel.instructions,
                        onDismiss: appViewModel.hideInstructions
                    )
                    .environmentObject(themeService)
                    .environmentObject(appViewModel)
                }
            }
            .animation(.easeInOut(duration: 0.3), value: isLandscape)
        }
        .preferredColorScheme(themeService.isDarkMode ? .dark : .light)
        .environmentObject(appViewModel)
        .environmentObject(themeService)
        .animation(.spring(response: 0.4, dampingFraction: 0.8, blendDuration: 0), value: appViewModel.isSettingsPanelOpen)
        .animation(.easeInOut(duration: 0.2), value: appViewModel.showingInstructions)
    }
}

#Preview {
    AppLayoutView()
}