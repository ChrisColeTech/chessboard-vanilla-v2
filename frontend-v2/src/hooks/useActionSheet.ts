import { useState } from "react";

export const useActionSheet = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSheet = () => setIsOpen(!isOpen);
  const closeSheet = () => setIsOpen(false);
  const openSheet = () => setIsOpen(true);

  return {
    isOpen,
    toggleSheet,
    closeSheet,
    openSheet,
  };
};
