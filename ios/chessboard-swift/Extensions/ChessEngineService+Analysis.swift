// ChessEngineService+Analysis.swift - Analysis-specific engine methods
import Foundation
import Combine

extension ChessEngineService {
    
    // MARK: - Analysis Workflow Methods
    
    func performFullAnalysis(_ position: ChessPosition, depth: AnalysisDepth) async throws -> AnalysisResult {
        try await ensureEngineReady()
        
        // Setup position
        await setPosition(fen: position.fen)
        
        // Start analysis
        let startTime = Date()
        try await startAnalysisWithDepth(depth)
        
        // Wait for completion and collect result
        let result = try await waitForAnalysisCompletion(position: position, startTime: startTime)
        
        print("✅ Full analysis completed in \(result.formattedTime)")
        return result
    }
    
    func performQuickAnalysis(_ position: ChessPosition, timeLimit: TimeInterval = 3.0) async throws -> AnalysisResult {
        return try await performFullAnalysis(position, depth: .time(timeLimit))
    }
    
    func performDeepAnalysis(_ position: ChessPosition, depth: Int = 20) async throws -> AnalysisResult {
        return try await performFullAnalysis(position, depth: .depth(depth))
    }
    
    // MARK: - Multi-PV Analysis
    
    func performMultiPVAnalysis(_ position: ChessPosition, lines: Int = 3, depth: Int = 15) async throws -> MultiPVAnalysisResult {
        try await ensureEngineReady()
        
        // Configure Multi-PV
        await sendCommand(.setOption(name: "MultiPV", value: "\(lines)"))
        
        // Setup position
        await setPosition(fen: position.fen)
        
        // Start analysis
        let startTime = Date()
        await analyzeToDepth(depth)
        
        // Collect multi-PV results
        let results = try await waitForMultiPVCompletion(position: position, startTime: startTime, expectedLines: lines)
        
        // Reset Multi-PV to 1
        await sendCommand(.setOption(name: "MultiPV", value: "1"))
        
        return MultiPVAnalysisResult(
            position: position,
            lines: results,
            depth: depth,
            analysisTime: Date().timeIntervalSince(startTime)
        )
    }
    
    // MARK: - Batch Analysis
    
    func performBatchAnalysis(_ positions: [ChessPosition], depth: AnalysisDepth) async throws -> [AnalysisResult] {
        var results: [AnalysisResult] = []
        
        for (index, position) in positions.enumerated() {
            print("📊 Analyzing position \(index + 1)/\(positions.count)")
            
            do {
                let result = try await performFullAnalysis(position, depth: depth)
                results.append(result)
            } catch {
                print("❌ Failed to analyze position \(index + 1): \(error)")
                // Continue with remaining positions
            }
        }
        
        print("📊 Batch analysis complete: \(results.count)/\(positions.count) successful")
        return results
    }
    
    // MARK: - Position Comparison Analysis
    
    func comparePositions(_ position1: ChessPosition, _ position2: ChessPosition, depth: Int = 15) async throws -> PositionComparison {
        let analysis1 = try await performFullAnalysis(position1, depth: .depth(depth))
        let analysis2 = try await performFullAnalysis(position2, depth: .depth(depth))
        
        return PositionComparison(
            position1: analysis1,
            position2: analysis2,
            evaluationDifference: calculateEvaluationDifference(analysis1.evaluation, analysis2.evaluation),
            recommendation: generateComparisonRecommendation(analysis1, analysis2)
        )
    }
    
    // MARK: - Interactive Analysis
    
    func startInteractiveAnalysis(_ position: ChessPosition) async throws {
        try await ensureEngineReady()
        
        // Setup position
        await setPosition(fen: position.fen)
        
        // Start infinite analysis
        await analyzeInfinite()
        
        updateStatus(.analyzing)
        print("🔄 Interactive analysis started - call stopInteractiveAnalysis() to end")
    }
    
    func stopInteractiveAnalysis() async -> AnalysisResult? {
        guard status == .analyzing else { return nil }
        
        await stopAnalysis()
        
        // Collect final result
        // This would normally be accumulated from UCI responses during analysis
        return createCurrentAnalysisSnapshot()
    }
    
