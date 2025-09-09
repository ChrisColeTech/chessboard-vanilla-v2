// AppTypes.swift - Core application types
import Foundation

enum TabID: String, CaseIterable {
    case layout = "layout"
    case worker = "worker" 
    case drag = "drag"
    case slots = "slots"
    
    var displayName: String {
        switch self {
        case .layout: return "Layout"
        case .worker: return "Stockfish"
        case .drag: return "Drag Test"
        case .slots: return "Casino"
        }
    }
    
    var description: String {
        switch self {
        case .layout: return "Background Test"
        case .worker: return "Engine Testing"
        case .drag: return "Drag & Drop"
        case .slots: return "Slot Machine"
        }
    }
    
    var systemImage: String {
        switch self {
        case .layout: return "paintbrush.pointed.fill"
        case .worker: return "cpu.fill"
        case .drag: return "grid.circle.fill"
        case .slots: return "dice.fill"
        }
    }
}