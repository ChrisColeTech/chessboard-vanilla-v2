// FileDownloader.swift - Network file download utilities
import Foundation
import Combine

class FileDownloader: NSObject, ObservableObject {
    @Published var downloadProgress: Double = 0
    @Published var downloadState: DownloadState = .idle
    @Published var downloadSpeed: Int64 = 0
    @Published var estimatedTimeRemaining: TimeInterval?
    
    private var downloadTask: URLSessionDownloadTask?
    private var urlSession: URLSession?
    private var startTime: Date?
    private var lastProgressUpdate: Date?
    private var bytesDownloadedAtLastUpdate: Int64 = 0
    
    enum DownloadState: Equatable {
        case idle
        case downloading
        case paused
        case completed(URL)
        case failed(Error)
        
        static func == (lhs: DownloadState, rhs: DownloadState) -> Bool {
            switch (lhs, rhs) {
            case (.idle, .idle), (.downloading, .downloading), (.paused, .paused):
                return true
            case (.completed(let lhsURL), .completed(let rhsURL)):
                return lhsURL == rhsURL
            case (.failed(let lhsError), .failed(let rhsError)):
                return lhsError.localizedDescription == rhsError.localizedDescription
            default:
                return false
            }
        }
        
        var isActive: Bool {
            switch self {
            case .downloading, .paused:
                return true
            default:
                return false
            }
        }
        
        var displayName: String {
            switch self {
            case .idle:
                return "Ready"
            case .downloading:
                return "Downloading"
            case .paused:
                return "Paused"
            case .completed(_):
                return "Completed"
            case .failed(_):
                return "Failed"
            }
        }
    }
    
    struct DownloadInfo {
        let url: String
        let destinationPath: URL
        let expectedSize: Int64?
        let filename: String
        let validateChecksum: String?
        
        init(url: String, destinationPath: URL, expectedSize: Int64? = nil, validateChecksum: String? = nil) {
            self.url = url
            self.destinationPath = destinationPath
            self.expectedSize = expectedSize
            self.filename = destinationPath.lastPathComponent
            self.validateChecksum = validateChecksum
        }
    }
    
    override init() {
        super.init()
        setupURLSession()
    }
    
    deinit {
        cancelDownload()
        urlSession?.invalidateAndCancel()
    }
    
    // MARK: - Download Management
    
    func downloadFile(_ downloadInfo: DownloadInfo) async throws -> URL {
        guard case .idle = downloadState else {
            throw DownloadError.downloadInProgress
        }
        
        guard let url = URL(string: downloadInfo.url) else {
            throw DownloadError.invalidURL
        }
        
        return try await withCheckedThrowingContinuation { continuation in
            startDownload(from: url, to: downloadInfo.destinationPath, expectedSize: downloadInfo.expectedSize) { result in
                continuation.resume(with: result)
            }
        }
    }
    
    private func startDownload(from url: URL, to destinationPath: URL, expectedSize: Int64?, completion: @escaping (Result<URL, Error>) -> Void) {
        
        // Create directory if it doesn't exist
        let directoryURL = destinationPath.deletingLastPathComponent()
        try? FileManager.default.createDirectory(at: directoryURL, withIntermediateDirectories: true)
        
        downloadTask = urlSession?.downloadTask(with: url) { [weak self] tempURL, response, error in
            DispatchQueue.main.async {
                self?.handleDownloadCompletion(tempURL: tempURL, response: response, error: error, destinationPath: destinationPath, completion: completion)
            }
        }
        
        startTime = Date()
        lastProgressUpdate = Date()
        bytesDownloadedAtLastUpdate = 0
        downloadState = .downloading
        
        downloadTask?.resume()
    }
    
