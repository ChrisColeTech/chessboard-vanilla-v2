import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { RoulettePage } from '../../pages/casino/RoulettePage'

export const RoulettePageWrapper: React.FC = () => {
  usePageInstructions('roulette')
  usePageActions('roulette')
  
  return <RoulettePage />
}