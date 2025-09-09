import React from 'react'
import { X } from 'lucide-react'
import { useAppStore } from '../../stores/appStore'
import { MinimalSplashPage } from '../../pages/splash/MinimalSplashPage'
import { AnimatedSplashPage } from '../../pages/splash/AnimatedSplashPage'
import { LoadingProgressPage } from '../../pages/splash/LoadingProgressPage'
import { BrandedSplashPage } from '../../pages/splash/BrandedSplashPage'

export const SplashModal: React.FC = () => {
  const splashModalOpen = useAppStore((state) => state.splashModalOpen)
  const splashModalPage = useAppStore((state) => state.splashModalPage)
  const closeSplashModal = useAppStore((state) => state.closeSplashModal)

  if (!splashModalOpen || !splashModalPage) {
    return null
  }

  // Render the appropriate splash page with modal variant
  let splashContent: React.ReactNode
  switch (splashModalPage) {
    case 'minimalsplash':
      splashContent = <MinimalSplashPage variant="modal" />
      break
    case 'animatedsplash':
      splashContent = <AnimatedSplashPage variant="modal" />
      break
    case 'loadingprogress':
      splashContent = <LoadingProgressPage variant="modal" />
      break
    case 'brandedsplash':
      splashContent = <BrandedSplashPage variant="modal" />
      break
    default:
      return null
  }

  return (
    <div className="fixed inset-0 z-[99999]">
      {/* Dark backdrop with blur */}
      <div 
        className="absolute inset-0 bg-black backdrop-blur-sm"
        onClick={closeSplashModal}
        aria-label="Close modal backdrop"
      />
      
      {/* Modal content container - full screen, no transparency */}
      <div className="relative w-full h-full">
        {/* Close button */}
        <button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            closeSplashModal();
          }}
          className="absolute top-6 right-6 z-[100] p-3 rounded-full bg-black/80 hover:bg-black/90 text-white transition-all duration-200 backdrop-blur-sm border border-white/40 cursor-pointer shadow-lg"
          aria-label="Close splash modal"
        >
          <X className="w-6 h-6" />
        </button>
        
        {/* Full-screen splash content */}
        {splashContent}
      </div>
    </div>
  )
}