    private func handleDownloadCompletion(tempURL: URL?, response: URLResponse?, error: Error?, destinationPath: URL, completion: @escaping (Result<URL, Error>) -> Void) {
        
        if let error = error {
            downloadState = .failed(error)
            completion(.failure(error))
            return
        }
        
        guard let tempURL = tempURL else {
            let error = DownloadError.noDataReceived
            downloadState = .failed(error)
            completion(.failure(error))
            return
        }
        
        do {
            // Remove existing file if it exists
            if FileManager.default.fileExists(atPath: destinationPath.path) {
                try FileManager.default.removeItem(at: destinationPath)
            }
            
            // Move downloaded file to destination
            try FileManager.default.moveItem(at: tempURL, to: destinationPath)
            
            downloadState = .completed(destinationPath)
            completion(.success(destinationPath))
            
            print("✅ File downloaded successfully: \(destinationPath.lastPathComponent)")
            
        } catch {
            downloadState = .failed(error)
            completion(.failure(error))
            print("❌ Failed to move downloaded file: \(error)")
        }
    }
    
    func cancelDownload() {
        downloadTask?.cancel()
        downloadTask = nil
        downloadState = .idle
        downloadProgress = 0
        downloadSpeed = 0
        estimatedTimeRemaining = nil
        
        print("🚫 Download cancelled")
    }
    
    func pauseDownload() {
        downloadTask?.suspend()
        downloadState = .paused
        print("⏸️ Download paused")
    }
    
    func resumeDownload() {
        guard case .paused = downloadState else { return }
        
        downloadTask?.resume()
        downloadState = .downloading
        print("▶️ Download resumed")
    }
    
    // MARK: - URL Session Setup
    
    private func setupURLSession() {
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 60
        configuration.timeoutIntervalForResource = 300 // 5 minutes
        configuration.allowsCellularAccess = true
        
        urlSession = URLSession(configuration: configuration, delegate: self, delegateQueue: nil)
    }
    
    // MARK: - Progress Calculation
    
    private func updateProgress(bytesWritten: Int64, totalBytesWritten: Int64, totalBytesExpectedToWrite: Int64) {
        let progress = totalBytesExpectedToWrite > 0 ? Double(totalBytesWritten) / Double(totalBytesExpectedToWrite) : 0
        
        DispatchQueue.main.async { [weak self] in
            self?.downloadProgress = progress
            self?.updateDownloadSpeed(bytesWritten: bytesWritten, totalBytesWritten: totalBytesWritten, totalBytesExpectedToWrite: totalBytesExpectedToWrite)
        }
    }
    
    private func updateDownloadSpeed(bytesWritten: Int64, totalBytesWritten: Int64, totalBytesExpectedToWrite: Int64) {
        let now = Date()
        
        guard let lastUpdate = lastProgressUpdate else {
            lastProgressUpdate = now
            bytesDownloadedAtLastUpdate = totalBytesWritten
            return
        }
        
        let timeInterval = now.timeIntervalSince(lastUpdate)
        
        // Update speed calculation every second
        if timeInterval >= 1.0 {
            let bytesDownloadedSinceLastUpdate = totalBytesWritten - bytesDownloadedAtLastUpdate
            downloadSpeed = Int64(Double(bytesDownloadedSinceLastUpdate) / timeInterval)
            
            // Calculate estimated time remaining
            if downloadSpeed > 0 && totalBytesExpectedToWrite > totalBytesWritten {
                let bytesRemaining = totalBytesExpectedToWrite - totalBytesWritten
                estimatedTimeRemaining = TimeInterval(bytesRemaining) / TimeInterval(downloadSpeed)
            }
            
            lastProgressUpdate = now
            bytesDownloadedAtLastUpdate = totalBytesWritten
        }
    }
    
    // MARK: - Utility Methods
    
    func validateDownloadedFile(at url: URL, expectedChecksum: String? = nil, expectedSize: Int64? = nil) throws -> Bool {
        let fileManager = FileManager.default
        
        guard fileManager.fileExists(atPath: url.path) else {
            throw DownloadError.fileNotFound
        }
        
        // Validate file size
        if let expectedSize = expectedSize {
            let attributes = try fileManager.attributesOfItem(atPath: url.path)
            let actualSize = attributes[.size] as? Int64 ?? 0
            
            guard actualSize == expectedSize else {
                throw DownloadError.fileSizeMismatch(expected: expectedSize, actual: actualSize)
            }
        }
        
        // Validate checksum if provided
        if let expectedChecksum = expectedChecksum {
            let actualChecksum = try calculateSHA256(for: url)
            
            guard actualChecksum == expectedChecksum else {
                throw DownloadError.checksumMismatch(expected: expectedChecksum, actual: actualChecksum)
            }
        }
        
        return true
    }
    
