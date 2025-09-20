// navigation.constants.ts - UI test navigation constants

import type { UITestRoute } from '../../types';

/**
 * UI test route definitions
 */
export const UI_TEST_ROUTES: readonly UITestRoute[] = [
  {
    id: 'ui-test-index',
    title: 'UI Tests Overview',
    description: 'Central hub for all UI testing pages and demos',
    path: '/ui-tests',
    icon: '🧪'
  },
  {
    id: 'audio-demo',
    title: 'UI Audio Demo',
    description: 'Interactive demonstration of Global UI Audio Service patterns and usage',
    path: '/ui-tests/audio-demo',
    icon: '🔊'
  },
  {
    id: 'drag-test',
    title: 'Chess Drag Testing',
    description: 'Interactive testing environment for chess piece drag and drop functionality',
    path: '/ui-tests/drag-test',
    icon: '♜'
  }
] as const;

/**
 * Default route for UI tests
 */
export const DEFAULT_UI_TEST_ROUTE = UI_TEST_ROUTES[0];

/**
 * UI test route paths as constants for type safety
 */
export const UI_TEST_PATHS = {
  INDEX: '/ui-tests',
  AUDIO_DEMO: '/ui-tests/audio-demo',
  DRAG_TEST: '/ui-tests/drag-test'
} as const;

/**
 * UI test route IDs as constants for type safety
 */
export const UI_TEST_ROUTE_IDS = {
  INDEX: 'ui-test-index',
  AUDIO_DEMO: 'audio-demo',
  DRAG_TEST: 'drag-test'
} as const;

/**
 * Navigation breadcrumb labels
 */
export const BREADCRUMB_LABELS = {
  UI_TESTS: 'UI Tests',
  AUDIO_DEMO: 'Audio Demo',
  DRAG_TEST: 'Drag Test',
  HOME: 'Home'
} as const;

/**
 * Navigation menu categories for organizing routes
 */
export const NAVIGATION_CATEGORIES = {
  OVERVIEW: {
    id: 'overview',
    title: 'Overview',
    icon: '📋',
    routes: [UI_TEST_ROUTE_IDS.INDEX]
  },
  AUDIO_TESTING: {
    id: 'audio-testing',
    title: 'Audio Testing',
    icon: '🔊',
    routes: [UI_TEST_ROUTE_IDS.AUDIO_DEMO]
  },
  INTERACTION_TESTING: {
    id: 'interaction-testing',
    title: 'Interaction Testing',
    icon: '🎯',
    routes: [UI_TEST_ROUTE_IDS.DRAG_TEST]
  }
} as const;

/**
 * Route access levels for future permissions system
 */
export const ROUTE_ACCESS_LEVELS = {
  PUBLIC: 'public',
  DEVELOPER: 'developer',
  ADMIN: 'admin'
} as const;

/**
 * Route metadata for enhanced navigation
 */
export const ROUTE_METADATA = {
  [UI_TEST_ROUTE_IDS.INDEX]: {
    accessLevel: ROUTE_ACCESS_LEVELS.PUBLIC,
    category: NAVIGATION_CATEGORIES.OVERVIEW.id,
    isLandingPage: true,
    requiresChessboard: false
  },
  [UI_TEST_ROUTE_IDS.AUDIO_DEMO]: {
    accessLevel: ROUTE_ACCESS_LEVELS.PUBLIC,
    category: NAVIGATION_CATEGORIES.AUDIO_TESTING.id,
    isLandingPage: false,
    requiresChessboard: false
  },
  [UI_TEST_ROUTE_IDS.DRAG_TEST]: {
    accessLevel: ROUTE_ACCESS_LEVELS.PUBLIC,
    category: NAVIGATION_CATEGORIES.INTERACTION_TESTING.id,
    isLandingPage: false,
    requiresChessboard: true
  }
} as const;