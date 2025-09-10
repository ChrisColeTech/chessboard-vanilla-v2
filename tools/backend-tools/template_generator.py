#!/usr/bin/env python3
"""
Template Generation Module
Generates TypeScript files (models, routes) based on patterns and configurations
"""

from pathlib import Path
from typing import Dict, List, Any
from parameter_mapper import get_route_parameters
from config import DEFAULT_BACKEND_PATH


class TemplateGenerator:
    def __init__(self, backend_path: str = None):
        self.backend_path = Path(backend_path or DEFAULT_BACKEND_PATH)
    
    def generate_model(self, entity: str, properties: Dict[str, str], config: Dict[str, Any] = None) -> None:
        """Generate TypeScript model file"""
        entity_upper = entity.capitalize()
        
        # For auth entity, use predefined auth models
        if entity.lower() == 'auth':
            content = self._generate_auth_model()
        else:
            # Build property strings
            entity_props = []
            create_props = []
            update_props = []
            response_props = []
            
            # Build properties without duplicates
            added_props = set()
            
            for prop_name, prop_type in properties.items():
                # Skip duplicates
                if prop_name in added_props:
                    continue
                added_props.add(prop_name)
                
                # Map property names to match database schema  
                if prop_name == "solutionMoves":
                    db_prop = "solution_moves"
                    response_props.append(f"  {db_prop}: {prop_type};")
                    if prop_name not in ['id', 'created_at', 'updated_at']:
                        create_props.append(f"  {db_prop}: {prop_type};")
                        update_props.append(f"  {db_prop}?: {prop_type};")
                else:
                    response_props.append(f"  {prop_name}: {prop_type};")
                    if prop_name not in ['id', 'created_at', 'updated_at']:
                        create_props.append(f"  {prop_name}: {prop_type};")
                        update_props.append(f"  {prop_name}?: {prop_type};")
            
            template = '''export interface {ENTITY_TYPE} {{
{ENTITY_PROPERTIES}
}}

export interface Create{ENTITY}Request {{
{CREATE_PROPERTIES}
}}

export interface Update{ENTITY}Request {{
{UPDATE_PROPERTIES}
}}'''
            content = template.format(
                ENTITY_TYPE=f"{entity_upper}Response",
                ENTITY=entity_upper,
                ENTITY_PROPERTIES='\n'.join(response_props),
                CREATE_PROPERTIES='\n'.join(create_props),
                UPDATE_PROPERTIES='\n'.join(update_props)
            )
        
        # Write model file
        model_path = self.backend_path / "src/models" / f"{entity_upper}.ts"
        model_path.parent.mkdir(parents=True, exist_ok=True)
        model_path.write_text(content)
        
        print(f"📝 Generated {model_path}")
    
    def generate_route(self, entity: str, entities: str, endpoints: List[Dict], config: Dict[str, Any] = None) -> None:
        """Generate TypeScript route file"""
        entity_upper = entity.capitalize()
        entity_lower = entity.lower()
        entities_lower = entities.lower()
        
        route_methods = []
        
        # Always start with standard CRUD routes as foundation
        standard_routes = [
            {'method': 'GET', 'path': '/', 'handler': f'getAll{entities.capitalize()}'},
            {'method': 'GET', 'path': '/:id', 'handler': f'get{entity_upper}ById'},
            {'method': 'POST', 'path': '/', 'handler': f'create{entity_upper}'},
            {'method': 'PUT', 'path': '/:id', 'handler': f'update{entity_upper}'},
            {'method': 'DELETE', 'path': '/:id', 'handler': f'delete{entity_upper}'}
        ]
        
        # Always ensure full CRUD operations are available
        if not endpoints:
            endpoints = standard_routes
        else:
            # Merge custom endpoints with missing standard CRUD operations
            existing_paths = {(ep.get('method', '').upper(), ep.get('path', '')) for ep in endpoints}
            
            # Add missing CRUD routes
            for standard_route in standard_routes:
                route_key = (standard_route['method'].upper(), standard_route['path'])
                if route_key not in existing_paths:
                    endpoints.append(standard_route)
        
        for endpoint in endpoints:
            method = endpoint['method'].lower()
            path = endpoint['path']
            handler = endpoint['handler']
            auth_required = endpoint.get('auth_required', True)
            
            # Generate proper parameters based on handler name and path
            params = self._get_handler_params(handler, path, method)
            
            # Add authentication middleware only if required
            auth_middleware = 'authenticate, ' if auth_required else ''
            
            route_method = f"""
// {endpoint['method']} {path}
router.{method}('{path}', {auth_middleware}async (req: any, res) => {{
  try {{
    const result = await {entity_lower}Service.{handler}({params});
    res.json({{ success: true, data: result }});
  }} catch (error: any) {{
    res.status(400).json({{ success: false, error: error.message }});
  }}
}});"""
            route_methods.append(route_method)
        
        # Handle Auth special case for imports
        if entity_lower == 'auth':
            request_types = "LoginRequest, RegisterRequest"
        else:
            request_types = f"Create{entity_upper}Request, Update{entity_upper}Request"
        
        template = '''import {{ Router }} from 'express';
import {{ authenticate }} from '../middleware/auth';
import {{ validate }} from '../middleware/validation';
import {{ {SERVICE_CLASS} }} from '../services/{service_name}Service';
import {{ {REQUEST_TYPES} }} from '../models/{MODEL_NAME}';

const router = Router();
const {service_instance} = new {SERVICE_CLASS}();

{ROUTE_METHODS}

export default router;'''
        content = template.format(
            SERVICE_CLASS=f"{entity_upper}Service",
            service_name=entity_lower,
            service_instance=f"{entity_lower}Service",
            MODEL_NAME=entity_upper,
            REQUEST_TYPES=request_types,
            ROUTE_METHODS='\n'.join(route_methods)
        )
        
        # Convert entities_lower to camelCase for file naming
        def snake_to_camel(snake_str):
            components = snake_str.split('_')
            return components[0] + ''.join(word.capitalize() for word in components[1:])
        
        camel_filename = snake_to_camel(entities_lower)
        
        # Write route file
        route_path = self.backend_path / "src/routes" / f"{camel_filename}.ts"
        route_path.parent.mkdir(parents=True, exist_ok=True)
        route_path.write_text(content)
        
        print(f"📝 Generated {route_path}")
    
    def _generate_auth_model(self) -> str:
        """Generate predefined auth model"""
        return '''export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  user: UserInfo;
  token: string;
}

export interface UserInfo {
  id: string;
  username: string;
  email: string;
  chess_elo: number;
  puzzle_rating: number;
  preferences: string;
  created_at: string;
  updated_at: string;
}

export interface MeResponse {
  user: UserInfo;
  progress: UserProgress;
}

export interface UserProgress {
  id: string;
  user_id: string;
  puzzles_solved: number;
  puzzles_correct: number;
  current_streak: number;
  best_streak: number;
  total_time_spent: number;
  achievements_unlocked: string;
  last_puzzle_date?: string;
  created_at: string;
  updated_at: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  resetToken: string;
  password: string;
}

export interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

export interface UpdateProfileRequest {
  username?: string;
  email?: string;
  chess_elo?: number;
  puzzle_rating?: number;
  preferences?: string;
}

export interface TokenVerificationResponse {
  user: UserInfo;
  tokenValid: boolean;
}

export interface EmailCheckRequest {
  email: string;
}

export interface UsernameCheckRequest {
  username: string;
}

export interface AvailabilityResponse {
  available: boolean;
}

export interface AuthResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}'''
    
    def _get_handler_params(self, handler_name: str, path: str, method: str) -> str:
        """Generate correct parameters for route handler calls"""
        
        # Puzzle-specific handlers
        if handler_name == "getNextPuzzle":
            return "req.userId"
        elif handler_name == "solvePuzzle":
            return "req.params.id, req.body"
        elif handler_name == "getPuzzleHint":
            return "req.params.id"
        elif handler_name == "getPuzzleCategories":
            return ""
        elif handler_name == "getPuzzleHistory":
            return "req.userId"
        elif handler_name == "createCustomPuzzle":
            return "req.body"
        elif handler_name == "getCustomPuzzles":
            return ""
        
        # Game-specific handlers
        elif handler_name == "getGames":
            return ""
        elif handler_name == "getGameById":
            return "req.params.id"
        elif handler_name == "createGame":
            return "req.body"
        elif handler_name == "updateGame":
            return "req.params.id, req.body"
        elif handler_name == "analyzeGame":
            return "req.params.id, req.body"
        elif handler_name == "getGameAnalysis":
            return "req.params.id"
        elif handler_name == "getGameReviews":
            return ""
        
        # Authentication-specific handlers
        elif handler_name == "register":
            return "req.body"
        elif handler_name == "login":
            return "req.body"
        elif handler_name == "getCurrentUser":
            return "req.userId"
        elif handler_name == "updateProfile":
            return "req.userId, req.body"
        elif handler_name == "changePassword":
            return "req.userId, req.body"
        elif handler_name == "verifyToken":
            return "req.body.token"
        elif handler_name == "forgotPassword":
            return "req.body"
        elif handler_name == "resetPassword":
            return "req.body"
        elif handler_name == "logout":
            return ""
        elif handler_name == "checkEmailAvailability":
            return "req.body"
        elif handler_name == "checkUsernameAvailability":
            return "req.body"
        elif handler_name == "deleteAccount":
            return "req.userId"
        elif handler_name == "healthCheck":
            return ""
        
        # User-specific handlers
        elif handler_name == "getUserProfile":
            return ""
        elif handler_name == "updateUserProfile":
            return "req.body"
        elif handler_name == "getUserPreferences":
            return ""
        elif handler_name == "updateUserPreferences":
            return "req.body"
        elif handler_name == "getUserSettings":
            return ""
        elif handler_name == "updateUserSettings":
            return "req.body"
        
        # Handle standard CRUD operations by pattern
        elif handler_name.startswith('update') and ':id' in path:
            return "req.params.id, req.body"
        elif handler_name.startswith('delete') and ':id' in path:
            return "req.params.id"
        elif handler_name.startswith('get') and ':id' in path:
            return "req.params.id"
        elif handler_name.startswith('getAll'):
            return ""
        elif handler_name.startswith('create'):
            return "req.body"
        
        # Use enhanced parameter mapper for intelligent parameter mapping
        else:
            return get_route_parameters(method, path, handler_name)