// LayoutTestPageView.swift - Background and layout testing page
import SwiftUI

struct LayoutTestPageView: View {
    @EnvironmentObject private var themeService: ThemeService
    
    var body: some View {
        VStack(spacing: 16) {
            Text("This is a minimal test page to view the background effects, floating chess pieces, and theme styling without any other content interfering.")
                .font(.system(size: 14))
                .foregroundColor(themeService.current.colors.mutedForeground)
                .multilineTextAlignment(.center)
                .padding(32)
                .background(
                    ZStack {
                        BlurView(style: .systemUltraThinMaterial, alpha: 0.85)
                        themeService.current.colors.background.opacity(0.05)
                    }
                )
                .clipShape(RoundedRectangle(cornerRadius: 16))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(.white.opacity(0.2), lineWidth: 1)
                )
            
            Spacer()
        }
    }
}

#Preview {
    LayoutTestPageView()
        .environmentObject(ThemeService())
        .padding()
        .background(Color.gray.opacity(0.1))
}