import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { MinimalSplashPage } from '../../pages/splash/MinimalSplashPage'

const MinimalSplashPageWrapper: React.FC = () => {
  usePageInstructions('minimalsplash')
  usePageActions('minimalsplash')
  
  return <MinimalSplashPage />
}

export default MinimalSplashPageWrapper;

export { MinimalSplashPageWrapper };
