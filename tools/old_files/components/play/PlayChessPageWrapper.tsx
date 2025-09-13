import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { PlayChessPage } from '../../pages/chess/PlayChessPage'

export const PlayChessPageWrapper: React.FC = () => {
  usePageInstructions('playchess')
  usePageActions('playchess')
  
  return <PlayChessPage />
}