// InstructionsService.swift - Centralized instruction content system
import SwiftUI

struct InstructionContent {
    let title: String
    let instructions: [String]
}

class InstructionsService {
    var currentTitle: String = ""
    var currentInstructions: [String] = []
    
    // Centralized instruction content for all pages
    private let instructionContent: [String: InstructionContent] = [
        "layout": InstructionContent(
            title: "Layout Test",
            instructions: [
                "This is a minimal test page to view the background effects, floating chess pieces, and theme styling without any other content interfering.",
                "Use this page to test the visual design and ensure all theme elements are working correctly.",
                "The glassmorphism effects and responsive layout can be evaluated here."
            ]
        ),
        "worker": InstructionContent(
            title: "Worker Test",
            instructions: [
                "Test if the chess computer is working and ready to play games",
                "Check how fast the computer can think and respond to moves", 
                "Adjust the computer's skill level from beginner to expert",
                "Verify that the chess engine is responding correctly to position analysis"
            ]
        ),
        "drag": InstructionContent(
            title: "Drag Test",
            instructions: [
                "Test drag and drop functionality with visual feedback, capture mechanics, and sound effects",
                "Drag the bottom-right corner of the dashed container to test responsive scaling", 
                "Use the control buttons below to test different sound effects",
                "Verify that pieces can be moved smoothly and accurately on the board"
            ]
        ),
        "slots": InstructionContent(
            title: "Slot Machine",
            instructions: [
                "Experience the thrill of a casino slot machine with visual and audio feedback",
                "Use the +/- buttons to adjust your coin wager amount", 
                "Click the SPIN button to start the slot machine animation",
                "Watch the reels spin and see if you can win coins to add to your balance"
            ]
        )
    ]
    
    func setInstructions(for page: String) {
        guard let content = instructionContent[page] else { return }
        currentTitle = content.title
        currentInstructions = content.instructions
    }
}