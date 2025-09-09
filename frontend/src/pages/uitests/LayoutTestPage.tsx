import React, { useState, useEffect } from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";

export const LayoutTestPage: React.FC = () => {
  usePageInstructions("layout");
  const [showElements, setShowElements] = useState(true);

  // Expose toggle function globally so the action can call it
  useEffect(() => {
    (window as any).__toggleLayoutElements = () => {
      setShowElements(prev => !prev);
    };
    
    return () => {
      delete (window as any).__toggleLayoutElements;
    };
  }, []);

  return (
    <section className="space-y-4">
      {showElements && (
        <div className="card-gaming p-8">
          <p className="text-muted-foreground text-center">
            This is a minimal test page to view the background effects, floating
            chess pieces, and theme styling without any other content interfering.
            Use the action menu to toggle this card visibility.
          </p>
        </div>
      )}
    </section>
  );
};
