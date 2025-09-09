// UCICommand.swift - UCI protocol commands and responses
import Foundation

enum UCICommand: Equatable {
    case uci
    case debug(Bool)
    case isReady
    case setOption(name: String, value: String?)
    case uciNewGame
    case position(fen: String?, moves: [String])
    case go(parameters: GoParameters)
    case stop
    case ponderhit
    case quit
    
    var commandString: String {
        switch self {
        case .uci:
            return "uci"
        case .debug(let enabled):
            return "debug \(enabled ? "on" : "off")"
        case .isReady:
            return "isready"
        case .setOption(let name, let value):
            if let value = value {
                return "setoption name \(name) value \(value)"
            } else {
                return "setoption name \(name)"
            }
        case .uciNewGame:
            return "ucinewgame"
        case .position(let fen, let moves):
            var command = "position"
            if let fen = fen {
                command += " fen \(fen)"
            } else {
                command += " startpos"
            }
            if !moves.isEmpty {
                command += " moves \(moves.joined(separator: " "))"
            }
            return command
        case .go(let parameters):
            return "go \(parameters.commandString)"
        case .stop:
            return "stop"
        case .ponderhit:
            return "ponderhit"
        case .quit:
            return "quit"
        }
    }
}

struct GoParameters: Equatable {
    let searchMoves: [String]?
    let ponder: Bool
    let whiteTime: TimeInterval?
    let blackTime: TimeInterval?
    let whiteIncrement: TimeInterval?
    let blackIncrement: TimeInterval?
    let movesToGo: Int?
    let depth: Int?
    let nodes: Int?
    let mate: Int?
    let moveTime: TimeInterval?
    let infinite: Bool
    
    init(
        searchMoves: [String]? = nil,
        ponder: Bool = false,
        whiteTime: TimeInterval? = nil,
        blackTime: TimeInterval? = nil,
        whiteIncrement: TimeInterval? = nil,
        blackIncrement: TimeInterval? = nil,
        movesToGo: Int? = nil,
        depth: Int? = nil,
        nodes: Int? = nil,
        mate: Int? = nil,
        moveTime: TimeInterval? = nil,
        infinite: Bool = false
    ) {
        self.searchMoves = searchMoves
        self.ponder = ponder
        self.whiteTime = whiteTime
        self.blackTime = blackTime
        self.whiteIncrement = whiteIncrement
        self.blackIncrement = blackIncrement
        self.movesToGo = movesToGo
        self.depth = depth
        self.nodes = nodes
        self.mate = mate
        self.moveTime = moveTime
        self.infinite = infinite
    }
    
    var commandString: String {
        var components: [String] = []
        
        if let searchMoves = searchMoves, !searchMoves.isEmpty {
            components.append("searchmoves \(searchMoves.joined(separator: " "))")
        }
        
        if ponder {
            components.append("ponder")
        }
        
        if let whiteTime = whiteTime {
            components.append("wtime \(Int(whiteTime * 1000))")
        }
        
        if let blackTime = blackTime {
            components.append("btime \(Int(blackTime * 1000))")
        }
        
        if let whiteIncrement = whiteIncrement {
            components.append("winc \(Int(whiteIncrement * 1000))")
        }
        
        if let blackIncrement = blackIncrement {
            components.append("binc \(Int(blackIncrement * 1000))")
        }
        
        if let movesToGo = movesToGo {
            components.append("movestogo \(movesToGo)")
        }
        
        if let depth = depth {
            components.append("depth \(depth)")
        }
        
        if let nodes = nodes {
            components.append("nodes \(nodes)")
        }
        
        if let mate = mate {
            components.append("mate \(mate)")
        }
        
        if let moveTime = moveTime {
            components.append("movetime \(Int(moveTime * 1000))")
        }
        
        if infinite {
            components.append("infinite")
        }
        
        return components.joined(separator: " ")
    }
    
    static let infinite = GoParameters(infinite: true)
    
    static func depth(_ depth: Int) -> GoParameters {
        return GoParameters(depth: depth)
    }
    
    static func time(_ seconds: TimeInterval) -> GoParameters {
        return GoParameters(moveTime: seconds)
    }
}

enum UCIResponse: Equatable {
    case id(name: String, value: String)
    case uciOk
    case readyOk
    case bestMove(move: String, ponder: String?)
    case info(InfoParameters)
    case option(OptionParameter)
    case copyprotection(CopyProtectionStatus)
    case registration(RegistrationStatus)
    case unknown(String)
    
    enum CopyProtectionStatus: String, Equatable {
        case checking, ok, error
    }
    
    enum RegistrationStatus: String, Equatable {
        case checking, ok, error
    }
}

struct InfoParameters: Equatable {
    let depth: Int?
    let selectiveDepth: Int?
    let time: TimeInterval?
    let nodes: Int?
    let principalVariation: [String]?
    let multiPV: Int?
    let score: ScoreInfo?
    let currentMove: String?
    let currentMoveNumber: Int?
    let hashfull: Int?
    let nps: Int?
    let tbhits: Int?
    let cpuload: Int?
    let string: String?
    let refutation: [String]?
    let currline: [String]?
    
    struct ScoreInfo: Equatable {
        let centipawns: Int?
        let mate: Int?
        let lowerbound: Bool
        let upperbound: Bool
    }
}

struct OptionParameter: Equatable {
    let name: String
    let type: OptionType
    let defaultValue: String?
    let minValue: String?
    let maxValue: String?
    let vars: [String]?
    
    enum OptionType: String, Equatable {
        case check, spin, combo, button, string
    }
}