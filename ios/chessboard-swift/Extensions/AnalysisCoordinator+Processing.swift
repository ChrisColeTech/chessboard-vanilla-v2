// AnalysisCoordinator+Processing.swift - Analysis processing methods for coordinator
import Foundation

extension AnalysisCoordinator {
    
    // MARK: - Enhanced Analysis Processing
    
    func processPositionWithOptions(_ position: ChessPosition, options: AnalysisOptions) async {
        let request = AnalysisRequest(
            position: position,
            depth: options.depth,
            priority: options.priority
        )
        
        // Validate position before queuing
        guard await validatePositionForAnalysis(position) else {
            print("❌ Invalid position for analysis: \(position.fen)")
            return
        }
        
        // Apply analysis options
        await configureEngineForRequest(request, options: options)
        
        // Add to queue
        insertRequestInQueue(request)
        await processAnalysisQueue()
    }
    
    func batchAnalyzePositions(_ positions: [ChessPosition], depth: AnalysisDepth, priority: AnalysisRequest.AnalysisPriority = .normal) async {
        let requests = positions.map { position in
            AnalysisRequest(position: position, depth: depth, priority: priority)
        }
        
        for request in requests {
            insertRequestInQueue(request)
        }
        
        print("📦 Batch added \(requests.count) positions for analysis")
        await processAnalysisQueue()
    }
    
    func analyzePositionFromFEN(_ fen: String, depth: AnalysisDepth, priority: AnalysisRequest.AnalysisPriority = .normal) async {
        guard FENValidator.isValid(fen) else {
            print("❌ Invalid FEN position: \(fen)")
            return
        }
        
        let position = ChessPosition(fen: fen)
        await analyzePosition(position, depth: depth, priority: priority)
    }
    
    // MARK: - Analysis Configuration
    
    private func configureEngineForRequest(_ request: AnalysisRequest, options: AnalysisOptions) async {
        // Configure Multi-PV if requested
        if options.multiPVLines > 1 {
            await engineService.configureEngine(options: ["MultiPV": "\(options.multiPVLines)"])
        }
        
        // Configure hash size based on analysis complexity
        let hashSize = calculateOptimalHashSize(for: request, options: options)
        await engineService.setHashSize(hashSize)
        
        // Set threads based on device capability
        let threadCount = determineOptimalThreadCount()
        await engineService.setThreadCount(threadCount)
    }
    
    private func calculateOptimalHashSize(for request: AnalysisRequest, options: AnalysisOptions) -> Int {
        // Calculate hash size based on analysis depth and available memory
        let baseHashSize: Int
        
        switch request.depth {
        case .depth(let d):
            baseHashSize = min(128, max(16, d * 8)) // 16-128 MB based on depth
        case .time(let seconds):
            baseHashSize = min(128, max(16, Int(seconds) * 4))
        case .infinite:
            baseHashSize = 256 // Larger hash for infinite analysis
        }
        
        // Adjust for multi-PV
        let adjustedSize = options.multiPVLines > 1 ? Int(Double(baseHashSize) * 1.5) : baseHashSize
        
        return min(adjustedSize, 512) // Cap at 512 MB
    }
    
    private func determineOptimalThreadCount() -> Int {
        let processorCount = ProcessInfo.processInfo.processorCount
        
        // Use 50-75% of available cores, minimum 1, maximum 4 for mobile
        let optimalThreads = max(1, min(4, Int(Double(processorCount) * 0.75)))
        
        print("🧮 Using \(optimalThreads) threads for analysis (of \(processorCount) available)")
        return optimalThreads
    }
    
    // MARK: - Position Validation
    
    private func validatePositionForAnalysis(_ position: ChessPosition) async -> Bool {
        // Basic FEN validation
        guard position.isValid else {
            return false
        }
        
        // Chess rules validation
        let validation = FENValidator.validateChessRules(position.fen)
        if !validation.isValid {
            print("❌ Position validation errors: \(validation.errors.map { $0.localizedDescription }.joined(separator: ", "))")
            return false
        }
        
        // Check for analysis-worthy positions
        return await isPositionWorthAnalyzing(position)
    }
    
