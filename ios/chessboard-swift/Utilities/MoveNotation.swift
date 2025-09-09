// MoveNotation.swift - Handle chess move notation conversions and parsing
import Foundation

struct MoveNotation {
    
    // MARK: - Move Parsing
    
    static func parseMove(_ moveString: String) -> ParsedMove? {
        let normalized = moveString.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        guard !normalized.isEmpty else { return nil }
        
        // Try different move formats
        if let uciMove = parseUCIMove(normalized) {
            return uciMove
        }
        
        if let algebraicMove = parseAlgebraicMove(normalized) {
            return algebraicMove
        }
        
        if let coordinateMove = parseCoordinateMove(normalized) {
            return coordinateMove
        }
        
        return nil
    }
    
    static func formatMove(_ move: ParsedMove, format: MoveFormat = .uci) -> String {
        switch format {
        case .uci:
            return formatAsUCI(move)
        case .algebraic:
            return formatAsAlgebraic(move)
        case .coordinate:
            return formatAsCoordinate(move)
        case .descriptive:
            return formatAsDescriptive(move)
        }
    }
    
    static func parsePV(_ pvString: String) -> [String] {
        return pvString
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .split(separator: " ")
            .map { String($0).trimmingCharacters(in: .punctuationCharacters) }
            .filter { !$0.isEmpty && isValidMoveString($0) }
    }
    
    // MARK: - Data Structures
    
    struct ParsedMove: Equatable {
        let from: Square
        let to: Square
        let piece: PieceType?
        let promotion: PieceType?
        let isCapture: Bool
        let isCheck: Bool
        let isCheckmate: Bool
        let isCastling: CastlingType?
        let disambiguation: String?
        let originalNotation: String
        
        enum CastlingType: String, CaseIterable {
            case kingside = "O-O"
            case queenside = "O-O-O"
            
            var uciMove: (white: String, black: String) {
                switch self {
                case .kingside:
                    return ("e1g1", "e8g8")
                case .queenside:
                    return ("e1c1", "e8c8")
                }
            }
        }
        
        init(from: Square, to: Square, piece: PieceType? = nil, promotion: PieceType? = nil, isCapture: Bool = false, isCheck: Bool = false, isCheckmate: Bool = false, isCastling: CastlingType? = nil, disambiguation: String? = nil, originalNotation: String) {
            self.from = from
            self.to = to
            self.piece = piece
            self.promotion = promotion
            self.isCapture = isCapture
            self.isCheck = isCheck
            self.isCheckmate = isCheckmate
            self.isCastling = isCastling
            self.disambiguation = disambiguation
            self.originalNotation = originalNotation
        }
    }
    
    struct Square: Equatable, Hashable {
        let file: Int // 0-7 (a-h)
        let rank: Int // 0-7 (1-8)
        
        init(file: Int, rank: Int) {
            self.file = file
            self.rank = rank
        }
        
        init?(algebraic: String) {
            guard algebraic.count == 2 else { return nil }
            
            let fileChar = algebraic.first!
            let rankChar = algebraic.last!
            
            guard let fileIndex = "abcdefgh".firstIndex(of: fileChar),
                  let rankValue = rankChar.wholeNumberValue,
                  rankValue >= 1 && rankValue <= 8 else {
                return nil
            }
            
            self.file = fileIndex.utf16Offset(in: "abcdefgh")
            self.rank = rankValue - 1
        }
        
        var algebraic: String {
            let files = "abcdefgh"
            let fileChar = files[files.index(files.startIndex, offsetBy: file)]
            let rankNumber = rank + 1
            return "\(fileChar)\(rankNumber)"
        }
        
        var isValid: Bool {
            return file >= 0 && file <= 7 && rank >= 0 && rank <= 7
        }
    }
    
    enum MoveFormat {
        case uci           // e2e4
        case algebraic     // e4, Nf3, O-O
        case coordinate    // e2-e4
        case descriptive   // P-K4
    }
    
    // MARK: - UCI Move Parsing
    
    private static func parseUCIMove(_ moveString: String) -> ParsedMove? {
        // UCI format: e2e4, e7e8q (with promotion)
        guard moveString.count >= 4 && moveString.count <= 5 else { return nil }
        
        let fromSquare = String(moveString.prefix(2))
        let toSquare = String(moveString.dropFirst(2).prefix(2))
        
        guard let from = Square(algebraic: fromSquare),
              let to = Square(algebraic: toSquare) else {
            return nil
        }
        
        var promotion: PieceType?
        if moveString.count == 5 {
            let promotionChar = moveString.last!
            promotion = PieceType(rawValue: String(promotionChar))
        }
        
        return ParsedMove(
            from: from,
            to: to,
            promotion: promotion,
            originalNotation: moveString
        )
    }
    
    // MARK: - Algebraic Move Parsing
    
