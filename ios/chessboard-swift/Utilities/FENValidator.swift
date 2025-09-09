// FENValidator.swift - Validate and parse FEN chess position strings
import Foundation

class FENValidator {
    
    // Standard chess positions for reference
    static let standardPositions: [String: String] = [
        "starting": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "empty": "8/8/8/8/8/8/8/8 w - - 0 1",
        "endgame_kqk": "8/8/8/8/8/8/4K3/4k2Q w - - 0 1",
        "sicilian": "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
        "french": "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
        "caro_kann": "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
        "queens_gambit": "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 2",
        "kings_indian": "rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3"
    ]
    
    // MARK: - Main Validation
    
    static func isValid(_ fen: String) -> Bool {
        let trimmed = fen.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return false }
        
        let components = trimmed.split(separator: " ")
        guard components.count == 6 else { return false }
        
        let position = String(components[0])
        let activeColor = String(components[1])
        let castling = String(components[2])
        let enPassant = String(components[3])
        let halfmove = String(components[4])
        let fullmove = String(components[5])
        
        return validatePosition(position) &&
               validateActiveColor(activeColor) &&
               validateCastling(castling) &&
               validateEnPassant(enPassant) &&
               validateHalfmove(halfmove) &&
               validateFullmove(fullmove)
    }
    
    static func parsePosition(_ fen: String) -> ChessPosition? {
        guard isValid(fen) else { return nil }
        return ChessPosition(fen: fen)
    }
    
    // MARK: - Component Validation
    
    private static func validatePosition(_ position: String) -> Bool {
        let ranks = position.split(separator: "/")
        guard ranks.count == 8 else { return false }
        
        for rank in ranks {
            guard validateRank(String(rank)) else { return false }
        }
        
        return true
    }
    
    private static func validateRank(_ rank: String) -> Bool {
        var squareCount = 0
        
        for char in rank {
            if char.isWholeNumber {
                guard let digit = char.wholeNumberValue,
                      digit >= 1 && digit <= 8 else { return false }
                squareCount += digit
            } else {
                guard "KQRBNPkqrbnp".contains(char) else { return false }
                squareCount += 1
            }
        }
        
        return squareCount == 8
    }
    
    private static func validateActiveColor(_ activeColor: String) -> Bool {
        return activeColor == "w" || activeColor == "b"
    }
    
    private static func validateCastling(_ castling: String) -> Bool {
        if castling == "-" { return true }
        
        let validChars = Set("KQkq")
        let castlingSet = Set(castling)
        
        return !castlingSet.isEmpty && castlingSet.isSubset(of: validChars)
    }
    
    private static func validateEnPassant(_ enPassant: String) -> Bool {
        if enPassant == "-" { return true }
        
        guard enPassant.count == 2 else { return false }
        
        let fileChar = enPassant.first!
        let rankChar = enPassant.last!
        
        guard "abcdefgh".contains(fileChar) else { return false }
        guard rankChar == "3" || rankChar == "6" else { return false }
        
        return true
    }
    
    private static func validateHalfmove(_ halfmove: String) -> Bool {
        guard let value = Int(halfmove) else { return false }
        return value >= 0 && value <= 150 // Reasonable upper limit
    }
    
    private static func validateFullmove(_ fullmove: String) -> Bool {
        guard let value = Int(fullmove) else { return false }
        return value >= 1
    }
    
    // MARK: - Advanced Validation
    
    static func validateChessRules(_ fen: String) -> (isValid: Bool, errors: [ValidationError]) {
        var errors: [ValidationError] = []
        
        // Basic FEN validation first
        guard isValid(fen) else {
            errors.append(.invalidFENFormat)
            return (false, errors)
        }
        
        let components = fen.split(separator: " ")
        let position = String(components[0])
        let activeColor = String(components[1])
        let castling = String(components[2])
        let enPassant = String(components[3])
        
        // Parse the board
        guard let board = parseBoard(position) else {
            errors.append(.invalidBoardPosition)
            return (false, errors)
        }
        
        // Validate chess-specific rules
        validateKings(board, errors: &errors)
        validatePawns(board, errors: &errors)
        validateCastlingRights(board, castling, errors: &errors)
        validateEnPassantTarget(board, enPassant, activeColor, errors: &errors)
        
        return (errors.isEmpty, errors)
    }
    
    enum ValidationError: Error, LocalizedError {
        case invalidFENFormat
        case invalidBoardPosition
        case missingKing(PieceColor)
        case multipleKings(PieceColor)
        case pawnOnBackRank
        case invalidCastlingRights
        case invalidEnPassantTarget
        case impossiblePosition
        
        var errorDescription: String? {
            switch self {
            case .invalidFENFormat:
                return "Invalid FEN format"
            case .invalidBoardPosition:
                return "Invalid board position"
            case .missingKing(let color):
                return "Missing \(color.displayName.lowercased()) king"
            case .multipleKings(let color):
                return "Multiple \(color.displayName.lowercased()) kings"
            case .pawnOnBackRank:
                return "Pawn on back rank (impossible)"
            case .invalidCastlingRights:
                return "Invalid castling rights"
            case .invalidEnPassantTarget:
                return "Invalid en passant target"
            case .impossiblePosition:
                return "Position violates chess rules"
            }
        }
    }
    
    // MARK: - Board Parsing
    
    private static func parseBoard(_ position: String) -> [[Character?]]? {
        let ranks = position.split(separator: "/")
        guard ranks.count == 8 else { return nil }
        
        var board: [[Character?]] = Array(repeating: Array(repeating: nil, count: 8), count: 8)
        
        for (rankIndex, rank) in ranks.enumerated() {
            var fileIndex = 0
            
            for char in rank {
                guard fileIndex < 8 else { return nil }
                
                if char.isWholeNumber {
                    guard let digit = char.wholeNumberValue else { return nil }
                    fileIndex += digit
                } else {
                    board[rankIndex][fileIndex] = char
                    fileIndex += 1
                }
            }
            
            guard fileIndex == 8 else { return nil }
        }
        
        return board
    }
    
    // MARK: - Chess Rules Validation
    
    private static func validateKings(_ board: [[Character?]], errors: inout [ValidationError]) {
        var whiteKingCount = 0
        var blackKingCount = 0
        
        for rank in board {
            for square in rank {
                if let piece = square {
                    if piece == "K" { whiteKingCount += 1 }
                    if piece == "k" { blackKingCount += 1 }
                }
            }
        }
        
        if whiteKingCount == 0 {
            errors.append(.missingKing(.white))
        } else if whiteKingCount > 1 {
            errors.append(.multipleKings(.white))
        }
        
        if blackKingCount == 0 {
            errors.append(.missingKing(.black))
        } else if blackKingCount > 1 {
            errors.append(.multipleKings(.black))
        }
    }
    
    private static func validatePawns(_ board: [[Character?]], errors: inout [ValidationError]) {
        // Check first and last ranks for pawns
        for fileIndex in 0..<8 {
            if let piece = board[0][fileIndex], piece == "P" || piece == "p" {
                errors.append(.pawnOnBackRank)
            }
            if let piece = board[7][fileIndex], piece == "P" || piece == "p" {
                errors.append(.pawnOnBackRank)
            }
        }
    }
    
    private static func validateCastlingRights(_ board: [[Character?]], castling: String, errors: inout [ValidationError]) {
        guard castling != "-" else { return }
        
        // Check if kings and rooks are in correct positions for castling rights
        let whiteKingOnSquare = board[7][4] == "K"
        let blackKingOnSquare = board[0][4] == "k"
        
        if castling.contains("K") {
            if !whiteKingOnSquare || board[7][7] != "R" {
                errors.append(.invalidCastlingRights)
            }
        }
        
        if castling.contains("Q") {
            if !whiteKingOnSquare || board[7][0] != "R" {
                errors.append(.invalidCastlingRights)
            }
        }
        
        if castling.contains("k") {
            if !blackKingOnSquare || board[0][7] != "r" {
                errors.append(.invalidCastlingRights)
            }
        }
        
        if castling.contains("q") {
            if !blackKingOnSquare || board[0][0] != "r" {
                errors.append(.invalidCastlingRights)
            }
        }
    }
    
    private static func validateEnPassantTarget(_ board: [[Character?]], enPassant: String, activeColor: String, errors: inout [ValidationError]) {
        guard enPassant != "-" else { return }
        guard enPassant.count == 2 else {
            errors.append(.invalidEnPassantTarget)
            return
        }
        
        let file = enPassant.first!
        let rank = enPassant.last!
        
        guard let fileIndex = "abcdefgh".firstIndex(of: file)?.utf16Offset(in: "abcdefgh") else {
            errors.append(.invalidEnPassantTarget)
            return
        }
        
        // Validate en passant target makes sense
        if activeColor == "w" && rank == "6" {
            // White to move, check if black pawn could have moved two squares
            if board[3][fileIndex] != "p" {
                errors.append(.invalidEnPassantTarget)
            }
        } else if activeColor == "b" && rank == "3" {
            // Black to move, check if white pawn could have moved two squares
            if board[4][fileIndex] != "P" {
                errors.append(.invalidEnPassantTarget)
            }
        } else {
            errors.append(.invalidEnPassantTarget)
        }
    }
    
    // MARK: - Utility Methods
    
    static func standardPosition(named name: String) -> String? {
        return standardPositions[name]
    }
    
    static func randomValidPosition() -> String {
        let positions = Array(standardPositions.values)
        return positions.randomElement() ?? standardPositions["starting"]!
    }
    
    static func isStartingPosition(_ fen: String) -> Bool {
        return fen == standardPositions["starting"]
    }
    
    static func normalizePosition(_ fen: String) -> String {
        // Remove extra whitespace and ensure standard format
        let trimmed = fen.trimmingCharacters(in: .whitespacesAndNewlines)
        let components = trimmed.split(separator: " ").map(String.init)
        
        guard components.count == 6 else { return fen }
        
        return components.joined(separator: " ")
    }
    
    // MARK: - FEN Generation
    
    static func createFEN(position: String, activeColor: PieceColor, castling: String = "KQkq", enPassant: String = "-", halfmove: Int = 0, fullmove: Int = 1) -> String {
        let colorString = activeColor == .white ? "w" : "b"
        return "\(position) \(colorString) \(castling) \(enPassant) \(halfmove) \(fullmove)"
    }
    
    // MARK: - Position Analysis
    
    static func getPositionInfo(_ fen: String) -> PositionInfo? {
        guard isValid(fen) else { return nil }
        
        let components = fen.split(separator: " ")
        let position = String(components[0])
        
        guard let board = parseBoard(position) else { return nil }
        
        var pieceCounts: [Character: Int] = [:]
        var totalPieces = 0
        
        for rank in board {
            for square in rank {
                if let piece = square {
                    pieceCounts[piece, default: 0] += 1
                    totalPieces += 1
                }
            }
        }
        
        let activeColor = String(components[1]) == "w" ? PieceColor.white : PieceColor.black
        let castling = String(components[2])
        let enPassant = String(components[3])
        let halfmove = Int(String(components[4])) ?? 0
        let fullmove = Int(String(components[5])) ?? 1
        
        return PositionInfo(
            pieceCounts: pieceCounts,
            totalPieces: totalPieces,
            activeColor: activeColor,
            castlingRights: castling,
            enPassantTarget: enPassant,
            halfmoveClock: halfmove,
            fullmoveNumber: fullmove
        )
    }
    
    struct PositionInfo {
        let pieceCounts: [Character: Int]
        let totalPieces: Int
        let activeColor: PieceColor
        let castlingRights: String
        let enPassantTarget: String
        let halfmoveClock: Int
        let fullmoveNumber: Int
        
        var isEndgame: Bool {
            return totalPieces <= 12
        }
        
        var isOpening: Bool {
            return fullmoveNumber <= 15 && totalPieces >= 28
        }
        
        var isMiddlegame: Bool {
            return !isOpening && !isEndgame
        }
        
        var materialBalance: Int {
            let pieceValues: [Character: Int] = [
                "P": 1, "p": -1,
                "N": 3, "n": -3,
                "B": 3, "b": -3,
                "R": 5, "r": -5,
                "Q": 9, "q": -9
            ]
            
            return pieceCounts.reduce(0) { total, pair in
                total + (pieceValues[pair.key] ?? 0) * pair.value
            }
        }
    }
}