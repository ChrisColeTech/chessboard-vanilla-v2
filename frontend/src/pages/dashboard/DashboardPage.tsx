import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";

export const DashboardPage: React.FC = () => {
  usePageInstructions("dashboard");

  return (
    <div className="relative h-full flex items-center justify-center bg-background">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-foreground mb-4">Dashboard Page</h1>
        <p className="text-muted-foreground">Placeholder for dashboard functionality</p>
      </div>
    </div>
  );
};