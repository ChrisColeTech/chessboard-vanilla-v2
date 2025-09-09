// AnalysisProcessor.swift - Process analysis requests and parse engine responses
import Foundation
import Combine

class AnalysisProcessor: ObservableObject {
    @Published private(set) var processingStatus: ProcessingStatus = .idle
    @Published private(set) var currentRequest: ProcessingRequest?
    @Published private(set) var lastResult: AnalysisResult?
    
    private var cancellables = Set<AnyCancellable>()
    private var analysisBuffer: [String] = []
    private var partialAnalysis: PartialAnalysisResult?
    
    enum ProcessingStatus {
        case idle
        case validating
        case processing
        case parsing
        case complete
        case error(String)
    }
    
    struct ProcessingRequest: Identifiable {
        let id = UUID()
        let position: ChessPosition
        let depth: AnalysisDepth
        let options: ProcessingOptions
        let startTime: Date
        
        struct ProcessingOptions {
            let multiPV: Int
            let enablePonder: Bool
            let maxTime: TimeInterval?
            let maxNodes: Int?
            
            static let `default` = ProcessingOptions(
                multiPV: 1,
                enablePonder: false,
                maxTime: nil,
                maxNodes: nil
            )
        }
        
        init(position: ChessPosition, depth: AnalysisDepth, options: ProcessingOptions = .default) {
            self.position = position
            self.depth = depth
            self.options = options
            self.startTime = Date()
        }
    }
    
    private struct PartialAnalysisResult {
        var bestMove: String?
        var evaluation: EvaluationScore?
        var depth: Int = 0
        var nodes: Int = 0
        var principalVariation: [String] = []
        var multiPVLines: [EngineVariation] = []
        var analysisTime: TimeInterval = 0
        var lastUpdate: Date = Date()
        
        var isComplete: Bool {
            return bestMove != nil && evaluation != nil
        }
    }
    
    init() {
        setupProcessing()
    }
    
    deinit {
        cancellables.removeAll()
    }
    
    // MARK: - Public Interface
    
    func processPosition(_ position: ChessPosition, depth: AnalysisDepth, options: ProcessingRequest.ProcessingOptions = .default) async throws -> AnalysisResult {
        
        let request = ProcessingRequest(position: position, depth: depth, options: options)
        currentRequest = request
        
        do {
            // Validate the request
            try await validateRequest(request)
            
            // Process the analysis
            let result = try await performAnalysis(request)
            
            // Complete processing
            await completeProcessing(result)
            
            return result
            
        } catch {
            await handleProcessingError(error)
            throw error
        }
    }
    
    func cancelProcessing() {
        guard processingStatus != .idle else { return }
        
        processingStatus = .idle
        currentRequest = nil
        clearAnalysisBuffer()
        
        print("🚫 Analysis processing cancelled")
    }
    
    // MARK: - Processing Pipeline
    
    private func validateRequest(_ request: ProcessingRequest) async throws {
        processingStatus = .validating
        
        // Validate position
        guard request.position.isValid else {
            throw ChessEngineError.invalidPosition
        }
        
        // Validate depth parameters
        switch request.depth {
        case .depth(let d):
            guard d > 0 && d <= 50 else {
                throw ChessEngineError.invalidPosition
            }
        case .time(let seconds):
            guard seconds > 0 && seconds <= 300 else { // Max 5 minutes
                throw ChessEngineError.analysisTimeout
            }
        case .infinite:
            break // Always valid
        }
        
        print("✅ Analysis request validated")
    }
    
    private func performAnalysis(_ request: ProcessingRequest) async throws -> AnalysisResult {
        processingStatus = .processing
        
        // Initialize partial result
        partialAnalysis = PartialAnalysisResult()
        clearAnalysisBuffer()
        
        // Create mock analysis for now (will be replaced with real engine communication)
        let result = try await simulateEngineAnalysis(request)
        
        return result
    }
    
    private func completeProcessing(_ result: AnalysisResult) async {
        processingStatus = .complete
        lastResult = result
        currentRequest = nil
        
        // Clean up processing state
        partialAnalysis = nil
        clearAnalysisBuffer()
        
        print("✅ Analysis processing complete: \(result.bestMove ?? "no move")")
    }
    
    private func handleProcessingError(_ error: Error) async {
        processingStatus = .error(error.localizedDescription)
        currentRequest = nil
        partialAnalysis = nil
        clearAnalysisBuffer()
        
        print("❌ Analysis processing error: \(error)")
    }
    
    // MARK: - Engine Response Processing
    
    func processEngineOutput(_ output: String) {
        let lines = output.trimmingCharacters(in: .whitespacesAndNewlines)
            .split(separator: "\n")
            .map(String.init)
        
        for line in lines {
            processEngineOutputLine(line)
        }
    }
    
    private func processEngineOutputLine(_ line: String) {
        guard !line.isEmpty else { return }
        
        analysisBuffer.append(line)
        
        let response = UCIParser.parseResponse(line)
        
        switch response {
        case .info(let info):
            updatePartialAnalysis(with: info)
            
        case .bestMove(let move, let ponder):
            finalizeBestMove(move, ponder: ponder)
            
        case .uciOk, .readyOk:
            // Engine status responses - handled elsewhere
            break
            
        case .unknown(let unknownLine):
            print("❓ Unknown engine output: \(unknownLine)")
            
        default:
            print("📋 Engine output: \(line)")
        }
    }
    
