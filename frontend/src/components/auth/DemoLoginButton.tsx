import React from "react";
import { useDemoLogin } from "../../hooks";
import { Button } from "../ui";

export interface DemoLoginButtonProps {
  className?: string;
  size?: "default" | "sm" | "lg";
  variant?: "default" | "secondary" | "outline" | "ghost" | "link";
}

/**
 * Demo Login Button Component
 * Provides one-click login with demo user credentials
 */
export const DemoLoginButton: React.FC<DemoLoginButtonProps> = ({ 
  className, 
  size = "sm",
  variant = "outline"
}) => {
  const { loginWithDemo, isLoading, error } = useDemoLogin();

  const handleDemoLogin = async () => {
    try {
      await loginWithDemo();
    } catch (error) {
      // Error is handled by the hook
    }
  };

  return (
    <>
      <Button
        onClick={handleDemoLogin}
        disabled={isLoading}
        variant={variant}
        size={size}
        className={className}
      >
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 border-2 border-current/30 border-t-current rounded-full animate-spin" />
            <span className="text-sm">Logging in...</span>
          </div>
        ) : (
          <span className="text-sm">🎯 Demo Login</span>
        )}
      </Button>
      {error && (
        <p className="text-xs text-destructive mt-2">Demo login failed: {error}</p>
      )}
    </>
  );
};