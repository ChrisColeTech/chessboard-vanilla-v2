import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { LoadingProgressPage } from '../../pages/splash/LoadingProgressPage'

<<<<<<< Updated upstream
export const LoadingProgressPageWrapper: React.FC = () => {
=======
const LoadingProgressPageWrapper: React.FC = () => {
>>>>>>> Stashed changes
  usePageInstructions('loadingprogress')
  usePageActions('loadingprogress')
  
  return <LoadingProgressPage />
<<<<<<< Updated upstream
}
=======
}

export default LoadingProgressPageWrapper;

export { LoadingProgressPageWrapper };
>>>>>>> Stashed changes
