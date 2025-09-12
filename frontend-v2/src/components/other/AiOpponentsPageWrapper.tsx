import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AiOpponentsPage } from "../../pages/other/AiOpponentsPage";

export const AiOpponentsPageWrapper = () => {
  usePageInstructions("ai-opponents");
  
  return <AiOpponentsPage />;
};
