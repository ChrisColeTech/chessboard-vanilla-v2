import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";

export const HoldemPage: React.FC = () => {
  usePageInstructions("holdem");
  return (
    <div className="relative min-h-full pb-12 pt-28">
      {/* Enhanced gaming background effects */}
      <div className="bg-overlay">
        {/* Floating Gaming Elements */}
        <div className="bg-orb bg-orb-lg bg-orb-primary top-20 left-20 animation-delay-500"></div>
        <div className="bg-orb bg-orb-md bg-orb-accent bottom-32 right-16 animation-delay-1000"></div>
        <div className="bg-orb bg-orb-sm bg-orb-primary-light top-1/3 left-1/4 animation-delay-1500"></div>

        {/* Sparkle Effects */}
        <div className="bg-sparkle bg-sparkle-lg bg-orb-primary-60 top-1/4 right-1/4 animation-delay-300"></div>
        <div className="bg-sparkle bg-sparkle-sm bg-orb-accent-40 bottom-1/3 left-1/3 animation-delay-700"></div>
        <div className="bg-sparkle bg-sparkle-md bg-orb-foreground-50 top-2/3 right-1/3 animation-delay-1200"></div>
      </div>

      <section className="relative z-10">
        <div className="card-gaming p-8 mx-4">
          <h2 className="text-2xl font-bold text-center mb-4">♔ Texas Hold'em Poker ♔</h2>
          <p className="text-muted-foreground text-center mb-6">
            Chess-themed Texas Hold'em poker coming soon! Play against AI opponents 
            with different difficulty levels and strategies. Features include blinds, 
            betting rounds, and complete poker hand rankings.
          </p>
          <div className="text-center">
            <div className="text-6xl mb-4">🎰</div>
            <p className="text-sm text-muted-foreground">
              Use the action menu to navigate between casino games
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};