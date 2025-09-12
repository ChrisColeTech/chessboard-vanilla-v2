import { AuthAPIClient } from '../../clients/AuthAPIClient';
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
