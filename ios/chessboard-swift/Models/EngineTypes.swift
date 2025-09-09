// EngineTypes.swift - Core engine enums and status types
import Foundation

// MARK: - Engine Status Types

/// Represents the current state of the chess engine
enum EngineStatus: Equatable {
    case notStarted
    case starting
    case ready
    case analyzing
    case stopped
    case error(String)
    
    var displayName: String {
        switch self {
        case .notStarted:
            return "Not Started"
        case .starting:
            return "Starting..."
        case .ready:
            return "Ready"
        case .analyzing:
            return "Analyzing..."
        case .stopped:
            return "Stopped"
        case .error(let message):
            return "Error: \(message)"
        }
    }
    
    var isOperational: Bool {
        switch self {
        case .ready, .analyzing:
            return true
        default:
            return false
        }
    }
}

// MARK: - Analysis Configuration Types

/// Defines how deep or how long the engine should analyze
enum AnalysisDepth: Equatable {
    case depth(Int)              // Analyze to specific depth
    case time(TimeInterval)      // Analyze for specific time
    case infinite                // Analyze until stopped
    
    var description: String {
        switch self {
        case .depth(let depth):
            return "Depth \(depth)"
        case .time(let seconds):
            return "Time \(Int(seconds))s"
        case .infinite:
            return "Infinite"
        }
    }
}

// MARK: - Engine Errors

/// Errors that can occur during engine operations
enum ChessEngineError: Error, LocalizedError {
    case engineNotReady
    case invalidPosition
    case analysisTimeout
    case communicationFailure
    case packageNotFound
    
    var errorDescription: String? {
        switch self {
        case .engineNotReady:
            return "Engine is not ready for analysis"
        case .invalidPosition:
            return "Invalid chess position provided"
        case .analysisTimeout:
            return "Analysis timed out"
        case .communicationFailure:
            return "Failed to communicate with engine"
        case .packageNotFound:
            return "ChessKitEngine package not found"
        }
    }
}