#!/usr/bin/env python3
"""
Profile Service Method Generator
Generates specialized profile service methods based on the gold standard implementation
"""

from base_generator import BaseMethodGenerator


class ProfileMethodGenerator(BaseMethodGenerator):
    """Generates profile service methods with professional gold standard implementation including upsert logic"""
    
    def generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str:
        """Generate profile service method based on gold standard implementation"""
        
        # getProfile - Flexible profile retrieval with optional user filtering
        if method_name == "getProfile":
            return f'''  async {method_name}(userId?: string): Promise<{entity_upper}Response[]> {{
    let query = 'SELECT * FROM {table_name}';
    let params: any[] = [];
    
    if (userId) {{
      query += ' WHERE user_id = $1';
      params.push(userId);
    }}
    
    query += ' ORDER BY created_at DESC LIMIT 50';
    
    const result = await this.db.query(query, params);
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # updateProfile - Complete implementation with upsert logic
        elif method_name == "updateProfile":
            return f'''  async {method_name}(userId: string, data: Update{entity_upper}Request): Promise<{entity_upper}Response> {{
    // First try to update existing profile
    let result = await this.db.query(`
      UPDATE {table_name} 
      SET display_name = COALESCE($2, display_name),
          avatar_url = COALESCE($3, avatar_url),
          bio = COALESCE($4, bio),
          country = COALESCE($5, country),
          timezone = COALESCE($6, timezone),
          updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `, [userId, data.display_name, data.avatar_url, data.bio, data.country, data.timezone]);
    
    // If no profile exists, create one (upsert logic)
    if (!result.rows.length) {{
      const profileId = uuidv4();
      result = await this.db.query(`
        INSERT INTO {table_name} (id, user_id, display_name, avatar_url, bio, country, timezone, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
        RETURNING *
      `, [profileId, userId, data.display_name, data.avatar_url, data.bio, data.country, data.timezone]);
    }}
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # getAllProfiles - Standard list with limit
        elif method_name.startswith("getAll") or method_name == f"getAll{entity_upper}s" or method_name == f"getAll{entity_upper}":
            return f'''  async {method_name}(): Promise<{entity_upper}Response[]> {{
    const result = await this.db.query('SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # getProfileById - Standard get by ID
        elif method_name.endswith("ById") or method_name == f"get{entity_upper}ById":
            return f'''  async {method_name}(id: string): Promise<{entity_upper}Response> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # getProfileByUserId - User-specific profile lookup with null handling
        elif method_name == "getProfileByUserId":
            return f'''  async {method_name}(userId: string): Promise<{entity_upper}Response | null> {{
    const result = await this.db.query('SELECT * FROM {table_name} WHERE user_id = $1', [userId]);
    return result.rows.length ? this.format{entity_upper}Response(result.rows[0]) : null;
  }}'''
        
        # createProfile - Complete creation with proper defaults
        elif method_name.startswith("create") or method_name == f"create{entity_upper}":
            return f'''  async {method_name}(data: Create{entity_upper}Request): Promise<{entity_upper}Response> {{
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO {table_name} (
        id, user_id, display_name, avatar_url, bio, country, timezone, created_at, updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
      RETURNING *
    `, [
      id, 
      data.user_id || null,
      data.display_name || null,
      data.avatar_url || null,
      data.bio || null,
      data.country || null,
      data.timezone || null
    ]);
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # deleteProfile - Standard deletion
        elif method_name.startswith("delete") or method_name == f"delete{entity_upper}":
            return f'''  async {method_name}(id: string): Promise<void> {{
    await this.db.query('DELETE FROM {table_name} WHERE id = $1', [id]);
  }}'''
        
        # deleteProfileByUserId - User-specific deletion
        elif method_name == "deleteProfileByUserId":
            return f'''  async {method_name}(userId: string): Promise<void> {{
    await this.db.query('DELETE FROM {table_name} WHERE user_id = $1', [userId]);
  }}'''
        
        # searchProfiles - Advanced search functionality
        elif method_name == "searchProfiles":
            return f'''  async {method_name}(searchTerm?: string): Promise<{entity_upper}Response[]> {{
    let query = 'SELECT * FROM {table_name}';
    let params: any[] = [];
    
    if (searchTerm) {{
      query += ' WHERE display_name ILIKE $1 OR bio ILIKE $1';
      params.push(`%${{searchTerm}}%`);
    }}
    
    query += ' ORDER BY created_at DESC LIMIT 50';
    
    const result = await this.db.query(query, params);
    return result.rows.map(row => this.format{entity_upper}Response(row));
  }}'''
        
        # updateProfileField - Secure field-specific updates
        elif method_name == "updateProfileField":
            return f'''  async {method_name}(userId: string, field: string, value: any): Promise<{entity_upper}Response> {{
    // Validate allowed fields for security
    const allowedFields = ['display_name', 'avatar_url', 'bio', 'country', 'timezone'];
    if (!allowedFields.includes(field)) {{
      throw new Error('Invalid field specified');
    }}
    
    const query = `
      UPDATE {table_name} 
      SET ${{field}} = $2, updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `;
    
    const result = await this.db.query(query, [userId, value]);
    if (!result.rows.length) throw new Error('{entity_upper} not found');
    
    return this.format{entity_upper}Response(result.rows[0]);
  }}'''
        
        # Generic fallback for any other methods
        else:
            return self._create_stub_method(method_name, table_name, entity_upper)