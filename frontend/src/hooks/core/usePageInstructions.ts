import { useEffect } from 'react'
import { useInstructions } from '../../contexts/InstructionsContext'
import { instructionsService } from '../../services/instructions/InstructionsService'

/**
 * Hook to automatically set page instructions from centralized service
 * Supports hierarchical page IDs like 'uitests.audio-demo'
 * Replaces manual setInstructions calls in individual pages
 */
export const usePageInstructions = (pageId: string) => {
  const { setInstructions } = useInstructions()

  useEffect(() => {
    const pageInstructions = instructionsService.getInstructions(pageId)
    
    if (pageInstructions) {
      setInstructions(pageInstructions.title, [...pageInstructions.instructions])
    }
  }, [pageId, setInstructions])
}