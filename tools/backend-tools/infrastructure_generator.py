#!/usr/bin/env python3
"""
Infrastructure Generator Module
Creates necessary infrastructure files (middleware, utils, etc.)
"""

import logging
from pathlib import Path
from typing import Dict, Any
from config import DEFAULT_BACKEND_PATH


class InfrastructureGenerator:
    """Generates infrastructure files required by the backend"""
    
    def __init__(self, backend_path: str = None):
        self.backend_path = Path(backend_path or DEFAULT_BACKEND_PATH)
        self.logger = logging.getLogger("infrastructure_generator")
    
    def generate_infrastructure(self) -> bool:
        """Generate all required infrastructure files"""
        try:
            self.logger.info("🏗️ Generating infrastructure files...")
            
            # Create directories
            self._create_directories()
            
            # Generate files
            self._generate_database_utils()
            self._generate_auth_middleware()
            self._generate_validation_middleware()
            self._generate_app_file()
            
            self.logger.info("✅ Infrastructure files generated successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Infrastructure generation failed: {e}")
            return False
    
    def _create_directories(self):
        """Create necessary directories"""
        dirs = [
            self.backend_path / "src" / "middleware",
            self.backend_path / "src" / "utils",
            self.backend_path / "src" / "models",
            self.backend_path / "src" / "services", 
            self.backend_path / "src" / "routes"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"📁 Created directory: {dir_path.relative_to(self.backend_path)}")
    
    def _generate_database_utils(self):
        """Generate database utility file"""
        content = '''import { Pool } from 'pg';

export class Database {
  private static instance: Database;
  private pool: Pool;

  private constructor() {
    this.pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
      max: 5,                           // Lower max for Supabase pooler compatibility
      min: 1,                           // Lower min to prevent connection exhaustion
      idleTimeoutMillis: 10000,         // Shorter idle timeout for Supabase
      connectionTimeoutMillis: 10000,   // Longer connection timeout
      allowExitOnIdle: false,           // Keep pool alive to prevent reconnection issues
      keepAlive: true,                  // Enable TCP keepalive
      keepAliveInitialDelayMillis: 10000 // TCP keepalive initial delay
    });

    // Handle pool errors with reconnection logic
    this.pool.on('error', (err) => {
      console.error('❌ Database pool error:', err);
      if (err.message && err.message.includes('termination')) {
        console.log('🔄 Database connection terminated, pool will handle reconnection');
      }
    });

    // Handle pool connect events
    this.pool.on('connect', (client) => {
      console.log('🔗 Database client connected');
      // Set statement timeout to prevent long-running queries
      client.query('SET statement_timeout = 30000');
    });

    // Handle pool disconnect events  
    this.pool.on('remove', (client) => {
      console.log('🔌 Database client disconnected');
    });
  }

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  async query(text: string, params?: any[]) {
    let client;
    try {
      client = await this.pool.connect();
      const result = await client.query(text, params);
      return result;
    } catch (error) {
      console.error('❌ Database query error:', error);
      if (error.message && error.message.includes('termination')) {
        console.log('🔄 Query failed due to connection termination, retrying...');
        // Retry once on termination
        try {
          const newClient = await this.pool.connect();
          const result = await newClient.query(text, params);
          newClient.release();
          return result;
        } catch (retryError) {
          console.error('❌ Retry also failed:', retryError);
          throw retryError;
        }
      }
      throw error;
    } finally {
      if (client) {
        client.release();
      }
    }
  }

  async getPoolInfo() {
    return {
      totalCount: this.pool.totalCount,
      idleCount: this.pool.idleCount,
      waitingCount: this.pool.waitingCount
    };
  }

  async close() {
    await this.pool.end();
  }
}

export const db = Database.getInstance();
export default Database;'''
        
        file_path = self.backend_path / "src" / "utils" / "database.ts"
        file_path.write_text(content)
        self.logger.info(f"📝 Generated: {file_path.relative_to(self.backend_path)}")
    
    def _generate_auth_middleware(self):
        """Generate authentication middleware"""
        content = '''import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    username: string;
    email: string;
  };
}

export const authenticate = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key', (err: any, user: any) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

export const optionalAuth = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return next();
  }

  jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key', (err: any, user: any) => {
    if (!err) {
      req.user = user;
    }
    next();
  });
};'''
        
        file_path = self.backend_path / "src" / "middleware" / "auth.ts"
        file_path.write_text(content)
        self.logger.info(f"📝 Generated: {file_path.relative_to(self.backend_path)}")
    
    def _generate_validation_middleware(self):
        """Generate validation middleware"""
        content = '''import { Request, Response, NextFunction } from 'express';
import { validationResult } from 'express-validator';

export const validate = (req: Request, res: Response, next: NextFunction) => {
  const errors = validationResult(req);
  
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation failed',
      details: errors.array()
    });
  }
  
  next();
};

export const validateSchema = (schema: any) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const { error } = schema.validate(req.body);
    
    if (error) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.details
      });
    }
    
    next();
  };
};'''
        
        file_path = self.backend_path / "src" / "middleware" / "validation.ts"
        file_path.write_text(content)
        self.logger.info(f"📝 Generated: {file_path.relative_to(self.backend_path)}")
    
    def _generate_app_file(self):
        """Generate main app.ts file with dynamic route registration"""
        # Load backend config to get available endpoints
        config_path = Path(__file__).parent.parent / "backend_config.json"
        route_imports = []
        route_registrations = []
        
        try:
            if config_path.exists():
                import json
                with open(config_path) as f:
                    config = json.load(f)
                
                # Generate route imports and registrations from config
                for endpoint_key, endpoint_config in config.get("endpoints", {}).items():
                    # Use the 'entities' field to determine the actual route filename
                    entities_name = endpoint_config.get('entities', endpoint_key)
                    
                    # Convert snake_case to camelCase for both file names and API paths
                    def snake_to_camel(snake_str):
                        components = snake_str.split('_')
                        return components[0] + ''.join(word.capitalize() for word in components[1:])
                    
                    # File name uses camelCase
                    route_filename = snake_to_camel(entities_name.replace('-', '_'))
                    
                    # Generate variable name from endpoint key for consistency
                    route_var_name = endpoint_key.replace('-', '_').replace(' ', '_')  # Variable name (no hyphens)
                    camel_var_name = ''.join(word.capitalize() for word in route_var_name.split('_')) + 'Router'
                    
                    # Generate import statement using camelCase filename
                    route_imports.append(f"import {camel_var_name} from './routes/{route_filename}';")
                    
                    # API URL also uses camelCase
                    camel_url = snake_to_camel(entities_name)
                    
                    # Generate route registration using camelCase for API path
                    route_registrations.append(f"app.use('/api/{camel_url}', {camel_var_name});")
            
        except Exception as e:
            self.logger.warning(f"Could not load backend config, using default routes: {e}")
        
        # Join imports and registrations
        imports_section = '\n'.join(route_imports)
        registrations_section = '\n'.join(route_registrations)
        
        content = f'''import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Request logging middleware
app.use((req, res, next) => {{
  console.log(`📥 ${{new Date().toISOString()}} - ${{req.method}} ${{req.path}}`);
  if (req.body && Object.keys(req.body).length > 0) {{
    console.log(`   Body:`, JSON.stringify(req.body, null, 2));
  }}
  if (req.query && Object.keys(req.query).length > 0) {{
    console.log(`   Query:`, JSON.stringify(req.query, null, 2));
  }}
  next();
}});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({{ extended: true }}));

// Health check endpoint
app.get('/health', (req, res) => {{
  res.json({{ status: 'OK', timestamp: new Date().toISOString() }});
}});

// Import route handlers
{imports_section}

// Register API routes
{registrations_section}

// Response logging middleware
app.use((req, res, next) => {{
  const originalSend = res.send;
  res.send = function(data) {{
    console.log(`📤 ${{new Date().toISOString()}} - ${{req.method}} ${{req.path}} - ${{res.statusCode}}`);
    if (res.statusCode >= 400) {{
      console.log(`   Error Response:`, data);
    }}
    return originalSend.call(this, data);
  }};
  next();
}});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {{
  console.error('❌ Internal Error:', err);
  console.error('   Stack:', err.stack);
  res.status(500).json({{ error: 'Internal server error' }});
}});

// 404 handler
app.use('*', (req, res) => {{
  res.status(404).json({{ error: 'Route not found' }});
}});

if (require.main === module) {{
  app.listen(PORT, () => {{
    console.log(`🚀 Server running on port ${{PORT}}`);
  }});
}}

export default app;'''
        
        file_path = self.backend_path / "src" / "app.ts"
        file_path.write_text(content)
        self.logger.info(f"📝 Generated: {file_path.relative_to(self.backend_path)} with {len(route_imports)} routes")


def main():
    """CLI for infrastructure generator"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Infrastructure Generator - Create necessary backend infrastructure')
    parser.add_argument('--backend-path', default='../backend', help='Backend directory path')
    
    args = parser.parse_args()
    
    generator = InfrastructureGenerator(args.backend_path)
    
    print("🏗️ Infrastructure Generator Starting...")
    
    success = generator.generate_infrastructure()
    
    if success:
        print("✅ Infrastructure generation completed successfully!")
    else:
        print("❌ Infrastructure generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()