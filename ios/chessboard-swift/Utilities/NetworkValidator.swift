// NetworkValidator.swift - Validate NNUE neural network files
import Foundation
import CryptoKit

class NetworkValidator {
    
    // MARK: - Validation Types
    
    struct ValidationResult {
        let isValid: Bool
        let validationScore: Double // 0.0 to 1.0
        let errors: [ValidationError]
        let warnings: [ValidationWarning]
        let metadata: NetworkMetadata?
        
        var summary: String {
            if isValid {
                return "Valid network file (\(String(format: "%.1f%%", validationScore * 100)))"
            } else {
                return "\(errors.count) validation error(s)"
            }
        }
        
        var hasWarnings: Bool {
            return !warnings.isEmpty
        }
        
        var canUseNetwork: Bool {
            return isValid && validationScore >= 0.7
        }
    }
    
    struct NetworkMetadata {
        let fileSize: Int64
        let creationDate: Date?
        let checksum: String
        let version: String?
        let architecture: NetworkArchitecture?
        let inputFeatures: Int?
        let outputNodes: Int?
        let estimatedEloGain: Int?
        
        enum NetworkArchitecture: String, CaseIterable {
            case nnue = "NNUE"
            case traditional = "Traditional"
            case hybrid = "Hybrid"
            case unknown = "Unknown"
            
            var description: String {
                switch self {
                case .nnue: return "NNUE (Efficiently Updatable Neural Network)"
                case .traditional: return "Traditional Evaluation"
                case .hybrid: return "Hybrid (Neural + Traditional)"
                case .unknown: return "Unknown Architecture"
                }
            }
        }
    }
    
    enum ValidationError: Error, LocalizedError {
        case fileNotFound
        case fileTooSmall
        case fileTooLarge
        case invalidFileFormat
        case corruptedHeader
        case unsupportedVersion
        case incompatibleArchitecture
        case checksumMismatch
        case insufficientMetadata
        
        var errorDescription: String? {
            switch self {
            case .fileNotFound:
                return "Network file not found"
            case .fileTooSmall:
                return "File too small to be a valid network"
            case .fileTooLarge:
                return "File too large (may not be a network file)"
            case .invalidFileFormat:
                return "Invalid network file format"
            case .corruptedHeader:
                return "Network file header is corrupted"
            case .unsupportedVersion:
                return "Unsupported network version"
            case .incompatibleArchitecture:
                return "Incompatible network architecture"
            case .checksumMismatch:
                return "File checksum validation failed"
            case .insufficientMetadata:
                return "Insufficient network metadata"
            }
        }
    }
    
    enum ValidationWarning: LocalizedError {
        case oldVersion
        case largeFileSize
        case unknownOrigin
        case missingOptimizations
        case suboptimalForDevice
        
        var errorDescription: String? {
            switch self {
            case .oldVersion:
                return "Network uses an older version format"
            case .largeFileSize:
                return "Large file size may impact performance"
            case .unknownOrigin:
                return "Network origin/source unknown"
            case .missingOptimizations:
                return "Network may lack mobile optimizations"
            case .suboptimalForDevice:
                return "Network may not be optimal for this device"
            }
        }
    }
    
    // MARK: - Validation Methods
    
