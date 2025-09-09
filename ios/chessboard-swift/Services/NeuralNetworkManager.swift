// NeuralNetworkManager.swift - NNUE neural network file management
import Foundation
import SwiftUI
import Combine

@MainActor
class NeuralNetworkManager: ObservableObject {
    @Published private(set) var networkStatus: NetworkStatus = .notLoaded
    @Published private(set) var downloadProgress: Double = 0
    @Published private(set) var availableNetworks: [NetworkInfo] = []
    @Published private(set) var currentNetwork: NetworkInfo?
    @Published private(set) var lastError: String?
    
    private var cancellables = Set<AnyCancellable>()
    private let fileManager = FileManager.default
    private var downloadTask: URLSessionDownloadTask?
    
    enum NetworkStatus: Equatable {
        case notLoaded
        case loading
        case loaded(NetworkInfo)
        case downloading
        case failed(String)
        
        var isReady: Bool {
            if case .loaded(_) = self { return true }
            return false
        }
        
        var displayName: String {
            switch self {
            case .notLoaded: return "No Network Loaded"
            case .loading: return "Loading Network..."
            case .loaded(let info): return "Loaded: \(info.name)"
            case .downloading: return "Downloading..."
            case .failed(let error): return "Failed: \(error)"
            }
        }
    }
    
    struct NetworkInfo: Identifiable, Equatable {
        let id = UUID()
        let name: String
        let filename: String
        let fileSize: Int64
        let elo: Int
        let description: String
        let downloadURL: String?
        let localPath: URL?
        let isBuiltIn: Bool
        let version: String
        
        var formattedSize: String {
            let formatter = ByteCountFormatter()
            formatter.allowedUnits = [.useMB, .useGB]
            formatter.countStyle = .file
            return formatter.string(fromByteCount: fileSize)
        }
        
        var strengthDescription: String {
            return "~\(elo) Elo"
        }
        
        static let builtInLight = NetworkInfo(
            name: "Stockfish Light",
            filename: "stockfish_light.nnue",
            fileSize: 5_242_880, // ~5MB
            elo: 3200,
            description: "Compact network suitable for mobile devices",
            downloadURL: nil,
            localPath: nil,
            isBuiltIn: true,
            version: "1.0"
        )
        
        static let standardNetwork = NetworkInfo(
            name: "Stockfish Standard",
            filename: "nn-1111cefa1111.nnue",
            fileSize: 52_428_800, // ~50MB
            elo: 3600,
            description: "Full-strength network for optimal play",
            downloadURL: "https://tests.stockfishchess.org/api/nn/nn-1111cefa1111.nnue",
            localPath: nil,
            isBuiltIn: false,
            version: "16.1"
        )
    }
    
    init() {
        setupDefaultNetworks()
        checkForExistingNetworks()
    }
    
    deinit {
        downloadTask?.cancel()
        cancellables.removeAll()
    }
    
    // MARK: - Network Management
    
    func loadBundledNetwork() async throws -> URL {
        networkStatus = .loading
        
        // Simulate loading bundled network
        try await Task.sleep(nanoseconds: 1_000_000_000) // 1 second
        
        guard let bundledNetworkPath = getBundledNetworkPath() else {
            let error = "Bundled network file not found"
            networkStatus = .failed(error)
            lastError = error
            throw NeuralNetworkError.networkFileNotFound
        }
        
        let networkInfo = NetworkInfo.builtInLight
        currentNetwork = networkInfo
        networkStatus = .loaded(networkInfo)
        
        print("✅ Bundled network loaded: \(networkInfo.name)")
        return bundledNetworkPath
    }
    
    func downloadNetworkFile(_ networkInfo: NetworkInfo) async throws -> URL {
        guard let downloadURL = networkInfo.downloadURL else {
            throw NeuralNetworkError.invalidDownloadURL
        }
        
        networkStatus = .downloading
        downloadProgress = 0
        
        do {
            let downloadedPath = try await performNetworkDownload(downloadURL, filename: networkInfo.filename)
            
            // Validate downloaded file
            guard validateNetworkFile(downloadedPath) else {
                try? fileManager.removeItem(at: downloadedPath)
                throw NeuralNetworkError.invalidNetworkFile
            }
            
            // Update network info with local path
            var updatedInfo = networkInfo
            updatedInfo = NetworkInfo(
                name: updatedInfo.name,
                filename: updatedInfo.filename,
                fileSize: updatedInfo.fileSize,
                elo: updatedInfo.elo,
                description: updatedInfo.description,
                downloadURL: updatedInfo.downloadURL,
                localPath: downloadedPath,
                isBuiltIn: false,
                version: updatedInfo.version
            )
            
            currentNetwork = updatedInfo
            networkStatus = .loaded(updatedInfo)
            
            print("✅ Network downloaded and validated: \(networkInfo.name)")
            return downloadedPath
            
        } catch {
            let errorMessage = error.localizedDescription
            networkStatus = .failed(errorMessage)
            lastError = errorMessage
            throw error
        }
    }
    
