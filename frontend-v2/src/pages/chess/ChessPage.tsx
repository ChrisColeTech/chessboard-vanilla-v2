import { useAppStore } from "../../stores/appStore";
import { ChessMainPage } from "./ChessMainPage";
import { PuzzlesPageWrapper } from "../../components/chess/PuzzlesPageWrapper";
import { GamesPageWrapper } from "../../components/chess/GamesPageWrapper";
import { OpeningsPageWrapper } from "../../components/chess/OpeningsPageWrapper";
import { AnalysisPageWrapper } from "../../components/chess/AnalysisPageWrapper";
import { EndgamesPageWrapper } from "../../components/chess/EndgamesPageWrapper";
import { HistoricGamesPageWrapper } from "../../components/chess/HistoricGamesPageWrapper";

export const ChessPage = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = ChessMainPage;

    if (currentChildPage === "puzzles") {
    CurrentPageComponent = PuzzlesPageWrapper;
  } else   if (currentChildPage === "games") {
    CurrentPageComponent = GamesPageWrapper;
  } else   if (currentChildPage === "openings") {
    CurrentPageComponent = OpeningsPageWrapper;
  } else   if (currentChildPage === "analysis") {
    CurrentPageComponent = AnalysisPageWrapper;
  } else   if (currentChildPage === "endgames") {
    CurrentPageComponent = EndgamesPageWrapper;
  } else   if (currentChildPage === "historic-games") {
    CurrentPageComponent = HistoricGamesPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};
