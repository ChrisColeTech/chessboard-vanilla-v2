// ChessPosition.swift - Represents chess position state and utilities
import Foundation
import ChessKitEngine

struct ChessPosition: Equatable, Hashable {
    let fen: String
    let moveCount: Int
    let isWhiteTurn: Bool
    
    init(fen: String = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") {
        self.fen = fen
        
        let components = fen.split(separator: " ")
        self.isWhiteTurn = components.count > 1 ? components[1] == "w" : true
        self.moveCount = components.count > 5 ? Int(String(components[5])) ?? 1 : 1
    }
    
    init(fen: String, moveCount: Int, isWhiteTurn: Bool) {
        self.fen = fen
        self.moveCount = moveCount
        self.isWhiteTurn = isWhiteTurn
    }
    
    static let startingPosition = ChessPosition()
    
    var isStartingPosition: Bool {
        return fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    }
    
    func afterMove(_ move: String) -> ChessPosition? {
        guard !move.isEmpty else { return nil }
        
        let newMoveCount = isWhiteTurn ? moveCount : moveCount + 1
        let newIsWhiteTurn = !isWhiteTurn
        
        return ChessPosition(
            fen: fen,
            moveCount: newMoveCount,
            isWhiteTurn: newIsWhiteTurn
        )
    }
    
    var displayText: String {
        let turn = isWhiteTurn ? "White" : "Black"
        return "Move \(moveCount) - \(turn) to play"
    }
}

extension ChessPosition {
    var isValid: Bool {
        return FENValidator.isValid(fen)
    }
    
    var boardPosition: String {
        return fen.split(separator: " ").first.map(String.init) ?? ""
    }
    
    var castlingRights: String {
        let components = fen.split(separator: " ")
        return components.count > 2 ? String(components[2]) : "-"
    }
    
    var enPassantTarget: String {
        let components = fen.split(separator: " ")
        return components.count > 3 ? String(components[3]) : "-"
    }
}