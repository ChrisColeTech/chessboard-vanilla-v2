// UCIParser.swift - Parses UCI protocol responses from chess engine
import Foundation

class UCIParser {
    
    static func parseResponse(_ line: String) -> UCIResponse {
        let trimmed = line.trimmingCharacters(in: .whitespacesAndNewlines)
        let components = trimmed.split(separator: " ", omittingEmptySubsequences: true).map(String.init)
        
        guard !components.isEmpty else {
            return .unknown(trimmed)
        }
        
        switch components[0].lowercased() {
        case "id":
            return parseId(components)
        case "uciok":
            return .uciOk
        case "readyok":
            return .readyOk
        case "bestmove":
            return parseBestMove(components)
        case "info":
            return parseInfo(components)
        case "option":
            return parseOption(components)
        case "copyprotection":
            return parseCopyProtection(components)
        case "registration":
            return parseRegistration(components)
        default:
            return .unknown(trimmed)
        }
    }
    
    private static func parseId(_ components: [String]) -> UCIResponse {
        guard components.count >= 3 else {
            return .unknown(components.joined(separator: " "))
        }
        
        let name = components[1]
        let value = components[2...].joined(separator: " ")
        return .id(name: name, value: value)
    }
    
    private static func parseBestMove(_ components: [String]) -> UCIResponse {
        guard components.count >= 2 else {
            return .unknown(components.joined(separator: " "))
        }
        
        let move = components[1]
        var ponder: String? = nil
        
        if components.count >= 4 && components[2] == "ponder" {
            ponder = components[3]
        }
        
        return .bestMove(move: move, ponder: ponder)
    }
    
