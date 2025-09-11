import React, { useState, useCallback } from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useBlackjack } from "../../hooks/casino/useBlackjack";
import { Hand } from "../../components/casino/blackjack/Hand";
import { ActionButtons } from "../../components/casino/blackjack/ActionButtons";
import { BetControls } from "../../components/casino/blackjack/BetControls";
import { BlackjackLogic } from "../../services/casino/BlackjackLogic";
import { BLACKJACK_RULES } from "../../constants/casino/blackjack.constants";

const blackjackLogic = new BlackjackLogic();

export const BlackjackPage: React.FC = () => {
  usePageInstructions("blackjack");
  
  const {
    gameState,
    startNewGame,
    hit,
    stand,
    doubleDown,
    resetGame,
    canStartNewGame,
    balance
  } = useBlackjack();

  const [betAmount, setBetAmount] = useState<number>(BLACKJACK_RULES.MIN_BET);

  const handleStartGame = useCallback(async () => {
    const success = await startNewGame(betAmount);
    if (!success) {
      // Could add toast notification here
      console.warn('Insufficient balance for bet');
    }
  }, [startNewGame, betAmount]);

  const getResultMessage = () => {
    if (!gameState.gameResult) return null;
    
    const message = blackjackLogic.getGameResultMessage(gameState.gameResult);
    const payout = blackjackLogic.calculatePayout(gameState.gameResult, gameState.currentBet);
    
    return { message, payout };
  };

  const resultInfo = getResultMessage();

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

      <section className="relative z-10 max-w-4xl mx-auto px-4">
        <div className="card-gaming p-6">
          <h2 className="text-2xl font-bold text-center mb-6">♠️ Blackjack ♠️</h2>
          
          {/* Dealer Section */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-center mb-4">Dealer</h3>
            <Hand 
              hand={gameState.dealerHand}
              isDealer={true}
              showValue={gameState.gamePhase !== 'player-turn' && gameState.gamePhase !== 'dealing'}
              isThinking={gameState.isThinking}
            />
          </div>

          {/* Game Status Area */}
          <div className="mb-8 min-h-32 flex items-center justify-center">
            {gameState.gamePhase === 'betting' && (
              <div className="text-center space-y-6">
                <h4 className="text-xl font-semibold">Place Your Bet</h4>
                <BetControls
                  currentBet={betAmount}
                  balance={balance}
                  minBet={BLACKJACK_RULES.MIN_BET}
                  maxBet={BLACKJACK_RULES.MAX_BET}
                  onBetChange={setBetAmount}
                  disabled={!canStartNewGame}
                />
                <button 
                  className="
                    px-8 py-3 rounded-xl font-bold text-lg
                    bg-green-600 hover:bg-green-700 text-white
                    transform transition-all duration-200 hover:scale-105
                    disabled:opacity-50 disabled:cursor-not-allowed
                    active:scale-95
                  "
                  onClick={handleStartGame}
                  disabled={!canStartNewGame || betAmount > balance || balance < BLACKJACK_RULES.MIN_BET}
                >
                  🎯 DEAL CARDS
                </button>
              </div>
            )}
            
            {gameState.gamePhase === 'dealing' && (
              <div className="text-center">
                <div className="text-lg font-semibold animate-pulse">
                  Dealing cards...
                </div>
              </div>
            )}
            
            {gameState.gamePhase === 'dealer-turn' && (
              <div className="text-center">
                <div className="text-lg font-semibold">
                  Dealer's turn...
                </div>
              </div>
            )}
            
            {gameState.gameResult && resultInfo && (
              <div className="text-center space-y-4">
                <h4 className="text-2xl font-bold">{resultInfo.message}</h4>
                <div className="space-y-2">
                  <p className="text-lg">
                    Bet: <span className="font-semibold">{gameState.currentBet} coins</span>
                  </p>
                  {resultInfo.payout > 0 ? (
                    <p className="text-lg text-green-500">
                      You won: <span className="font-bold">{resultInfo.payout} coins</span>
                    </p>
                  ) : (
                    <p className="text-lg text-red-500">
                      You lost your bet
                    </p>
                  )}
                </div>
                <button 
                  className="
                    px-6 py-2 rounded-lg font-semibold
                    bg-blue-600 hover:bg-blue-700 text-white
                    transform transition-all duration-200 hover:scale-105
                    active:scale-95
                  "
                  onClick={resetGame}
                >
                  🎮 NEW GAME
                </button>
              </div>
            )}
          </div>

          {/* Player Section */}
          <div>
            <h3 className="text-lg font-semibold text-center mb-4">Your Hand</h3>
            <Hand 
              hand={gameState.playerHand}
              showValue={true}
            />
            
            {gameState.gamePhase === 'player-turn' && (
              <ActionButtons
                canHit={gameState.canHit}
                canStand={gameState.canStand}
                canDouble={gameState.canDouble}
                onHit={hit}
                onStand={stand}
                onDouble={doubleDown}
                currentBet={gameState.currentBet}
                balance={balance}
              />
            )}
          </div>

          {/* Game Info */}
          <div className="mt-8 text-center text-sm text-muted-foreground">
            <p>Balance: <span className="font-semibold">{balance} coins</span></p>
            {gameState.currentBet > 0 && (
              <p>Current Bet: <span className="font-semibold">{gameState.currentBet} coins</span></p>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};