// LaunchCoordinator.swift - Manages app launch flow
import SwiftUI

struct LaunchCoordinator: View {
    @State private var isLaunchComplete = false
    @State private var showMainApp = false
    
    var body: some View {
        ZStack {
            // Main app (hidden initially)
            if showMainApp {
                AppLayoutView()
                    .transition(.opacity.combined(with: .scale(scale: 1.05)))
            }
            
            // Launch screen overlay
            if !isLaunchComplete {
                LaunchScreenView()
                    .transition(.opacity)
                    .zIndex(1)
            }
        }
        .onAppear {
            startLaunchSequence()
        }
        .animation(.easeInOut(duration: 0.8), value: isLaunchComplete)
        .animation(.easeInOut(duration: 0.8), value: showMainApp)
    }
    
    private func startLaunchSequence() {
        // Show launch screen for 2.5 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.5) {
            // Start loading main app
            showMainApp = true
            
            // Slight delay then hide launch screen
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                isLaunchComplete = true
            }
        }
    }
}

#Preview {
    LaunchCoordinator()
}