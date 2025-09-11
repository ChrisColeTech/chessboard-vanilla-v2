import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";

export const OtherMainPage: React.FC = () => {
  usePageInstructions("other");

  return (
    <section className="space-y-4">
      <div className="card-gaming p-8">
        <div className="text-center space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            Other
          </h1>
          <p className="text-muted-foreground">
            Welcome to the other hub. This page groups related functionality 
            and follows the domain-driven architecture.
          </p>
          <div className="mt-6 p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm mb-2">Page Domain: Other</h3>
            <p className="text-xs text-muted-foreground">
              Endpoints: ai-opponents
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
            <div className="p-4 bg-card border border-border rounded-lg">
              <h4 className="font-semibold text-sm">Related Features</h4>
              <div className="text-xs text-muted-foreground mt-1 space-y-1">
                <div>• Ai Opponents</div>
              </div>
            </div>
            <div className="p-4 bg-card border border-border rounded-lg">
              <h4 className="font-semibold text-sm">Actions</h4>
              <p className="text-xs text-muted-foreground mt-1">
                Use the action menu to navigate between specific features
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
