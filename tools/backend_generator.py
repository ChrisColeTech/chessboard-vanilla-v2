#!/usr/bin/env python3
"""
Backend Pattern Generator (Legacy - now uses modular components)
Generates TypeScript backend files (routes, services, models) based on established patterns
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

# Import the refactored modular components
try:
    from backend_tools import BackendGeneratorRefactored
    REFACTORED_AVAILABLE = True
except ImportError:
    REFACTORED_AVAILABLE = False

class BackendGenerator:
    def __init__(self, backend_path: str = "../backend"):
        self.backend_path = Path(backend_path)
        self.templates = {}
        
        # Use refactored generator if available
        if REFACTORED_AVAILABLE:
            self.refactored_generator = BackendGeneratorRefactored(backend_path)
        
    def analyze_existing_pattern(self, reference_service: str = "puzzles"):
        """Analyze existing files to extract patterns"""
        # Use refactored pattern analyzer if available
        if REFACTORED_AVAILABLE:
            return self.refactored_generator.analyze_existing_pattern(reference_service)
        else:
            print(f"🔍 Analyzing existing {reference_service} pattern...")
            
            patterns = {
                'route': self._analyze_route_pattern(f"{reference_service}.ts"),
                'service': self._analyze_service_pattern(f"{reference_service}Service.ts"),
                'model': self._analyze_model_pattern("Puzzle.ts")
            }
            
            return patterns
    
    def _analyze_route_pattern(self, filename: str) -> Dict:
        """Extract route pattern from existing route file"""
        route_path = self.backend_path / "src/routes" / filename
        if not route_path.exists():
            return self._create_default_route_pattern()
            
        # For now, return default pattern - could parse existing file
        return self._create_default_route_pattern()
    
    def _analyze_service_pattern(self, filename: str) -> Dict:
        """Extract service pattern from existing service file"""
        service_path = self.backend_path / "src/services" / filename
        if not service_path.exists():
            return self._create_default_service_pattern()
            
        return self._create_default_service_pattern()
    
    def _analyze_model_pattern(self, filename: str) -> Dict:
        """Extract model pattern from existing model file"""
        model_path = self.backend_path / "src/models" / filename
        if not model_path.exists():
            return self._create_default_model_pattern()
            
        return self._create_default_model_pattern()
    
    def _create_default_route_pattern(self) -> Dict:
        """Create default route template pattern"""
        return {
            'template': '''import {{ Router }} from 'express';
import {{ authenticate }} from '../middleware/auth';
import {{ validate }} from '../middleware/validation';
import {{ {SERVICE_CLASS} }} from '../services/{service_name}Service';
import {{ {REQUEST_TYPES} }} from '../models/{MODEL_NAME}';

const router = Router();
const {service_instance} = new {SERVICE_CLASS}();

{ROUTE_METHODS}

export default router;''',
            'imports': [
                "Router from 'express'",
                "authenticate from '../middleware/auth'",
                "validate from '../middleware/validation'"
            ]
        }
    
    def _create_default_service_pattern(self) -> Dict:
        """Create default service template pattern"""
        return {
            'template': '''import {{ Database }} from '../utils/database';
import {{ {MODEL_TYPES} }} from '../models/{MODEL_NAME}';

export class {SERVICE_CLASS} {{
  private db = Database.getInstance();

{SERVICE_METHODS}
}}''',
            'methods': {
                'getAll': '''  async getAll{ENTITIES}(options: {{
    page: number;
    limit: number;
  }}): Promise<{{
    data: any[];
    pagination: {{
      page: number;
      limit: number;
      total: number;
      totalPages: number;
    }};
  }}> {{
    const {{ page, limit }} = options;
    const offset = (page - 1) * limit;

    // Get total count
    const totalResult = await this.db.db.get(
      `SELECT COUNT(*) as total FROM {table_name}`,
      []
    );
    const total = totalResult.total;

    // Get {entities}
    const {entities} = await this.db.db.all(
      `SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT ? OFFSET ?`,
      [limit, offset]
    );

    return {{
      data: {entities}.map(({entity}: any) => this.format{ENTITY}Response({entity})),
      pagination: {{
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit)
      }}
    }};
  }}''',
                'getById': '''  async get{ENTITY}ById(id: string): Promise<{ENTITY_TYPE}> {{
    const {entity} = await this.db.db.get('SELECT * FROM {table_name} WHERE id = ?', [id]);
    if (!{entity}) throw new Error('{ENTITY} not found');
    
    return this.format{ENTITY}Response({entity});
  }}''',
                'create': '''  async create{ENTITY}(data: Create{ENTITY}Request): Promise<{ENTITY_TYPE}> {{
    const id = uuidv4();
    await this.db.db.run(`
      INSERT INTO {table_name} (id, {INSERT_COLUMNS})
      VALUES (?, {INSERT_VALUES})
    `, [id, ...Object.values(data)]);
    
    return this.get{ENTITY}ById(id);
  }}''',
                'update': '''  async update{ENTITY}(id: string, data: Update{ENTITY}Request): Promise<{ENTITY_TYPE}> {{
    await this.db.db.run(
      'UPDATE {table_name} SET {UPDATE_COLUMNS} WHERE id = ?',
      [...Object.values(data), id]
    );
    
    return this.get{ENTITY}ById(id);
  }}''',
                'delete': '''  async delete{ENTITY}(id: string): Promise<void> {{
    await this.db.db.run('DELETE FROM {table_name} WHERE id = ?', [id]);
  }}'''
            }
        }
    
    def _create_default_model_pattern(self) -> Dict:
        """Create default model template pattern"""
        return {
            'template': '''export interface {ENTITY_TYPE} {{
{ENTITY_PROPERTIES}
}}

export interface Create{ENTITY}Request {{
{CREATE_PROPERTIES}
}}

export interface Update{ENTITY}Request {{
{UPDATE_PROPERTIES}
}}'''
        }
    
    def generate_endpoint(self, config: Dict[str, Any]):
        """Generate a complete endpoint (route + service + model)"""
        # Use refactored generator if available, otherwise use legacy code
        if REFACTORED_AVAILABLE:
            print("🔄 Using refactored modular generator...")
            return self.refactored_generator.generate_endpoint(config)
        else:
            print("⚠️  Using legacy generator (modular components not found)...")
            # Store config for use in other methods
            self.current_config = config
            
            entity = config['entity']
            entities = config.get('entities', f"{entity.lower()}s")
            table_name = config.get('table_name', entities)
            
            print(f"🔧 Generating {entity} endpoint...")
            
            # Generate model
            self._generate_model(entity, config.get('properties', {}))
            
            # Generate service  
            self._generate_service(entity, entities, table_name, config.get('methods', ['getAll', 'getById', 'create', 'update', 'delete']))
            
            # Generate route
            self._generate_route(entity, entities, config.get('endpoints', []))
            
            print(f"✅ Generated {entity} endpoint files")
    
    def _generate_model(self, entity: str, properties: Dict[str, str]):
        """Generate TypeScript model file"""
        entity_upper = entity.capitalize()
        
        # For auth entity, use predefined auth models
        if entity.lower() == 'auth':
            content = '''export interface LoginRequest {
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
            
            template = self._create_default_model_pattern()['template']
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
    
    def _generate_service(self, entity: str, entities: str, table_name: str, methods: List[str]):
        """Generate TypeScript service file"""
        entity_upper = entity.capitalize()
        entity_lower = entity.lower()
        entities_lower = entities.lower()
        
        service_methods = []
        
        # Generate specific methods based on method names
        for method in methods:
            service_method = self._generate_service_method(method, entity_upper, entity_lower, table_name)
            if service_method:
                service_methods.append(service_method)
        
        # Add format method - make it entity-specific  
        # Get original config properties for this method call
        entity_config = self.current_config if hasattr(self, 'current_config') else {}
        entity_properties = entity_config.get('properties', {})
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
      achievements_unlocked: progress.achievements_unlocked ? JSON.parse(progress.achievements_unlocked) : [],
      last_puzzle_date: progress.last_puzzle_date,
      created_at: progress.created_at,
      updated_at: progress.updated_at
    };
  }'''
            ]
            service_methods.extend(auth_helpers)
        
        # Handle Auth special case for imports
        if entity_lower == 'auth':
            model_types = f"LoginRequest, RegisterRequest, UserInfo, AuthResponse"
        else:
            model_types = f"{entity_upper}Response, Create{entity_upper}Request, Update{entity_upper}Request"
        
        template = self._create_default_service_pattern()['template']
        content = template.format(
            SERVICE_CLASS=f"{entity_upper}Service",
            MODEL_NAME=entity_upper,
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
    
    def _generate_route(self, entity: str, entities: str, endpoints: List[Dict]):
        """Generate TypeScript route file"""
        entity_upper = entity.capitalize()
        entity_lower = entity.lower()
        entities_lower = entities.lower()
        
        route_methods = []
        
        # Generate standard CRUD routes if no custom endpoints specified
        if not endpoints:
            endpoints = [
                {'method': 'GET', 'path': '/', 'handler': f'getAll{entities.capitalize()}'},
                {'method': 'GET', 'path': '/:id', 'handler': f'get{entity_upper}ById'},
                {'method': 'POST', 'path': '/', 'handler': f'create{entity_upper}'},
                {'method': 'PUT', 'path': '/:id', 'handler': f'update{entity_upper}'},
                {'method': 'DELETE', 'path': '/:id', 'handler': f'delete{entity_upper}'}
            ]
        
        for endpoint in endpoints:
            method = endpoint['method'].lower()
            path = endpoint['path']
            handler = endpoint['handler']
            auth_required = endpoint.get('auth_required', True)
            
            # Generate proper parameters based on handler name and path
            params = self._get_handler_params(handler, path)
            
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
        
        template = self._create_default_route_pattern()['template']
        content = template.format(
            SERVICE_CLASS=f"{entity_upper}Service",
            service_name=entity_lower,
            service_instance=f"{entity_lower}Service",
            MODEL_NAME=entity_upper,
            REQUEST_TYPES=request_types,
            ROUTE_METHODS='\n'.join(route_methods)
        )
        
        # Write route file
        route_path = self.backend_path / "src/routes" / f"{entities_lower}.ts"
        route_path.parent.mkdir(parents=True, exist_ok=True)
        route_path.write_text(content)
        
        print(f"📝 Generated {route_path}")
    
    def _generate_service_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate individual service method based on method name"""
        
        # Puzzle-specific methods
        if method_name == "getNextPuzzle":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response> {{
    // Get next puzzle for user based on rating and history
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE rating BETWEEN $1 AND $2 
      ORDER BY RANDOM() 
      LIMIT 1
    `, [800, 2000]);
    
    if (!result.rows.length) {{
      throw new Error('No puzzles available');
    }}
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "solvePuzzle":
            return f'''  async {method_name}(puzzleId: string, solutionData: any): Promise<{{correct: boolean, solution?: string[]}}> {{
    const puzzle = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [puzzleId]);
    if (!puzzle.rows.length) throw new Error('{entity_upper} not found');
    
    const puzzleData = puzzle.rows[0];
    const userMoves = solutionData.moves || [];
    const solutionMoves = JSON.parse(puzzleData.solution_moves || '[]');
    
    const isCorrect = JSON.stringify(userMoves) === JSON.stringify(solutionMoves);
    
    return {{
      correct: isCorrect,
      solution: isCorrect ? undefined : solutionMoves
    }};
  }}'''
        
        elif method_name == "getPuzzleHint":
            return f'''  async {method_name}(puzzleId: string): Promise<{{hint: string}}> {{
    const puzzle = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [puzzleId]);
    if (!puzzle.rows.length) throw new Error('{entity_upper} not found');
    
    const themes = JSON.parse(puzzle.rows[0].themes || '[]');
    const hint = themes.length > 0 ? `Look for ${{themes[0]}} tactics` : 'Look for the best move';
    
    return {{ hint }};
  }}'''
        
        elif method_name == "getPuzzleCategories":
            return f'''  async {method_name}(): Promise<string[]> {{
    const result = await this.db.query(`
      SELECT DISTINCT themes FROM {table_name} 
      WHERE themes IS NOT NULL AND themes != ''
      LIMIT 50
    `);
    
    const allThemes = new Set<string>();
    result.rows.forEach(row => {{
      try {{
        const themes = JSON.parse(row.themes || '[]');
        themes.forEach((theme: string) => allThemes.add(theme));
      }} catch (e) {{
        // Skip invalid JSON
      }}
    }});
    
    return Array.from(allThemes).slice(0, 20);
  }}'''
        
        elif method_name == "getPuzzleHistory":
            return f'''  async {method_name}(userId: string): Promise<any[]> {{
    // Return empty array for now - would need puzzle_attempts table
    return [];
  }}'''
        
        elif method_name == "createCustomPuzzle":
            return f'''  async {method_name}(puzzleData: any): Promise<{entity_upper}Response> {{
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (id, fen, solution_moves, themes, rating, description)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *
    `, [
      id,
      puzzleData.fen,
      JSON.stringify(puzzleData.solutionMoves || []),
      JSON.stringify(puzzleData.themes || []),
      puzzleData.rating || 1000,
      puzzleData.description || ''
    ]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "getCustomPuzzles":
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query(`
      SELECT * FROM {table_name} 
      WHERE description LIKE '%custom%' 
      ORDER BY created_at DESC 
      LIMIT 20
    `);
    
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # Game-specific methods
        elif method_name == "getGames":
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        elif method_name == "getGameById":
            return f'''  async {method_name}(id: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "createGame":
            return f'''  async {method_name}(gameData: any): Promise<{entity_upper}Response> {{
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (id, user_id, ai_level, user_color, current_fen, status)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *
    `, [
      id,
      gameData.user_id,
      gameData.ai_level || 1,
      gameData.user_color || 'white',
      gameData.current_fen || 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
      'active'
    ]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateGame":
            return f'''  async {method_name}(id: string, gameData: any): Promise<{entity_upper}Response> {{
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET current_fen = $1, pgn = $2, status = $3, result = $4, updated_at = NOW()
      WHERE id = $5
      RETURNING *
    `, [
      gameData.current_fen,
      gameData.pgn,
      gameData.status,
      gameData.result,
      id
    ]);
    
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "analyzeGame":
            return f'''  async {method_name}(id: string, analysisData: any): Promise<{{analysis: string}}> {{
    // Basic game analysis implementation
    const game = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!game.rows.length) throw new Error('{entity_upper} not found');
    
    return {{ analysis: 'Game analysis not yet implemented' }};
  }}'''
        
        elif method_name == "getGameAnalysis":
            return f'''  async {method_name}(id: string): Promise<{{analysis: string}}> {{
    const game = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!game.rows.length) throw new Error('{entity_upper} not found');
    
    return {{ analysis: 'Analysis for game ' + id }};
  }}'''
        
        elif method_name == "getGameReviews":
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE status = $1 ORDER BY created_at DESC LIMIT 20', ['completed']);
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # User-specific methods
        elif method_name == "getUserProfile":
            return f'''  async {method_name}(): Promise<{entity_upper}Response> {{
    // TODO: Get user ID from authentication context
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', ['current_user_id']);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateUserProfile":
            return f'''  async {method_name}(profileData: any): Promise<{entity_upper}Response> {{
    // TODO: Get user ID from authentication context
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET username = $1, email = $2, updated_at = NOW()
      WHERE id = $3
      RETURNING *
    `, [
      profileData.username,
      profileData.email,
      'current_user_id'
    ]);
    
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "getUserPreferences":
            return f'''  async {method_name}(): Promise<{entity_upper}Response> {{
    // TODO: Get user ID from authentication context
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', ['current_user_id']);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateUserPreferences":
            return f'''  async {method_name}(preferencesData: any): Promise<{entity_upper}Response> {{
    // TODO: Get user ID from authentication context
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET preferences = $1, updated_at = NOW()
      WHERE id = $2
      RETURNING *
    `, [
      JSON.stringify(preferencesData),
      'current_user_id'
    ]);
    
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "getUserSettings":
            return f'''  async {method_name}(): Promise<{entity_upper}Response> {{
    // TODO: Get user ID from authentication context  
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', ['current_user_id']);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == "updateUserSettings":
            return f'''  async {method_name}(settingsData: any): Promise<{entity_upper}Response> {{
    // TODO: Get user ID from authentication context
    const result = await this.db.query(`
      UPDATE {table_name} 
      SET chess_elo = $1, puzzle_rating = $2, updated_at = NOW()
      WHERE id = $3
      RETURNING *
    `, [
      settingsData.chess_elo,
      settingsData.puzzle_rating,
      'current_user_id'
    ]);
    
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # Authentication-specific methods
        elif method_name == "register":
            return f'''  async {method_name}(registerData: any): Promise<any> {{
    const {{ username, email, password }} = registerData;

    // Check if user already exists
    const existingUser = await this.db.query(
      'SELECT id FROM {table_name} WHERE email = $1 OR username = $2',
      [email, username]
    );

    if (existingUser.rows.length > 0) {{
      throw new Error('User with this email or username already exists');
    }}

    // Hash password
    const bcrypt = require('bcrypt');
    const passwordHash = await bcrypt.hash(password, 12);

    // Create user
    const userId = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (id, username, email, password_hash, chess_elo, puzzle_rating, preferences, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
      RETURNING *
    `, [userId, username, email, passwordHash, 1000, 1000, '{{}}']);

    if (!result.rows.length) {{
      throw new Error('Failed to create user');
    }}

    return this.format{entity_upper}Response(result.rows[0]);
  }}'''

        elif method_name == "login":
            return f'''  async {method_name}(loginData: any): Promise<any> {{
    const {{ email, password }} = loginData;

    // Find user by email
    const result = await this.db.query(
      'SELECT * FROM {table_name} WHERE email = $1',
      [email]
    );

    if (!result.rows.length) {{
      throw new Error('Invalid credentials');
    }}

    const user = result.rows[0];

    // Verify password
    const bcrypt = require('bcrypt');
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    if (!isValidPassword) {{
      throw new Error('Invalid credentials');
    }}

    // Generate JWT token
    const jwt = require('jsonwebtoken');
    const token = jwt.sign(
      {{ 
        userId: user.id, 
        email: user.email,
        username: user.username 
      }},
      process.env.JWT_SECRET!,
      {{ expiresIn: '7d' }}
    );

    return {{
      user: this.formatUserInfo(user),
      token
    }};
  }}'''

        elif method_name == "getCurrentUser":
            return f'''  async {method_name}(userId: string): Promise<any> {{
    // Get user info
    const userResult = await this.db.query(
      'SELECT * FROM {table_name} WHERE id = $1',
      [userId]
    );

    if (!userResult.rows.length) {{
      throw new Error('User not found');
    }}

    // Get user progress (or create default if doesn't exist)
    let progressResult = await this.db.query(
      'SELECT * FROM user_progress WHERE user_id = $1',
      [userId]
    );

    // If no progress exists, create default progress
    if (!progressResult.rows.length) {{
      const progressId = require('uuid').v4();
      await this.db.query(`
        INSERT INTO user_progress 
        (id, user_id, puzzles_solved, puzzles_correct, current_streak, best_streak, 
         total_time_spent, achievements_unlocked, created_at, updated_at)
        VALUES ($1, $2, 0, 0, 0, 0, 0, '[]', NOW(), NOW())
      `, [progressId, userId]);
      
      progressResult = await this.db.query(
        'SELECT * FROM user_progress WHERE user_id = $1',
        [userId]
      );
    }}

    return {{
      user: this.formatUserInfo(userResult.rows[0]),
      progress: this.formatUserProgress(progressResult.rows[0])
    }};
  }}'''

        elif method_name == "updateProfile":
            return f'''  async {method_name}(userId: string, profileData: any): Promise<any> {{
    const {{ username, email, chess_elo, puzzle_rating, preferences }} = profileData;

    // Build dynamic update query
    const updates = [];
    const values = [];
    let paramCount = 1;

    if (username !== undefined) {{
      updates.push(`username = $${{paramCount++}}`);
      values.push(username);
    }}
    if (email !== undefined) {{
      updates.push(`email = $=${{paramCount++}}`);
      values.push(email);
    }}
    if (chess_elo !== undefined) {{
      updates.push(`chess_elo = $=${{paramCount++}}`);
      values.push(chess_elo);
    }}
    if (puzzle_rating !== undefined) {{
      updates.push(`puzzle_rating = $=${{paramCount++}}`);
      values.push(puzzle_rating);
    }}
    if (preferences !== undefined) {{
      updates.push(`preferences = $=${{paramCount++}}`);
      values.push(typeof preferences === 'string' ? preferences : JSON.stringify(preferences));
    }}

    if (updates.length === 0) {{
      throw new Error('No fields to update');
    }}

    updates.push(`updated_at = NOW()`);
    values.push(userId); // For WHERE clause

    const query = `
      UPDATE {table_name} 
      SET ${{updates.join(', ')}}
      WHERE id = $$${{paramCount}}
      RETURNING *
    `;

    const result = await this.db.query(query, values);

    if (!result.rows.length) {{
      throw new Error('User not found');
    }}

    return this.format{entity_upper}Response(result.rows[0]);
  }}'''

        elif method_name == "changePassword":
            return f'''  async {method_name}(userId: string, passwordData: any): Promise<void> {{
    const {{ currentPassword, newPassword }} = passwordData;

    // Get current user
    const result = await this.db.query(
      'SELECT password_hash FROM {table_name} WHERE id = $1',
      [userId]
    );

    if (!result.rows.length) {{
      throw new Error('User not found');
    }}

    // Verify current password
    const bcrypt = require('bcrypt');
    const isValidPassword = await bcrypt.compare(currentPassword, result.rows[0].password_hash);
    if (!isValidPassword) {{
      throw new Error('Current password is incorrect');
    }}

    // Hash new password
    const newPasswordHash = await bcrypt.hash(newPassword, 12);

    // Update password
    await this.db.query(
      'UPDATE {table_name} SET password_hash = $1, updated_at = NOW() WHERE id = $2',
      [newPasswordHash, userId]
    );
  }}'''

        elif method_name == "verifyToken":
            return f'''  async {method_name}(token: string): Promise<any> {{
    try {{
      const jwt = require('jsonwebtoken');
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
      
      // Get updated user info
      const result = await this.db.query(
        'SELECT * FROM {table_name} WHERE id = $1',
        [decoded.userId]
      );

      if (!result.rows.length) {{
        throw new Error('User not found');
      }}

      return {{
        user: this.formatUserInfo(result.rows[0]),
        tokenValid: true
      }};
    }} catch (error) {{
      throw new Error('Invalid token');
    }}
  }}'''

        elif method_name == "forgotPassword":
            return f'''  async {method_name}(forgotData: any): Promise<void> {{
    const {{ email }} = forgotData;

    // Check if user exists
    const result = await this.db.query(
      'SELECT id FROM {table_name} WHERE email = $1',
      [email]
    );

    if (!result.rows.length) {{
      // Don't reveal if email exists or not for security
      return;
    }}

    // In a real app, you would:
    // 1. Generate a reset token
    // 2. Store it in database with expiration
    // 3. Send email with reset link
    console.log(`Password reset requested for email: ${{email}}`);
  }}'''

        elif method_name == "resetPassword":
            return f'''  async {method_name}(resetData: any): Promise<void> {{
    const {{ resetToken, password }} = resetData;

    // In a real app, you would:
    // 1. Verify reset token from database
    // 2. Check if token is not expired
    // 3. Update user password
    // 4. Invalidate the reset token
    
    // For now, we'll throw an error since token system isn't implemented
    throw new Error('Password reset functionality requires email service integration');
  }}'''

        elif method_name == "logout":
            return f'''  async {method_name}(): Promise<void> {{
    // JWT tokens are stateless, so logout is handled client-side
    // In a real app with token blacklisting, you would store the token
    // in a blacklist until it expires
    return;
  }}'''

        elif method_name == "checkEmailAvailability":
            return f'''  async {method_name}(emailData: any): Promise<any> {{
    const {{ email }} = emailData;

    const result = await this.db.query(
      'SELECT id FROM {table_name} WHERE email = $1',
      [email]
    );

    return {{ available: result.rows.length === 0 }};
  }}'''

        elif method_name == "checkUsernameAvailability":
            return f'''  async {method_name}(usernameData: any): Promise<any> {{
    const {{ username }} = usernameData;

    const result = await this.db.query(
      'SELECT id FROM {table_name} WHERE username = $1',
      [username]
    );

    return {{ available: result.rows.length === 0 }};
  }}'''

        elif method_name == "deleteAccount":
            return f'''  async {method_name}(userId: string): Promise<void> {{
    // Delete user and all related data
    // This should be done in a transaction in production
    await this.db.query('DELETE FROM user_progress WHERE user_id = $1', [userId]);
    await this.db.query('DELETE FROM {table_name} WHERE id = $1', [userId]);
  }}'''

        elif method_name == "healthCheck":
            return f'''  async {method_name}() {{
    return {{
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      service: 'auth'
    }};
  }}'''
        
        # Generic methods
        elif method_name.startswith("get") and method_name.endswith("ById"):
            return f'''  async {method_name}(id: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name.startswith("getAll") or method_name.startswith("get") and not method_name.endswith("ById"):
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        else:
            # Default stub method
            return f'''  async {method_name}(...args: any[]): Promise<any> {{
    // TODO: Implement {method_name}
    throw new Error('{method_name} not implemented');
  }}'''

    def _get_handler_params(self, handler_name: str, path: str) -> str:
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
        
        # Generic patterns
        elif "ById" in handler_name or ":id" in path:
            return "req.params.id"
        elif handler_name.startswith("create") or handler_name.startswith("update"):
            return "req.body"
        elif handler_name.startswith("get"):
            return ""
        else:
            return "req.body"

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
        
        return f'''  private format{entity_upper}Response(row: any): {entity_upper}Response {{
    return {{
{chr(10).join(format_fields)}
    }};
  }}'''

def main():
    """Main function to run the generator"""
    import sys
    
    print("🚀 Backend Generator Starting...")
    if REFACTORED_AVAILABLE:
        print("✅ Using refactored modular architecture")
    else:
        print("⚠️  Using legacy generator (install backend_tools for improved functionality)")
    
    if len(sys.argv) < 2:
        print("Usage: python backend_generator.py <endpoint_name>")
        print("Available endpoints: users, puzzles, games, stats, learning, tutorials")
        return
    
    endpoint_name = sys.argv[1].lower()
    
    # Load config
    with open('backend_config.json', 'r') as f:
        config = json.load(f)
    
    if endpoint_name not in config['endpoints']:
        print(f"Error: {endpoint_name} not found in config")
        print(f"Available endpoints: {', '.join(config['endpoints'].keys())}")
        return
    
    target_dir = config.get('target_directory', '../backend')
    generator = BackendGenerator(target_dir)
    endpoint_config = config['endpoints'][endpoint_name]
    
    print(f"🔧 Generating {endpoint_config['entity']} endpoint...")
    success = generator.generate_endpoint(endpoint_config)
    
    if success:
        print(f"✅ Generated {endpoint_config['entity']} endpoint files")
        print("✅ Backend generation complete!")
    else:
        print("❌ Failed to generate endpoint files")

if __name__ == "__main__":
    main()