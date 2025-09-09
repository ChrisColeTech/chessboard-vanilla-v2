// ChessEngineService.swift - Core chess engine communication service
import Foundation
import ChessKitEngine
import SwiftUI
import Combine

@MainActor
class ChessEngineService: ObservableObject {
    @Published private(set) var status: EngineStatus = .notStarted
    @Published private(set) var engineInfo: [String: String] = [:]
    @Published private(set) var availableOptions: [OptionParameter] = []
    
    private var engine: ChessEngine?
    private var engineProcess: Process?
    private var inputPipe: Pipe?
    private var outputPipe: Pipe?
    private var cancellables = Set<AnyCancellable>()
    
    private var pendingCommands: [UCICommand] = []
    private var isProcessingCommands = false
    
    init() {
        setupEngineInitialization()
    }
    
    deinit {
        Task {
            await stopEngine()
        }
    }
    
    // MARK: - Engine Lifecycle
    
    func startEngine() async throws {
        guard status == .notStarted || status == .stopped else {
            throw ChessEngineError.engineNotReady
        }
        
        updateStatus(.starting)
        
        do {
            try await initializeEngine()
            updateStatus(.ready)
        } catch {
            updateStatus(.error(error.localizedDescription))
            throw error
        }
    }
    
    func stopEngine() async {
        guard status != .notStarted && status != .stopped else { return }
        
        if status == .analyzing {
            await sendCommand(.stop)
        }
        
        await sendCommand(.quit)
        
        cleanupEngine()
        updateStatus(.stopped)
    }
    
    func restartEngine() async throws {
        await stopEngine()
        try await Task.sleep(nanoseconds: 500_000_000) // 0.5 second delay
        try await startEngine()
    }
    
    // MARK: - Engine Communication
    
    func sendCommand(_ command: UCICommand) async {
        guard status.isOperational || command == .quit else {
            print("⚠️ Engine not ready for command: \(command.commandString)")
            return
        }
        
        pendingCommands.append(command)
        await processCommandQueue()
    }
    
    private func processCommandQueue() async {
        guard !isProcessingCommands && !pendingCommands.isEmpty else { return }
        
        isProcessingCommands = true
        
        while !pendingCommands.isEmpty {
            let command = pendingCommands.removeFirst()
            await executeCommand(command)
            
            // Small delay between commands to prevent overwhelming the engine
            try? await Task.sleep(nanoseconds: 50_000_000) // 50ms
        }
        
        isProcessingCommands = false
    }
    
    private func executeCommand(_ command: UCICommand) async {
        guard let inputPipe = inputPipe else {
            print("❌ No input pipe available for command: \(command.commandString)")
            return
        }
        
        let commandString = command.commandString + "\n"
        
        do {
            if let data = commandString.data(using: .utf8) {
                try inputPipe.fileHandleForWriting.write(contentsOf: data)
                print("📤 Sent: \(command.commandString)")
            }
        } catch {
            print("❌ Failed to send command \(command.commandString): \(error)")
            updateStatus(.error("Communication failure"))
        }
    }
    
    // MARK: - Engine Initialization
    
    private func setupEngineInitialization() {
        // Engine initialization will be handled when ChessKitEngine package is added
        print("🔧 ChessEngineService initialized - waiting for ChessKitEngine package")
    }
    
    private func initializeEngine() async throws {
        // This will be implemented once ChessKitEngine package is added
        // For now, simulate successful initialization
        
        print("🚀 Initializing chess engine...")
        
        // Simulate engine startup delay
        try await Task.sleep(nanoseconds: 1_000_000_000) // 1 second
        
        // Setup mock engine info for testing
        await MainActor.run {
            engineInfo = [
                "id name": "Stockfish 16",
                "id author": "ChessKit Integration"
            ]
        }
        
        print("✅ Engine initialized successfully")
    }
    
    private func setupEngineProcess() throws {
        // This will create the actual engine process once ChessKitEngine is available
        let process = Process()
        let inputPipe = Pipe()
        let outputPipe = Pipe()
        
        // Store references
        self.engineProcess = process
        self.inputPipe = inputPipe
        self.outputPipe = outputPipe
        
        // Setup output monitoring
        setupOutputMonitoring()
        
        print("🔌 Engine process setup complete")
    }
    
    private func setupOutputMonitoring() {
        guard let outputPipe = outputPipe else { return }
        
        outputPipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            if !data.isEmpty, let output = String(data: data, encoding: .utf8) {
                Task { @MainActor in
                    await self?.processEngineOutput(output)
                }
            }
        }
    }
    
    private func processEngineOutput(_ output: String) async {
        let lines = output.trimmingCharacters(in: .whitespacesAndNewlines)
            .split(separator: "\n")
            .map(String.init)
        
        for line in lines {
            guard !line.isEmpty else { continue }
            
            print("📥 Received: \(line)")
            let response = UCIParser.parseResponse(line)
            await handleEngineResponse(response)
        }
    }
    
    private func handleEngineResponse(_ response: UCIResponse) async {
        switch response {
        case .id(let name, let value):
            engineInfo[name] = value
            
        case .uciOk:
            print("✅ Engine UCI initialization complete")
            
        case .readyOk:
            print("✅ Engine ready for commands")
            
        case .option(let option):
            availableOptions.append(option)
            
        case .bestMove(let move, let ponder):
            print("🎯 Best move: \(move)" + (ponder != nil ? " (ponder: \(ponder!))" : ""))
            
        case .info(let info):
            handleInfoResponse(info)
            
        case .unknown(let line):
            print("❓ Unknown engine response: \(line)")
            
        default:
            print("📋 Engine response: \(response)")
        }
    }
    
    private func handleInfoResponse(_ info: InfoParameters) {
        // Handle analysis info updates
        if let depth = info.depth, let nodes = info.nodes {
            print("📊 Analysis: depth \(depth), nodes \(nodes)")
        }
        
        if let pv = info.principalVariation, !pv.isEmpty {
            print("🔍 Principal variation: \(pv.prefix(5).joined(separator: " "))")
        }
    }
    
    // MARK: - Utility Methods
    
    private func updateStatus(_ newStatus: EngineStatus) {
        guard status != newStatus else { return }
        status = newStatus
        print("🔄 Engine status: \(newStatus.displayName)")
    }
    
    private func cleanupEngine() {
        // Clean up engine resources
        inputPipe?.fileHandleForWriting.closeFile()
        outputPipe?.fileHandleForReading.closeFile()
        
        if let process = engineProcess, process.isRunning {
            process.terminate()
        }
        
        engineProcess = nil
        inputPipe = nil
        outputPipe = nil
        engine = nil
        
        cancellables.removeAll()
        pendingCommands.removeAll()
        isProcessingCommands = false
        
        print("🧹 Engine cleanup complete")
    }
    
    // MARK: - Public Properties
    
    var isReady: Bool {
        return status.isOperational
    }
    
    var canAnalyze: Bool {
        return status == .ready
    }
    
    var engineName: String {
        return engineInfo["id name"] ?? "Unknown Engine"
    }
    
    var engineAuthor: String {
        return engineInfo["id author"] ?? "Unknown Author"
    }
}