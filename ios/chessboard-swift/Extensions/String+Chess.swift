// String+Chess.swift - Chess-specific string extensions and utilities
import Foundation

extension String {
    
    var isValidFEN: Bool {
        return FENValidator.isValid(self)
    }
    
    var isValidMove: Bool {
        let movePattern = "^[a-h][1-8][a-h][1-8][qrnb]?$"
        return self.range(of: movePattern, options: .regularExpression) != nil
    }
    
    var isValidSquare: Bool {
        let squarePattern = "^[a-h][1-8]$"
        return self.range(of: squarePattern, options: .regularExpression) != nil
    }
    
    var squareToCoordinates: (file: Int, rank: Int)? {
        guard count == 2 else { return nil }
        
        let fileChar = self[startIndex]
        let rankChar = self[index(startIndex, offsetBy: 1)]
        
        guard let fileInt = fileChar.asciiValue,
              let rankInt = rankChar.wholeNumberValue,
              fileInt >= 97 && fileInt <= 104,
              rankInt >= 1 && rankInt <= 8 else {
            return nil
        }
        
        let file = Int(fileInt - 97)
        let rank = rankInt - 1
        
        return (file: file, rank: rank)
    }
    
    var moveComponents: (from: String, to: String, promotion: String?)? {
        guard count >= 4 else { return nil }
        
        let fromSquare = String(prefix(2))
        let toSquare = String(dropFirst(2).prefix(2))
        
        guard fromSquare.isValidSquare && toSquare.isValidSquare else {
            return nil
        }
        
        var promotion: String?
        if count == 5 {
            let promotionPiece = String(suffix(1))
            if ["q", "r", "n", "b"].contains(promotionPiece.lowercased()) {
                promotion = promotionPiece
            }
        }
        
        return (from: fromSquare, to: toSquare, promotion: promotion)
    }
    
    var fenComponents: (position: String, activeColor: String, castling: String, enPassant: String, halfmove: String, fullmove: String)? {
        let components = self.split(separator: " ")
        guard components.count == 6 else { return nil }
        
        return (
            position: String(components[0]),
            activeColor: String(components[1]),
            castling: String(components[2]),
            enPassant: String(components[3]),
            halfmove: String(components[4]),
            fullmove: String(components[5])
        )
    }
    
    var isValidPieceSymbol: Bool {
        let validPieces = "KQRBNPkqrbnp"
        return count == 1 && validPieces.contains(self)
    }
    
    var pieceColor: PieceColor? {
        guard isValidPieceSymbol else { return nil }
        return self == self.uppercased() ? .white : .black
    }
    
    var pieceType: PieceType? {
        guard isValidPieceSymbol else { return nil }
        
        switch self.lowercased() {
        case "k": return .king
        case "q": return .queen
        case "r": return .rook
        case "b": return .bishop
        case "n": return .knight
        case "p": return .pawn
        default: return nil
        }
    }
    
    func algebraicToUCI() -> String? {
        var normalized = self.trimmingCharacters(in: .whitespacesAndNewlines)
        
        if normalized.hasSuffix("+") || normalized.hasSuffix("#") {
            normalized = String(normalized.dropLast())
        }
        
        normalized = normalized.replacingOccurrences(of: "x", with: "")
        normalized = normalized.replacingOccurrences(of: "+", with: "")
        normalized = normalized.replacingOccurrences(of: "#", with: "")
        normalized = normalized.replacingOccurrences(of: "=", with: "")
        
        if normalized == "O-O" || normalized == "0-0" {
            return nil
        }
        
        if normalized == "O-O-O" || normalized == "0-0-0" {
            return nil
        }
        
        if normalized.count >= 4 && normalized.isValidMove {
            return normalized
        }
        
        return nil
    }
    
    func formatAsMove() -> String {
        guard let components = moveComponents else { return self }
        
        var formatted = "\(components.from)-\(components.to)"
        if let promotion = components.promotion {
            formatted += "=\(promotion.uppercased())"
        }
        return formatted
    }
    
    var isCheckmate: Bool {
        return hasSuffix("#")
    }
    
    var isCheck: Bool {
        return hasSuffix("+") && !isCheckmate
    }
    
    var isCapture: Bool {
        return contains("x")
    }
    
    var isCastling: Bool {
        let normalized = self.replacingOccurrences(of: " ", with: "")
        return normalized == "O-O" || normalized == "0-0" || normalized == "O-O-O" || normalized == "0-0-0"
    }
}

enum PieceColor: String, CaseIterable {
    case white = "w"
    case black = "b"
    
    var opposite: PieceColor {
        return self == .white ? .black : .white
    }
    
    var displayName: String {
        return rawValue == "w" ? "White" : "Black"
    }
}

enum PieceType: String, CaseIterable {
    case king = "k"
    case queen = "q" 
    case rook = "r"
    case bishop = "b"
    case knight = "n"
    case pawn = "p"
    
    var symbol: String {
        return rawValue
    }
    
    var displayName: String {
        return rawValue.capitalized
    }
    
    var unicodeSymbol: (white: String, black: String) {
        switch self {
        case .king: return ("♔", "♚")
        case .queen: return ("♕", "♛")
        case .rook: return ("♖", "♜")
        case .bishop: return ("♗", "♝")
        case .knight: return ("♘", "♞")
        case .pawn: return ("♙", "♟")
        }
    }
}