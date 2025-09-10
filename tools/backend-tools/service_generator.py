#!/usr/bin/env python3
"""
Service Generation Module
Generates TypeScript service files with entity-specific and generic methods
"""

from pathlib import Path
from typing import Dict, List, Any
from config import DEFAULT_BACKEND_PATH


class ServiceGenerator:
    def __init__(self, backend_path: str = None):
        self.backend_path = Path(backend_path or DEFAULT_BACKEND_PATH)
    
    def generate_service(self, entity: str, entities: str, table_name: str, methods: List[str], config: Dict[str, Any]) -> None:
        """Generate TypeScript service file"""
        entity_upper = entity.capitalize()
        entity_lower = entity.lower()
        entities_lower = entities.lower()
        
        service_methods = []
        
        # Ensure all standard CRUD methods are included
        standard_methods = [
            f"getAll{entities.capitalize()}",
            f"get{entity_upper}ById", 
            f"create{entity_upper}",
            f"update{entity_upper}",
            f"delete{entity_upper}"
        ]
        
        # Add missing standard CRUD methods
        for standard_method in standard_methods:
            if standard_method not in methods:
                methods.append(standard_method)
        
        # Generate specific methods based on method names
        for method in methods:
            service_method = self.generate_service_method(method, entity_upper, entity_lower, table_name)
            if service_method:
                service_methods.append(service_method)
        
        # Add format method - make it entity-specific  
        entity_properties = config.get('properties', {})
        format_method = self._generate_format_method(entity_upper, entity_properties)
        service_methods.append(format_method)
        
        # Add special helper methods for Auth service
        if entity_lower == 'auth':
            auth_helpers = [
                '''  private formatUserInfo(user: any): any {
    return {
      id: user.id,
      username: user.username,
      email: user.email,
      chess_elo: user.chess_elo,
      puzzle_rating: user.puzzle_rating,
      preferences: user.preferences,
      created_at: user.created_at,
      updated_at: user.updated_at
    };
  }''',
                '''  private formatUserProgress(progress: any): any {
    return {
      id: progress.id,
      user_id: progress.user_id,
      puzzles_solved: progress.puzzles_solved,
      puzzles_correct: progress.puzzles_correct,
      current_streak: progress.current_streak,
      best_streak: progress.best_streak,
      total_time_spent: progress.total_time_spent,
      achievements_unlocked: progress.achievements_unlocked || [],
      last_puzzle_date: progress.last_puzzle_date,
      created_at: progress.created_at,
      updated_at: progress.updated_at
    };
  }'''
            ]
            service_methods.extend(auth_helpers)
        
        # Handle special cases for imports
        if entity_lower == 'auth':
            model_types = f"LoginRequest, RegisterRequest, UserInfo, AuthResponse"
            model_import_name = entity_upper
        elif entity_lower == 'learningpath':
            # Use proper LearningPath naming throughout
            model_types = f"LearningPathResponse, CreateLearningPathRequest, UpdateLearningPathRequest"
            model_import_name = 'LearningPath'
            entity_upper = 'LearningPath'  # Override entity_upper for consistent naming
        else:
            model_types = f"{entity_upper}Response, Create{entity_upper}Request, Update{entity_upper}Request"
            model_import_name = entity_upper
        
        template = '''import {{ Database }} from '../utils/database';
import {{ {MODEL_TYPES} }} from '../models/{MODEL_IMPORT_NAME}';

export class {SERVICE_CLASS} {{
  private db = Database.getInstance();

{SERVICE_METHODS}
}}'''
        # Handle special class naming for LearningPath
        if entity_lower == 'learningpath':
            service_class_name = f"{entity_upper}Service"  # This will be "LearningPathService"
        else:
            service_class_name = f"{entity_upper}Service"
        
        content = template.format(
            SERVICE_CLASS=service_class_name,
            MODEL_IMPORT_NAME=model_import_name,
            MODEL_TYPES=model_types,
            SERVICE_METHODS='\n\n'.join(service_methods)
        )
        
        # Add missing imports
        imports = [
            "import { v4 as uuidv4 } from 'uuid';"
        ]
        content = '\n'.join(imports) + '\n' + content
        
        # Write service file
        service_path = self.backend_path / "src/services" / f"{entity_lower}Service.ts"
        service_path.parent.mkdir(parents=True, exist_ok=True)
        service_path.write_text(content)
        
        print(f"📝 Generated {service_path}")
    
    def generate_service_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate individual service method based on method name"""
        
        # Import the method generators
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'method_generators'))
        from puzzle_methods import PuzzleMethodGenerator
        from game_methods import GameMethodGenerator
        from auth_methods import AuthMethodGenerator
        from user_methods import UserMethodGenerator
        from learning_path_methods import LearningPathMethodGenerator
        from generic_methods import GenericMethodGenerator
        
        # Determine which generator to use based on entity or method name
        if 'puzzle' in entity_lower or method_name.startswith(('getNext', 'solve', 'getHint', 'getCategories')):
            generator = PuzzleMethodGenerator()
        elif 'game' in entity_lower or method_name.startswith(('getGame', 'createGame', 'updateGame', 'analyze')):
            generator = GameMethodGenerator()
        elif 'auth' in entity_lower or method_name in ['register', 'login', 'logout', 'verifyToken', 'forgotPassword', 'resetPassword', 'changePassword', 'checkEmailAvailability', 'checkUsernameAvailability', 'deleteAccount', 'healthCheck']:
            generator = AuthMethodGenerator()
        elif 'user' in entity_lower or method_name.startswith(('getUser', 'updateUser')):
            generator = UserMethodGenerator()
        elif entity_lower == 'learningpath' or method_name in ['getLearningPaths', 'getLearningPathById', 'enrollInPath', 'updateProgress']:
            generator = LearningPathMethodGenerator()
        else:
            generator = GenericMethodGenerator()
        
        return generator.generate_method(method_name, entity_upper, entity_lower, table_name)
    
    def _generate_format_method(self, entity_upper: str, properties: dict) -> str:
        """Generate entity-specific format method"""
        
        # Special case for Auth - return UserInfo, not AuthResponse
        if entity_upper == 'Auth':
            return '''  private formatAuthResponse(row: any): UserInfo {
    return {
      id: row.id,
      username: row.username,
      email: row.email,
      chess_elo: row.chess_elo,
      puzzle_rating: row.puzzle_rating,
      preferences: row.preferences,
      created_at: row.created_at,
      updated_at: row.updated_at
    };
  }'''
        
        format_fields = []
        for prop_name, prop_type in properties.items():
            if prop_name == "solutionMoves":
                format_fields.append("      solution_moves: row.solution_moves ? JSON.parse(row.solution_moves) : [],")
            elif prop_name in ["themes"] and "Puzzle" in entity_upper:
                format_fields.append("      themes: row.themes ? JSON.parse(row.themes) : [],")
            elif prop_type == "string" and prop_name.endswith("_moves"):
                format_fields.append(f"      {prop_name}: row.{prop_name} ? JSON.parse(row.{prop_name}) : [],")
            elif prop_type == "string" and "json" in prop_name.lower():
                format_fields.append(f"      {prop_name}: row.{prop_name} ? JSON.parse(row.{prop_name}) : {{}},")
            else:
                format_fields.append(f"      {prop_name}: row.{prop_name},")
        
        # Special case for LearningPath - use proper naming
        if entity_upper == 'LearningPath':
            format_method_name = 'formatLearningPathResponse'
            response_type = 'LearningPathResponse'
        else:
            format_method_name = f'format{entity_upper}Response'
            response_type = f'{entity_upper}Response'
        
        return f'''  private {format_method_name}(row: any): {response_type} {{
    return {{
{chr(10).join(format_fields)}
    }};
  }}'''