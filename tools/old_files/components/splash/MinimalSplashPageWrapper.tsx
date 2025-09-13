import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { MinimalSplashPage } from '../../pages/splash/MinimalSplashPage'

export const MinimalSplashPageWrapper: React.FC = () => {
  usePageInstructions('minimalsplash')
  usePageActions('minimalsplash')
  
  return <MinimalSplashPage />
}