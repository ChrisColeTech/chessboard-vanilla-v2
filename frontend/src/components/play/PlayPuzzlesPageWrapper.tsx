import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { PlayPuzzlesPage } from '../../pages/chess/PlayPuzzlesPage'

export const PlayPuzzlesPageWrapper: React.FC = () => {
  usePageInstructions('playpuzzles')
  usePageActions('playpuzzles')
  
  return <PlayPuzzlesPage />
}