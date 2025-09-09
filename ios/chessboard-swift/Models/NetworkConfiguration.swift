// NetworkConfiguration.swift - NNUE neural network configuration and settings
import Foundation

struct NetworkConfiguration: Codable, Equatable, Identifiable {
    let id = UUID()
    let networkInfo: NetworkInfo
    let engineSettings: EngineSettings
    let performanceSettings: PerformanceSettings
    let createdAt: Date
    let lastUsed: Date?
    
    struct NetworkInfo: Codable, Equatable {
        let name: String
        let filename: String
        let filePath: String
        let fileHash: String?
        let version: String
        let eloRating: Int
        let description: String
        let isBuiltIn: Bool
        let fileSize: Int64
        
        var formattedSize: String {
            let formatter = ByteCountFormatter()
            formatter.allowedUnits = [.useMB, .useGB]
            formatter.countStyle = .file
            return formatter.string(fromByteCount: fileSize)
        }
        
        var strengthDescription: String {
            return "~\(eloRating) Elo"
        }
    }
    
    struct EngineSettings: Codable, Equatable {
        let hashSizeMB: Int
        let threadCount: Int
        let enableNNUE: Bool
        let nnueFilePath: String?
        let contemptValue: Int
        let analysisDepthLimit: Int?
        let analysisTimeLimit: TimeInterval?
        
        static let `default` = EngineSettings(
            hashSizeMB: 128,
            threadCount: 2,
            enableNNUE: true,
            nnueFilePath: nil,
            contemptValue: 0,
            analysisDepthLimit: nil,
            analysisTimeLimit: nil
        )
        
        static let mobile = EngineSettings(
            hashSizeMB: 64,
            threadCount: 1,
            enableNNUE: true,
            nnueFilePath: nil,
            contemptValue: 0,
            analysisDepthLimit: 20,
            analysisTimeLimit: 30.0
        )
        
        static let performance = EngineSettings(
            hashSizeMB: 256,
            threadCount: 4,
            enableNNUE: true,
            nnueFilePath: nil,
            contemptValue: 0,
            analysisDepthLimit: nil,
            analysisTimeLimit: nil
        )
        
        var uciOptions: [String: String] {
            var options: [String: String] = [:]
            
            options["Hash"] = "\(hashSizeMB)"
            options["Threads"] = "\(threadCount)"
            options["Use NNUE"] = enableNNUE ? "true" : "false"
            options["Contempt"] = "\(contemptValue)"
            
            if let nnueFilePath = nnueFilePath {
                options["EvalFile"] = nnueFilePath
            }
            
            return options
        }
    }
    
    struct PerformanceSettings: Codable, Equatable {
        let enableMultiPV: Bool
        let multiPVLines: Int
        let enablePonder: Bool
        let enableOwnBook: Bool
        let bookDepth: Int
        let minimumThinkingTime: TimeInterval
        let maximumThinkingTime: TimeInterval?
        
        static let `default` = PerformanceSettings(
            enableMultiPV: false,
            multiPVLines: 1,
            enablePonder: false,
            enableOwnBook: false,
            bookDepth: 12,
            minimumThinkingTime: 0.1,
            maximumThinkingTime: nil
        )
        
        static let analysis = PerformanceSettings(
            enableMultiPV: true,
            multiPVLines: 3,
            enablePonder: true,
            enableOwnBook: false,
            bookDepth: 20,
            minimumThinkingTime: 0.5,
            maximumThinkingTime: 60.0
        )
        
        static let fastPlay = PerformanceSettings(
            enableMultiPV: false,
            multiPVLines: 1,
            enablePonder: false,
            enableOwnBook: true,
            bookDepth: 8,
            minimumThinkingTime: 0.1,
            maximumThinkingTime: 5.0
        )
        
        var uciOptions: [String: String] {
            var options: [String: String] = [:]
            
            if enableMultiPV {
                options["MultiPV"] = "\(multiPVLines)"
            }
            
            options["Ponder"] = enablePonder ? "true" : "false"
            options["OwnBook"] = enableOwnBook ? "true" : "false"
            
            if enableOwnBook {
                options["Book Depth"] = "\(bookDepth)"
            }
            
            return options
        }
    }
    
    init(networkInfo: NetworkInfo, engineSettings: EngineSettings = .default, performanceSettings: PerformanceSettings = .default) {
        self.networkInfo = networkInfo
        self.engineSettings = engineSettings
        self.performanceSettings = performanceSettings
        self.createdAt = Date()
        self.lastUsed = nil
    }
    
    // MARK: - Configuration Validation
    
