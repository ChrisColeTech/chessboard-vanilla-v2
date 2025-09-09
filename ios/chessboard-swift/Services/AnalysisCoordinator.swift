// AnalysisCoordinator.swift - Coordinates chess position analysis workflows
import Foundation
import SwiftUI
import Combine

@MainActor
class AnalysisCoordinator: ObservableObject {
    @Published private(set) var currentAnalysis: AnalysisResult?
    @Published private(set) var isAnalyzing: Bool = false
    @Published private(set) var analysisQueue: [AnalysisRequest] = []
    @Published private(set) var analysisHistory: [AnalysisResult] = []
    
    private let engineService: ChessEngineService
    private let statusService: EngineStatusService
    private var cancellables = Set<AnyCancellable>()
    
    private var currentRequest: AnalysisRequest?
    private var analysisStartTime: Date?
    
    struct AnalysisRequest: Identifiable, Equatable {
        let id = UUID()
        let position: ChessPosition
        let depth: AnalysisDepth
        let priority: AnalysisPriority
        let timestamp: Date
        
        enum AnalysisPriority: Int, CaseIterable {
            case low = 0
            case normal = 1
            case high = 2
            case urgent = 3
            
            var displayName: String {
                switch self {
                case .low: return "Low"
                case .normal: return "Normal"
                case .high: return "High"
                case .urgent: return "Urgent"
                }
            }
        }
        
        init(position: ChessPosition, depth: AnalysisDepth, priority: AnalysisPriority = .normal) {
            self.position = position
            self.depth = depth
            self.priority = priority
            self.timestamp = Date()
        }
        
        static func == (lhs: AnalysisRequest, rhs: AnalysisRequest) -> Bool {
            return lhs.id == rhs.id
        }
    }
    
    init(engineService: ChessEngineService, statusService: EngineStatusService) {
        self.engineService = engineService
        self.statusService = statusService
        
        setupAnalysisMonitoring()
    }
    
    deinit {
        cancellables.removeAll()
    }
    
    // MARK: - Analysis Management
    
    func analyzePosition(_ position: ChessPosition, depth: AnalysisDepth, priority: AnalysisRequest.AnalysisPriority = .normal) async {
        let request = AnalysisRequest(position: position, depth: depth, priority: priority)
        
        // Add to queue in priority order
        insertRequestInQueue(request)
        
        // Process queue if not already analyzing
        await processAnalysisQueue()
    }
    
    func stopCurrentAnalysis() async {
        guard isAnalyzing else { return }
        
        await engineService.sendCommand(.stop)
        await completeCurrentAnalysis(cancelled: true)
    }
    
    func clearQueue() {
        analysisQueue.removeAll()
        print("🗑️ Analysis queue cleared")
    }
    
    func removeFromQueue(_ request: AnalysisRequest) {
        analysisQueue.removeAll { $0.id == request.id }
    }
    
    // MARK: - Queue Management
    
    private func insertRequestInQueue(_ request: AnalysisRequest) {
        // Find insertion point based on priority
        let insertionIndex = analysisQueue.firstIndex { existingRequest in
            existingRequest.priority.rawValue < request.priority.rawValue
        } ?? analysisQueue.count
        
        analysisQueue.insert(request, at: insertionIndex)
        
        print("📥 Added analysis request: \(request.position.displayText) (Priority: \(request.priority.displayName))")
        print("📊 Queue size: \(analysisQueue.count)")
    }
    
    private func processAnalysisQueue() async {
        guard !isAnalyzing && !analysisQueue.isEmpty else { return }
        
        guard engineService.canAnalyze else {
            print("⚠️ Engine not ready for analysis")
            return
        }
        
        let request = analysisQueue.removeFirst()
        currentRequest = request
        
        await startAnalysis(request)
    }
    
    // MARK: - Analysis Execution
    
    private func startAnalysis(_ request: AnalysisRequest) async {
        isAnalyzing = true
        analysisStartTime = Date()
        currentRequest = request
        
        print("🔍 Starting analysis: \(request.position.displayText)")
        
        // Set up position
        await engineService.sendCommand(.position(fen: request.position.fen, moves: []))
        
        // Start analysis based on depth type
        let goCommand = createGoCommand(for: request.depth)
        await engineService.sendCommand(goCommand)
        
        // Set up timeout handling
        setupAnalysisTimeout(for: request)
    }
    
    private func createGoCommand(for depth: AnalysisDepth) -> UCICommand {
        switch depth {
        case .depth(let d):
            return .go(parameters: GoParameters.depth(d))
        case .time(let seconds):
            return .go(parameters: GoParameters.time(seconds))
        case .infinite:
            return .go(parameters: GoParameters.infinite)
        }
    }
    