    private func isPositionWorthAnalyzing(_ position: ChessPosition) async -> Bool {
        // Skip analysis for trivial positions
        guard let positionInfo = FENValidator.getPositionInfo(position.fen) else {
            return false
        }
        
        // Skip positions with very few pieces (unless it's a specific endgame study)
        if positionInfo.totalPieces < 6 && !position.fen.contains("K") {
            print("⚠️ Skipping position with too few pieces")
            return false
        }
        
        // Skip positions that are clearly drawn
        if abs(positionInfo.materialBalance) == 0 && positionInfo.totalPieces <= 8 {
            // Could be a theoretical draw, but might still be worth analyzing
        }
        
        return true
    }
    
    // MARK: - Advanced Analysis Features
    
    func analyzeWithComparison(_ position: ChessPosition, compareWith otherPosition: ChessPosition, depth: AnalysisDepth) async {
        // Analyze both positions and compare results
        let originalRequest = AnalysisRequest(position: position, depth: depth, priority: .high)
        let comparisonRequest = AnalysisRequest(position: otherPosition, depth: depth, priority: .high)
        
        // Process both analyses
        insertRequestInQueue(originalRequest)
        insertRequestInQueue(comparisonRequest)
        
        await processAnalysisQueue()
        
        // Results will be available in analysis history for comparison
        print("📊 Comparative analysis queued for two positions")
    }
    
    func analyzePositionDepth(_ position: ChessPosition, startingDepth: Int = 10, maxDepth: Int = 20, depthIncrement: Int = 2) async {
        var currentDepth = startingDepth
        
        while currentDepth <= maxDepth {
            let request = AnalysisRequest(
                position: position,
                depth: .depth(currentDepth),
                priority: .normal
            )
            
            insertRequestInQueue(request)
            currentDepth += depthIncrement
        }
        
        print("📈 Progressive depth analysis queued: \(startingDepth) to \(maxDepth)")
        await processAnalysisQueue()
    }
    
    // MARK: - Analysis Result Processing
    
    func processAnalysisResult(_ result: AnalysisResult) -> ProcessedAnalysisResult {
        let processed = ProcessedAnalysisResult(
            originalResult: result,
            positionType: classifyPosition(result.position),
            moveQuality: evaluateMoveQuality(result),
            strategicAdvice: generateStrategicAdvice(result),
            alternativeMoves: findAlternativeMoves(result),
            timestamp: Date()
        )
        
        return processed
    }
    
    private func classifyPosition(_ position: ChessPosition) -> PositionType {
        guard let positionInfo = FENValidator.getPositionInfo(position.fen) else {
            return .unknown
        }
        
        if positionInfo.isOpening {
            return .opening
        } else if positionInfo.isMiddlegame {
            return .middlegame
        } else if positionInfo.isEndgame {
            return .endgame
        } else {
            return .unknown
        }
    }
    
    private func evaluateMoveQuality(_ result: AnalysisResult) -> MoveQuality {
        guard let bestMove = result.bestMove else {
            return .unknown
        }
        
        // Evaluate based on engine evaluation and depth
        switch result.evaluation.type {
        case .centipawns(let cp):
            let absScore = abs(cp)
            if absScore < 25 {
                return .excellent
            } else if absScore < 100 {
                return .good
            } else if absScore < 200 {
                return .inaccurate
            } else {
                return .blunder
            }
        case .mate(let moves):
            return abs(moves) <= 3 ? .excellent : .good
        case .unknown:
            return .unknown
        }
    }
    
    private func generateStrategicAdvice(_ result: AnalysisResult) -> [String] {
        var advice: [String] = []
        
        // Advice based on evaluation
        switch result.evaluation.type {
        case .centipawns(let cp):
            if abs(cp) > 200 {
                advice.append("Large material advantage - convert to a win")
            } else if abs(cp) < 50 {
                advice.append("Position is roughly equal - look for tactical opportunities")
            }
        case .mate(let moves):
            if moves > 0 {
                advice.append("Forced mate in \(moves) - follow the principal variation")
            } else {
                advice.append("Defend precisely to avoid mate in \(abs(moves))")
            }
        case .unknown:
            advice.append("Position evaluation unclear - analyze further")
        }
        
        // Advice based on position type
        if let positionInfo = FENValidator.getPositionInfo(result.position.fen) {
            if positionInfo.isOpening {
                advice.append("Develop pieces and control center")
            } else if positionInfo.isEndgame {
                advice.append("Activate king and promote pawns")
            }
        }
        
        return advice
    }
    