    private static func parseInfo(_ components: [String]) -> UCIResponse {
        var depth: Int?
        var selectiveDepth: Int?
        var time: TimeInterval?
        var nodes: Int?
        var principalVariation: [String]?
        var multiPV: Int?
        var score: InfoParameters.ScoreInfo?
        var currentMove: String?
        var currentMoveNumber: Int?
        var hashfull: Int?
        var nps: Int?
        var tbhits: Int?
        var cpuload: Int?
        var string: String?
        var refutation: [String]?
        var currline: [String]?
        
        var i = 1
        while i < components.count {
            switch components[i] {
            case "depth":
                if i + 1 < components.count {
                    depth = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "seldepth":
                if i + 1 < components.count {
                    selectiveDepth = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "time":
                if i + 1 < components.count {
                    time = Double(components[i + 1]).map { $0 / 1000.0 }
                    i += 2
                } else {
                    i += 1
                }
            case "nodes":
                if i + 1 < components.count {
                    nodes = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "pv":
                let pvStart = i + 1
                var pvEnd = pvStart
                while pvEnd < components.count && !isInfoKeyword(components[pvEnd]) {
                    pvEnd += 1
                }
                if pvEnd > pvStart {
                    principalVariation = Array(components[pvStart..<pvEnd])
                }
                i = pvEnd
            case "multipv":
                if i + 1 < components.count {
                    multiPV = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "score":
                let (scoreInfo, nextIndex) = parseScore(components, startingAt: i + 1)
                score = scoreInfo
                i = nextIndex
            case "currmove":
                if i + 1 < components.count {
                    currentMove = components[i + 1]
                    i += 2
                } else {
                    i += 1
                }
            case "currmovenumber":
                if i + 1 < components.count {
                    currentMoveNumber = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "hashfull":
                if i + 1 < components.count {
                    hashfull = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "nps":
                if i + 1 < components.count {
                    nps = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "tbhits":
                if i + 1 < components.count {
                    tbhits = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "cpuload":
                if i + 1 < components.count {
                    cpuload = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "string":
                string = components[(i + 1)...].joined(separator: " ")
                i = components.count
            case "refutation":
                let refStart = i + 1
                var refEnd = refStart
                while refEnd < components.count && !isInfoKeyword(components[refEnd]) {
                    refEnd += 1
                }
                if refEnd > refStart {
                    refutation = Array(components[refStart..<refEnd])
                }
                i = refEnd
            case "currline":
                let lineStart = i + 1
                var lineEnd = lineStart
                while lineEnd < components.count && !isInfoKeyword(components[lineEnd]) {
                    lineEnd += 1
                }
                if lineEnd > lineStart {
                    currline = Array(components[lineStart..<lineEnd])
                }
                i = lineEnd
            default:
                i += 1
            }
        }
        
        let info = InfoParameters(
            depth: depth,
            selectiveDepth: selectiveDepth,
            time: time,
            nodes: nodes,
            principalVariation: principalVariation,
            multiPV: multiPV,
            score: score,
            currentMove: currentMove,
            currentMoveNumber: currentMoveNumber,
            hashfull: hashfull,
            nps: nps,
            tbhits: tbhits,
            cpuload: cpuload,
            string: string,
            refutation: refutation,
            currline: currline
        )
        
        return .info(info)
    }
    
    private static func parseScore(_ components: [String], startingAt: Int) -> (InfoParameters.ScoreInfo?, Int) {
        var i = startingAt
        var centipawns: Int?
        var mate: Int?
        var lowerbound = false
        var upperbound = false
        
        while i < components.count && !isInfoKeyword(components[i]) {
            switch components[i] {
            case "cp":
                if i + 1 < components.count {
                    centipawns = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "mate":
                if i + 1 < components.count {
                    mate = Int(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            case "lowerbound":
                lowerbound = true
                i += 1
            case "upperbound":
                upperbound = true
                i += 1
            default:
                i += 1
                break
            }
        }
        
        let scoreInfo = InfoParameters.ScoreInfo(
            centipawns: centipawns,
            mate: mate,
            lowerbound: lowerbound,
            upperbound: upperbound
        )
        
        return (scoreInfo, i)
    }
    
    private static func parseOption(_ components: [String]) -> UCIResponse {
        var name: String = ""
        var type: OptionParameter.OptionType = .string
        var defaultValue: String?
        var minValue: String?
        var maxValue: String?
        var vars: [String]?
        
        var i = 1
        while i < components.count {
            switch components[i] {
            case "name":
                i += 1
                var nameComponents: [String] = []
                while i < components.count && components[i] != "type" {
                    nameComponents.append(components[i])
                    i += 1
                }
                name = nameComponents.joined(separator: " ")
            case "type":
                if i + 1 < components.count {
                    type = OptionParameter.OptionType(rawValue: components[i + 1]) ?? .string
                    i += 2
                } else {
                    i += 1
                }
            case "default":
                if i + 1 < components.count {
                    defaultValue = components[i + 1]
                    i += 2
                } else {
                    i += 1
                }
            case "min":
                if i + 1 < components.count {
                    minValue = components[i + 1]
                    i += 2
                } else {
                    i += 1
                }
            case "max":
                if i + 1 < components.count {
                    maxValue = components[i + 1]
                    i += 2
                } else {
                    i += 1
                }
            case "var":
                if vars == nil {
                    vars = []
                }
                if i + 1 < components.count {
                    vars?.append(components[i + 1])
                    i += 2
                } else {
                    i += 1
                }
            default:
                i += 1
            }
        }
        
        let option = OptionParameter(
            name: name,
            type: type,
            defaultValue: defaultValue,
            minValue: minValue,
            maxValue: maxValue,
            vars: vars
        )
        
        return .option(option)
    }
    
    private static func parseCopyProtection(_ components: [String]) -> UCIResponse {
        guard components.count >= 2 else {
            return .unknown(components.joined(separator: " "))
        }
        
        let status = UCIResponse.CopyProtectionStatus(rawValue: components[1]) ?? .error
        return .copyprotection(status)
    }
    
    private static func parseRegistration(_ components: [String]) -> UCIResponse {
        guard components.count >= 2 else {
            return .unknown(components.joined(separator: " "))
        }
        
        let status = UCIResponse.RegistrationStatus(rawValue: components[1]) ?? .error
        return .registration(status)
    }
    
    private static func isInfoKeyword(_ word: String) -> Bool {
        let keywords = [
            "depth", "seldepth", "time", "nodes", "pv", "multipv", "score",
            "currmove", "currmovenumber", "hashfull", "nps", "tbhits",
            "cpuload", "string", "refutation", "currline"
        ]
        return keywords.contains(word.lowercased())
    }
}