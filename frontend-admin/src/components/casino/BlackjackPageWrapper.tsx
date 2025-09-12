import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { BlackjackPage } from '../../pages/casino/BlackjackPage'

export const BlackjackPageWrapper: React.FC = () => {
  usePageInstructions('blackjack')
  usePageActions('blackjack')
  
  return <BlackjackPage />
}