    private func findAlternativeMoves(_ result: AnalysisResult) -> [String] {
        // Extract alternative moves from principal variation
        return Array(result.principalVariation.dropFirst().prefix(3))
    }
    
    // MARK: - Analysis Statistics
    
    func getAnalysisStatistics() -> AnalysisStatistics {
        let totalAnalyses = analysisHistory.count
        let averageDepth = analysisHistory.isEmpty ? 0 : analysisHistory.map { $0.depth }.reduce(0, +) / totalAnalyses
        let averageTime = analysisHistory.isEmpty ? 0 : analysisHistory.map { $0.analysisTime }.reduce(0, +) / Double(totalAnalyses)
        let totalNodes = analysisHistory.map { $0.nodesSearched }.reduce(0, +)
        
        return AnalysisStatistics(
            totalAnalyses: totalAnalyses,
            averageDepth: averageDepth,
            averageAnalysisTime: averageTime,
            totalNodesSearched: totalNodes,
            queuedAnalyses: analysisQueue.count,
            successRate: calculateSuccessRate()
        )
    }
    
    private func calculateSuccessRate() -> Double {
        let total = analysisHistory.count
        guard total > 0 else { return 0.0 }
        
        let successful = analysisHistory.filter { $0.hasValidMove }.count
        return Double(successful) / Double(total)
    }
    
    // MARK: - Data Structures
    
    struct AnalysisOptions {
        let depth: AnalysisDepth
        let multiPVLines: Int
        let priority: AnalysisRequest.AnalysisPriority
        let timeout: TimeInterval?
        
        static let `default` = AnalysisOptions(
            depth: .depth(15),
            multiPVLines: 1,
            priority: .normal,
            timeout: nil
        )
        
        static func quick() -> AnalysisOptions {
            return AnalysisOptions(
                depth: .depth(10),
                multiPVLines: 1,
                priority: .high,
                timeout: 5.0
            )
        }
        
        static func deep() -> AnalysisOptions {
            return AnalysisOptions(
                depth: .depth(25),
                multiPVLines: 3,
                priority: .normal,
                timeout: 60.0
            )
        }
    }
    
    struct ProcessedAnalysisResult {
        let originalResult: AnalysisResult
        let positionType: PositionType
        let moveQuality: MoveQuality
        let strategicAdvice: [String]
        let alternativeMoves: [String]
        let timestamp: Date
    }
    
    enum PositionType {
        case opening
        case middlegame
        case endgame
        case unknown
        
        var description: String {
            switch self {
            case .opening: return "Opening"
            case .middlegame: return "Middlegame"
            case .endgame: return "Endgame"
            case .unknown: return "Unknown"
            }
        }
    }
    
    enum MoveQuality {
        case excellent
        case good
        case inaccurate
        case blunder
        case unknown
        
        var description: String {
            switch self {
            case .excellent: return "Excellent"
            case .good: return "Good"
            case .inaccurate: return "Inaccurate"
            case .blunder: return "Blunder"
            case .unknown: return "Unknown"
            }
        }
        
        var emoji: String {
            switch self {
            case .excellent: return "✨"
            case .good: return "✅"
            case .inaccurate: return "⚠️"
            case .blunder: return "❌"
            case .unknown: return "❓"
            }
        }
    }
    
    struct AnalysisStatistics {
        let totalAnalyses: Int
        let averageDepth: Int
        let averageAnalysisTime: TimeInterval
        let totalNodesSearched: Int
        let queuedAnalyses: Int
        let successRate: Double
        
        var formattedAverageTime: String {
            return String(format: "%.1fs", averageAnalysisTime)
        }
        
        var formattedSuccessRate: String {
            return String(format: "%.1f%%", successRate * 100)
        }
        
        var nodesPerSecond: Int {
            guard totalAnalyses > 0, averageAnalysisTime > 0 else { return 0 }
            return Int(Double(totalNodesSearched) / (averageAnalysisTime * Double(totalAnalyses)))
        }
    }
}