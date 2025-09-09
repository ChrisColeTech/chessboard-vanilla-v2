// BlurView.swift - Custom UIVisualEffectView wrapper for proper glassmorphism
import SwiftUI
import UIKit

struct BlurView: UIViewRepresentable {
    let style: UIBlurEffect.Style
    let alpha: CGFloat
    
    init(style: UIBlurEffect.Style = .systemUltraThinMaterial, alpha: CGFloat = 1.0) {
        self.style = style
        self.alpha = alpha
    }
    
    func makeUIView(context: Context) -> UIVisualEffectView {
        let view = UIVisualEffectView(effect: UIBlurEffect(style: style))
        view.alpha = alpha
        return view
    }
    
    func updateUIView(_ uiView: UIVisualEffectView, context: Context) {
        uiView.effect = UIBlurEffect(style: style)
        uiView.alpha = alpha
    }
}