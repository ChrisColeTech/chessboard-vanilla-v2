import { useEffect } from 'react'
import { useInstructions } from '../../contexts/InstructionsContext'
import { dynamicInstructionsService } from '../../services/instructions/InstructionsService.dynamic'

/**
 * Hook to automatically set page instructions from dynamic service
 * Supports hierarchical page IDs like 'uitests.audio-demo'
 * Uses dynamic file loading for zero-configuration instruction management
 */
export const usePageInstructions = (pageId: string) => {
  const { setInstructions } = useInstructions()

  useEffect(() => {
    const pageInstructions = dynamicInstructionsService.getInstructions(pageId)
    
    if (pageInstructions) {
      setInstructions(pageInstructions.title, [...pageInstructions.instructions])
    }
  }, [pageId, setInstructions])
}