    func validate() -> ValidationResult {
        var errors: [ValidationError] = []
        var warnings: [ValidationWarning] = []
        
        // Validate network file exists
        let fileManager = FileManager.default
        if !fileManager.fileExists(atPath: networkInfo.filePath) {
            errors.append(.networkFileNotFound)
        }
        
        // Validate engine settings
        if engineSettings.hashSizeMB < 1 || engineSettings.hashSizeMB > 1024 {
            warnings.append(.hashSizeOutOfRange)
        }
        
        if engineSettings.threadCount < 1 || engineSettings.threadCount > 8 {
            warnings.append(.threadCountSuboptimal)
        }
        
        // Validate performance settings
        if performanceSettings.enableMultiPV && performanceSettings.multiPVLines > 5 {
            warnings.append(.tooManyMultiPVLines)
        }
        
        if let maxTime = performanceSettings.maximumThinkingTime,
           maxTime > 300 { // 5 minutes
            warnings.append(.excessiveThinkingTime)
        }
        
        // Validate device compatibility
        let deviceCapability = DeviceCapabilityAssessor.assessCapability()
        switch deviceCapability {
        case .low:
            if engineSettings.hashSizeMB > 64 {
                warnings.append(.highMemoryUsageOnLowEndDevice)
            }
            if engineSettings.threadCount > 1 {
                warnings.append(.highThreadCountOnLowEndDevice)
            }
        case .medium:
            if engineSettings.hashSizeMB > 256 {
                warnings.append(.highMemoryUsageOnMediumDevice)
            }
        case .high:
            break // High-end device can handle most settings
        }
        
        return ValidationResult(errors: errors, warnings: warnings)
    }
    
    struct ValidationResult {
        let errors: [ValidationError]
        let warnings: [ValidationWarning]
        
        var isValid: Bool {
            return errors.isEmpty
        }
        
        var hasWarnings: Bool {
            return !warnings.isEmpty
        }
        
        var summary: String {
            if !isValid {
                return "Configuration has \(errors.count) error(s)"
            } else if hasWarnings {
                return "Configuration has \(warnings.count) warning(s)"
            } else {
                return "Configuration is valid"
            }
        }
    }
    
    enum ValidationError: Error, LocalizedError {
        case networkFileNotFound
        case invalidNetworkFile
        case incompatibleEngineVersion
        case insufficientMemory
        
        var errorDescription: String? {
            switch self {
            case .networkFileNotFound:
                return "Neural network file not found"
            case .invalidNetworkFile:
                return "Invalid neural network file"
            case .incompatibleEngineVersion:
                return "Incompatible engine version"
            case .insufficientMemory:
                return "Insufficient device memory for configuration"
            }
        }
    }
    
    enum ValidationWarning: LocalizedError {
        case hashSizeOutOfRange
        case threadCountSuboptimal
        case tooManyMultiPVLines
        case excessiveThinkingTime
        case highMemoryUsageOnLowEndDevice
        case highThreadCountOnLowEndDevice
        case highMemoryUsageOnMediumDevice
        
        var errorDescription: String? {
            switch self {
            case .hashSizeOutOfRange:
                return "Hash size should be between 1-1024 MB"
            case .threadCountSuboptimal:
                return "Thread count should be between 1-8"
            case .tooManyMultiPVLines:
                return "Too many Multi-PV lines may impact performance"
            case .excessiveThinkingTime:
                return "Maximum thinking time is very high"
            case .highMemoryUsageOnLowEndDevice:
                return "High memory usage on low-end device"
            case .highThreadCountOnLowEndDevice:
                return "High thread count on low-end device"
            case .highMemoryUsageOnMediumDevice:
                return "High memory usage on medium device"
            }
        }
    }
    
    // MARK: - Configuration Templates
    
    static func createMobileOptimized(networkInfo: NetworkInfo) -> NetworkConfiguration {
        let engineSettings = EngineSettings.mobile
        let performanceSettings = PerformanceSettings.fastPlay
        
        return NetworkConfiguration(
            networkInfo: networkInfo,
            engineSettings: engineSettings,
            performanceSettings: performanceSettings
        )
    }
    
    static func createAnalysisOptimized(networkInfo: NetworkInfo) -> NetworkConfiguration {
        let engineSettings = EngineSettings.performance
        let performanceSettings = PerformanceSettings.analysis
        
        return NetworkConfiguration(
            networkInfo: networkInfo,
            engineSettings: engineSettings,
            performanceSettings: performanceSettings
        )
    }
    
    static func createBalanced(networkInfo: NetworkInfo) -> NetworkConfiguration {
        let engineSettings = EngineSettings.default
        let performanceSettings = PerformanceSettings.default
        
        return NetworkConfiguration(
            networkInfo: networkInfo,
            engineSettings: engineSettings,
            performanceSettings: performanceSettings
        )
    }
    
