// Authentication API service for backend communication
import type {
  AuthApiClient,
  AuthResponse,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  ResetPasswordRequest,
  ChangePasswordRequest,
  UpdateProfileRequest,
  MeResponse,
  TokenVerificationResponse,
  User
} from '../types';

import { DEFAULT_AUTH_CONFIG, ApiUtils, AuthErrorUtils } from '../utils';

/**
 * Authentication API client implementation
 */
export class AuthService implements AuthApiClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || DEFAULT_AUTH_CONFIG.apiBaseUrl;
  }

  /**
   * User login
   */
  async login(credentials: LoginRequest): Promise<AuthResponse<LoginResponse>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await ApiUtils.handleResponse<AuthResponse<LoginResponse>>(response);
      return data;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * User registration
   */
  async register(userData: RegisterRequest): Promise<AuthResponse<User>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await ApiUtils.handleResponse<AuthResponse<User>>(response);
      return data;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Request password reset
   */
  async forgotPassword(email: string): Promise<AuthResponse<void>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await ApiUtils.handleResponse<AuthResponse<void>>(response);
      return data;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Reset password with token
   */
  async resetPassword(data: ResetPasswordRequest): Promise<AuthResponse<void>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await ApiUtils.handleResponse<AuthResponse<void>>(response);
      return result;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Change password (authenticated)
   */
  async changePassword(data: ChangePasswordRequest): Promise<AuthResponse<void>> {
    try {
      const response = await ApiUtils.fetchWithAuth(
        `${this.baseUrl}/auth/change-password`,
        {
          method: 'POST',
          body: JSON.stringify(data),
        }
      );

      const result = await ApiUtils.handleResponse<AuthResponse<void>>(response);
      return result;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Update user profile (authenticated)
   */
  async updateProfile(data: UpdateProfileRequest): Promise<AuthResponse<User>> {
    try {
      const response = await ApiUtils.fetchWithAuth(
        `${this.baseUrl}/auth/profile`,
        {
          method: 'PUT',
          body: JSON.stringify(data),
        }
      );

      const result = await ApiUtils.handleResponse<AuthResponse<User>>(response);
      return result;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Get current user info (authenticated)
   */
  async getCurrentUser(): Promise<AuthResponse<MeResponse>> {
    try {
      const response = await ApiUtils.fetchWithAuth(
        `${this.baseUrl}/auth/me`,
        {
          method: 'GET',
        }
      );

      const data = await ApiUtils.handleResponse<AuthResponse<MeResponse>>(response);
      return data;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Verify JWT token
   */
  async verifyToken(token: string): Promise<AuthResponse<TokenVerificationResponse>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/verify-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      });

      const data = await ApiUtils.handleResponse<AuthResponse<TokenVerificationResponse>>(response);
      return data;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Logout user (client-side token removal)
   */
  async logout(): Promise<AuthResponse<void>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await ApiUtils.handleResponse<AuthResponse<void>>(response);
      return data;
    } catch (error: any) {
      // Logout can fail gracefully - we'll clear local storage anyway
      console.warn('Logout API call failed:', error);
      return {
        success: true,
        message: 'Logged out successfully'
      };
    }
  }

  /**
   * Check if the API is reachable
   */
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    try {
      const response = await fetch(`${this.baseUrl.replace('/api', '')}/health`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }

      return response.json();
    } catch (error: any) {
      console.error('Health check failed:', error);
      throw AuthErrorUtils.createAuthError(
        'NETWORK_ERROR',
        'Unable to connect to authentication server',
        0,
        error
      );
    }
  }

  /**
   * Refresh user data
   */
  async refreshUserData(): Promise<AuthResponse<MeResponse>> {
    return this.getCurrentUser();
  }

  /**
   * Check if email is available (for registration)
   */
  async checkEmailAvailable(email: string): Promise<{ available: boolean }> {
    try {
      // This would be a custom endpoint if implemented on backend
      // For now, we'll just try to register and catch the error
      const response = await fetch(`${this.baseUrl}/auth/check-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        // If endpoint doesn't exist, assume email checking isn't supported
        return { available: true };
      }

      return response.json();
    } catch (error: any) {
      // If endpoint doesn't exist, assume email checking isn't supported
      return { available: true };
    }
  }

  /**
   * Check if username is available (for registration)
   */
  async checkUsernameAvailable(username: string): Promise<{ available: boolean }> {
    try {
      // This would be a custom endpoint if implemented on backend
      const response = await fetch(`${this.baseUrl}/auth/check-username`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
      });

      if (!response.ok) {
        return { available: true };
      }

      return response.json();
    } catch (error: any) {
      return { available: true };
    }
  }

  /**
   * Request account deletion (would need backend implementation)
   */
  async deleteAccount(): Promise<AuthResponse<void>> {
    try {
      const response = await ApiUtils.fetchWithAuth(
        `${this.baseUrl}/auth/delete-account`,
        {
          method: 'DELETE',
        }
      );

      const data = await ApiUtils.handleResponse<AuthResponse<void>>(response);
      return data;
    } catch (error: any) {
      throw AuthErrorUtils.parseApiError(error);
    }
  }

  /**
   * Update API base URL
   */
  setBaseUrl(baseUrl: string): void {
    this.baseUrl = baseUrl;
  }

  /**
   * Get current API base URL
   */
  getBaseUrl(): string {
    return this.baseUrl;
  }
}

// Create singleton instance
export const authService = new AuthService();

// Export the service class for custom instances
export default AuthService;