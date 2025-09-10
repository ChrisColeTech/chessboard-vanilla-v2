export interface TutorialstepResponse {
  id: string;
  tutorial_id: string;
  step_number: number;
  title: string;
  content: string;
  action_required: string;
  completed: boolean;
}

export interface CreateTutorialstepRequest {
  tutorial_id: string;
  step_number: number;
  title: string;
  content: string;
  action_required: string;
  completed: boolean;
}

export interface UpdateTutorialstepRequest {
  tutorial_id?: string;
  step_number?: number;
  title?: string;
  content?: string;
  action_required?: string;
  completed?: boolean;
}