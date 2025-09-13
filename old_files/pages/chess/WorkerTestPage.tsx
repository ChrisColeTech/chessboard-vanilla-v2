import React from "react";
import { CheckCircle, XCircle, Clock, Brain } from "lucide-react";
import { useStockfish } from "../../hooks/chess/useStockfish";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useWorkerTestStore } from "../../stores/workerTestStore";

export const WorkerTestPage: React.FC = () => {
  const { isReady, isThinking, skillLevel, setSkillLevel, error } =
    useStockfish();

  // Use Zustand store for reactive state updates
  const {
    testResults,
    lastMove,
    responseTime,
    evaluation,
    // Note: Action functions moved to useWorkerActions hook for action sheet system
  } = useWorkerTestStore();

  usePageInstructions("worker");

  // All test actions moved to useWorkerActions hook for action sheet integration

  const getSkillDescription = (level: number) => {
    if (level <= 2) return "Beginner (learning the rules)";
    if (level <= 4) return "Casual player (plays for fun)";
    if (level <= 6) return "Club player (plays regularly)";
    if (level <= 8) return "Strong club player (quite good)";
    return "Expert level (very strong)";
  };

  return (
    <div className="relative space-y-8">
      {/* Main Content - Consolidated */}
      <div className="card-gaming p-6 space-y-6">
        {/* Worker Status */}
        <div className="flex items-center gap-3">
          {isReady ? (
            <>
              <CheckCircle className="w-6 h-6 text-green-500" />
              <span className="text-lg text-foreground">
                ✅ Chess computer is ready!
              </span>
            </>
          ) : error ? (
            <>
              <XCircle className="w-6 h-6 text-red-500" />
              <span className="text-lg text-red-500">
                ❌ Something went wrong: {error}
              </span>
            </>
          ) : (
            <>
              <Clock className="w-6 h-6 text-yellow-500 animate-spin" />
              <span className="text-lg text-foreground">
                ⏳ Starting up the chess computer...
              </span>
            </>
          )}
          {isThinking && (
            <div className="flex items-center gap-2 text-foreground/70 ml-4">
              <Brain className="w-4 h-4 animate-pulse" />
              <span>Thinking...</span>
            </div>
          )}
        </div>

        {/* Skill Level Control */}
        <div>
          <div className="flex justify-between text-sm text-muted-foreground mb-2">
            <span>Skill Level: Beginner</span>
            <span>Expert</span>
          </div>
          <input
            type="range"
            min="1"
            max="10"
            value={skillLevel}
            onChange={(e) => setSkillLevel(parseInt(e.target.value))}
            className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer"
            disabled={!isReady}
          />
          <div className="mt-2 text-center">
            <span className="text-foreground font-medium">
              Level {skillLevel}:{" "}
            </span>
            <span className="text-muted-foreground">
              {getSkillDescription(skillLevel)}
            </span>
          </div>
        </div>

        {/* Results Display */}
        <div className="status-card">
          <h4 className="font-medium text-foreground mb-3">Test Results:</h4>
          {lastMove && (
            <div className="mb-2 text-foreground">
              → Computer suggests: Move{" "}
              <span className="font-mono bg-muted px-1 rounded">
                {lastMove}
              </span>
            </div>
          )}
          {responseTime > 0 && (
            <div className="mb-2 text-foreground">
              → Answered in{" "}
              <span className="font-mono bg-muted px-1 rounded">
                {responseTime}ms
              </span>
            </div>
          )}
          {evaluation !== null && evaluation !== undefined && (
            <div className="mb-2 text-foreground">
              → Position:{" "}
              <span className="font-mono bg-muted px-1 rounded">
                {typeof evaluation === "number"
                  ? evaluation === 0
                    ? "equal"
                    : evaluation > 0
                    ? `+${evaluation} (white advantage)`
                    : `${evaluation} (black advantage)`
                  : String(evaluation)}
              </span>
            </div>
          )}

          {/* Test Results Log - Scrollable */}
          <div className="max-h-64 overflow-y-auto border border-border rounded bg-card/50 p-3 font-mono text-sm">
            {testResults.length === 0 ? (
              <div className="text-muted-foreground italic">
                No test results yet. Use the action sheet menu to run tests.
              </div>
            ) : (
              testResults.map((result, i) => (
                <div
                  key={i}
                  className={`
                    ${
                      result.type === "success"
                        ? "text-green-400"
                        : result.type === "error"
                        ? "text-red-400"
                        : result.type === "warning"
                        ? "text-yellow-400"
                        : "text-foreground"
                    }
                    ${
                      i === testResults.length - 1
                        ? ""
                        : "border-b border-border/50 pb-1 mb-1"
                    }
                  `}
                >
                  {result.message}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
