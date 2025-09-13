// Authentication utility functions for token handling, validation, and storage
import type { User, TokenInfo, AuthStorage, AuthConfig, AuthError, AuthErrorType } from '../types';

// Default auth configuration
export const DEFAULT_AUTH_CONFIG: AuthConfig = {
  apiBaseUrl: 'http://localhost:3001/api',
  tokenStorageKey: 'chess_app_token',
  tokenExpirationBuffer: 5 // 5 minutes before expiry
};

// Token utilities
export class TokenUtils {
  private static readonly STORAGE_KEY = DEFAULT_AUTH_CONFIG.tokenStorageKey;
  private static readonly USER_STORAGE_KEY = 'chess_app_user';

  /**
   * Decode JWT token payload without verification
   * Note: This is for client-side token inspection only, not security validation
   */
  static decodeTokenPayload(token: string): any {
    try {
      const payload = token.split('.')[1];
      const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
      return JSON.parse(decoded);
    } catch (error) {
      return null;
    }
  }

  /**
   * Get token information including expiration status
   */
  static getTokenInfo(token: string): TokenInfo | null {
    const payload = this.decodeTokenPayload(token);
    if (!payload || !payload.exp) {
      return null;
    }

    const expiresAt = new Date(payload.exp * 1000);
    const now = new Date();
    const bufferTime = DEFAULT_AUTH_CONFIG.tokenExpirationBuffer * 60 * 1000;
    const isExpired = now.getTime() > (expiresAt.getTime() - bufferTime);

    return {
      token,
      expiresAt,
      isExpired
    };
  }

  /**
   * Check if token is valid and not expired
   */
  static isTokenValid(token: string | null): boolean {
    if (!token) return false;
    
    const tokenInfo = this.getTokenInfo(token);
    return tokenInfo ? !tokenInfo.isExpired : false;
  }

  /**
   * Extract user ID from token
   */
  static getUserIdFromToken(token: string): string | null {
    const payload = this.decodeTokenPayload(token);
    return payload?.id || null;
  }

  /**
   * Get token from storage
   */
  static getStoredToken(): string | null {
    try {
      return localStorage.getItem(this.STORAGE_KEY);
    } catch (error) {
      console.error('Error getting token from storage:', error);
      return null;
    }
  }

  /**
   * Store token in local storage
   */
  static setStoredToken(token: string): void {
    try {
      localStorage.setItem(this.STORAGE_KEY, token);
    } catch (error) {
      console.error('Error storing token:', error);
    }
  }

  /**
   * Remove token from storage
   */
  static removeStoredToken(): void {
    try {
      localStorage.removeItem(this.STORAGE_KEY);
    } catch (error) {
      console.error('Error removing token:', error);
    }
  }

  /**
   * Get stored user data
   */
  static getStoredUser(): User | null {
    try {
      const userData = localStorage.getItem(this.USER_STORAGE_KEY);
      return userData ? JSON.parse(userData) : null;
    } catch (error) {
      console.error('Error getting user from storage:', error);
      return null;
    }
  }

  /**
   * Store user data
   */
  static setStoredUser(user: User): void {
    try {
      localStorage.setItem(this.USER_STORAGE_KEY, JSON.stringify(user));
    } catch (error) {
      console.error('Error storing user:', error);
    }
  }

  /**
   * Remove user data from storage
   */
  static removeStoredUser(): void {
    try {
      localStorage.removeItem(this.USER_STORAGE_KEY);
    } catch (error) {
      console.error('Error removing user:', error);
    }
  }

  /**
   * Clear all auth data from storage
   */
  static clearAuthStorage(): void {
    this.removeStoredToken();
    this.removeStoredUser();
  }
}

// Auth storage implementation
export class AuthStorageService implements AuthStorage {
  getToken(): string | null {
    return TokenUtils.getStoredToken();
  }

  setToken(token: string): void {
    TokenUtils.setStoredToken(token);
  }

  removeToken(): void {
    TokenUtils.removeStoredToken();
  }

  getUser(): User | null {
    return TokenUtils.getStoredUser();
  }

  setUser(user: User): void {
    TokenUtils.setStoredUser(user);
  }

  removeUser(): void {
    TokenUtils.removeStoredUser();
  }

  clear(): void {
    TokenUtils.clearAuthStorage();
  }
}

// Form validation utilities
export class ValidationUtils {
  /**
   * Validate email format
   */
  static isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Validate password strength
   */
  static validatePassword(password: string): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];
    
    if (password.length < 6) {
      errors.push('Password must be at least 6 characters long');
    }

    // Add more password requirements if needed
    // if (!/(?=.*[a-z])/.test(password)) {
    //   errors.push('Password must contain at least one lowercase letter');
    // }
    
    // if (!/(?=.*[A-Z])/.test(password)) {
    //   errors.push('Password must contain at least one uppercase letter');
    // }
    
    // if (!/(?=.*\d)/.test(password)) {
    //   errors.push('Password must contain at least one number');
    // }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Validate username format
   */
  static validateUsername(username: string): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];
    
    if (username.length < 3 || username.length > 20) {
      errors.push('Username must be between 3 and 20 characters');
    }

    const usernameRegex = /^[a-zA-Z0-9_-]+$/;
    if (!usernameRegex.test(username)) {
      errors.push('Username can only contain letters, numbers, underscores, and hyphens');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Validate passwords match
   */
  static validatePasswordsMatch(password: string, confirmPassword: string): boolean {
    return password === confirmPassword;
  }
}

