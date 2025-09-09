// SlotMachinePageView.swift - Casino slot machine game page
import SwiftUI

struct SlotMachinePageView: View {
    @EnvironmentObject private var themeService: ThemeService
    @EnvironmentObject private var appViewModel: AppViewModel
    @State private var reels = ["🍎", "🍊", "🍇"]
    @State private var isSpinning = false
    @State private var lastWin = 0
    @State private var totalSpins = 0
    
    private let symbols = ["🍎", "🍊", "🍇", "🍒", "🔔", "💎", "⭐", "🍋"]
    
    var body: some View {
        VStack(spacing: 24) {
            // Header Card
            VStack(alignment: .leading, spacing: 16) {
                HStack {
                    Image(systemName: "bitcoinsign.circle.fill")
                        .font(.system(size: 24, weight: .medium))
                        .foregroundColor(themeService.current.colors.primary)
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Casino Slots")
                            .font(.system(size: 24, weight: .bold, design: .rounded))
                            .foregroundColor(themeService.current.colors.foreground)
                        
                        Text("Luck-based Gaming Experience")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(themeService.current.colors.mutedForeground)
                    }
                    
                    Spacer()
                    
                    // Coin balance
                    HStack(spacing: 6) {
                        Image(systemName: "bitcoinsign.circle.fill")
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(themeService.current.colors.accent)
                        
                        Text("\(appViewModel.coinBalance)")
                            .font(.system(size: 16, weight: .bold, design: .rounded))
                            .foregroundColor(themeService.current.colors.foreground)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(themeService.current.colors.card.opacity(0.5))
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                }
                
                Text("Test your luck with this simple slot machine! Each spin costs 10 coins. Match three symbols to win big rewards.")
                    .font(.system(size: 14))
                    .foregroundColor(themeService.current.colors.mutedForeground)
                    .multilineTextAlignment(.leading)
            }
            .padding(20)
            .cardGaming()
            
            // Slot Machine
            VStack(spacing: 20) {
                Text("🎰 SLOT MACHINE 🎰")
                    .font(.system(size: 20, weight: .bold, design: .rounded))
                    .foregroundColor(themeService.current.colors.primary)
                
                // Reels
                HStack(spacing: 16) {
                    ForEach(0..<3, id: \.self) { index in
                        SlotReel(
                            symbol: reels[index],
                            isSpinning: isSpinning
                        )
                    }
                }
                .padding(.vertical, 20)
                
                // Spin Button
                Button(action: spinReels) {
                    HStack(spacing: 8) {
                        if isSpinning {
                            ProgressView()
                                .scaleEffect(0.8)
                                .progressViewStyle(CircularProgressViewStyle(tint: themeService.current.colors.primaryForeground))
                        } else {
                            Image(systemName: "play.fill")
                                .font(.system(size: 16, weight: .semibold))
                        }
                        
                        Text(isSpinning ? "Spinning..." : "SPIN (10 coins)")
                            .font(.system(size: 18, weight: .bold))
                    }
                    .foregroundColor(themeService.current.colors.primaryForeground)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 16)
                    .background(
                        isSpinning || appViewModel.coinBalance < 10
                        ? themeService.current.colors.muted
                        : themeService.current.colors.primary
                    )
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    .shadow(
                        color: themeService.current.colors.primary.opacity(0.3),
                        radius: isSpinning ? 0 : 8,
                        x: 0,
                        y: 4
                    )
                }
                .disabled(isSpinning || appViewModel.coinBalance < 10)
                .animation(.easeInOut(duration: 0.2), value: isSpinning)
            }
            .padding(24)
            .background(
                LinearGradient(
                    gradient: Gradient(colors: [
                        themeService.current.colors.card.opacity(0.3),
                        themeService.current.colors.primary.opacity(0.1)
                    ]),
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(themeService.current.colors.border, lineWidth: 1)
            )
            
            // Game Stats
            VStack(alignment: .leading, spacing: 16) {
                Text("Game Statistics")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundColor(themeService.current.colors.foreground)
                
                VStack(spacing: 12) {
                    StatRow(label: "Total Spins", value: "\(totalSpins)")
                    StatRow(label: "Last Win", value: lastWin > 0 ? "\(lastWin) coins" : "No wins yet")
                    StatRow(label: "Win Rate", value: totalSpins > 0 ? String(format: "%.1f%%", (lastWin > 0 ? 1.0 : 0.0) / Double(totalSpins) * 100) : "0%")
                }
            }
            .padding(20)
            .cardGaming()
            
            Spacer()
        }
    }
    
    private func spinReels() {
        guard !isSpinning && appViewModel.coinBalance >= 10 else { return }
        
        isSpinning = true
        appViewModel.updateCoinBalance(appViewModel.coinBalance - 10)
        totalSpins += 1
        
        // Simulate spinning animation
        let spinDuration = 2.0
        let spinCount = 20
        let interval = spinDuration / Double(spinCount)
        
        var currentSpin = 0
        Timer.scheduledTimer(withTimeInterval: interval, repeats: true) { timer in
            currentSpin += 1
            
            // Randomize reels during spin
            for i in 0..<3 {
                reels[i] = symbols.randomElement() ?? "🍎"
            }
            
            if currentSpin >= spinCount {
                timer.invalidate()
                finalizeSpin()
            }
        }
    }
    
    private func finalizeSpin() {
        // Set final reel values
        for i in 0..<3 {
            reels[i] = symbols.randomElement() ?? "🍎"
        }
        
        // Check for wins
        let winAmount = calculateWin()
        if winAmount > 0 {
            lastWin = winAmount
            appViewModel.updateCoinBalance(appViewModel.coinBalance + winAmount)
        } else {
            lastWin = 0
        }
        
        isSpinning = false
    }
    
    private func calculateWin() -> Int {
        // Three of a kind
        if reels[0] == reels[1] && reels[1] == reels[2] {
            switch reels[0] {
            case "💎": return 500
            case "⭐": return 300
            case "🔔": return 200
            case "🍒": return 150
            case "🍋": return 100
            default: return 50
            }
        }
        
        // Two of a kind
        if reels[0] == reels[1] || reels[1] == reels[2] || reels[0] == reels[2] {
            return 20
        }
        
        return 0
    }
}

struct SlotReel: View {
    let symbol: String
    let isSpinning: Bool
    @EnvironmentObject private var themeService: ThemeService
    @State private var rotation: Double = 0
    
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 12)
                .fill(themeService.current.colors.background)
                .frame(width: 80, height: 80)
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(themeService.current.colors.border, lineWidth: 2)
                )
            
            Text(symbol)
                .font(.system(size: 40))
                .rotationEffect(.degrees(rotation))
                .animation(
                    isSpinning
                    ? .linear(duration: 0.1).repeatForever(autoreverses: false)
                    : .easeOut(duration: 0.3),
                    value: rotation
                )
        }
        .onChange(of: isSpinning) { _, spinning in
            if spinning {
                rotation += 360
            } else {
                rotation = 0
            }
        }
    }
}

struct StatRow: View {
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
    SlotMachinePageView()
        .environmentObject(ThemeService())
        .environmentObject(AppViewModel())
        .padding()
        .background(Color.gray.opacity(0.1))
}