    private static func parseAlgebraicMove(_ moveString: String) -> ParsedMove? {
        var normalized = moveString
            .replacingOccurrences(of: "+", with: "")
            .replacingOccurrences(of: "#", with: "")
            .replacingOccurrences(of: "x", with: "")
        
        let isCheck = moveString.contains("+")
        let isCheckmate = moveString.contains("#")
        let isCapture = moveString.contains("x")
        
        // Handle castling
        if normalized == "o-o" || normalized == "0-0" {
            return ParsedMove(
                from: Square(file: 4, rank: 0), // Will be adjusted based on color
                to: Square(file: 6, rank: 0),
                isCastling: .kingside,
                isCheck: isCheck,
                isCheckmate: isCheckmate,
                originalNotation: moveString
            )
        }
        
        if normalized == "o-o-o" || normalized == "0-0-0" {
            return ParsedMove(
                from: Square(file: 4, rank: 0), // Will be adjusted based on color
                to: Square(file: 2, rank: 0),
                isCastling: .queenside,
                isCheck: isCheck,
                isCheckmate: isCheckmate,
                originalNotation: moveString
            )
        }
        
        // Handle promotion
        var promotion: PieceType?
        if normalized.contains("=") {
            let components = normalized.split(separator: "=")
            if components.count == 2, let promotionPiece = PieceType(rawValue: String(components[1])) {
                promotion = promotionPiece
                normalized = String(components[0])
            }
        }
        
        // Parse piece and destination
        let piece: PieceType?
        let destination: Square?
        var disambiguation: String?
        
        if normalized.count >= 2 {
            let lastTwoChars = String(normalized.suffix(2))
            if let square = Square(algebraic: lastTwoChars) {
                destination = square
                let remaining = String(normalized.dropLast(2))
                
                if remaining.isEmpty {
                    // Pawn move
                    piece = .pawn
                } else if remaining.count == 1 {
                    if let pieceType = PieceType(rawValue: remaining.uppercased()) {
                        piece = pieceType
                    } else {
                        // Disambiguation (file or rank)
                        piece = .pawn
                        disambiguation = remaining
                    }
                } else {
                    // Piece with disambiguation
                    let pieceChar = String(remaining.first!)
                    piece = PieceType(rawValue: pieceChar.uppercased())
                    disambiguation = String(remaining.dropFirst())
                }
            } else {
                return nil
            }
        } else {
            return nil
        }
        
        guard let dest = destination else { return nil }
        
        // For algebraic notation, we don't have the source square
        // This would need position context to determine
        let from = Square(file: 0, rank: 0) // Placeholder
        
        return ParsedMove(
            from: from,
            to: dest,
            piece: piece,
            promotion: promotion,
            isCapture: isCapture,
            isCheck: isCheck,
            isCheckmate: isCheckmate,
            disambiguation: disambiguation,
            originalNotation: moveString
        )
    }
    
    // MARK: - Coordinate Move Parsing
    
    private static func parseCoordinateMove(_ moveString: String) -> ParsedMove? {
        // Coordinate format: e2-e4, Ng1-f3
        let separators = ["-", "→", "—"]
        var components: [String] = []
        var usedSeparator = ""
        
        for separator in separators {
            if moveString.contains(separator) {
                components = moveString.split(separator: Character(separator)).map(String.init)
                usedSeparator = separator
                break
            }
        }
        
        guard components.count == 2 else { return nil }
        
        let fromPart = components[0].trimmingCharacters(in: .whitespacesAndNewlines)
        let toPart = components[1].trimmingCharacters(in: .whitespacesAndNewlines)
        
        // Extract piece from 'from' part if present
        var piece: PieceType?
        var fromSquareString = fromPart
        
        if fromPart.count > 2 {
            let firstChar = String(fromPart.first!)
            if let pieceType = PieceType(rawValue: firstChar.uppercased()) {
                piece = pieceType
                fromSquareString = String(fromPart.dropFirst())
            }
        }
        
        guard let from = Square(algebraic: fromSquareString),
              let to = Square(algebraic: toPart) else {
            return nil
        }
        
        return ParsedMove(
            from: from,
            to: to,
            piece: piece,
            originalNotation: moveString
        )
    }
    
    // MARK: - Move Formatting
    
    private static func formatAsUCI(_ move: ParsedMove) -> String {
        var result = "\(move.from.algebraic)\(move.to.algebraic)"
        
        if let promotion = move.promotion {
            result += promotion.rawValue.lowercased()
        }
        
        return result
    }
    
    private static func formatAsAlgebraic(_ move: ParsedMove) -> String {
        if let castling = move.isCastling {
            var result = castling.rawValue
            if move.isCheck { result += "+" }
            if move.isCheckmate { result += "#" }
            return result
        }
        
        var result = ""
        
        // Piece notation (skip for pawn moves to empty square)
        if let piece = move.piece, piece != .pawn || move.isCapture {
            result += piece == .pawn ? "" : piece.rawValue.uppercased()
        }
        
        // Disambiguation
        if let disambiguation = move.disambiguation {
            result += disambiguation
        }
        
        // Capture notation
        if move.isCapture {
            result += "x"
        }
        
        // Destination square
        result += move.to.algebraic
        
        // Promotion
        if let promotion = move.promotion {
            result += "=\(promotion.rawValue.uppercased())"
        }
        
        // Check/checkmate
        if move.isCheckmate {
            result += "#"
        } else if move.isCheck {
            result += "+"
        }
        
        return result
    }
    
