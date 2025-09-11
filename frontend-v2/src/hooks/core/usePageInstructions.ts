import { useEffect } from "react";
import { useInstructions } from "../useInstructions";

export const usePageInstructions = (pageId: string) => {
  const { setInstructions } = useInstructions();

  useEffect(() => {
    // Set basic instructions for the page
    setInstructions(`${pageId.charAt(0).toUpperCase() + pageId.slice(1)} Page`, [
      `Welcome to the ${pageId} page`,
      "Use the action menu to navigate",
      "This page follows the domain-driven architecture"
    ]);
  }, [pageId, setInstructions]);
};
