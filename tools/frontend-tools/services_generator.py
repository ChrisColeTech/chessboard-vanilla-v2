#!/usr/bin/env python3
"""
Services Generator Module
Handles generation of service layer files for all domains
"""

from typing import List
from base_generator import BaseFrontendGenerator

class ServicesGenerator(BaseFrontendGenerator):
    """Generates service layer files for all domains"""
    
    def generate_domain_services(self, domain: str, endpoints: List[str]):
        """Generate individual service files for a domain"""
        src_path = self.get_src_path()
        services_path = src_path / "services" / domain
        
        # Get relevant endpoints for this domain
        domain_endpoints = []
        for endpoint_name in endpoints:
            if endpoint_name in self.backend_config['endpoints']:
                domain_endpoints.append(endpoint_name)
        
        if not domain_endpoints:
            return
            
        # Create main domain service file
        service_name = f"{self.capitalize_domain(domain)}Service"
        service_content = self._generate_base_service_content(domain, service_name)
        
        service_file = services_path / f"{service_name}.ts"
        self.write_file(service_file, service_content)
        
        # Create additional specialized service files based on domain
        generated_services = [service_name]
        
        if domain == 'auth':
            auth_service_content = self._generate_auth_service_content()
            auth_file = services_path / "AuthService.ts"
            self.write_file(auth_file, auth_service_content)
            generated_services.append('AuthService')
            
        elif domain == 'chess':
            chess_service_content = self._generate_chess_service_content()
            chess_file = services_path / "ChessService.ts"
            self.write_file(chess_file, chess_service_content)
            generated_services.append('ChessService')
        
        # Generate index file that exports all services
        self._generate_services_index(services_path, domain, generated_services)
    
    def _generate_base_service_content(self, domain: str, service_name: str) -> str:
        """Generate base service content"""
        return f"""/**
 * {self.capitalize_domain(domain)} Domain Service
 * Business logic layer for {domain} operations
 */
export class {service_name} {{
  // Service methods will be implemented based on specific domain requirements
  // This is a placeholder - implement specific methods as needed
  
  static async healthCheck(): Promise<any> {{
    try {{
      // Placeholder health check
      return {{ success: true, data: {{ status: 'healthy', domain: '{domain}' }} }};
    }} catch (error) {{
      throw new Error(`{domain} service health check failed`);
    }}
  }}
}}

export default {service_name};
"""
    
    def _generate_auth_service_content(self) -> str:
        """Generate AuthService with actual auth methods"""
        return """import { AuthAPIClient } from '../../clients/AuthAPIClient';
import type { ApiResponse } from '../../types/common';

/**
 * Authentication Service
 * Handles user authentication and authorization
 */
export class AuthService {
  private static client = new AuthAPIClient();

  static async login(credentials: { email: string; password: string }): Promise<ApiResponse<any>> {
    return this.client.login(credentials);
  }

  static async register(userData: { username: string; email: string; password: string }): Promise<ApiResponse<any>> {
    return this.client.register(userData);
  }

  static async logout(): Promise<ApiResponse<void>> {
    return this.client.logout({});
  }

  static async getCurrentUser(): Promise<ApiResponse<any>> {
    return this.client.getCurrentUser();
  }

  static async updateProfile(data: any): Promise<ApiResponse<any>> {
    return this.client.updateProfile(data);
  }

  static async changePassword(data: { currentPassword: string; newPassword: string }): Promise<ApiResponse<void>> {
    return this.client.changePassword(data);
  }

  static async verifyToken(token: string): Promise<ApiResponse<any>> {
    return this.client.verifyToken({ token });
  }

  static async forgotPassword(email: string): Promise<ApiResponse<void>> {
    return this.client.forgotPassword({ email });
  }

  static async resetPassword(data: { token: string; password: string }): Promise<ApiResponse<void>> {
    return this.client.resetPassword(data);
  }

  static async checkEmailAvailability(email: string): Promise<ApiResponse<boolean>> {
    return this.client.checkEmailAvailability({ email });
  }

  static async checkUsernameAvailability(username: string): Promise<ApiResponse<boolean>> {
    return this.client.checkUsernameAvailability({ username });
  }

  static async deleteAccount(id: string): Promise<ApiResponse<void>> {
    return this.client.deleteAccount(id);
  }
}

export default AuthService;
"""
    
    def _generate_chess_service_content(self) -> str:
        """Generate ChessService with chess-specific methods"""
        return """import { ChessAPIClient } from '../../clients/ChessAPIClient';
import type { ApiResponse } from '../../types/common';

/**
 * Chess Service
 * Handles chess games and puzzles
 */
export class ChessService {
  private static client = new ChessAPIClient();

  static async getNextPuzzle(filters?: any): Promise<ApiResponse<any>> {
    return this.client.getNextPuzzle(filters);
  }

  static async solvePuzzle(id: string, solution: any): Promise<ApiResponse<any>> {
    return this.client.solvePuzzle(id, solution);
  }

  static async getPuzzleHint(id: string): Promise<ApiResponse<any>> {
    return this.client.getPuzzleHint(id);
  }

  static async createGame(gameData: any): Promise<ApiResponse<any>> {
    return this.client.createGame(gameData);
  }

  static async updateGame(id: string, gameData: any): Promise<ApiResponse<any>> {
    return this.client.updateGame(id, gameData);
  }

  static async analyzeGame(id: string, analysisData: any): Promise<ApiResponse<any>> {
    return this.client.analyzeGame(id, analysisData);
  }

  static async getGameById(id: string): Promise<ApiResponse<any>> {
    return this.client.getGameById(id);
  }

  static async getGames(filters?: any): Promise<ApiResponse<any[]>> {
    return this.client.getGames(filters);
  }
}

export default ChessService;
"""
    
    def _generate_services_index(self, services_path, domain: str, generated_services: List[str]):
        """Generate index file that exports all services for the domain"""
        # Remove duplicates and ensure we only export what exists
        unique_services = list(set(generated_services))
            
        index_content = f"""// {self.capitalize_domain(domain)} Domain Services
{chr(10).join([f'export {{ {service} }} from \'./{service}\';' for service in unique_services])}
"""
        
        index_file = services_path / "index.ts"
        self.write_file(index_file, index_content)