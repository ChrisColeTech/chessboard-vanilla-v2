// InstructionsFABView.swift - Floating Action Button for instructions
import SwiftUI

struct InstructionsFABView: View {
    let onClick: () -> Void
    @EnvironmentObject private var themeService: ThemeService
    @State private var isPressed = false
    
    var body: some View {
        Button(action: onClick) {
            Image(systemName: "questionmark.circle.fill")
                .font(.system(size: 20, weight: .medium))
                .foregroundColor(themeService.current.colors.primaryForeground)
                .scaleEffect(isPressed ? 1.1 : 1.0)
                .animation(.easeInOut(duration: 0.2), value: isPressed)
        }
        .frame(width: 48, height: 48)
        .background(themeService.current.colors.primary)
        .clipShape(Circle())
        .shadow(
            color: themeService.current.colors.primary.opacity(0.3),
            radius: 12,
            x: 0,
            y: 6
        )
        .shadow(
            color: Color.black.opacity(0.1),
            radius: 8,
            x: 0,
            y: 2
        )
        .scaleEffect(isPressed ? 0.95 : 1.0)
        .onLongPressGesture(minimumDuration: 0, maximumDistance: .infinity, perform: {}, onPressingChanged: { pressing in
            withAnimation(.easeInOut(duration: 0.2)) {
                isPressed = pressing
            }
        })
        .accessibilityLabel("Show instructions")
    }
}

#Preview {
    InstructionsFABView {
        print("FAB tapped")
    }
    .environmentObject(ThemeService())
    .padding(50)
    .background(Color.gray.opacity(0.3))
}