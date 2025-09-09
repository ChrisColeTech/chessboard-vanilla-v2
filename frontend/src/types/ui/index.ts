// index.ts - UI tests types barrel export

// Navigation types
export type {
  UITestRoute,
  UITestNavigationState,
  UITestNavigationActions,
  UITestNavigationHook
} from './navigation.types';

// Audio demo types
export type {
  AudioDemoConfiguration,
  DemoSection,
  DemoButtonExample,
  ExclusionExample,
  CodeSnippet,
  AudioDemoState,
  AudioDemoActions,
  AudioDemoHook
} from './audio-demo.types';

// Drag testing types
export type {
  DragTestConfiguration,
  DragTestState,
  DragTestActions,
  MoveHandler,
  DragTestingHook
} from './drag-testing.types';