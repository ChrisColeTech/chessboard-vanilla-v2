import React from "react";
import { SlotMachine } from "../../components/casino/SlotMachine";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useAppStore } from "../../stores/appStore";

export const SlotMachineTestPage: React.FC = () => {
  const coinBalance = useAppStore((state) => state.coinBalance);
  const setCoinBalance = useAppStore((state) => state.setCoinBalance);
  usePageInstructions("slots");

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

      <section className="relative z-10">
        {/* Slot Machine Container */}
        <div className="flex justify-center">
          <SlotMachine
            coinBalance={coinBalance}
            setCoinBalance={setCoinBalance}
          />
        </div>
      </section>
    </div>
  );
};
