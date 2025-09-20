// navigation.types.ts - UI test navigation type definitions

/**
 * Represents a single UI test route
 */
export interface UITestRoute {
  readonly id: string;
  readonly title: string;
  readonly description: string;
  readonly path: string;
  readonly icon: string;
}

/**
 * Navigation state for UI test pages
 */
export interface UITestNavigationState {
  readonly currentRoute: UITestRoute;
  readonly availableRoutes: readonly UITestRoute[];
  readonly navigationHistory: readonly UITestRoute[];
  readonly isNavigating: boolean;
  readonly canGoBack: boolean;
  readonly isOnHomePage: boolean;
  readonly breadcrumbs: readonly { route: UITestRoute; isLast: boolean; isCurrent: boolean }[];
}

/**
 * Navigation actions interface
 */
export interface UITestNavigationActions {
  readonly navigateToRoute: (routeId: string) => void;
  readonly navigateToPath: (path: string) => void;
  readonly navigateBack: () => void;
  readonly navigateToHome: () => void;
  readonly resetNavigation: () => void;
  readonly getRouteById: (id: string) => UITestRoute | null;
  readonly getRouteByPath: (path: string) => UITestRoute | null;
  readonly isCurrentRoute: (routeId: string) => boolean;
  readonly isRouteInHistory: (routeId: string) => boolean;
}

/**
 * Complete navigation hook return type
 */
export interface UITestNavigationHook extends UITestNavigationState, UITestNavigationActions {}