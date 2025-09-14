import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { MinimalSplashPage } from '../../pages/splash/MinimalSplashPage'

<<<<<<< Updated upstream
export const MinimalSplashPageWrapper: React.FC = () => {
=======
const MinimalSplashPageWrapper: React.FC = () => {
>>>>>>> Stashed changes
  usePageInstructions('minimalsplash')
  usePageActions('minimalsplash')
  
  return <MinimalSplashPage />
<<<<<<< Updated upstream
}
=======
}

export default MinimalSplashPageWrapper;

export { MinimalSplashPageWrapper };
>>>>>>> Stashed changes
