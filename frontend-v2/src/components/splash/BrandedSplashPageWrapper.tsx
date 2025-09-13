import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { BrandedSplashPage } from '../../pages/splash/BrandedSplashPage'

export const BrandedSplashPageWrapper: React.FC = () => {
  usePageInstructions('brandedsplash')
  usePageActions('brandedsplash')
  
  return <BrandedSplashPage />
}