    private static func formatAsCoordinate(_ move: ParsedMove) -> String {
        var result = ""
        
        if let piece = move.piece, piece != .pawn {
            result += piece.rawValue.uppercased()
        }
        
        result += "\(move.from.algebraic)-\(move.to.algebraic)"
        
        if let promotion = move.promotion {
            result += "=\(promotion.rawValue.uppercased())"
        }
        
        return result
    }
    
    private static func formatAsDescriptive(_ move: ParsedMove) -> String {
        // Simplified descriptive notation
        guard let piece = move.piece else { return move.originalNotation }
        
        let pieceSymbol = piece == .pawn ? "P" : piece.rawValue.uppercased()
        let destination = move.to.algebraic.uppercased()
        
        return move.isCapture ? "\(pieceSymbol)x\(destination)" : "\(pieceSymbol)-\(destination)"
    }
    
    // MARK: - Utility Methods
    
    private static func isValidMoveString(_ moveString: String) -> Bool {
        return parseMove(moveString) != nil
    }
    
    static func convertPVToAlgebraic(_ pvMoves: [String]) -> [String] {
        return pvMoves.compactMap { moveString in
            guard let parsed = parseMove(moveString) else { return nil }
            return formatMove(parsed, format: .algebraic)
        }
    }
    
    static func convertPVToCoordinate(_ pvMoves: [String]) -> [String] {
        return pvMoves.compactMap { moveString in
            guard let parsed = parseMove(moveString) else { return nil }
            return formatMove(parsed, format: .coordinate)
        }
    }
    
    static func extractMoveSequence(_ text: String) -> [String] {
        // Extract moves from text using regex
        let movePattern = #"([KQRBN]?[a-h]?[1-8]?[x]?[a-h][1-8][=]?[QRBN]?[+#]?|O-O-O|O-O)"#
        
        do {
            let regex = try NSRegularExpression(pattern: movePattern, options: [])
            let matches = regex.matches(in: text, options: [], range: NSRange(location: 0, length: text.count))
            
            return matches.compactMap { match in
                guard let range = Range(match.range, in: text) else { return nil }
                return String(text[range])
            }
        } catch {
            print("❌ Regex error in move extraction: \(error)")
            return []
        }
    }
    
    static func validateMoveSequence(_ moves: [String]) -> Bool {
        return moves.allSatisfy { isValidMoveString($0) }
    }
    
    // MARK: - Move Analysis
    
    static func analyzeMoveString(_ moveString: String) -> MoveAnalysis {
        guard let move = parseMove(moveString) else {
            return MoveAnalysis(isValid: false, format: .unknown, errors: ["Invalid move format"])
        }
        
        let format = detectMoveFormat(moveString)
        var characteristics: [String] = []
        var errors: [String] = []
        
        if move.isCapture {
            characteristics.append("capture")
        }
        
        if move.isCheck {
            characteristics.append("check")
        }
        
        if move.isCheckmate {
            characteristics.append("checkmate")
        }
        
        if move.isCastling != nil {
            characteristics.append("castling")
        }
        
        if move.promotion != nil {
            characteristics.append("promotion")
        }
        
        if !move.from.isValid || !move.to.isValid {
            errors.append("Invalid square coordinates")
        }
        
        return MoveAnalysis(
            isValid: errors.isEmpty,
            format: format,
            characteristics: characteristics,
            errors: errors
        )
    }
    
    private static func detectMoveFormat(_ moveString: String) -> MoveFormatType {
        let normalized = moveString.lowercased()
        
        if normalized.count >= 4 && normalized.count <= 5,
           normalized.prefix(2).allSatisfy({ "abcdefgh12345678".contains($0) }),
           normalized.dropFirst(2).prefix(2).allSatisfy({ "abcdefgh12345678".contains($0) }) {
            return .uci
        }
        
        if normalized.contains("-") || normalized.contains("→") {
            return .coordinate
        }
        
        if normalized.contains("o-o") || normalized.contains("0-0") {
            return .algebraic
        }
        
        if normalized.last?.isLetter == true || normalized.contains("x") || normalized.contains("+") || normalized.contains("#") {
            return .algebraic
        }
        
        return .unknown
    }
    
    struct MoveAnalysis {
        let isValid: Bool
        let format: MoveFormatType
        let characteristics: [String]
        let errors: [String]
        
        init(isValid: Bool, format: MoveFormatType, characteristics: [String] = [], errors: [String] = []) {
            self.isValid = isValid
            self.format = format
            self.characteristics = characteristics
            self.errors = errors
        }
    }
    
    enum MoveFormatType {
        case uci
        case algebraic
        case coordinate
        case descriptive
        case unknown
    }
}