<<<<<<< Updated upstream
import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { PlayPuzzlesPage } from '../../pages/chess/PlayPuzzlesPage'

export const PlayPuzzlesPageWrapper: React.FC = () => {
  usePageInstructions('playpuzzles')
  usePageActions('playpuzzles')
  
  return <PlayPuzzlesPage />
}
=======
import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { PlayPuzzlesPage } from '../../pages/chess/PlayPuzzlesPage'

const PlayPuzzlesPageWrapper: React.FC = () => {
  usePageInstructions('playpuzzles')
  usePageActions('playpuzzles')
  
  return <PlayPuzzlesPage />
}

export default PlayPuzzlesPageWrapper;

export { PlayPuzzlesPageWrapper };
>>>>>>> Stashed changes
