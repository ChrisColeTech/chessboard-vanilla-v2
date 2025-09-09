// InstructionsModalView.swift - Modal dialog for showing instructions
import SwiftUI

struct InstructionsModalView: View {
    let isVisible: Bool
    let title: String
    let instructions: [String]
    let onDismiss: () -> Void
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        if isVisible {
            ZStack {
                // Backdrop - fixed inset-0 z-50 bg-black/50 backdrop-blur-sm
                ZStack {
                    Color.black.opacity(0.5)
                    BlurView(style: .systemUltraThinMaterial, alpha: 0.3)
                }
                .ignoresSafeArea()
                .onTapGesture {
                    onDismiss()
                }
                
                // Modal Content - relative bg-background border rounded-xl shadow-2xl p-6 max-w-md
                VStack(alignment: .leading, spacing: 0) {
                    // Header
                    HStack {
                        // Icon and title
                        HStack(spacing: 12) {
                            // Icon container
                            ZStack {
                                Circle()
                                    .fill(themeService.current.colors.primary.opacity(0.1))
                                    .frame(width: 40, height: 40)
                                
                                Circle()
                                    .stroke(themeService.current.colors.primary.opacity(0.2), lineWidth: 1)
                                    .frame(width: 40, height: 40)
                                
                                Image(systemName: "target")
                                    .font(.system(size: 20, weight: .medium))
                                    .foregroundColor(themeService.current.colors.primary)
                            }
                            
                            Text(title.isEmpty ? "How to Use" : title)
                                .font(.system(size: 18, weight: .semibold))
                                .foregroundColor(themeService.current.colors.foreground)
                        }
                        
                        Spacer()
                        
                        // Close button
                        Button(action: onDismiss) {
                            Image(systemName: "xmark")
                                .font(.system(size: 16, weight: .medium))
                                .foregroundColor(themeService.current.colors.mutedForeground)
                        }
                        .padding(4)
                        .background(themeService.current.colors.muted)
                        .clipShape(RoundedRectangle(cornerRadius: 6))
                        .accessibilityLabel("Close instructions")
                    }
                    .padding(.bottom, 16)
                    
                    // Instructions list
                    ScrollView {
                        VStack(alignment: .leading, spacing: 12) {
                            ForEach(Array(instructions.enumerated()), id: \.offset) { index, instruction in
                                InstructionRow(
                                    text: instruction,
                                    bulletColor: themeService.current.colors.primary
                                )
                                .environmentObject(themeService)
                            }
                        }
                    }
                    .frame(maxHeight: 300)
                    
                    // Action button
                    Button(action: onDismiss) {
                        Text("Got it!")
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(themeService.current.colors.primaryForeground)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 12)
                            .background(themeService.current.colors.primary)
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                    .padding(.top, 24)
                }
                .padding(24)
                .frame(maxWidth: 400)
                .background(
                    ZStack {
                        BlurView(style: .systemUltraThinMaterial, alpha: 0.85)
                        themeService.current.colors.background.opacity(0.05)
                    }
                )
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(.white.opacity(0.2), lineWidth: 1)
                )
                .shadow(
                    color: themeService.current.colors.primary.opacity(0.15),
                    radius: 20,
                    x: 0,
                    y: 10
                )
                .shadow(
                    color: Color.black.opacity(0.1),
                    radius: 8,
                    x: 0,
                    y: 4
                )
                .padding(.horizontal, 16)
            }
            .zIndex(50)
        }
    }
}

struct InstructionRow: View {
    let text: String
    let bulletColor: Color
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            // Bullet point
            Circle()
                .fill(bulletColor)
                .frame(width: 8, height: 8)
                .padding(.top, 6)
            
            // Instruction text
            Text(text)
                .font(.system(size: 14))
                .foregroundColor(themeService.current.colors.foreground)
                .multilineTextAlignment(.leading)
                .fixedSize(horizontal: false, vertical: true)
            
            Spacer(minLength: 0)
        }
    }
}

#Preview {
    InstructionsModalView(
        isVisible: true,
        title: "Test Instructions",
        instructions: [
            "This is the first instruction to test the modal",
            "This is a longer second instruction that might wrap to multiple lines to test the layout",
            "Third instruction here",
            "Fourth and final instruction for testing purposes"
        ],
        onDismiss: { print("Modal dismissed") }
    )
    .environmentObject(ThemeService())
}