    static func validateNetworkFile(at url: URL, expectedChecksum: String? = nil) -> ValidationResult {
        var errors: [ValidationError] = []
        var warnings: [ValidationWarning] = []
        var validationScore: Double = 0.0
        var metadata: NetworkMetadata?
        
        // Check file exists
        guard FileManager.default.fileExists(atPath: url.path) else {
            errors.append(.fileNotFound)
            return ValidationResult(isValid: false, validationScore: 0, errors: errors, warnings: warnings, metadata: nil)
        }
        
        do {
            // Get file attributes
            let attributes = try FileManager.default.attributesOfItem(atPath: url.path)
            let fileSize = attributes[.size] as? Int64 ?? 0
            let creationDate = attributes[.creationDate] as? Date
            
            // Validate file size
            let sizeValidation = validateFileSize(fileSize)
            errors.append(contentsOf: sizeValidation.errors)
            warnings.append(contentsOf: sizeValidation.warnings)
            validationScore += sizeValidation.score
            
            // Read and validate file content
            let fileData = try Data(contentsOf: url)
            let contentValidation = validateFileContent(fileData)
            errors.append(contentsOf: contentValidation.errors)
            warnings.append(contentsOf: contentValidation.warnings)
            validationScore += contentValidation.score
            
            // Calculate checksum
            let checksum = calculateSHA256(data: fileData)
            
            // Validate checksum if provided
            if let expectedChecksum = expectedChecksum {
                if checksum != expectedChecksum {
                    errors.append(.checksumMismatch)
                } else {
                    validationScore += 0.2
                }
            }
            
            // Extract metadata
            metadata = extractMetadata(from: fileData, fileSize: fileSize, creationDate: creationDate, checksum: checksum)
            
            // Validate metadata
            if let meta = metadata {
                let metadataValidation = validateMetadata(meta)
                warnings.append(contentsOf: metadataValidation.warnings)
                validationScore += metadataValidation.score
            } else {
                errors.append(.insufficientMetadata)
            }
            
        } catch {
            errors.append(.fileNotFound)
        }
        
        // Normalize validation score
        validationScore = min(1.0, max(0.0, validationScore / 3.0))
        
        let isValid = errors.isEmpty
        return ValidationResult(
            isValid: isValid,
            validationScore: validationScore,
            errors: errors,
            warnings: warnings,
            metadata: metadata
        )
    }
    
    // MARK: - File Size Validation
    
    private static func validateFileSize(_ fileSize: Int64) -> (errors: [ValidationError], warnings: [ValidationWarning], score: Double) {
        var errors: [ValidationError] = []
        var warnings: [ValidationWarning] = []
        var score: Double = 0.0
        
        // NNUE networks typically range from 5MB to 100MB
        let minSize: Int64 = 1_048_576 // 1MB minimum
        let maxSize: Int64 = 104_857_600 // 100MB maximum
        let optimalMinSize: Int64 = 5_242_880 // 5MB
        let optimalMaxSize: Int64 = 52_428_800 // 50MB
        
        if fileSize < minSize {
            errors.append(.fileTooSmall)
        } else if fileSize > maxSize {
            errors.append(.fileTooLarge)
        } else {
            score = 0.5
            
            if fileSize >= optimalMinSize && fileSize <= optimalMaxSize {
                score = 1.0
            } else if fileSize > optimalMaxSize {
                warnings.append(.largeFileSize)
                score = 0.7
            }
        }
        
        return (errors, warnings, score)
    }
    
    // MARK: - File Content Validation
    
    private static func validateFileContent(_ data: Data) -> (errors: [ValidationError], warnings: [ValidationWarning], score: Double) {
        var errors: [ValidationError] = []
        var warnings: [ValidationWarning] = []
        var score: Double = 0.0
        
        // Check minimum data length
        guard data.count >= 1024 else {
            errors.append(.invalidFileFormat)
            return (errors, warnings, 0.0)
        }
        
        // Check for NNUE magic header
        let magicNumbers = extractMagicNumbers(from: data)
        if validateNNUEMagicNumbers(magicNumbers) {
            score += 0.8
        } else {
            // Try alternative validation methods
            if validateAlternativeFormat(data) {
                score += 0.5
                warnings.append(.unknownOrigin)
            } else {
                errors.append(.invalidFileFormat)
                return (errors, warnings, 0.0)
            }
        }
        
        // Validate data structure integrity
        if validateDataStructure(data) {
            score += 0.2
        } else {
            warnings.append(.missingOptimizations)
        }
        
        return (errors, warnings, score)
    }
    
    private static func extractMagicNumbers(from data: Data) -> [UInt8] {
        guard data.count >= 16 else { return [] }
        return Array(data.prefix(16))
    }
    
