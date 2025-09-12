import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";

export const UITestsMainPage: React.FC = () => {
  usePageInstructions("uitests");

  return (
    <section className="space-y-4">
      <div className="card-gaming p-8">
        <div className="text-center space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            UI Tests
          </h1>
          <p className="text-muted-foreground">
            Welcome to the UI tests page. This page handles UI testing operations.
          </p>
        </div>
      </div>
    </section>
  );
};