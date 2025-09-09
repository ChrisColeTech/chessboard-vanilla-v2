// DragTestPageView.swift - Drag and drop testing page
import SwiftUI

struct DragTestPageView: View {
    @EnvironmentObject private var themeService: ThemeService
    @State private var draggedItem: String? = nil
    @State private var dropZones: [String: String?] = [
        "zone1": nil,
        "zone2": nil,
        "zone3": nil,
        "zone4": nil
    ]
    
    private let chessPieces = ["♔", "♕", "♖", "♗", "♘", "♙"]
    
    var body: some View {
        VStack(spacing: 24) {
            // Header Card
            VStack(alignment: .leading, spacing: 16) {
                HStack {
                    Image(systemName: "target")
                        .font(.system(size: 24, weight: .medium))
                        .foregroundColor(themeService.current.colors.primary)
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Drag & Drop Test")
                            .font(.system(size: 24, weight: .bold, design: .rounded))
                            .foregroundColor(themeService.current.colors.foreground)
                        
                        Text("Interactive Gesture Testing")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(themeService.current.colors.mutedForeground)
                    }
                    
                    Spacer()
                }
                
                Text("This page tests drag and drop functionality for chess pieces. Try dragging pieces from the palette below into the drop zones to test the interaction system.")
                    .font(.system(size: 14))
                    .foregroundColor(themeService.current.colors.mutedForeground)
                    .multilineTextAlignment(.leading)
            }
            .padding(20)
            .cardGaming()
            
            // Drop Zones
            VStack(alignment: .leading, spacing: 16) {
                Text("Drop Zones")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundColor(themeService.current.colors.foreground)
                
                LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 16) {
                    ForEach(Array(dropZones.keys.sorted()), id: \.self) { zoneId in
                        DropZone(
                            id: zoneId,
                            content: dropZones[zoneId] ?? nil,
                            onDrop: { piece in
                                withAnimation(.easeInOut(duration: 0.3)) {
                                    dropZones[zoneId] = piece
                                }
                            }
                        )
                    }
                }
            }
            .padding(20)
            .cardGaming()
            
            // Chess Pieces Palette
            VStack(alignment: .leading, spacing: 16) {
                Text("Piece Palette")
                    .font(.system(size: 18, weight: .semibold))
                    .foregroundColor(themeService.current.colors.foreground)
                
                LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 3), spacing: 16) {
                    ForEach(chessPieces, id: \.self) { piece in
                        DraggablePiece(piece: piece)
                    }
                }
                
                // Reset button
                Button(action: {
                    withAnimation(.easeInOut(duration: 0.3)) {
                        for key in dropZones.keys {
                            dropZones[key] = nil
                        }
                    }
                }) {
                    Text("Reset All")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(themeService.current.colors.destructiveForeground)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(themeService.current.colors.destructive)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                }
                .padding(.top, 8)
            }
            .padding(20)
            .cardGaming()
            
            Spacer()
        }
    }
}

struct DropZone: View {
    let id: String
    let content: String?
    let onDrop: (String) -> Void
    @EnvironmentObject private var themeService: ThemeService
    @State private var isTargeted = false
    
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 12)
                .fill(
                    isTargeted 
                    ? themeService.current.colors.primary.opacity(0.1)
                    : themeService.current.colors.card.opacity(0.3)
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .strokeBorder(
                            isTargeted 
                            ? themeService.current.colors.primary 
                            : themeService.current.colors.border,
                            lineWidth: isTargeted ? 2 : 1
                        )
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(
                                    themeService.current.colors.border,
                                    style: StrokeStyle(lineWidth: 1, dash: isTargeted ? [] : [5, 5])
                                )
                                .opacity(isTargeted ? 0 : 1)
                        )
                )
                .frame(height: 80)
            
            if let piece = content {
                Text(piece)
                    .font(.system(size: 40))
                    .foregroundColor(themeService.current.colors.foreground)
            } else {
                VStack(spacing: 4) {
                    Image(systemName: "plus")
                        .font(.system(size: 20, weight: .medium))
                        .foregroundColor(themeService.current.colors.mutedForeground)
                    
                    Text("Zone \(id.suffix(1))")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(themeService.current.colors.mutedForeground)
                }
            }
        }
        .onDrop(of: [.text], isTargeted: $isTargeted) { providers in
            guard let provider = providers.first else { return false }
            
            provider.loadObject(ofClass: String.self) { piece, error in
                if let piece = piece as? String {
                    DispatchQueue.main.async {
                        onDrop(piece)
                    }
                }
            }
            return true
        }
    }
}

struct DraggablePiece: View {
    let piece: String
    @EnvironmentObject private var themeService: ThemeService
    @State private var isDragging = false
    
    var body: some View {
        Text(piece)
            .font(.system(size: 32))
            .foregroundColor(themeService.current.colors.foreground)
            .frame(width: 60, height: 60)
            .background(themeService.current.colors.card.opacity(0.5))
            .clipShape(RoundedRectangle(cornerRadius: 8))
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(themeService.current.colors.border, lineWidth: 1)
            )
            .scaleEffect(isDragging ? 1.1 : 1.0)
            .opacity(isDragging ? 0.8 : 1.0)
            .animation(.easeInOut(duration: 0.2), value: isDragging)
            .onDrag {
                isDragging = true
                return NSItemProvider(object: piece as NSString)
            }
            .onAppear {
                isDragging = false
            }
    }
}

#Preview {
    DragTestPageView()
        .environmentObject(ThemeService())
        .padding()
        .background(Color.gray.opacity(0.1))
}