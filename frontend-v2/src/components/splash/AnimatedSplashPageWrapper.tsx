import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { AnimatedSplashPage } from '../../pages/splash/AnimatedSplashPage'

<<<<<<< Updated upstream
export const AnimatedSplashPageWrapper: React.FC = () => {
=======
const AnimatedSplashPageWrapper: React.FC = () => {
>>>>>>> Stashed changes
  usePageInstructions('animatedsplash')
  usePageActions('animatedsplash')
  
  return <AnimatedSplashPage />
<<<<<<< Updated upstream
}
=======
}

export default AnimatedSplashPageWrapper;

export { AnimatedSplashPageWrapper };
>>>>>>> Stashed changes