    private static func validateNNUEMagicNumbers(_ magicNumbers: [UInt8]) -> Bool {
        // Common NNUE magic number patterns
        let knownMagicPatterns = [
            [0x7F, 0x45, 0x4C, 0x46], // Common NNUE pattern
            [0x4E, 0x4E, 0x55, 0x45], // "NNUE" ASCII
            [0xFF, 0xFE, 0xFD, 0xFC]  // Alternative pattern
        ]
        
        for pattern in knownMagicPatterns {
            if magicNumbers.prefix(pattern.count).elementsEqual(pattern) {
                return true
            }
        }
        
        // Check for binary patterns that suggest neural network data
        let hasVariedBytes = Set(magicNumbers.prefix(8)).count >= 4
        let hasReasonableRange = magicNumbers.prefix(8).allSatisfy { $0 != 0x00 && $0 != 0xFF }
        
        return hasVariedBytes && hasReasonableRange
    }
    
    private static func validateAlternativeFormat(_ data: Data) -> Bool {
        // Try to validate as alternative network format
        // This is a simplified check for demonstration
        let entropy = calculateEntropy(data.prefix(1024))
        return entropy > 0.5 && entropy < 0.9 // Neural network data typically has moderate entropy
    }
    
    private static func validateDataStructure(_ data: Data) -> Bool {
        // Simplified structure validation
        // Real implementation would check layer structures, weights, etc.
        let chunkSize = 1024
        var validChunks = 0
        
        for i in stride(from: 0, to: data.count, by: chunkSize) {
            let endIndex = min(i + chunkSize, data.count)
            let chunk = data[i..<endIndex]
            
            if validateChunk(chunk) {
                validChunks += 1
            }
        }
        
        let validChunkRatio = Double(validChunks) / Double((data.count + chunkSize - 1) / chunkSize)
        return validChunkRatio > 0.8
    }
    
    private static func validateChunk(_ chunk: Data) -> Bool {
        // Check for reasonable data distribution
        let entropy = calculateEntropy(chunk)
        return entropy > 0.3 && entropy < 0.8
    }
    
    private static func calculateEntropy(_ data: Data) -> Double {
        var counts = Array(repeating: 0, count: 256)
        
        for byte in data {
            counts[Int(byte)] += 1
        }
        
        let length = Double(data.count)
        var entropy = 0.0
        
        for count in counts {
            if count > 0 {
                let probability = Double(count) / length
                entropy -= probability * log2(probability)
            }
        }
        
        return entropy / 8.0 // Normalize to 0-1 range
    }
    
    // MARK: - Metadata Extraction
    
    private static func extractMetadata(from data: Data, fileSize: Int64, creationDate: Date?, checksum: String) -> NetworkMetadata? {
        
        // Extract version information (simplified)
        let version = extractVersion(from: data)
        
        // Determine architecture
        let architecture = determineArchitecture(from: data)
        
        // Estimate network parameters
        let inputFeatures = estimateInputFeatures(from: data)
        let outputNodes = estimateOutputNodes(from: data)
        
        // Estimate Elo gain (simplified calculation)
        let estimatedEloGain = estimateEloGain(fileSize: fileSize, architecture: architecture)
        
        return NetworkMetadata(
            fileSize: fileSize,
            creationDate: creationDate,
            checksum: checksum,
            version: version,
            architecture: architecture,
            inputFeatures: inputFeatures,
            outputNodes: outputNodes,
            estimatedEloGain: estimatedEloGain
        )
    }
    
    private static func extractVersion(from data: Data) -> String? {
        // Simplified version extraction
        guard data.count > 100 else { return nil }
        
        // Look for version patterns in first 1KB
        let searchData = data.prefix(1024)
        
        // This is a placeholder - real implementation would parse actual network headers
        if searchData.contains(where: { $0 > 0x10 && $0 < 0x20 }) {
            return "1.6" // Stockfish 16 era
        } else {
            return "1.5"
        }
    }
    
    private static func determineArchitecture(from data: Data) -> NetworkMetadata.NetworkArchitecture {
        // Simplified architecture detection
        let entropy = calculateEntropy(data.prefix(1024))
        
        if entropy > 0.6 && data.count > 10_000_000 {
            return .nnue
        } else if entropy > 0.4 {
            return .hybrid
        } else {
            return .traditional
        }
    }
    
    private static func estimateInputFeatures(from data: Data) -> Int? {
        // Estimate based on file size and structure
        // NNUE networks typically have 768 input features
        let typicalInputs = [768, 1024, 2048]
        
        // Simple heuristic based on file size
        if data.count < 20_000_000 {
            return 768
        } else if data.count < 50_000_000 {
            return 1024
        } else {
            return 2048
        }
    }
    