// Error handling utilities
export class AuthErrorUtils {
  /**
   * Create standardized auth error
   */
  static createAuthError(
    type: AuthErrorType,
    message: string,
    statusCode?: number,
    details?: any
  ): AuthError {
    const error = new Error(message) as AuthError;
    error.name = 'AuthError';
    error.type = type;
    error.statusCode = statusCode;
    error.details = details;
    return error;
  }

  /**
   * Parse API error response
   */
  static parseApiError(error: any): AuthError {
    // Network error
    if (!error.response) {
      return this.createAuthError(
        'NETWORK_ERROR',
        'Network error. Please check your connection.',
        0,
        error
      );
    }

    const { status, data } = error.response;
    const message = data?.error || data?.message || 'An error occurred';

    // Map status codes to error types
    let errorType: AuthErrorType;
    switch (status) {
      case 400:
        errorType = 'VALIDATION_ERROR';
        break;
      case 401:
        errorType = 'INVALID_CREDENTIALS';
        break;
      case 403:
        errorType = 'INVALID_TOKEN';
        break;
      case 409:
        errorType = 'USER_EXISTS';
        break;
      case 500:
      default:
        errorType = 'SERVER_ERROR';
        break;
    }

    return this.createAuthError(errorType, message, status, data);
  }

  /**
   * Get user-friendly error message
   */
  static getUserFriendlyMessage(error: AuthError): string {
    switch (error.type) {
      case 'INVALID_CREDENTIALS':
        return 'Invalid email or password. Please try again.';
      case 'USER_EXISTS':
        return 'An account with this email already exists.';
      case 'INVALID_TOKEN':
      case 'EXPIRED_TOKEN':
        return 'Your session has expired. Please log in again.';
      case 'NETWORK_ERROR':
        return 'Network error. Please check your connection and try again.';
      case 'VALIDATION_ERROR':
        return error.message || 'Please check your input and try again.';
      case 'SERVER_ERROR':
        return 'Server error. Please try again later.';
      default:
        return error.message || 'An unexpected error occurred.';
    }
  }
}

// HTTP utilities for API requests
export class ApiUtils {
  /**
   * Create auth headers for API requests
   */
  static createAuthHeaders(token?: string): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    const authToken = token || TokenUtils.getStoredToken();
    if (authToken) {
      headers.Authorization = `Bearer ${authToken}`;
    }

    return headers;
  }

  /**
   * Handle API response
   */
  static async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw AuthErrorUtils.createAuthError(
        'SERVER_ERROR',
        errorData?.error || `HTTP ${response.status}`,
        response.status,
        errorData
      );
    }

    return response.json();
  }

  /**
   * Create fetch request with auth headers
   */
  static async fetchWithAuth(
    url: string,
    options: RequestInit = {},
    token?: string
  ): Promise<Response> {
    const headers = {
      ...ApiUtils.createAuthHeaders(token),
      ...options.headers,
    };

    return fetch(url, {
      ...options,
      headers,
    });
  }
}

// Session management utilities
export class SessionUtils {
  private static readonly SESSION_KEY = 'chess_app_session';

  /**
   * Check if user session is active
   */
  static isSessionActive(): boolean {
    const token = TokenUtils.getStoredToken();
    return TokenUtils.isTokenValid(token);
  }

  /**
   * Initialize session from storage
   */
  static initializeSession(): { user: User | null; token: string | null; isAuthenticated: boolean } {
    const token = TokenUtils.getStoredToken();
    const user = TokenUtils.getStoredUser();
    const isAuthenticated = token && user && TokenUtils.isTokenValid(token) ? true : false;

    return {
      user: isAuthenticated ? user : null,
      token: isAuthenticated ? token : null,
      isAuthenticated
    };
  }

  /**
   * Clear session data
   */
  static clearSession(): void {
    TokenUtils.clearAuthStorage();
    try {
      sessionStorage.removeItem(this.SESSION_KEY);
    } catch (error) {
      console.error('Error clearing session:', error);
    }
  }

  /**
   * Set session data
   */
  static setSession(user: User, token: string): void {
    TokenUtils.setStoredUser(user);
    TokenUtils.setStoredToken(token);
  }
}

// Create singleton instances
export const authStorage = new AuthStorageService();
export const tokenUtils = TokenUtils;
export const validationUtils = ValidationUtils;
export const authErrorUtils = AuthErrorUtils;
export const apiUtils = ApiUtils;
export const sessionUtils = SessionUtils;