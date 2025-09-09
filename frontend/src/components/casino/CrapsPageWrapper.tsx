import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { CrapsPage } from '../../pages/casino/CrapsPage'

export const CrapsPageWrapper: React.FC = () => {
  usePageInstructions('craps')
  usePageActions('craps')
  
  return <CrapsPage />
}