    func configureEngine(with networkPath: URL) async throws {
        // This would configure the engine with the network file
        // For now, simulate configuration
        try await Task.sleep(nanoseconds: 500_000_000) // 0.5 seconds
        
        print("⚙️ Engine configured with network: \(networkPath.lastPathComponent)")
    }
    
    func validateNetworkFile(_ url: URL) -> Bool {
        guard fileManager.fileExists(atPath: url.path) else {
            return false
        }
        
        do {
            let attributes = try fileManager.attributesOfItem(atPath: url.path)
            let fileSize = attributes[.size] as? Int64 ?? 0
            
            // Basic validation - NNUE files should be substantial in size
            guard fileSize > 1_000_000 else { // At least 1MB
                print("❌ Network file too small: \(fileSize) bytes")
                return false
            }
            
            // Check file extension
            guard url.pathExtension.lowercased() == "nnue" else {
                print("❌ Invalid file extension: \(url.pathExtension)")
                return false
            }
            
            // Additional validation could check file headers, etc.
            print("✅ Network file validated: \(fileSize) bytes")
            return true
            
        } catch {
            print("❌ Error validating network file: \(error)")
            return false
        }
    }
    
    // MARK: - Network Discovery
    
    private func setupDefaultNetworks() {
        availableNetworks = [
            .builtInLight,
            .standardNetwork
        ]
    }
    
    private func checkForExistingNetworks() {
        Task {
            // Check if any networks are already downloaded
            let documentsPath = getNetworksDirectory()
            
            do {
                let contents = try fileManager.contentsOfDirectory(at: documentsPath, includingPropertiesForKeys: [.fileSizeKey])
                
                for fileURL in contents where fileURL.pathExtension == "nnue" {
                    if let networkInfo = createNetworkInfoFromFile(fileURL) {
                        await MainActor.run {
                            if !availableNetworks.contains(where: { $0.filename == networkInfo.filename }) {
                                availableNetworks.append(networkInfo)
                            }
                        }
                    }
                }
            } catch {
                print("❌ Error checking existing networks: \(error)")
            }
        }
    }
    
    private func createNetworkInfoFromFile(_ fileURL: URL) -> NetworkInfo? {
        do {
            let attributes = try fileManager.attributesOfItem(atPath: fileURL.path)
            let fileSize = attributes[.size] as? Int64 ?? 0
            
            return NetworkInfo(
                name: "Custom Network",
                filename: fileURL.lastPathComponent,
                fileSize: fileSize,
                elo: 3400, // Default estimate
                description: "Locally stored network file",
                downloadURL: nil,
                localPath: fileURL,
                isBuiltIn: false,
                version: "Unknown"
            )
        } catch {
            return nil
        }
    }
    
    // MARK: - File Management
    
    private func getBundledNetworkPath() -> URL? {
        // In a real implementation, this would return the bundled network file
        // For now, simulate that we have a bundled network
        let documentsPath = getNetworksDirectory()
        return documentsPath.appendingPathComponent("bundled_light.nnue")
    }
    
    private func getNetworksDirectory() -> URL {
        let documentsPath = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!
        let networksPath = documentsPath.appendingPathComponent("NeuralNetworks")
        
        // Create directory if it doesn't exist
        try? fileManager.createDirectory(at: networksPath, withIntermediateDirectories: true)
        
        return networksPath
    }
    
