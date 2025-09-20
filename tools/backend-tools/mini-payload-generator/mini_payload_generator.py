#!/usr/bin/env python3
"""
Mini Payload Generator for Troubleshooting Failing Endpoints

This is a focused payload generator specifically designed to test the 8 failing endpoints:
1. POST http://localhost:3001/api/content/ (400 Bad Request - invalid JSON syntax)
2. PUT http://localhost:3001/api/content/ (400 Bad Request - invalid JSON syntax)  
3. POST http://localhost:3001/api/puzzles/ (400 Bad Request - invalid JSON syntax)
4. GET http://localhost:3001/api/puzzles/ (400 Bad Request - JSON parse error)
5. PUT http://localhost:3001/api/puzzles/ (400 Bad Request - invalid JSON syntax)
6. GET http://localhost:3001/api/puzzles/ (400 Bad Request - JSON parse error)
7. POST http://localhost:3001/api/user-achievements/ (400 Bad Request - foreign key constraint)
8. DELETE http://localhost:3001/api/users/ (400 Bad Request - foreign key constraint)
"""

import json
import random
from typing import Dict, Any, List
import os
import sys

# Add parent directory to path to import from the main payload generator
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'payload-generator'))

from json_formatter import JSONFormatter


class MiniPayloadGenerator:
    def __init__(self):
        """Initialize the mini payload generator with real test IDs."""
        self.json_formatter = JSONFormatter()
        
        # Load real test IDs
        real_ids_path = os.path.join(os.path.dirname(__file__), '..', 'payload-generator', 'real_test_ids.json')
        with open(real_ids_path, 'r') as f:
            self.real_ids = json.load(f)
    
    def generate_content_payload(self) -> Dict[str, Any]:
        """Generate payload for content endpoints (POST/PUT)."""
        payload = {
            "title": "Test Content for Debugging",
            "content_body": {
                "sections": [
                    {"type": "text", "content": "Introduction to chess tactics"},
                    {"type": "diagram", "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
                ],
                "difficulty": "intermediate",
                "estimated_time": "15 minutes"
            },
            "content_type": "lesson",
            "difficulty_level": "intermediate",
            "estimated_duration": 15,
            "tags": ["tactics", "puzzle"],
            "requirements": {
                "min_rating": 1200,
                "prerequisites": ["basic_tactics"]
            },
            "metadata": {
                "author": "Chess Master",
                "created_date": "2024-01-15",
                "category": "tactics"
            }
        }
        
        # Format JSON fields for database storage (not API)
        return self.json_formatter.format_payload_json_fields(payload, for_api=True)
    
    def generate_puzzle_payload(self) -> Dict[str, Any]:
        """Generate payload for puzzle endpoints (POST/PUT)."""
        payload = {
            "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 4",
            "solution_moves": "Nxe5",
            "themes": ['fork', 'tactics'],  # Send as actual array for JSONB column
            "description": "intermediate",
            "rating": 1400
            }
        
        # For puzzles, send JSON strings like content does - this matches the working pattern
        return self.json_formatter.format_payload_json_fields(payload, for_api=True)

    
    def generate_user_achievement_payload(self) -> Dict[str, Any]:
        """Generate payload for user-achievements endpoint (POST)."""
        payload = {
            "user_id": self.real_ids["user_id"],
            "achievement_id": self.real_ids["achievement_id"],
            "earned_at": "2024-01-15T10:30:00Z",
            "progress_data": {
                "completion_percentage": 100,
                "milestones_reached": ["first_puzzle", "ten_puzzles", "hundred_points"]
            }
        }
        
        # Format JSON fields for database storage (not API)
        return self.json_formatter.format_payload_json_fields(payload, for_api=True)

    
    def get_user_id_for_deletion(self) -> str:
        """Get a user ID that can be safely deleted (no foreign key constraints)."""
        # Use a user ID with zero session dependencies
        return "b3c27a78-e44a-4ce3-a24a-5ea4fdf3d1db"
    
    def generate_payloads_for_failing_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """Generate all payloads for the 8 failing endpoints."""
        payloads = {
            "content_post": self.generate_content_payload(),
            "content_put": self.generate_content_payload(),
            "puzzle_post": self.generate_puzzle_payload(),
            "puzzle_put": self.generate_puzzle_payload(),
            "user_achievement_post": self.generate_user_achievement_payload(),
            "user_delete_id": self.get_user_id_for_deletion()
        }
        
        return payloads
    
    def save_payloads_to_file(self, filename: str = "debug_payloads.json"):
        """Save generated payloads to a file for inspection."""
        payloads = self.generate_payloads_for_failing_endpoints()
        
        output_path = os.path.join(os.path.dirname(__file__), filename)
        with open(output_path, 'w') as f:
            json.dump(payloads, f, indent=2, default=str)
        
        print(f"💾 Debug payloads saved to: {output_path}")
        return output_path
    
    def print_payload_analysis(self):
        """Print analysis of generated payloads for debugging."""
        payloads = self.generate_payloads_for_failing_endpoints()
        
        print("🔍 MINI PAYLOAD GENERATOR ANALYSIS")
        print("=" * 50)
        
        for endpoint_name, payload in payloads.items():
            if endpoint_name == "user_delete_id":
                print(f"\n📌 {endpoint_name}: {payload}")
                continue
                
            print(f"\n📌 {endpoint_name}:")
            print(f"   Payload size: {len(str(payload))} characters")
            
            # Check JSON fields
            json_fields = []
            for field_name, value in payload.items():
                if self.json_formatter.should_be_json_formatted(field_name, ""):
                    json_fields.append(f"{field_name}: {type(value).__name__}")
            
            if json_fields:
                print(f"   JSON fields: {', '.join(json_fields)}")
            
            # Validate JSON structure
            try:
                json_str = json.dumps(payload, default=str)
                json.loads(json_str)
                print(f"   ✅ Valid JSON structure")
            except Exception as e:
                print(f"   ❌ Invalid JSON: {e}")


if __name__ == "__main__":
    generator = MiniPayloadGenerator()
    
    # Generate and save payloads
    generator.save_payloads_to_file()
    
    # Print analysis
    generator.print_payload_analysis()