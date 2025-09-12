import React from 'react';

export const CasinoMainPage: React.FC = () => {
  return (
    <div className="relative h-full flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center space-y-6">
        <h1 className="text-4xl font-bold text-foreground">🎰 Chess Casino Hub</h1>
        <p className="text-lg text-muted-foreground">
          Welcome to the chess-themed casino! Choose from our exciting selection of games using the action menu.
        </p>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-8">
          <div className="p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm">♠️ Slots</h3>
            <p className="text-xs text-muted-foreground">Chess piece slots</p>
          </div>
          <div className="p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm">🃏 Blackjack</h3>
            <p className="text-xs text-muted-foreground">Coming soon</p>
          </div>
          <div className="p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm">♥️ Hold'em</h3>
            <p className="text-xs text-muted-foreground">Coming soon</p>
          </div>
          <div className="p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm">🎯 Roulette</h3>
            <p className="text-xs text-muted-foreground">Coming soon</p>
          </div>
          <div className="p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm">🎲 Craps</h3>
            <p className="text-xs text-muted-foreground">Coming soon</p>
          </div>
        </div>
        <p className="text-sm text-muted-foreground mt-6">
          Use the action menu to navigate between games
        </p>
      </div>
    </div>
  );
};