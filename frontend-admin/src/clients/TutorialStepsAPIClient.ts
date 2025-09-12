import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * TutorialSteps Domain API Client
 * Handles all tutorial-steps-related API operations
 */
export class TutorialStepsAPIClient extends BaseAPIClient {
  async getStepsByTutorial(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/tutorialSteps/tutorial/:tutorialId${queryString}`);
  }
  async completeStep(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/tutorialSteps/${id}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default TutorialStepsAPIClient;