    private static func estimateOutputNodes(from data: Data) -> Int? {
        // Most chess engines use single output
        return 1
    }
    
    private static func estimateEloGain(fileSize: Int64, architecture: NetworkMetadata.NetworkArchitecture?) -> Int? {
        // Simplified Elo gain estimation
        switch architecture {
        case .nnue:
            if fileSize > 40_000_000 {
                return 200 // Large NNUE networks typically gain ~200 Elo
            } else {
                return 150 // Smaller networks still significant gain
            }
        case .hybrid:
            return 100
        case .traditional:
            return 50
        default:
            return nil
        }
    }
    
    // MARK: - Metadata Validation
    
    private static func validateMetadata(_ metadata: NetworkMetadata) -> (warnings: [ValidationWarning], score: Double) {
        var warnings: [ValidationWarning] = []
        var score: Double = 1.0
        
        // Check version
        if let version = metadata.version {
            let versionNumber = Double(version) ?? 0.0
            if versionNumber < 1.5 {
                warnings.append(.oldVersion)
                score -= 0.1
            }
        }
        
        // Check file size appropriateness
        if metadata.fileSize > 60_000_000 {
            warnings.append(.largeFileSize)
            score -= 0.1
        }
        
        // Check device compatibility
        let deviceCapability = DeviceCapabilityAssessor.assessCapability()
        if deviceCapability == .low && metadata.fileSize > 20_000_000 {
            warnings.append(.suboptimalForDevice)
            score -= 0.2
        }
        
        return (warnings, max(0.0, score))
    }
    
    // MARK: - Utility Methods
    
    private static func calculateSHA256(data: Data) -> String {
        let digest = SHA256.hash(data: data)
        return digest.compactMap { String(format: "%02x", $0) }.joined()
    }
    
    // MARK: - Public Validation Interface
    
    static func quickValidation(at url: URL) -> Bool {
        let result = validateNetworkFile(at: url)
        return result.canUseNetwork
    }
    
    static func detailedValidation(at url: URL, expectedChecksum: String? = nil) -> ValidationResult {
        return validateNetworkFile(at: url, expectedChecksum: expectedChecksum)
    }
    
    static func validateMultipleFiles(_ urls: [URL]) -> [URL: ValidationResult] {
        var results: [URL: ValidationResult] = [:]
        
        for url in urls {
            results[url] = validateNetworkFile(at: url)
        }
        
        return results
    }
    
    static func getBestNetworkFromCandidates(_ candidates: [URL]) -> URL? {
        let results = validateMultipleFiles(candidates)
        
        return results
            .filter { $0.value.canUseNetwork }
            .max { $0.value.validationScore < $1.value.validationScore }?
            .key
    }
    
    static func generateValidationReport(_ result: ValidationResult) -> String {
        var report = "Network Validation Report\n"
        report += "========================\n\n"
        
        report += "Overall Status: \(result.summary)\n"
        report += "Validation Score: \(String(format: "%.1f%%", result.validationScore * 100))\n\n"
        
        if !result.errors.isEmpty {
            report += "Errors:\n"
            for error in result.errors {
                report += "- \(error.localizedDescription)\n"
            }
            report += "\n"
        }
        
        if result.hasWarnings {
            report += "Warnings:\n"
            for warning in result.warnings {
                report += "- \(warning.localizedDescription)\n"
            }
            report += "\n"
        }
        
        if let metadata = result.metadata {
            report += "Network Metadata:\n"
            report += "- File Size: \(ByteCountFormatter().string(fromByteCount: metadata.fileSize))\n"
            if let arch = metadata.architecture {
                report += "- Architecture: \(arch.description)\n"
            }
            if let version = metadata.version {
                report += "- Version: \(version)\n"
            }
            if let eloGain = metadata.estimatedEloGain {
                report += "- Estimated Elo Gain: ~\(eloGain)\n"
            }
            report += "- Checksum: \(metadata.checksum.prefix(16))...\n"
        }
        
        return report
    }
}