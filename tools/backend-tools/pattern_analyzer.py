#!/usr/bin/env python3
"""
Pattern Analysis Module
Analyzes existing backend files to extract patterns for code generation
"""

from pathlib import Path
from typing import Dict
from config import DEFAULT_BACKEND_PATH


class PatternAnalyzer:
    def __init__(self, backend_path: str = None):
        self.backend_path = Path(backend_path or DEFAULT_BACKEND_PATH)
    
    def analyze_existing_pattern(self, reference_service: str = "puzzles") -> Dict:
        """Analyze existing files to extract patterns"""
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