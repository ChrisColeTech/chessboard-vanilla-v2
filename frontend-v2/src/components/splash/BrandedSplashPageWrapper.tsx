import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { BrandedSplashPage } from '../../pages/splash/BrandedSplashPage'

<<<<<<< Updated upstream
export const BrandedSplashPageWrapper: React.FC = () => {
=======
const BrandedSplashPageWrapper: React.FC = () => {
>>>>>>> Stashed changes
  usePageInstructions('brandedsplash')
  usePageActions('brandedsplash')
  
  return <BrandedSplashPage />
<<<<<<< Updated upstream
}
=======
}

export default BrandedSplashPageWrapper;

export { BrandedSplashPageWrapper };
>>>>>>> Stashed changes
