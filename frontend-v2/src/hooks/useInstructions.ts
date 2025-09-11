import { create } from "zustand";

interface InstructionsState {
  title: string;
  instructions: string[];
  setInstructions: (title: string, instructions: string[]) => void;
}

export const useInstructions = create<InstructionsState>((set) => ({
  title: "",
  instructions: [],
  setInstructions: (title, instructions) => set({ title, instructions }),
}));