    private func calculateSHA256(for url: URL) throws -> String {
        let data = try Data(contentsOf: url)
        let hash = SHA256.hash(data: data)
        return hash.compactMap { String(format: "%02x", $0) }.joined()
    }
    
    // MARK: - Public Properties
    
    var isDownloading: Bool {
        return downloadState == .downloading
    }
    
    var canPause: Bool {
        return downloadState == .downloading
    }
    
    var canResume: Bool {
        return downloadState == .paused
    }
    
    var formattedProgress: String {
        return String(format: "%.1f%%", downloadProgress * 100)
    }
    
    var formattedSpeed: String {
        if downloadSpeed < 1024 {
            return "\(downloadSpeed) B/s"
        } else if downloadSpeed < 1024 * 1024 {
            return String(format: "%.1f KB/s", Double(downloadSpeed) / 1024)
        } else {
            return String(format: "%.1f MB/s", Double(downloadSpeed) / (1024 * 1024))
        }
    }
    
    var formattedTimeRemaining: String {
        guard let timeRemaining = estimatedTimeRemaining else {
            return "Unknown"
        }
        
        if timeRemaining < 60 {
            return "\(Int(timeRemaining))s"
        } else if timeRemaining < 3600 {
            return "\(Int(timeRemaining / 60))m \(Int(timeRemaining.truncatingRemainder(dividingBy: 60)))s"
        } else {
            let hours = Int(timeRemaining / 3600)
            let minutes = Int((timeRemaining.truncatingRemainder(dividingBy: 3600)) / 60)
            return "\(hours)h \(minutes)m"
        }
    }
}

// MARK: - URLSessionDownloadDelegate

extension FileDownloader: URLSessionDownloadDelegate {
    
    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didWriteData bytesWritten: Int64, totalBytesWritten: Int64, totalBytesExpectedToWrite: Int64) {
        
        updateProgress(bytesWritten: bytesWritten, totalBytesWritten: totalBytesWritten, totalBytesExpectedToWrite: totalBytesExpectedToWrite)
    }
    
    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didFinishDownloadingTo location: URL) {
        // This is handled in the completion handler of startDownload
    }
    
    func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        if let error = error {
            DispatchQueue.main.async { [weak self] in
                self?.downloadState = .failed(error)
            }
        }
    }
}

// MARK: - Error Types

enum DownloadError: Error, LocalizedError {
    case downloadInProgress
    case invalidURL
    case noDataReceived
    case fileNotFound
    case fileSizeMismatch(expected: Int64, actual: Int64)
    case checksumMismatch(expected: String, actual: String)
    case networkUnavailable
    case insufficientStorage
    
    var errorDescription: String? {
        switch self {
        case .downloadInProgress:
            return "A download is already in progress"
        case .invalidURL:
            return "Invalid download URL"
        case .noDataReceived:
            return "No data received from server"
        case .fileNotFound:
            return "Downloaded file not found"
        case .fileSizeMismatch(let expected, let actual):
            return "File size mismatch: expected \(expected) bytes, got \(actual) bytes"
        case .checksumMismatch(let expected, let actual):
            return "Checksum mismatch: expected \(expected), got \(actual)"
        case .networkUnavailable:
            return "Network connection unavailable"
        case .insufficientStorage:
            return "Insufficient storage space"
        }
    }
}

// MARK: - SHA256 Implementation

import CryptoKit

struct SHA256 {
    static func hash(data: Data) -> Data {
        let digest = CryptoKit.SHA256.hash(data: data)
        return Data(digest)
    }
}