    private func updatePartialAnalysis(with info: InfoParameters) {
        guard var partial = partialAnalysis else { return }
        
        // Update depth
        if let depth = info.depth {
            partial.depth = max(partial.depth, depth)
        }
        
        // Update nodes
        if let nodes = info.nodes {
            partial.nodes = nodes
        }
        
        // Update principal variation
        if let pv = info.principalVariation, !pv.isEmpty {
            partial.principalVariation = pv
        }
        
        // Update evaluation
        if let score = info.score {
            partial.evaluation = convertScoreToEvaluation(score)
        }
        
        // Update time
        if let time = info.time {
            partial.analysisTime = time
        }
        
        // Handle multi-PV
        if let multiPV = info.multiPV, let pv = info.principalVariation, !pv.isEmpty {
            updateMultiPVLine(multiPV, pv: pv, score: info.score)
        }
        
        partial.lastUpdate = Date()
        partialAnalysis = partial
        
        // Publish progress if needed
        publishAnalysisProgress()
    }
    
    private func finalizeBestMove(_ move: String, ponder: String?) {
        guard var partial = partialAnalysis else { return }
        
        partial.bestMove = move
        partialAnalysis = partial
        
        print("🎯 Best move received: \(move)" + (ponder != nil ? " (ponder: \(ponder!))" : ""))
    }
    
    // MARK: - Utility Methods
    
    private func convertScoreToEvaluation(_ score: InfoParameters.ScoreInfo) -> EvaluationScore {
        let perspective: EvaluationScore.PlayerPerspective = currentRequest?.position.isWhiteTurn == true ? .white : .black
        
        if let mate = score.mate {
            return EvaluationScore(type: .mate(mate), perspective: perspective)
        } else if let cp = score.centipawns {
            return EvaluationScore(type: .centipawns(cp), perspective: perspective)
        } else {
            return EvaluationScore(type: .unknown, perspective: perspective)
        }
    }
    
    private func updateMultiPVLine(_ lineNumber: Int, pv: [String], score: InfoParameters.ScoreInfo?) {
        guard var partial = partialAnalysis else { return }
        
        let evaluation = score != nil ? convertScoreToEvaluation(score!) : EvaluationScore.equal
        
        let variation = EngineVariation(
            moves: pv,
            evaluation: evaluation,
            depth: partial.depth
        )
        
        // Update or add the multi-PV line
        if lineNumber <= partial.multiPVLines.count {
            if lineNumber == partial.multiPVLines.count + 1 {
                partial.multiPVLines.append(variation)
            } else {
                partial.multiPVLines[lineNumber - 1] = variation
            }
        }
        
        partialAnalysis = partial
    }
    
    private func publishAnalysisProgress() {
        // This could emit progress updates for UI
        // For now, we'll just track the status
        if processingStatus == .processing {
            // Keep processing status
        }
    }
    
    private func clearAnalysisBuffer() {
        analysisBuffer.removeAll()
    }
    
    // MARK: - Mock Analysis (Temporary)
    
    private func simulateEngineAnalysis(_ request: ProcessingRequest) async throws -> AnalysisResult {
        // Simulate processing time
        let processingTime: TimeInterval
        
        switch request.depth {
        case .depth(let d):
            processingTime = min(Double(d) * 0.2, 5.0) // Max 5 seconds
        case .time(let seconds):
            processingTime = min(seconds, 5.0)
        case .infinite:
            processingTime = 2.0 // Short simulation for infinite
        }
        
        try await Task.sleep(nanoseconds: UInt64(processingTime * 1_000_000_000))
        
        // Generate mock result
        let bestMove = generateMockBestMove(for: request.position)
        let evaluation = EvaluationScore(
            type: .centipawns(Int.random(in: -200...200)),
            perspective: request.position.isWhiteTurn ? .white : .black
        )
        
        let result = AnalysisResult(
            position: request.position,
            bestMove: bestMove,
            evaluation: evaluation,
            depth: extractDepthValue(from: request.depth),
            principalVariation: generateMockPV(),
            analysisTime: processingTime,
            nodesSearched: Int.random(in: 50000...500000)
        )
        
        return result
    }
    
    private func generateMockBestMove(for position: ChessPosition) -> String? {
        // Simple mock move generation
        if position.isStartingPosition {
            return ["e2e4", "d2d4", "g1f3", "c2c4"].randomElement()
        } else {
            return ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5", "d2d3", "d7d6"].randomElement()
        }
    }
    
    private func generateMockPV() -> [String] {
        let moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5", "d2d3", "d7d6", "c1e3"]
        let length = Int.random(in: 3...7)
        return Array(moves.prefix(length))
    }
    
    private func extractDepthValue(from depth: AnalysisDepth) -> Int {
        switch depth {
        case .depth(let d):
            return d
        case .time(_):
            return 0
        case .infinite:
            return 99
        }
    }
    
    // MARK: - Setup
    
    private func setupProcessing() {
        // Setup any necessary processing monitoring
        print("🔧 Analysis processor initialized")
    }
    
    // MARK: - Public Properties
    
    var isProcessing: Bool {
        switch processingStatus {
        case .validating, .processing, .parsing:
            return true
        default:
            return false
        }
    }
    
    var processingProgress: String {
        guard let request = currentRequest else {
            return "Ready for analysis"
        }
        
        let elapsed = Date().timeIntervalSince(request.startTime)
        
        switch processingStatus {
        case .idle:
            return "Ready"
        case .validating:
            return "Validating position..."
        case .processing:
            return "Analyzing (\(String(format: "%.1fs", elapsed)))"
        case .parsing:
            return "Processing results..."
        case .complete:
            return "Analysis complete"
        case .error(let message):
            return "Error: \(message)"
        }
    }
    
    var hasResult: Bool {
        return lastResult != nil
    }
}