    func updateInteractiveAnalysis(with newPosition: ChessPosition) async {
        guard status == .analyzing else { return }
        
        // Stop current analysis
        await stopAnalysis()
        
        // Update position
        await setPosition(fen: newPosition.fen)
        
        // Restart analysis
        await analyzeInfinite()
    }
    
    // MARK: - Analysis Helpers
    
    private func ensureEngineReady() async throws {
        guard status.isOperational else {
            if status == .notStarted || status == .stopped {
                try await startEngine()
            } else {
                throw ChessEngineError.engineNotReady
            }
        }
    }
    
    private func startAnalysisWithDepth(_ depth: AnalysisDepth) async throws {
        switch depth {
        case .depth(let d):
            await analyzeToDepth(d)
        case .time(let seconds):
            await analyzeForTime(seconds)
        case .infinite:
            await analyzeInfinite()
        }
        
        updateStatus(.analyzing)
    }
    
    private func waitForAnalysisCompletion(position: ChessPosition, startTime: Date) async throws -> AnalysisResult {
        // This would normally wait for bestmove response from engine
        // For now, simulate completion with mock data
        
        let analysisTime = Date().timeIntervalSince(startTime)
        
        // Wait for simulation (replace with real UCI monitoring)
        let waitTime = min(analysisTime + 2.0, 10.0) // Cap at 10 seconds for testing
        try await Task.sleep(nanoseconds: UInt64(waitTime * 1_000_000_000))
        
        // Create mock result (replace with real engine response parsing)
        let result = AnalysisResult(
            position: position,
            bestMove: generateMockBestMove(for: position),
            evaluation: generateMockEvaluation(),
            depth: 15, // Would come from engine response
            principalVariation: generateMockPV(),
            analysisTime: analysisTime,
            nodesSearched: Int.random(in: 100000...1000000)
        )
        
        updateStatus(.ready)
        return result
    }
    
    private func waitForMultiPVCompletion(position: ChessPosition, startTime: Date, expectedLines: Int) async throws -> [EngineVariation] {
        // Simulate multi-PV analysis completion
        try await Task.sleep(nanoseconds: 3_000_000_000) // 3 seconds
        
        var variations: [EngineVariation] = []
        
        for line in 1...expectedLines {
            let evaluation = EvaluationScore(
                type: .centipawns(Int.random(in: -200...200) - (line - 1) * 50),
                perspective: position.isWhiteTurn ? .white : .black
            )
            
            let variation = EngineVariation(
                moves: generateMockPV(),
                evaluation: evaluation,
                depth: 15
            )
            
            variations.append(variation)
        }
        
        updateStatus(.ready)
        return variations
    }
    
    // MARK: - Analysis Data Processing
    
    private func calculateEvaluationDifference(_ eval1: EvaluationScore, _ eval2: EvaluationScore) -> Int {
        let score1: Int
        let score2: Int
        
        switch (eval1.type, eval2.type) {
        case (.centipawns(let cp1), .centipawns(let cp2)):
            score1 = eval1.perspective == .white ? cp1 : -cp1
            score2 = eval2.perspective == .white ? cp2 : -cp2
        case (.mate(let m1), .mate(let m2)):
            score1 = m1 > 0 ? 10000 : -10000
            score2 = m2 > 0 ? 10000 : -10000
        case (.centipawns(let cp), .mate(let m)):
            score1 = eval1.perspective == .white ? cp : -cp
            score2 = m > 0 ? 10000 : -10000
        case (.mate(let m), .centipawns(let cp)):
            score1 = m > 0 ? 10000 : -10000
            score2 = eval2.perspective == .white ? cp : -cp
        default:
            return 0
        }
        
        return score1 - score2
    }
    
    private func generateComparisonRecommendation(_ analysis1: AnalysisResult, _ analysis2: AnalysisResult) -> String {
        guard let bestMove1 = analysis1.bestMove,
              let bestMove2 = analysis2.bestMove else {
            return "Unable to compare - missing moves"
        }
        
        let evalDiff = calculateEvaluationDifference(analysis1.evaluation, analysis2.evaluation)
        
        if abs(evalDiff) < 50 {
            return "Positions are roughly equivalent"
        } else if evalDiff > 0 {
            return "First position is better by \(abs(evalDiff)) centipawns"
        } else {
            return "Second position is better by \(abs(evalDiff)) centipawns"
        }
    }
    
