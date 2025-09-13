import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { AnimatedSplashPage } from '../../pages/splash/AnimatedSplashPage'

export const AnimatedSplashPageWrapper: React.FC = () => {
  usePageInstructions('animatedsplash')
  usePageActions('animatedsplash')
  
  return <AnimatedSplashPage />
}