    // MARK: - Configuration Export/Import
    
    func exportToData() throws -> Data {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        return try encoder.encode(self)
    }
    
    static func importFromData(_ data: Data) throws -> NetworkConfiguration {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode(NetworkConfiguration.self, from: data)
    }
    
    func exportToFile(at url: URL) throws {
        let data = try exportToData()
        try data.write(to: url)
    }
    
    static func importFromFile(at url: URL) throws -> NetworkConfiguration {
        let data = try Data(contentsOf: url)
        return try importFromData(data)
    }
    
    // MARK: - Configuration Comparison
    
    func compareWith(_ other: NetworkConfiguration) -> ConfigurationComparison {
        var differences: [ConfigurationDifference] = []
        
        // Compare network info
        if networkInfo.name != other.networkInfo.name {
            differences.append(.networkName(self: networkInfo.name, other: other.networkInfo.name))
        }
        
        if networkInfo.eloRating != other.networkInfo.eloRating {
            differences.append(.eloRating(self: networkInfo.eloRating, other: other.networkInfo.eloRating))
        }
        
        // Compare engine settings
        if engineSettings.hashSizeMB != other.engineSettings.hashSizeMB {
            differences.append(.hashSize(self: engineSettings.hashSizeMB, other: other.engineSettings.hashSizeMB))
        }
        
        if engineSettings.threadCount != other.engineSettings.threadCount {
            differences.append(.threadCount(self: engineSettings.threadCount, other: other.engineSettings.threadCount))
        }
        
        // Compare performance settings
        if performanceSettings.enableMultiPV != other.performanceSettings.enableMultiPV {
            differences.append(.multiPVEnabled(self: performanceSettings.enableMultiPV, other: other.performanceSettings.enableMultiPV))
        }
        
        return ConfigurationComparison(differences: differences)
    }
    
    struct ConfigurationComparison {
        let differences: [ConfigurationDifference]
        
        var hasDifferences: Bool {
            return !differences.isEmpty
        }
        
        var summary: String {
            if differences.isEmpty {
                return "Configurations are identical"
            } else {
                return "\(differences.count) difference(s) found"
            }
        }
    }
    
    enum ConfigurationDifference {
        case networkName(self: String, other: String)
        case eloRating(self: Int, other: Int)
        case hashSize(self: Int, other: Int)
        case threadCount(self: Int, other: Int)
        case multiPVEnabled(self: Bool, other: Bool)
        
        var description: String {
            switch self {
            case .networkName(let selfValue, let otherValue):
                return "Network name: '\(selfValue)' vs '\(otherValue)'"
            case .eloRating(let selfValue, let otherValue):
                return "Elo rating: \(selfValue) vs \(otherValue)"
            case .hashSize(let selfValue, let otherValue):
                return "Hash size: \(selfValue)MB vs \(otherValue)MB"
            case .threadCount(let selfValue, let otherValue):
                return "Thread count: \(selfValue) vs \(otherValue)"
            case .multiPVEnabled(let selfValue, let otherValue):
                return "Multi-PV: \(selfValue) vs \(otherValue)"
            }
        }
    }
    
    // MARK: - Helper Methods
    
    var displayName: String {
        return "\(networkInfo.name) Configuration"
    }
    
    var strengthEstimate: String {
        return networkInfo.strengthDescription
    }
    
    var memoryFootprint: String {
        let totalMB = engineSettings.hashSizeMB + Int(networkInfo.fileSize / 1_048_576)
        return "\(totalMB) MB"
    }
    
    var isOptimalForDevice: Bool {
        let validation = validate()
        return validation.isValid && !validation.hasWarnings
    }
    
    mutating func updateLastUsed() {
        let updatedConfig = NetworkConfiguration(
            networkInfo: self.networkInfo,
            engineSettings: self.engineSettings,
            performanceSettings: self.performanceSettings
        )
        self = NetworkConfiguration(
            id: self.id,
            networkInfo: self.networkInfo,
            engineSettings: self.engineSettings,
            performanceSettings: self.performanceSettings,
            createdAt: self.createdAt,
            lastUsed: Date()
        )
    }
    
    private init(id: UUID, networkInfo: NetworkInfo, engineSettings: EngineSettings, performanceSettings: PerformanceSettings, createdAt: Date, lastUsed: Date?) {
        self.id = id
        self.networkInfo = networkInfo
        self.engineSettings = engineSettings
        self.performanceSettings = performanceSettings
        self.createdAt = createdAt
        self.lastUsed = lastUsed
    }
}