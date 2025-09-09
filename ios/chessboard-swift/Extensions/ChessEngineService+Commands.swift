// ChessEngineService+Commands.swift - UCI command convenience methods
import Foundation

extension ChessEngineService {
    
    // MARK: - Engine Initialization Commands
    
    func initializeUCI() async throws {
        await sendCommand(.uci)
        // Wait for engine to be ready after UCI initialization
        try await waitForReady(timeout: 5.0)
    }
    
    func setEngineReady() async throws {
        await sendCommand(.isReady)
        try await waitForReady(timeout: 3.0)
    }
    
    func newGame() async {
        await sendCommand(.uciNewGame)
    }
    
    // MARK: - Engine Configuration Commands
    
    func configureEngine(options: [String: String]) async {
        for (name, value) in options {
            let command = UCICommand.setOption(name: name, value: value)
            await sendCommand(command)
        }
    }
    
    func setHashSize(_ sizeMB: Int) async {
        await sendCommand(.setOption(name: "Hash", value: "\(sizeMB)"))
    }
    
    func setThreadCount(_ threads: Int) async {
        await sendCommand(.setOption(name: "Threads", value: "\(threads)"))
    }
    
    func enableDebugMode(_ enabled: Bool) async {
        await sendCommand(.debug(enabled))
    }
    
    // MARK: - Position Commands
    
    func setStartingPosition() async {
        await sendCommand(.position(fen: nil, moves: []))
    }
    
    func setPosition(fen: String) async {
        await sendCommand(.position(fen: fen, moves: []))
    }
    
    func setPositionWithMoves(fen: String? = nil, moves: [String]) async {
        await sendCommand(.position(fen: fen, moves: moves))
    }
    
    func makeMove(_ move: String, from position: ChessPosition? = nil) async {
        if let position = position {
            await setPosition(fen: position.fen)
        }
        await sendCommand(.position(fen: position?.fen, moves: [move]))
    }
    
    // MARK: - Analysis Commands
    
    func analyzeToDepth(_ depth: Int) async {
        let goParams = GoParameters.depth(depth)
        await sendCommand(.go(parameters: goParams))
    }
    
    func analyzeForTime(_ seconds: TimeInterval) async {
        let goParams = GoParameters.time(seconds)
        await sendCommand(.go(parameters: goParams))
    }
    
    func analyzeInfinite() async {
        await sendCommand(.go(parameters: GoParameters.infinite))
    }
    
    func analyzeWithTimeControl(whiteTime: TimeInterval, blackTime: TimeInterval, whiteIncrement: TimeInterval = 0, blackIncrement: TimeInterval = 0) async {
        let goParams = GoParameters(
            whiteTime: whiteTime,
            blackTime: blackTime,
            whiteIncrement: whiteIncrement,
            blackIncrement: blackIncrement
        )
        await sendCommand(.go(parameters: goParams))
    }
    
    func stopAnalysis() async {
        guard status == .analyzing else { return }
        await sendCommand(.stop)
    }
    
    // MARK: - Multi-PV Analysis Commands
    
    func analyzeMultiPV(_ lines: Int, depth: Int) async {
        // First set the Multi-PV option
        await sendCommand(.setOption(name: "MultiPV", value: "\(lines)"))
        
        // Then start analysis
        await analyzeToDepth(depth)
    }
    
    func analyzeMultiPVForTime(_ lines: Int, seconds: TimeInterval) async {
        await sendCommand(.setOption(name: "MultiPV", value: "\(lines)"))
        await analyzeForTime(seconds)
    }
    
    // MARK: - Utility Commands
    
    func ponderHit() async {
        await sendCommand(.ponderhit)
    }
    
    func quitEngine() async {
        await sendCommand(.quit)
    }
    
    // MARK: - Command Waiting Helpers
    
    private func waitForReady(timeout: TimeInterval) async throws {
        let startTime = Date()
        
        while Date().timeIntervalSince(startTime) < timeout {
            if status == .ready {
                return
            }
            
            if case .error(_) = status {
                throw ChessEngineError.communicationFailure
            }
            
            try await Task.sleep(nanoseconds: 100_000_000) // 100ms
        }
        
        throw ChessEngineError.analysisTimeout
    }
    
    // MARK: - Batch Commands
    
    func setupNewAnalysis(position: ChessPosition, depth: AnalysisDepth) async throws {
        // Setup position
        await setPosition(fen: position.fen)
        
        // Ensure engine is ready
        try await setEngineReady()
        
        // Start analysis based on depth type
        switch depth {
        case .depth(let d):
            await analyzeToDepth(d)
        case .time(let seconds):
            await analyzeForTime(seconds)
        case .infinite:
            await analyzeInfinite()
        }
    }
    
    func quickAnalysis(fen: String, depth: Int = 15) async throws -> String? {
        // Set position
        await setPosition(fen: fen)
        
        // Wait for ready
        try await setEngineReady()
        
        // Start analysis
        await analyzeToDepth(depth)
        
        // This would normally wait for the analysis to complete
        // For now, we'll return a placeholder
        return "Analysis started for depth \(depth)"
    }
    
    // MARK: - Engine Health Commands
    
    func performHealthCheck() async -> Bool {
        let originalStatus = status
        
        do {
            await sendCommand(.isReady)
            try await waitForReady(timeout: 2.0)
            return status == .ready
        } catch {
            print("❌ Engine health check failed: \(error)")
            return false
        }
    }
    
    func resetEngine() async throws {
        // Stop any ongoing analysis
        if status == .analyzing {
            await stopAnalysis()
        }
        
        // Send new game command
        await newGame()
        
        // Wait for engine to be ready
        try await setEngineReady()
    }
    
    // MARK: - Command Validation
    
    func canExecuteCommand(_ command: UCICommand) -> Bool {
        switch command {
        case .quit:
            return true // Can always quit
        case .uci, .debug(_):
            return status == .notStarted || status == .starting
        case .isReady, .uciNewGame, .setOption(_, _):
            return status != .notStarted
        case .position(_, _), .go(_):
            return status.isOperational
        case .stop, .ponderhit:
            return status == .analyzing
        }
    }
    
    // MARK: - Command History (for debugging)
    
    private var commandHistory: [UCICommandHistoryEntry] = []
    
    private struct UCICommandHistoryEntry {
        let command: UCICommand
        let timestamp: Date
        let success: Bool
        let response: String?
        
        init(command: UCICommand, success: Bool = true, response: String? = nil) {
            self.command = command
            self.timestamp = Date()
            self.success = success
            self.response = response
        }
    }
    
    private func recordCommand(_ command: UCICommand, success: Bool = true, response: String? = nil) {
        let entry = UCICommandHistoryEntry(command: command, success: success, response: response)
        commandHistory.append(entry)
        
        // Keep only recent commands (last 50)
        if commandHistory.count > 50 {
            commandHistory.removeFirst()
        }
    }
    
    func getCommandHistory() -> [(command: String, timestamp: Date, success: Bool)] {
        return commandHistory.map { entry in
            (command: entry.command.commandString, timestamp: entry.timestamp, success: entry.success)
        }
    }
    
    func clearCommandHistory() {
        commandHistory.removeAll()
    }
}