import React, { useState, useEffect } from "react";
import { MinimalSplashPage } from "../../pages/splash/MinimalSplashPage";

// Higher-Order Component that adds splash screen functionality
export default function withSplashScreen<P extends object>(
  WrappedComponent: React.ComponentType<P>
) {
  return function WithSplashScreenComponent(props: P) {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      // Simulate app initialization time
      // You can replace this with actual initialization logic like:
      // - Preloading sounds
      // - Loading user preferences
      // - Initializing game engine
      // - API calls, etc.
      
      const initializeApp = async () => {
        try {
          // Simulate initialization tasks
          await new Promise(resolve => setTimeout(resolve, 1500)); // Allow time for initialization
          
          // You could add real initialization here:
          // await preloadSounds();
          // await loadUserPreferences();
          // await initializeStockfish();
          
          // Remove splash immediately without fade animation
          setLoading(false);
        } catch (error) {
          console.error("App initialization error:", error);
          // Even if there's an error, don't stay stuck on splash screen
          setLoading(false);
        }
      };

      initializeApp();
    }, []);

    // Show splash screen while loading using your existing MinimalSplashPage
    if (loading) {
      return (
        <div className="fixed inset-0 z-50">
          <MinimalSplashPage variant="modal" />
        </div>
      );
    }

    // Once loaded, render the actual app
    return <WrappedComponent {...props} />;
  };
}