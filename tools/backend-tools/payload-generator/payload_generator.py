#!/usr/bin/env python3
"""
Test Payload Generator

This tool reads the backend_config.json file and generates valid test payloads
for each endpoint based on the entity properties and endpoint requirements.
"""

import json
import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class PayloadGenerator:
    def __init__(self, config_path: str):
        """Initialize the payload generator with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.real_ids = self._load_real_ids()
        self.test_user_id = self.real_ids['user_id']
        self.test_timestamp = datetime.now().isoformat()
        
        # Generate consistent test user credentials for register/login flow
        self.test_user_credentials = self._generate_random_user_credentials()
    
    def _load_config(self) -> Dict:
        """Load the backend configuration file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def _generate_random_user_credentials(self):
        """Generate a matching username/email pair."""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        timestamp = datetime.now().strftime('%H%M%S')
        username = f"testuser_{timestamp}_{random_str}"
        email = f"{username}@example.com"
        return username, email
    
    def _load_real_ids(self) -> Dict:
        """Load real database IDs for testing."""
        real_ids_path = os.path.join(os.path.dirname(__file__), 'real_test_ids.json')
        try:
            with open(real_ids_path, 'r') as f:
                real_ids = json.load(f)
                # Validate required IDs
                required_ids = ['user_id', 'puzzle_id', 'game_id', 'tutorial_id']
                missing_ids = [id_key for id_key in required_ids if not real_ids.get(id_key)]
                if missing_ids:
                    raise ValueError(f"Missing required real IDs: {missing_ids}")
                return real_ids
        except FileNotFoundError:
            raise FileNotFoundError(f"Real IDs file required but not found: {real_ids_path}. Run db_query.py first.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing real IDs file: {e}")
    
    def _get_sample_value_by_type(self, property_name: str, property_type: str, entity_name: str) -> Any:
        """Generate a sample value based on property type and context."""
        # Handle special cases based on property name
        if 'id' in property_name.lower():
            return f"test-{property_name.lower()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if 'email' in property_name.lower():
            # Generate random email with timestamp and random string
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            timestamp = datetime.now().strftime('%H%M%S')
            return f"test_{timestamp}_{random_str}@example.com"
        
        if 'password' in property_name.lower():
            return "password123"
        
        if 'username' in property_name.lower():
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            timestamp = datetime.now().strftime('%H%M%S')
            return f"testuser_{timestamp}_{random_str}"
        
        if 'fen' in property_name.lower():
            return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        
        if 'pgn' in property_name.lower():
            return "1. e4 e5 2. Nf3 Nc6"
        
        if 'user_color' in property_name.lower():
            return "white"
        
        if 'token' in property_name.lower():
            return f"token_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if any(time_field in property_name.lower() for time_field in ['created_at', 'updated_at', 'expires_at', 'timestamp']):
            return self.test_timestamp
        
        # Handle ID fields with real database IDs
        if property_name == 'id':
            if entity_name == 'progress':
                return self.real_ids.get('progress_id', f"test_{property_name}")
            elif entity_name == 'profiles':
                return self.real_ids.get('profile_id', f"test_{property_name}")
            elif entity_name == 'learning':
                return self.real_ids.get('enrollment_id', f"test_{property_name}")
            else:
                # For other entities, still generate dynamic ID but check for entity-specific mapping
                return f"test-{property_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
        # Handle type-based defaults
        if property_type == "string":
            return f"test_{property_name}"
        elif property_type == "number":
            # Context-aware numbers
            if 'rating' in property_name.lower() or 'elo' in property_name.lower():
                return 1500
            elif 'level' in property_name.lower():
                return 1
            elif 'progress' in property_name.lower():
                return 0.5
            elif 'time' in property_name.lower():
                return 30
            else:
                return 100
        elif property_type == "boolean":
            return True
        else:
            return f"test_{property_name}"
    
    def _generate_entity_payload(self, entity_name: str, endpoint_config: Dict, endpoint: Dict) -> Dict:
        """Generate a payload for a specific entity and endpoint."""
        properties = endpoint_config.get('properties', {})
        payload = {}
        
        # Add user_id if this entity has one and we have a test user
        if 'user_id' in properties:
            payload['user_id'] = self.test_user_id
            payload['userId'] = self.test_user_id  # Also camelCase
        
        # Generate matching username/email pair if both are present
        if 'username' in properties and 'email' in properties:
            username, email = self._generate_random_user_credentials()
            has_username = False
            has_email = False
        else:
            username, email = None, None
            has_username = False
            has_email = False
        
        # Generate values for each property
        for prop_name, prop_type in properties.items():
            # Skip auto-generated fields for certain endpoints
            if endpoint.get('method') in ['POST'] and prop_name in ['id', 'created_at', 'updated_at']:
                continue
            
            # Use matching credentials if available
            if prop_name == 'username' and username:
                payload[prop_name] = username
                has_username = True
            elif prop_name == 'email' and email:
                payload[prop_name] = email
                has_email = True
            else:
                payload[prop_name] = self._get_sample_value_by_type(prop_name, prop_type, entity_name)
        
        # Add specific payload adjustments based on endpoint path and method
        payload = self._customize_payload_for_endpoint(payload, entity_name, endpoint)
        
        return payload
    
    def _customize_payload_for_endpoint(self, payload: Dict, entity_name: str, endpoint: Dict) -> Dict:
        """Customize payload based on specific endpoint requirements."""
        method = endpoint.get('method', '').upper()
        path = endpoint.get('path', '')
        handler = endpoint.get('handler', '')
        
        # Auth endpoints
        if entity_name == 'auth':
            if 'profile' in path and method == 'PUT':
                # Auth profile updates should NOT change username/email
                return {
                    'chess_elo': 1600,
                    'puzzle_rating': 1550
                }
            elif 'register' in handler:
                # Use consistent test user credentials for register/login flow
                username, email = self.test_user_credentials
                return {
                    'username': username,
                    'email': email,
                    'password': 'password123'
                }
            elif 'login' in handler:
                # Use the SAME credentials as register for proper testing flow
                username, email = self.test_user_credentials
                return {
                    'email': email,
                    'password': 'password123'
                }
            elif 'change-password' in path:
                return {
                    'currentPassword': 'password123',
                    'newPassword': 'newpassword123'
                }
            elif 'verify-token' in path:
                return {
                    'token': 'test-jwt-token-12345'
                }
            elif 'forgot-password' in path:
                username, email = self._generate_random_user_credentials()
                return {
                    'email': email
                }
            elif 'reset-password' in path:
                username, email = self._generate_random_user_credentials()
                return {
                    'email': email,
                    'currentPassword': 'password123',
                    'newPassword': 'newpassword123'
                }
            elif 'check-email' in path:
                username, email = self._generate_random_user_credentials()
                return {
                    'email': email
                }
            elif 'check-username' in path:
                username, email = self._generate_random_user_credentials()
                return {
                    'username': username
                }
        
        # User endpoints
        elif entity_name == 'users':
            if 'profile' in path and method == 'PUT':
                # Profile updates should NOT change username/email (unique constraints)
                return {
                    'chess_elo': 1600,
                    'puzzle_rating': 1550
                }
            elif 'preferences' in path and method == 'PUT':
                return {
                    'preferences': {
                        'theme': 'dark',
                        'sound_enabled': True,
                        'auto_promotion': False
                    }
                }
            elif 'settings' in path and method == 'PUT':
                return {
                    'chess_elo': 1500,
                    'puzzle_rating': 1500
                }
        
        # Game endpoints
        elif entity_name == 'games':
            if method == 'POST' and path == '/':
                return {
                    'ai_level': 1,
                    'user_color': 'white',
                    'time_control': 'blitz'
                }
            elif 'analyze' in path:
                return {
                    'depth': 15
                }
        
        # Puzzle endpoints
        elif entity_name == 'puzzles':
            if 'solve' in path:
                return {
                    'moves': 'e2e4',
                    'time_taken': 30
                }
            elif method == 'POST' and 'custom' in path:
                return {
                    'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                    'solution_moves': 'e2e4 e7e5',
                    'themes': 'checkmate',
                    'rating': 1200,
                    'description': 'Test custom puzzle'
                }
        
        # Session endpoints
        elif entity_name == 'sessions':
            if 'create' in path:
                return {
                    'user_id': self.test_user_id,
                    'refresh_token': f"refresh_token_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
                }
        
        # Progress endpoints
        elif entity_name == 'progress':
            if 'update' in path:
                # Use existing progress record ID
                return {
                    'id': 'test-progress-001',  # Use existing record
                    'user_id': self.test_user_id,
                    'puzzles_solved': 100,
                    'puzzles_correct': 90,
                    'current_streak': 5,
                    'best_streak': 15,
                    'total_time_spent': 3600
                }
        
        # Achievement endpoints
        elif entity_name == 'achievements':
            if 'unlock' in path:
                return {
                    'user_id': self.test_user_id,
                    'achievement_id': 'test-achievement-123'
                }
        
        # Learning path endpoints
        elif entity_name == 'learning':
            if 'enroll' in path:
                return {
                    'user_id': self.test_user_id
                }
            elif 'progress' in path:
                return {
                    'user_id': self.test_user_id,
                    'progress': 0.75
                }
        
        # Tutorial endpoints
        elif entity_name == 'tutorials':
            if 'complete' in path:
                return {
                    'user_id': self.test_user_id,
                    'completion_time': 300
                }
        
        # Analysis endpoints
        elif entity_name == 'analysis':
            if 'position' in path and method == 'POST':
                return {
                    'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                    'depth': 15
                }
        
        # Profiles endpoints  
        elif entity_name == 'profiles':
            if method == 'PUT':
                # Update existing profile, don't change user_id
                return {
                    'display_name': 'Updated Test User',
                    'bio': 'Updated chess enthusiast',
                    'country': 'US',
                    'timezone': 'EST'
                }
        
        # Analytics endpoints
        elif entity_name == 'analytics':
            if 'track' in path:
                return {
                    'user_id': self.test_user_id,
                    'event_type': 'puzzle_solved',
                    'event_data': json.dumps({'puzzle_id': 'test-puzzle-123', 'time': 30}),
                    'session_id': 'test-session-123'
                }
        
        # Minimal payloads for endpoints that typically need minimal data
        minimal_endpoints = ['enroll', 'complete', 'unlock']
        if any(keyword in path for keyword in minimal_endpoints):
            return {
                'user_id': self.test_user_id,
                'userId': self.test_user_id
            }
        
        return payload
    
    def generate_all_payloads(self) -> Dict[str, List[Dict]]:
        """Generate payloads for all endpoints in the configuration."""
        all_payloads = {}
        
        endpoints_config = self.config.get('endpoints', {})
        
        for entity_name, entity_config in endpoints_config.items():
            entity_payloads = []
            endpoints = entity_config.get('endpoints', [])
            
            for endpoint in endpoints:
                method = endpoint.get('method', '').upper()
                path = endpoint.get('path', '')
                handler = endpoint.get('handler', '')
                
                # Generate payload for mutation endpoints (POST, PUT, PATCH)
                payload_data = None
                if method in ['POST', 'PUT', 'PATCH']:
                    payload_data = self._generate_entity_payload(entity_name, entity_config, endpoint)
                
                endpoint_info = {
                    'entity': entity_name,
                    'method': method,
                    'path': path,
                    'handler': handler,
                    'auth_required': endpoint.get('auth_required', True),
                    'payload': payload_data,
                    'url_params': self._extract_url_params(path, entity_name)
                }
                
                entity_payloads.append(endpoint_info)
            
            if entity_payloads:
                all_payloads[entity_name] = entity_payloads
        
        return all_payloads
    
    def _extract_url_params(self, path: str, entity_name: str = None) -> Dict[str, str]:
        """Extract URL parameters from endpoint path and provide real database values."""
        params = {}
        import re
        
        # Find all :param patterns
        param_matches = re.findall(r':(\w+)', path)
        
        for param in param_matches:
            if param == 'id':
                # Use appropriate real ID based on entity context
                if entity_name == 'puzzles':
                    params[param] = self.real_ids['puzzle_id']
                elif entity_name == 'games':
                    params[param] = self.real_ids['game_id']
                elif entity_name == 'tutorials':
                    params[param] = self.real_ids['tutorial_id']
                elif entity_name == 'achievements':
                    params[param] = self.real_ids['achievement_id']
                elif entity_name == 'learning':
                    params[param] = self.real_ids['learning_path_id']
                elif entity_name == 'ai-opponents':
                    params[param] = self.real_ids['ai_opponent_id']
                elif entity_name == 'historic-games':
                    params[param] = self.real_ids['historic_game_id']
                elif entity_name == 'learning-modules':
                    params[param] = self.real_ids['learning_module_id']
                elif entity_name == 'subscriptions':
                    params[param] = self.real_ids['subscription_id']
                elif entity_name == 'profiles':
                    params[param] = self.real_ids['user_id']  # profiles use user_id
                elif entity_name == 'study-plans':
                    params[param] = self.real_ids['study_plan_id']
                else:
                    params[param] = self.real_ids['game_id']  # Default fallback
            elif param == 'userId':
                params[param] = self.real_ids['user_id']
            elif param == 'puzzleId':
                params[param] = self.real_ids['puzzle_id']
            elif param == 'gameId':
                params[param] = self.real_ids['game_id']
            elif param == 'tutorialId':
                params[param] = self.real_ids['tutorial_id']
            elif param == 'pathId':
                params[param] = self.real_ids['learning_path_id']
            elif param == 'code':
                params[param] = self.real_ids['opening_eco_code']
            elif param == 'fen':
                params[param] = 'rnbqkbnr-pppppppp-8-8-8-8-PPPPPPPP-RNBQKBNR'
            elif param == 'level':
                params[param] = 'beginner'
            elif param == 'category':
                params[param] = 'endgame'
            elif param == 'player':
                params[param] = 'kasparov'
            elif param == 'token':
                params[param] = 'test-session-token'
            else:
                # Try to map to a real ID or fail
                if param.endswith('Id') and param[:-2] + '_id' in self.real_ids:
                    params[param] = self.real_ids[param[:-2] + '_id']
                else:
                    raise ValueError(f"No real ID mapping found for parameter: {param}")
        
        return params
    
    def save_payloads_to_file(self, output_path: str) -> None:
        """Generate and save all payloads to a JSON file."""
        payloads = self.generate_all_payloads()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(payloads, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Payloads saved to: {output_path}")
        
        # Print summary
        total_endpoints = sum(len(endpoints) for endpoints in payloads.values())
        mutation_endpoints = sum(
            len([ep for ep in endpoints if ep['method'] in ['POST', 'PUT', 'PATCH']]) 
            for endpoints in payloads.values()
        )
        
        print(f"📊 Summary:")
        print(f"   - Total endpoints: {total_endpoints}")
        print(f"   - Endpoints with payloads: {mutation_endpoints}")
        print(f"   - Entity groups: {len(payloads)}")


def main():
    """Main function to run the payload generator."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'backend_config.json')
    output_path = os.path.join(script_dir, 'generated_payloads.json')
    
    try:
        generator = PayloadGenerator(config_path)
        generator.save_payloads_to_file(output_path)
        
        print(f"\n🚀 Payload generation complete!")
        print(f"📁 Output file: {output_path}")
        print(f"💡 Use this file with the v3 test script for comprehensive API testing.")
        
    except Exception as e:
        print(f"❌ Error generating payloads: {e}")
        exit(1)


if __name__ == "__main__":
    main()