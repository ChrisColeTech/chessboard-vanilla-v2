// Authentication types for user management and auth flow

// Core user types
export interface User {
  id: string;
  username: string;
  email: string;
  chess_elo?: number;
  puzzle_rating?: number;
  preferences?: string;
  created_at: string;
  updated_at: string;
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

// Auth request/response types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
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

export interface VerifyTokenRequest {
  token: string;
}

// API response types
export interface AuthResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface LoginResponse {
  user: User;
  token: string;
}

export interface MeResponse {
  user: User;
  progress: UserProgress;
}

export interface TokenVerificationResponse {
  user: User;
  tokenValid: boolean;
}

// Auth state types
export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
  progress: UserProgress | null;
}

export interface AuthActions {
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => void;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (data: ResetPasswordRequest) => Promise<void>;
  changePassword: (data: ChangePasswordRequest) => Promise<void>;
  updateProfile: (data: UpdateProfileRequest) => Promise<void>;
  verifyToken: (token: string) => Promise<boolean>;
  refreshUser: () => Promise<void>;
  clearError: () => void;
}

// Hook return types
export interface UseAuthReturn extends AuthState, AuthActions {}

export interface UseLoginReturn {
  login: (credentials: LoginRequest) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  clearError: () => void;
}

export interface UseRegisterReturn {
  register: (userData: RegisterRequest) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  clearError: () => void;
}

export interface UseForgotPasswordReturn {
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (data: ResetPasswordRequest) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  success: boolean;
  clearError: () => void;
  clearSuccess: () => void;
}

// Form validation types
export interface FormValidationError {
  field: string;
  message: string;
}

export interface AuthFormState {
  isSubmitting: boolean;
  errors: FormValidationError[];
  touched: Record<string, boolean>;
}

// Auth utility types
export interface TokenInfo {
  token: string;
  expiresAt: Date;
  isExpired: boolean;
}

export interface AuthConfig {
  apiBaseUrl: string;
  tokenStorageKey: string;
  tokenExpirationBuffer: number; // minutes before expiry to consider token expired
}

// Protected route types
export interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
  requireAuth?: boolean;
  fallback?: React.ComponentType;
}

export interface AuthGuardProps extends ProtectedRouteProps {
  allowedRoles?: string[];
  checkPermission?: (user: User) => boolean;
}

// Auth context types
export interface AuthContextValue extends UseAuthReturn {
  config: AuthConfig;
}

// Error types
export type AuthErrorType = 
  | 'INVALID_CREDENTIALS'
  | 'USER_EXISTS' 
  | 'INVALID_TOKEN'
  | 'EXPIRED_TOKEN'
  | 'NETWORK_ERROR'
  | 'VALIDATION_ERROR'
  | 'SERVER_ERROR'
  | 'UNKNOWN_ERROR';

export interface AuthError extends Error {
  type: AuthErrorType;
  code?: string;
  statusCode?: number;
  details?: any;
}

// Storage types
export interface AuthStorage {
  getToken: () => string | null;
  setToken: (token: string) => void;
  removeToken: () => void;
  getUser: () => User | null;
  setUser: (user: User) => void;
  removeUser: () => void;
  clear: () => void;
}

// API client types
export interface AuthApiClient {
  login: (credentials: LoginRequest) => Promise<AuthResponse<LoginResponse>>;
  register: (userData: RegisterRequest) => Promise<AuthResponse<User>>;
  forgotPassword: (email: string) => Promise<AuthResponse<void>>;
  resetPassword: (data: ResetPasswordRequest) => Promise<AuthResponse<void>>;
  changePassword: (data: ChangePasswordRequest) => Promise<AuthResponse<void>>;
  updateProfile: (data: UpdateProfileRequest) => Promise<AuthResponse<User>>;
  getCurrentUser: () => Promise<AuthResponse<MeResponse>>;
  verifyToken: (token: string) => Promise<AuthResponse<TokenVerificationResponse>>;
  logout: () => Promise<AuthResponse<void>>;
}