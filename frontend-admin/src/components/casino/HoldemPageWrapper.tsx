import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { HoldemPage } from '../../pages/casino/HoldemPage'

export const HoldemPageWrapper: React.FC = () => {
  usePageInstructions('holdem')
  usePageActions('holdem')
  
  return <HoldemPage />
}