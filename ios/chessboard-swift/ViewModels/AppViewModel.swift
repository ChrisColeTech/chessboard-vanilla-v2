// AppViewModel.swift - Main app state coordination
import SwiftUI

@MainActor
class AppViewModel: ObservableObject {
    // Navigation state
    @Published var selectedTab: TabID = .layout
    @Published var isSettingsPanelOpen: Bool = false
    
    // Instructions state
    @Published var showingInstructions: Bool = false
    @Published var instructionsTitle: String = ""
    @Published var instructions: [String] = []
    
    // Game state
    @Published var coinBalance: Int = 350
    
    // Drag state (for global drag overlay)
    @Published var isDragging: Bool = false
    
    // Instructions service (simple class, not StateObject)
    private let instructionsService = InstructionsService()
    
    // MARK: - Navigation Actions
    
    func setSelectedTab(_ tab: TabID) {
        selectedTab = tab
    }
    
    func toggleSettingsPanel() {
        isSettingsPanelOpen.toggle()
    }
    
    func openSettingsPanel() {
        isSettingsPanelOpen = true
    }
    
    func closeSettingsPanel() {
        isSettingsPanelOpen = false
    }
    
    // MARK: - Instructions Actions
    
    func showInstructions() {
        let tabKey = tabToKey(selectedTab)
        instructionsService.setInstructions(for: tabKey)
        instructionsTitle = instructionsService.currentTitle
        instructions = instructionsService.currentInstructions
        showingInstructions = true
    }
    
    func hideInstructions() {
        showingInstructions = false
    }
    
    private func tabToKey(_ tab: TabID) -> String {
        switch tab {
        case .layout: return "layout"
        case .worker: return "worker"  
        case .drag: return "drag"
        case .slots: return "slots"
        }
    }
    
    // MARK: - Game Actions
    
    func updateCoinBalance(_ newBalance: Int) {
        coinBalance = max(0, newBalance)
    }
}