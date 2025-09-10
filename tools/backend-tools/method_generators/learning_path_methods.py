#!/usr/bin/env python3
"""
Learning Path Method Generator
Generates learning path-specific service methods
"""

from base_generator import BaseMethodGenerator


class LearningPathMethodGenerator(BaseMethodGenerator):
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate learning path-specific methods"""
        
        if method_name == "getLearningPaths":
            return '''  async getLearningPaths(): Promise<LearningPathResponse[]> {
    const result = await this.db.query('SELECT * FROM learning_paths ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningPathResponse(row));
  }'''
        
        elif method_name == "getLearningPathById":
            return '''  async getLearningPathById(id: string): Promise<LearningPathResponse> {
    const result = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Learning path not found');
    
    return this.formatLearningPathResponse(result.rows[0]);
  }'''
        
        elif method_name == "enrollInPath":
            return '''  async enrollInPath(pathId: string, userId: string): Promise<any> {
    // First, verify the learning path exists
    const pathResult = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [pathId]);
    if (!pathResult.rows.length) throw new Error('Learning path not found');
    
    // Check if user is already enrolled
    const enrollmentCheck = await this.db.query(
      'SELECT * FROM user_learning_paths WHERE user_id = $1 AND learning_path_id = $2', 
      [userId, pathId]
    );
    
    if (enrollmentCheck.rows.length > 0) {
      throw new Error('User already enrolled in this learning path');
    }
    
    // Create enrollment record
    const enrollmentId = require('uuid').v4();
    await this.db.query(`
      INSERT INTO user_learning_paths (id, user_id, learning_path_id, progress, enrolled_at, created_at, updated_at)
      VALUES ($1, $2, $3, 0, NOW(), NOW(), NOW())
    `, [enrollmentId, userId, pathId]);
    
    // Return the learning path with enrollment status
    const learningPath = this.formatLearningPathResponse(pathResult.rows[0]);
    return {
      ...learningPath,
      enrolled: true,
      progress: 0,
      enrolled_at: new Date().toISOString()
    };
  }'''
        
        elif method_name == "updateProgress":
            return '''  async updateProgress(pathId: string, userId: string, progressData: any): Promise<any> {
    // Update user's progress in the learning path
    const result = await this.db.query(`
      UPDATE user_learning_paths 
      SET progress = $3, updated_at = NOW()
      WHERE user_id = $1 AND learning_path_id = $2
      RETURNING *
    `, [userId, pathId, progressData.progress || 0]);
    
    if (!result.rows.length) throw new Error('Enrollment not found - user must enroll first');
    
    // Get the learning path details
    const pathResult = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [pathId]);
    if (!pathResult.rows.length) throw new Error('Learning path not found');
    
    const learningPath = this.formatLearningPathResponse(pathResult.rows[0]);
    return {
      ...learningPath,
      progress: result.rows[0].progress,
      updated_at: result.rows[0].updated_at
    };
  }'''
        
        # Standard CRUD methods
        elif method_name == f"getAll{entity_upper}s":
            return f'''  async getAll{entity_upper}s(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        elif method_name == f"get{entity_upper}ById":
            return f'''  async get{entity_upper}ById(id: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == f"create{entity_upper}":
            return f'''  async create{entity_upper}(data: Create{entity_upper}Request): Promise<{entity_upper}Response> {{
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (id, title, description, difficulty, modules, progress, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
      RETURNING *
    `, [id, data.title, data.description, data.difficulty, JSON.stringify(data.modules || []), data.progress || 0]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == f"update{entity_upper}":
            return f'''  async update{entity_upper}(id: string, data: Update{entity_upper}Request): Promise<{entity_upper}Response> {{
    const updateFields = [];
    const updateValues = [];
    let paramIndex = 2;
    
    if (data.title) {{
      updateFields.push(`title = ${{paramIndex}}`);
      updateValues.push(data.title);
      paramIndex++;
    }}
    if (data.description) {{
      updateFields.push(`description = ${{paramIndex}}`);
      updateValues.push(data.description);
      paramIndex++;
    }}
    if (data.difficulty) {{
      updateFields.push(`difficulty = ${{paramIndex}}`);
      updateValues.push(data.difficulty);
      paramIndex++;
    }}
    if (data.modules) {{
      updateFields.push(`modules = ${{paramIndex}}`);
      updateValues.push(JSON.stringify(data.modules));
      paramIndex++;
    }}
    if (data.progress !== undefined) {{
      updateFields.push(`progress = ${{paramIndex}}`);
      updateValues.push(data.progress);
      paramIndex++;
    }}
    
    updateFields.push('updated_at = NOW()');
    
    const query = `UPDATE {table_name} SET ${{updateFields.join(', ')}} WHERE id = $1 RETURNING *`;
    const result = await this.db.query(query, [id, ...updateValues]);
    
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        elif method_name == f"delete{entity_upper}":
            return f'''  async delete{entity_upper}(id: string): Promise<void> {{
    await this.db.query('DELETE FROM {table_name} WHERE id = $1', [id]);
  }}'''
        
        else:
            # Use the base generator's stub method for unknown methods
            return self._create_stub_method(method_name, table_name, entity_upper)