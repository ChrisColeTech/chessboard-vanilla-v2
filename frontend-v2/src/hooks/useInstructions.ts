import { useState } from "react";

export const useInstructions = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [instructions, setInstructions] = useState<string[]>([]);

  const showInstructions = (instructionTitle: string, instructionList: string[]) => {
    setTitle(instructionTitle);
    setInstructions(instructionList);
    setIsOpen(true);
  };

  const openInstructions = () => setIsOpen(true);
  const closeInstructions = () => setIsOpen(false);

  return {
    isOpen,
    title,
    instructions,
    showInstructions,
    openInstructions,
    closeInstructions,
    setInstructions: (instructionTitle: string, instructionList: string[]) => {
      setTitle(instructionTitle);
      setInstructions(instructionList);
    },
    clearInstructions: () => {
      setTitle("");
      setInstructions([]);
    },
  };
};