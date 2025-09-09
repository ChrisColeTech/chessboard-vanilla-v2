import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'
import { usePageActions } from '../../hooks/core/usePageActions'
import { SlotMachineTestPage } from '../../pages/casino/SlotMachineTestPage'

export const SlotMachinePageWrapper: React.FC = () => {
  usePageInstructions('slots')
  usePageActions('slots')
  
  return <SlotMachineTestPage />
}