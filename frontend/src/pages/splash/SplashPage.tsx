import React from "react";
import { useAppStore } from "../../stores/appStore";
import { MinimalSplashPageWrapper } from "../../components/splash/MinimalSplashPageWrapper";
import { AnimatedSplashPageWrapper } from "../../components/splash/AnimatedSplashPageWrapper";
import { LoadingProgressPageWrapper } from "../../components/splash/LoadingProgressPageWrapper";
import { BrandedSplashPageWrapper } from "../../components/splash/BrandedSplashPageWrapper";
import { FunctionalSplashPageWrapper } from "../../components/splash/FunctionalSplashPageWrapper";

export const SplashPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  let CurrentPageComponent = SplashMainPage;

  if (currentChildPage === "minimalsplash") {
    CurrentPageComponent = MinimalSplashPageWrapper;
  } else if (currentChildPage === "animatedsplash") {
    CurrentPageComponent = AnimatedSplashPageWrapper;
  } else if (currentChildPage === "loadingprogress") {
    CurrentPageComponent = LoadingProgressPageWrapper;
  } else if (currentChildPage === "brandedsplash") {
    CurrentPageComponent = BrandedSplashPageWrapper;
  } else if (currentChildPage === "functionalsplash") {
    CurrentPageComponent = FunctionalSplashPageWrapper;
  }

  return <CurrentPageComponent />;
};

const SplashMainPage: React.FC = () => {
  return (
    <div className="splash-container splash-in-app splash-fade-in relative">
      {/* Enhanced Chess Background */}
      <div className="bg-overlay">
        <div className="hidden md:block bg-chess-piece text-4xl lg:text-5xl xl:text-6xl chess-piece-color-primary-30 absolute top-16 left-12 animate-pulse">♛</div>
        <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-accent-25 absolute top-32 right-20 animation-delay-400">♞</div>
        <div className="hidden md:block bg-chess-piece text-4xl lg:text-5xl xl:text-6xl chess-piece-color-primary-20 absolute bottom-40 left-16 animation-delay-800">♜</div>
        <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-foreground-15 absolute bottom-16 right-24 animation-delay-1200">♝</div>
        <div className="hidden lg:block bg-chess-piece text-2xl chess-piece-color-muted absolute top-1/4 left-4 animation-delay-600">♟</div>
        <div className="hidden lg:block bg-chess-piece text-2xl chess-piece-color-muted absolute top-3/4 right-6 animation-delay-1000">♟</div>
        <div className="hidden xl:block bg-chess-piece text-3xl chess-piece-color-accent-20 absolute top-1/2 left-2 animation-delay-200">♙</div>
        <div className="hidden xl:block bg-chess-piece text-3xl chess-piece-color-primary-15 absolute bottom-1/3 right-4 animation-delay-1400">♘</div>
      </div>
      
      <div className="splash-brand-section relative z-10">
        <div className="splash-logo-area text-center">
          {/* Enhanced Chess Crown */}
          <div className="text-8xl sm:text-9xl lg:text-[10rem] xl:text-[12rem] mb-6 animate-pulse">♔</div>
          
          <h1 className="splash-title text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold tracking-tight mb-4">Master Chess Training</h1>
          
          <p className="splash-subtitle text-xl sm:text-2xl lg:text-3xl xl:text-4xl font-medium mb-6">
            Splash Screen Examples Hub
          </p>
          
          {/* Chess piece row */}
          <div className="flex justify-center space-x-3 mb-6 text-2xl sm:text-3xl lg:text-4xl xl:text-5xl opacity-70">
            <span className="animate-bounce">♚</span>
            <span className="animate-bounce animation-delay-200">♛</span>
            <span className="animate-bounce animation-delay-400">♜</span>
            <span className="animate-bounce animation-delay-600">♝</span>
            <span className="animate-bounce animation-delay-800">♞</span>
            <span className="animate-bounce animation-delay-1000">♟</span>
          </div>
          
          <div className="splash-description text-base sm:text-lg lg:text-xl xl:text-2xl font-medium">
            Use the action sheet to navigate to different splash screen examples
          </div>
        </div>
      </div>
    </div>
  );
};
