// WorkerTestPageView.swift - Stockfish engine testing page
import SwiftUI

struct WorkerTestPageView: View {
    @EnvironmentObject private var themeService: ThemeService
    @State private var isEngineRunning = false
    
    var body: some View {
        VStack(spacing: 24) {
            // Header Card
            VStack(alignment: .leading, spacing: 16) {
                HStack {
                    Image(systemName: "cpu.fill")
                        .font(.system(size: 24, weight: .medium))
                        .foregroundColor(themeService.current.colors.primary)
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Stockfish Engine")
                            .font(.system(size: 24, weight: .bold, design: .rounded))
                            .foregroundColor(themeService.current.colors.foreground)
                        
                        Text("AI Chess Engine Testing")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(themeService.current.colors.mutedForeground)
                    }
                    
                    Spacer()
                    
                    // Status indicator
                    HStack(spacing: 6) {
                        Circle()
                            .fill(isEngineRunning ? Color.green : themeService.current.colors.muted)
                            .frame(width: 8, height: 8)
                        
                        Text(isEngineRunning ? "Running" : "Idle")
                            .font(.system(size: 12, weight: .medium))
                            .foregroundColor(themeService.current.colors.mutedForeground)
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(themeService.current.colors.card)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                }
                
                Text("This page will integrate the Stockfish chess engine for AI analysis and gameplay. The engine runs as a background worker to analyze positions and suggest moves.")
                    .font(.system(size: 14))
                    .foregroundColor(themeService.current.colors.mutedForeground)
                    .multilineTextAlignment(.leading)
            }
            .padding(20)
            .cardGaming()
            
            // Engine Controls
            VStack(alignment: .leading, spacing: 16) {
                Text("Engine Controls")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundColor(themeService.current.colors.foreground)
                
                VStack(spacing: 12) {
                    EngineControlButton(
                        icon: isEngineRunning ? "stop.fill" : "play.fill",
                        title: isEngineRunning ? "Stop Engine" : "Start Engine",
                        description: isEngineRunning ? "Terminate the chess engine" : "Initialize Stockfish engine",
                        action: {
                            withAnimation {
                                isEngineRunning.toggle()
                            }
                        }
                    )
                    
                    EngineControlButton(
                        icon: "brain.head.profile",
                        title: "Analyze Position",
                        description: "Get AI analysis of current board state",
                        action: {
                            // Placeholder for position analysis
                        }
                    )
                    
                    EngineControlButton(
                        icon: "lightbulb.fill",
                        title: "Get Hint",
                        description: "Request best move suggestion",
                        action: {
                            // Placeholder for hint request
                        }
                    )
                }
            }
            .padding(20)
            .cardGaming()
            
            // Engine Stats
            VStack(alignment: .leading, spacing: 16) {
                Text("Engine Information")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundColor(themeService.current.colors.foreground)
                
                VStack(spacing: 12) {
                    EngineStatRow(label: "Version", value: "Stockfish 16")
                    EngineStatRow(label: "Strength", value: "3000+ Elo")
                    EngineStatRow(label: "Threads", value: "Auto")
                    EngineStatRow(label: "Hash Size", value: "256 MB")
                    EngineStatRow(label: "Status", value: isEngineRunning ? "Active" : "Inactive")
                }
            }
            .padding(20)
            .cardGaming()
            
            Spacer()
        }
    }
}

struct EngineControlButton: View {
    let icon: String
    let title: String
    let description: String
    let action: () -> Void
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        Button(action: action) {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.system(size: 20, weight: .medium))
                    .foregroundColor(themeService.current.colors.primary)
                    .frame(width: 24)
                
                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(themeService.current.colors.foreground)
                    
                    Text(description)
                        .font(.system(size: 12))
                        .foregroundColor(themeService.current.colors.mutedForeground)
                        .multilineTextAlignment(.leading)
                }
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(themeService.current.colors.mutedForeground)
            }
            .padding(16)
            .background(themeService.current.colors.card.opacity(0.5))
            .clipShape(RoundedRectangle(cornerRadius: 8))
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(themeService.current.colors.border.opacity(0.3), lineWidth: 1)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct EngineStatRow: View {
    let label: String
    let value: String
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        HStack {
            Text(label)
                .font(.system(size: 14, weight: .medium))
                .foregroundColor(themeService.current.colors.mutedForeground)
            
            Spacer()
            
            Text(value)
                .font(.system(size: 14, weight: .semibold))
                .foregroundColor(themeService.current.colors.foreground)
        }
    }
}

#Preview {
    WorkerTestPageView()
        .environmentObject(ThemeService())
        .padding()
        .background(Color.gray.opacity(0.1))
}