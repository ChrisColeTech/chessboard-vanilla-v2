import React from "react";
import { AuthBackgroundEffects } from "./AuthBackgroundEffects";

/**
 * AUTH LAYOUT DESIGN SYSTEM
 * =========================
 * 
 * Following the app's established glassmorphism pattern:
 * - Uses `card-gaming` for content cards (rounded corners, entry animations)
 * - Specialized AuthBackgroundEffects for chess-themed authentication
 * - Consistent with AppLayout architecture but optimized for auth flows
 */

interface AuthLayoutProps {
  children: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="relative min-h-screen min-h-[100dvh] bg-background text-foreground">
      {/* Auth-specific background effects */}
      <AuthBackgroundEffects />

      {/* Content Container - Form resizes to fit viewport */}
      <div className="h-screen flex flex-col py-4 sm:py-6 md:py-8 lg:py-12 px-4 sm:px-6 md:px-8 lg:px-12 xl:px-16 relative z-10">
        {/* Form content - resizes to fit */}
        <div className="flex-1 flex items-stretch justify-center">
          <div className="w-full max-w-md sm:max-w-lg md:max-w-xl lg:max-w-2xl flex flex-col">
            {/* Using custom auth card with lighter transparency and blur */}
            <div className="auth-card p-4 sm:p-6 md:p-8 lg:p-10 flex-1 flex flex-col justify-center items-center">
              <div className="w-full max-w-sm sm:max-w-md md:max-w-lg text-center">
                {children}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};