    private func setupAnalysisTimeout(for request: AnalysisRequest) {
        let timeoutDuration: TimeInterval
        
        switch request.depth {
        case .depth(let d):
            // Estimate timeout based on depth (rough calculation)
            timeoutDuration = max(10.0, Double(d) * 2.0)
        case .time(let seconds):
            // Add buffer time
            timeoutDuration = seconds + 5.0
        case .infinite:
            return // No timeout for infinite analysis
        }
        
        Task {
            try? await Task.sleep(nanoseconds: UInt64(timeoutDuration * 1_000_000_000))
            
            if let currentReq = currentRequest, currentReq.id == request.id && isAnalyzing {
                print("⏰ Analysis timeout for request: \(request.id)")
                await stopCurrentAnalysis()
            }
        }
    }
    
    private func completeCurrentAnalysis(cancelled: Bool = false) async {
        guard let request = currentRequest else { return }
        
        isAnalyzing = false
        
        if !cancelled {
            // Create analysis result from current engine state
            let result = createAnalysisResult(from: request)
            
            currentAnalysis = result
            analysisHistory.append(result)
            
            // Limit history size
            if analysisHistory.count > 100 {
                analysisHistory.removeFirst()
            }
            
            print("✅ Analysis complete: \(result.bestMove ?? "no move") in \(result.formattedTime)")
        } else {
            print("❌ Analysis cancelled")
        }
        
        currentRequest = nil
        analysisStartTime = nil
        
        // Process next in queue
        await processAnalysisQueue()
    }
    
    private func createAnalysisResult(from request: AnalysisRequest) -> AnalysisResult {
        let analysisTime = analysisStartTime?.timeIntervalSinceNow.magnitude ?? 0
        
        // For now, create a mock result until engine integration is complete
        let result = AnalysisResult(
            position: request.position,
            bestMove: generateMockBestMove(for: request.position),
            evaluation: EvaluationScore(type: .centipawns(Int.random(in: -100...100)), perspective: request.position.isWhiteTurn ? .white : .black),
            depth: extractDepthValue(from: request.depth),
            principalVariation: generateMockPrincipalVariation(),
            analysisTime: analysisTime,
            nodesSearched: Int.random(in: 10000...500000)
        )
        
        return result
    }
    
    // MARK: - Analysis Monitoring
    
    private func setupAnalysisMonitoring() {
        // Monitor engine status for analysis completion
        engineService.$status
            .sink { [weak self] status in
                Task { @MainActor in
                    await self?.handleEngineStatusChange(status)
                }
            }
            .store(in: &cancellables)
    }
    
    private func handleEngineStatusChange(_ status: EngineStatus) async {
        switch status {
        case .ready:
            // Engine became ready, might have finished analysis
            if isAnalyzing {
                await completeCurrentAnalysis()
            }
        case .error(_):
            // Handle analysis error
            if isAnalyzing {
                await completeCurrentAnalysis(cancelled: true)
            }
        case .stopped:
            // Engine stopped, cancel any ongoing analysis
            if isAnalyzing {
                await completeCurrentAnalysis(cancelled: true)
            }
        default:
            break
        }
    }
    
    // MARK: - Utility Methods
    
    private func extractDepthValue(from depth: AnalysisDepth) -> Int {
        switch depth {
        case .depth(let d):
            return d
        case .time(_):
            return 0 // Time-based analysis, depth will be determined by engine
        case .infinite:
            return 99 // Represent infinite as high depth
        }
    }
    
    private func generateMockBestMove(for position: ChessPosition) -> String? {
        // Generate a simple mock move for testing
        let commonMoves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"]
        return commonMoves.randomElement()
    }
    
    private func generateMockPrincipalVariation() -> [String] {
        let moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]
        return Array(moves.prefix(Int.random(in: 2...5)))
    }
    
    // MARK: - Public Properties
    
    var queueCount: Int {
        return analysisQueue.count
    }
    
    var hasHistory: Bool {
        return !analysisHistory.isEmpty
    }
    
    var recentAnalysis: [AnalysisResult] {
        return Array(analysisHistory.suffix(10))
    }
    
    var isQueueEmpty: Bool {
        return analysisQueue.isEmpty
    }
    
    var nextInQueue: AnalysisRequest? {
        return analysisQueue.first
    }
    
    var analysisProgress: String {
        if let request = currentRequest {
            let elapsed = analysisStartTime?.timeIntervalSinceNow.magnitude ?? 0
            return "Analyzing \(request.position.displayText) (\(String(format: "%.1fs", elapsed)))"
        } else if !analysisQueue.isEmpty {
            return "Queue: \(analysisQueue.count) positions"
        } else {
            return "Ready for analysis"
        }
    }
}