    private func createCurrentAnalysisSnapshot() -> AnalysisResult? {
        // This would create a snapshot of current analysis state
        // For now, return nil as we don't have real UCI monitoring
        return nil
    }
    
    // MARK: - Mock Data Generation (Temporary)
    
    private func generateMockBestMove(for position: ChessPosition) -> String? {
        if position.isStartingPosition {
            return ["e2e4", "d2d4", "g1f3", "c2c4"].randomElement()
        } else {
            return ["e4e5", "f3g5", "c4d5", "g1h3", "a2a4"].randomElement()
        }
    }
    
    private func generateMockEvaluation() -> EvaluationScore {
        let randomCP = Int.random(in: -300...300)
        return EvaluationScore(type: .centipawns(randomCP), perspective: .white)
    }
    
    private func generateMockPV() -> [String] {
        let moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5", "d2d3", "d7d6"]
        let length = Int.random(in: 3...6)
        return Array(moves.prefix(length))
    }
    
    // MARK: - Analysis Result Data Structures
    
    struct MultiPVAnalysisResult {
        let position: ChessPosition
        let lines: [EngineVariation]
        let depth: Int
        let analysisTime: TimeInterval
        
        var primaryLine: EngineVariation? {
            return lines.first
        }
        
        var alternativeLines: [EngineVariation] {
            return Array(lines.dropFirst())
        }
        
        var bestMove: String? {
            return primaryLine?.moves.first
        }
        
        var formattedTime: String {
            return String(format: "%.1fs", analysisTime)
        }
    }
    
    struct PositionComparison {
        let position1: AnalysisResult
        let position2: AnalysisResult
        let evaluationDifference: Int
        let recommendation: String
        
        var betterPosition: AnalysisResult {
            return evaluationDifference > 0 ? position1 : position2
        }
        
        var significantDifference: Bool {
            return abs(evaluationDifference) > 100
        }
        
        var formattedDifference: String {
            let diff = Double(abs(evaluationDifference)) / 100.0
            return String(format: "%.2f", diff)
        }
    }
    
    // MARK: - Analysis Settings
    
    func configureAnalysisSettings(_ settings: AnalysisSettings) async {
        var options: [String: String] = [:]
        
        // Hash size
        options["Hash"] = "\(settings.hashSizeMB)"
        
        // Threads
        options["Threads"] = "\(settings.threadCount)"
        
        // Analysis options
        if settings.enableMultiPV {
            options["MultiPV"] = "\(settings.multiPVLines)"
        }
        
        if settings.enablePonder {
            options["Ponder"] = "true"
        }
        
        // Neural network evaluation
        if let nnueFile = settings.nnueFilePath {
            options["EvalFile"] = nnueFile
        }
        
        // Apply all settings
        await configureEngine(options: options)
        
        print("⚙️ Analysis settings applied: \(options.count) options")
    }
    
    struct AnalysisSettings {
        let hashSizeMB: Int
        let threadCount: Int
        let enableMultiPV: Bool
        let multiPVLines: Int
        let enablePonder: Bool
        let nnueFilePath: String?
        
        static let `default` = AnalysisSettings(
            hashSizeMB: 128,
            threadCount: 2,
            enableMultiPV: false,
            multiPVLines: 1,
            enablePonder: false,
            nnueFilePath: nil
        )
        
        static let performance = AnalysisSettings(
            hashSizeMB: 256,
            threadCount: 4,
            enableMultiPV: true,
            multiPVLines: 3,
            enablePonder: true,
            nnueFilePath: nil
        )
        
        static let mobile = AnalysisSettings(
            hashSizeMB: 64,
            threadCount: 2,
            enableMultiPV: false,
            multiPVLines: 1,
            enablePonder: false,
            nnueFilePath: nil
        )
    }
}