    private func performNetworkDownload(_ urlString: String, filename: String) async throws -> URL {
        guard let url = URL(string: urlString) else {
            throw NeuralNetworkError.invalidDownloadURL
        }
        
        let destinationPath = getNetworksDirectory().appendingPathComponent(filename)
        
        // Simulate download for now (in real implementation, would use URLSession)
        for i in 1...10 {
            try await Task.sleep(nanoseconds: 200_000_000) // 0.2 seconds
            await MainActor.run {
                downloadProgress = Double(i) / 10.0
            }
        }
        
        // Create a placeholder file for testing
        let placeholderData = Data(count: 5_242_880) // 5MB placeholder
        try placeholderData.write(to: destinationPath)
        
        return destinationPath
    }
    
    // MARK: - Network Operations
    
    func switchToNetwork(_ networkInfo: NetworkInfo) async throws {
        if networkInfo.isBuiltIn {
            _ = try await loadBundledNetwork()
        } else if let localPath = networkInfo.localPath {
            guard validateNetworkFile(localPath) else {
                throw NeuralNetworkError.invalidNetworkFile
            }
            currentNetwork = networkInfo
            networkStatus = .loaded(networkInfo)
            try await configureEngine(with: localPath)
        } else {
            _ = try await downloadNetworkFile(networkInfo)
        }
    }
    
    func deleteNetwork(_ networkInfo: NetworkInfo) throws {
        guard !networkInfo.isBuiltIn else {
            throw NeuralNetworkError.cannotDeleteBuiltIn
        }
        
        guard let localPath = networkInfo.localPath else {
            throw NeuralNetworkError.networkFileNotFound
        }
        
        try fileManager.removeItem(at: localPath)
        
        // Remove from available networks
        availableNetworks.removeAll { $0.id == networkInfo.id }
        
        // If this was the current network, reset status
        if currentNetwork?.id == networkInfo.id {
            currentNetwork = nil
            networkStatus = .notLoaded
        }
        
        print("🗑️ Deleted network: \(networkInfo.name)")
    }
    
    func cancelDownload() {
        downloadTask?.cancel()
        downloadTask = nil
        networkStatus = .notLoaded
        downloadProgress = 0
        print("🚫 Network download cancelled")
    }
    
    // MARK: - Utility Methods
    
    func getNetworkStrengthEstimate(_ networkInfo: NetworkInfo) -> String {
        return "Approximately \(networkInfo.elo) Elo strength"
    }
    
    func getRecommendedNetwork() -> NetworkInfo {
        // Recommend based on device capabilities
        let deviceCapability = DeviceCapabilityAssessor.assessCapability()
        
        switch deviceCapability {
        case .low:
            return .builtInLight
        case .medium, .high:
            return .standardNetwork
        }
    }
    
    var networkLoadStatus: String {
        switch networkStatus {
        case .notLoaded:
            return "No neural network loaded. Engine will use standard evaluation."
        case .loading:
            return "Loading neural network..."
        case .loaded(let info):
            return "Neural network active: \(info.name) (\(info.strengthDescription))"
        case .downloading:
            return "Downloading neural network... \(Int(downloadProgress * 100))%"
        case .failed(let error):
            return "Network load failed: \(error)"
        }
    }
    
    var hasActiveNetwork: Bool {
        return networkStatus.isReady
    }
    
    var downloadProgressPercent: String {
        return "\(Int(downloadProgress * 100))%"
    }
}

// MARK: - Supporting Types

enum NeuralNetworkError: Error, LocalizedError {
    case networkFileNotFound
    case invalidNetworkFile
    case downloadFailed
    case invalidDownloadURL
    case cannotDeleteBuiltIn
    case configurationFailed
    
    var errorDescription: String? {
        switch self {
        case .networkFileNotFound:
            return "Neural network file not found"
        case .invalidNetworkFile:
            return "Invalid neural network file"
        case .downloadFailed:
            return "Failed to download neural network"
        case .invalidDownloadURL:
            return "Invalid download URL"
        case .cannotDeleteBuiltIn:
            return "Cannot delete built-in network"
        case .configurationFailed:
            return "Failed to configure engine with network"
        }
    }
}

enum DeviceCapabilityAssessor {
    enum Capability {
        case low, medium, high
    }
    
    static func assessCapability() -> Capability {
        let processorCount = ProcessInfo.processInfo.processorCount
        let physicalMemory = ProcessInfo.processInfo.physicalMemory
        
        // Simple heuristic based on device specs
        if processorCount >= 8 && physicalMemory >= 6_000_000_000 { // 6GB+
            return .high
        } else if processorCount >= 4 && physicalMemory >= 3_000_000_000 { // 3GB+
            return .medium
        } else {
            return .low
        }
    }
}