// EngineStatusService.swift - Manages engine status and health monitoring
import Foundation
import SwiftUI
import Combine

@MainActor
class EngineStatusService: ObservableObject {
    @Published private(set) var currentStatus: EngineStatus = .notStarted
    @Published private(set) var isHealthy: Bool = true
    @Published private(set) var lastError: String?
    @Published private(set) var connectionAttempts: Int = 0
    @Published private(set) var uptime: TimeInterval = 0
    
    private var statusHistory: [EngineStatusEntry] = []
    private var healthCheckTimer: Timer?
    private var uptimeTimer: Timer?
    private var startTime: Date?
    private var cancellables = Set<AnyCancellable>()
    
    private weak var engineService: ChessEngineService?
    
    struct EngineStatusEntry {
        let status: EngineStatus
        let timestamp: Date
        let duration: TimeInterval?
        
        init(status: EngineStatus, timestamp: Date = Date(), duration: TimeInterval? = nil) {
            self.status = status
            self.timestamp = timestamp
            self.duration = duration
        }
    }
    
    init(engineService: ChessEngineService? = nil) {
        self.engineService = engineService
        setupStatusMonitoring()
        setupHealthMonitoring()
    }
    
    deinit {
        stopMonitoring()
    }
    
    // MARK: - Status Monitoring
    
    private func setupStatusMonitoring() {
        // Monitor engine service status changes
        engineService?.$status
            .removeDuplicates()
            .sink { [weak self] newStatus in
                Task { @MainActor in
                    self?.handleStatusChange(newStatus)
                }
            }
            .store(in: &cancellables)
    }
    
    private func handleStatusChange(_ newStatus: EngineStatus) {
        let previousStatus = currentStatus
        let now = Date()
        
        // Calculate duration of previous status
        let duration = statusHistory.last?.timestamp.timeIntervalSince(now) ?? 0
        
        // Update current status
        currentStatus = newStatus
        
        // Add entry to history
        let entry = EngineStatusEntry(
            status: previousStatus,
            timestamp: statusHistory.last?.timestamp ?? now,
            duration: abs(duration)
        )
        statusHistory.append(entry)
        
        // Limit history size
        if statusHistory.count > 50 {
            statusHistory.removeFirst()
        }
        
        // Handle specific status changes
        handleSpecificStatusChange(newStatus, previous: previousStatus)
        
        print("📊 Status change: \(previousStatus.displayName) → \(newStatus.displayName)")
    }
    
    private func handleSpecificStatusChange(_ newStatus: EngineStatus, previous: EngineStatus) {
        switch newStatus {
        case .starting:
            connectionAttempts += 1
            startTime = Date()
            startUptimeTimer()
            
        case .ready:
            isHealthy = true
            lastError = nil
            
        case .error(let message):
            isHealthy = false
            lastError = message
            stopUptimeTimer()
            
        case .stopped:
            stopUptimeTimer()
            uptime = 0
            
        default:
            break
        }
    }
    
    // MARK: - Health Monitoring
    
    private func setupHealthMonitoring() {
        // Start periodic health checks
        healthCheckTimer = Timer.scheduledTimer(withTimeInterval: 30.0, repeats: true) { [weak self] _ in
            Task { @MainActor in
                await self?.performHealthCheck()
            }
        }
    }
    
    private func performHealthCheck() async {
        guard let engineService = engineService else { return }
        
        // Check if engine is responsive
        let wasHealthy = isHealthy
        
        switch engineService.status {
        case .ready, .analyzing:
            isHealthy = true
            
        case .error(_):
            isHealthy = false
            
        case .notStarted, .stopped:
            isHealthy = currentStatus == engineService.status
            
        case .starting:
            // Give starting status some time before considering unhealthy
            let startingTime = statusHistory.last(where: { 
                if case .starting = $0.status { return true }
                return false
            })?.timestamp ?? Date()
            
            let timeSinceStarting = Date().timeIntervalSince(startingTime)
            isHealthy = timeSinceStarting < 10.0 // 10 seconds timeout
        }
        
        // Log health status changes
        if wasHealthy != isHealthy {
            print("🏥 Health status changed: \(isHealthy ? "Healthy" : "Unhealthy")")
        }
    }
    
    // MARK: - Uptime Tracking
    
    private func startUptimeTimer() {
        stopUptimeTimer()
        startTime = Date()
        uptime = 0
        
        uptimeTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            Task { @MainActor in
                self?.updateUptime()
            }
        }
    }
    
    private func stopUptimeTimer() {
        uptimeTimer?.invalidate()
        uptimeTimer = nil
    }
    
    private func updateUptime() {
        guard let startTime = startTime else { return }
        uptime = Date().timeIntervalSince(startTime)
    }
    
    // MARK: - Public Interface
    
    func reset() {
        statusHistory.removeAll()
        connectionAttempts = 0
        uptime = 0
        lastError = nil
        isHealthy = true
        startTime = nil
        
        print("🔄 Engine status service reset")
    }
    
    func getStatusHistory() -> [EngineStatusEntry] {
        return statusHistory
    }
    
    func getAverageStatusDuration(for status: EngineStatus) -> TimeInterval {
        let entries = statusHistory.filter { 
            if case status = $0.status { return true }
            return false
        }
        
        let totalDuration = entries.compactMap { $0.duration }.reduce(0, +)
        return entries.isEmpty ? 0 : totalDuration / Double(entries.count)
    }
    
    func getStatusCount(for status: EngineStatus) -> Int {
        return statusHistory.filter { 
            if case status = $0.status { return true }
            return false
        }.count
    }
    
    var formattedUptime: String {
        let hours = Int(uptime) / 3600
        let minutes = Int(uptime) % 3600 / 60
        let seconds = Int(uptime) % 60
        
        if hours > 0 {
            return String(format: "%d:%02d:%02d", hours, minutes, seconds)
        } else {
            return String(format: "%d:%02d", minutes, seconds)
        }
    }
    
    var statusSummary: String {
        switch currentStatus {
        case .notStarted:
            return "Engine not started"
        case .starting:
            return "Starting engine... (attempt \(connectionAttempts))"
        case .ready:
            return "Ready - Uptime: \(formattedUptime)"
        case .analyzing:
            return "Analyzing position - Uptime: \(formattedUptime)"
        case .stopped:
            return "Engine stopped"
        case .error(let message):
            return "Error: \(message)"
        }
    }
    
    var healthIndicator: String {
        if !isHealthy {
            return "🔴 Unhealthy"
        } else {
            switch currentStatus {
            case .ready, .analyzing:
                return "🟢 Healthy"
            case .starting:
                return "🟡 Starting"
            default:
                return "⚫ Inactive"
            }
        }
    }
    
    // MARK: - Cleanup
    
    private func stopMonitoring() {
        healthCheckTimer?.invalidate()
        healthCheckTimer = nil
        
        stopUptimeTimer()
        cancellables.removeAll()
        
        print("🛑 Engine status monitoring stopped")
    }
}