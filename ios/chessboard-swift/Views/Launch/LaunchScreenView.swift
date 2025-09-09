// LaunchScreenView.swift - Splash screen for app launch
import SwiftUI

struct LaunchScreenView: View {
    @State private var isAnimating = false
    @State private var opacity: Double = 0
    
    var body: some View {
        ZStack {
            // Background gradient matching app theme
            LinearGradient(
                colors: [
                    Color(red: 0.05, green: 0.05, blue: 0.1),
                    Color(red: 0.1, green: 0.1, blue: 0.15),
                    Color(red: 0.15, green: 0.1, blue: 0.2)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            // Floating chess pieces background effect
            ForEach(0..<6, id: \.self) { index in
                ChessPieceBackground(
                    piece: chessPieces[index % chessPieces.count],
                    delay: Double(index) * 0.3
                )
            }
            
            // Main logo/title content
            VStack(spacing: 24) {
                // Chess piece icon
                ZStack {
                    Circle()
                        .fill(
                            RadialGradient(
                                colors: [
                                    Color(red: 0.4, green: 0.6, blue: 1.0).opacity(0.3),
                                    Color(red: 0.2, green: 0.4, blue: 0.8).opacity(0.1)
                                ],
                                center: .center,
                                startRadius: 20,
                                endRadius: 80
                            )
                        )
                        .frame(width: 120, height: 120)
                        .blur(radius: isAnimating ? 0 : 20)
                    
                    Image(systemName: "crown.fill")
                        .font(.system(size: 48, weight: .light))
                        .foregroundColor(.white)
                        .scaleEffect(isAnimating ? 1.0 : 0.3)
                }
                .scaleEffect(isAnimating ? 1.0 : 0.8)
                .opacity(opacity)
                
                // App title
                Text("Chess Training")
                    .font(.system(size: 32, weight: .light, design: .rounded))
                    .foregroundColor(.white)
                    .opacity(opacity)
                    .offset(y: isAnimating ? 0 : 30)
                
                // Subtitle
                Text("Master Your Skills")
                    .font(.system(size: 16, weight: .light))
                    .foregroundColor(.white.opacity(0.7))
                    .opacity(opacity)
                    .offset(y: isAnimating ? 0 : 20)
            }
            .onAppear {
                withAnimation(.easeInOut(duration: 1.5)) {
                    isAnimating = true
                    opacity = 1.0
                }
            }
        }
        .preferredColorScheme(.dark)
    }
    
    private let chessPieces = ["♔", "♕", "♖", "♗", "♘", "♙"]
}

struct ChessPieceBackground: View {
    let piece: String
    let delay: Double
    @State private var isFloating = false
    @State private var opacity: Double = 0.1
    
    var body: some View {
        Text(piece)
            .font(.system(size: CGFloat.random(in: 30...60), weight: .light))
            .foregroundColor(.white.opacity(opacity))
            .position(
                x: CGFloat.random(in: 50...350),
                y: CGFloat.random(in: 100...700)
            )
            .offset(
                x: isFloating ? CGFloat.random(in: -20...20) : 0,
                y: isFloating ? CGFloat.random(in: -30...30) : 0
            )
            .onAppear {
                DispatchQueue.main.asyncAfter(deadline: .now() + delay) {
                    withAnimation(
                        .easeInOut(duration: Double.random(in: 3...5))
                        .repeatForever(autoreverses: true)
                    ) {
                        isFloating = true
                        opacity = Double.random(in: 0.05...0.2)
                    }
                }
            }
    }
}

#Preview {
    LaunchScreenView()
}