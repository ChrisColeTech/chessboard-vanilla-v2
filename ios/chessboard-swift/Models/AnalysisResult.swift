// AnalysisResult.swift - Chess engine analysis result data structures
import Foundation

struct AnalysisResult: Equatable, Identifiable {
    let id = UUID()
    let position: ChessPosition
    let bestMove: String?
    let evaluation: EvaluationScore
    let depth: Int
    let principalVariation: [String]
    let analysisTime: TimeInterval
    let nodesSearched: Int
    
    var hasValidMove: Bool {
        return bestMove != nil && !(bestMove?.isEmpty ?? true)
    }
    
    var formattedTime: String {
        return String(format: "%.1fs", analysisTime)
    }
    
    var formattedNodes: String {
        if nodesSearched < 1000 {
            return "\(nodesSearched)"
        } else if nodesSearched < 1_000_000 {
            return String(format: "%.1fk", Double(nodesSearched) / 1000)
        } else {
            return String(format: "%.1fM", Double(nodesSearched) / 1_000_000)
        }
    }
    
    var principalVariationText: String {
        return principalVariation.prefix(5).joined(separator: " ")
    }
}

struct EvaluationScore: Equatable {
    enum ScoreType: Equatable {
        case centipawns(Int)
        case mate(Int)
        case unknown
    }
    
    let type: ScoreType
    let perspective: PlayerPerspective
    
    enum PlayerPerspective: Equatable {
        case white
        case black
    }
    
    var displayText: String {
        switch type {
        case .centipawns(let cp):
            let score = perspective == .white ? cp : -cp
            return String(format: "%+.2f", Double(score) / 100.0)
        case .mate(let moves):
            let adjustedMoves = perspective == .white ? moves : -moves
            return "M\(adjustedMoves)"
        case .unknown:
            return "?"
        }
    }
    
    var isSignificantAdvantage: Bool {
        switch type {
        case .centipawns(let cp):
            return abs(cp) > 200
        case .mate(_):
            return true
        case .unknown:
            return false
        }
    }
    
    var advantageDescription: String {
        switch type {
        case .centipawns(let cp):
            let absScore = abs(cp)
            let winner = (perspective == .white ? cp > 0 : cp < 0) ? "White" : "Black"
            
            if absScore < 50 {
                return "Equal position"
            } else if absScore < 150 {
                return "\(winner) slightly better"
            } else if absScore < 300 {
                return "\(winner) better"
            } else {
                return "\(winner) winning"
            }
        case .mate(let moves):
            let winner = (perspective == .white ? moves > 0 : moves < 0) ? "White" : "Black"
            return "\(winner) mates in \(abs(moves))"
        case .unknown:
            return "Unknown evaluation"
        }
    }
    
    static let equal = EvaluationScore(type: .centipawns(0), perspective: .white)
}

struct EngineVariation: Equatable, Identifiable {
    let id = UUID()
    let moves: [String]
    let evaluation: EvaluationScore
    let depth: Int
    
    var moveSequence: String {
        return moves.prefix(5).joined(separator: " ")
    }
}