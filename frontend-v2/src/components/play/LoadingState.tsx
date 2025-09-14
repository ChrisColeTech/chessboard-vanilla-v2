<<<<<<< Updated upstream
// LoadingState.tsx - Loading state display following SRP
// Single Responsibility: Display loading state during chess engine initialization

import React from 'react';

interface LoadingStateProps {
  /** Loading message to display */
  message?: string;
  /** Optional additional details */
  details?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Initializing chess engine...',
  details
}) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] px-4">
      <div className="text-center max-w-sm">
        {/* Mobile-responsive spinner */}
        <div className="animate-spin rounded-full h-8 w-8 sm:h-12 sm:w-12 border-b-2 border-primary mx-auto mb-4"></div>
        
        {/* Loading message */}
        <p className="text-sm sm:text-base text-foreground mb-2 font-medium">
          {message}
        </p>
        
        {/* Additional details if provided */}
        {details && (
          <p className="text-xs sm:text-sm text-muted-foreground">
            {details}
          </p>
        )}
        
        {/* Progress indicator dots */}
        <div className="flex justify-center gap-1 mt-4">
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
};
=======
// LoadingState.tsx - Loading state display following SRP
// Single Responsibility: Display loading state during chess engine initialization

import React from 'react';

interface LoadingStateProps {
  /** Loading message to display */
  message?: string;
  /** Optional additional details */
  details?: string;
}

const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Initializing chess engine...',
  details
}) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] px-4">
      <div className="text-center max-w-sm">
        {/* Mobile-responsive spinner */}
        <div className="animate-spin rounded-full h-8 w-8 sm:h-12 sm:w-12 border-b-2 border-primary mx-auto mb-4"></div>
        
        {/* Loading message */}
        <p className="text-sm sm:text-base text-foreground mb-2 font-medium">
          {message}
        </p>
        
        {/* Additional details if provided */}
        {details && (
          <p className="text-xs sm:text-sm text-muted-foreground">
            {details}
          </p>
        )}
        
        {/* Progress indicator dots */}
        <div className="flex justify-center gap-1 mt-4">
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingState;
export { LoadingState };
>>>>>>> Stashed changes
