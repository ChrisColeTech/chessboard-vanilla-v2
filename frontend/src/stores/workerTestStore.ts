import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'

interface TestResult {
  id: string
  timestamp: Date
  message: string
  type: 'info' | 'success' | 'error' | 'warning'
}

interface WorkerTestState {
  testResults: TestResult[]
  lastMove: string
  responseTime: number
  evaluation: string
  isTestingReady: boolean
  isTestingSpeed: boolean
  isTestingPosition: boolean
  isRunningAllTests: boolean
}

interface WorkerTestActions {
  addTestResult: (message: string, type?: TestResult['type']) => void
  setLastMove: (move: string) => void
  setResponseTime: (time: number) => void
  setEvaluation: (evaluation: string) => void
  setIsTestingReady: (testing: boolean) => void
  setIsTestingSpeed: (testing: boolean) => void
  setIsTestingPosition: (testing: boolean) => void
  setIsRunningAllTests: (running: boolean) => void
  clearResults: () => void
}

export const useWorkerTestStore = create<WorkerTestState & WorkerTestActions>()(
  subscribeWithSelector((set) => ({
    // State
    testResults: [],
    lastMove: '',
    responseTime: 0,
    evaluation: '',
    isTestingReady: false,
    isTestingSpeed: false,
    isTestingPosition: false,
    isRunningAllTests: false,

    // Actions
    addTestResult: (message, type = 'info') => 
      set((state) => ({
        testResults: [
          ...state.testResults,
          {
            id: Date.now().toString(),
            timestamp: new Date(),
            message,
            type
          }
        ]
      })),

    setLastMove: (move) => set({ lastMove: move }),
    setResponseTime: (time) => set({ responseTime: time }),
    setEvaluation: (evaluation) => set({ evaluation }),
    setIsTestingReady: (testing) => set({ isTestingReady: testing }),
    setIsTestingSpeed: (testing) => set({ isTestingSpeed: testing }),
    setIsTestingPosition: (testing) => set({ isTestingPosition: testing }),
    setIsRunningAllTests: (running) => set({ isRunningAllTests: running }),
    
    clearResults: () => set({
      testResults: [],
      lastMove: '',
      responseTime: 0,
      evaluation: ''
    })
  }))
)