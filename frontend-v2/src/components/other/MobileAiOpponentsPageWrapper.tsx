import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileAiOpponentsPage } from "../../pages/other/MobileAiOpponentsPage";

export const MobileAiOpponentsPageWrapper = () => {
  usePageInstructions("ai-opponents");
  
  return <MobileAiOpponentsPage />;
};
