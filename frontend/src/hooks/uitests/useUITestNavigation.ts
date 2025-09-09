// useUITestNavigation.ts - Hook for managing UI test navigation

import { useState, useCallback, useMemo } from 'react';
import type { 
  UITestNavigationState,
  UITestNavigationActions,
  UITestNavigationHook,
  UITestRoute 
} from '../../types';
import { UIDemoService } from '../../services';
import { UI_TEST_ROUTES, DEFAULT_UI_TEST_ROUTE } from '../../constants';

/**
 * Hook for managing UI test navigation state and actions
 */
export const useUITestNavigation = (
  initialRoute?: string
): UITestNavigationHook => {
  const demoService = useMemo(() => UIDemoService.getInstance(), []);
  
  // Initialize state
  const [currentRoute, setCurrentRoute] = useState<UITestRoute>(() => {
    if (initialRoute) {
      const foundRoute = demoService.getRouteByPath(initialRoute) || 
                        demoService.getRouteById(initialRoute);
      if (foundRoute) return foundRoute;
    }
    return DEFAULT_UI_TEST_ROUTE;
  });

  const [navigationHistory, setNavigationHistory] = useState<UITestRoute[]>([currentRoute]);
  const [isNavigating, setIsNavigating] = useState(false);

  // Available routes
  const availableRoutes = useMemo(() => UI_TEST_ROUTES, []);

  // Navigation actions
  const navigateToRoute = useCallback((routeId: string) => {
    const route = demoService.getRouteById(routeId);
    if (!route) {
      console.warn(`Route not found: ${routeId}`);
      return;
    }

    setIsNavigating(true);
    setCurrentRoute(route);
    setNavigationHistory(prev => [...prev, route]);
    
    // Simulate navigation delay for UX
    setTimeout(() => setIsNavigating(false), 100);
  }, [demoService]);

  const navigateToPath = useCallback((path: string) => {
    const route = demoService.getRouteByPath(path);
    if (!route) {
      console.warn(`Route not found for path: ${path}`);
      return;
    }

    setIsNavigating(true);
    setCurrentRoute(route);
    setNavigationHistory(prev => [...prev, route]);
    
    // Simulate navigation delay for UX
    setTimeout(() => setIsNavigating(false), 100);
  }, [demoService]);

  const navigateBack = useCallback(() => {
    if (navigationHistory.length <= 1) {
      console.warn('Cannot navigate back - no previous route');
      return;
    }

    setIsNavigating(true);
    const newHistory = navigationHistory.slice(0, -1);
    const previousRoute = newHistory[newHistory.length - 1];
    
    setCurrentRoute(previousRoute);
    setNavigationHistory(newHistory);
    
    setTimeout(() => setIsNavigating(false), 100);
  }, [navigationHistory]);

  const navigateToHome = useCallback(() => {
    setIsNavigating(true);
    setCurrentRoute(DEFAULT_UI_TEST_ROUTE);
    setNavigationHistory([DEFAULT_UI_TEST_ROUTE]);
    
    setTimeout(() => setIsNavigating(false), 100);
  }, []);

  const resetNavigation = useCallback(() => {
    setCurrentRoute(DEFAULT_UI_TEST_ROUTE);
    setNavigationHistory([DEFAULT_UI_TEST_ROUTE]);
    setIsNavigating(false);
  }, []);

  // Computed state
  const canGoBack = navigationHistory.length > 1;
  const isOnHomePage = currentRoute.id === DEFAULT_UI_TEST_ROUTE.id;

  // Breadcrumb generation
  const breadcrumbs = useMemo(() => {
    return navigationHistory.map((route, index) => ({
      route,
      isLast: index === navigationHistory.length - 1,
      isCurrent: route.id === currentRoute.id
    }));
  }, [navigationHistory, currentRoute]);

  // Route utilities
  const getRouteById = useCallback((id: string) => {
    return demoService.getRouteById(id);
  }, [demoService]);

  const getRouteByPath = useCallback((path: string) => {
    return demoService.getRouteByPath(path);
  }, [demoService]);

  const isCurrentRoute = useCallback((routeId: string) => {
    return currentRoute.id === routeId;
  }, [currentRoute]);

  const isRouteInHistory = useCallback((routeId: string) => {
    return navigationHistory.some(route => route.id === routeId);
  }, [navigationHistory]);

  // State object
  const state: UITestNavigationState = {
    currentRoute,
    availableRoutes,
    navigationHistory,
    isNavigating,
    canGoBack,
    isOnHomePage,
    breadcrumbs
  };

  // Actions object
  const actions: UITestNavigationActions = {
    navigateToRoute,
    navigateToPath,
    navigateBack,
    navigateToHome,
    resetNavigation,
    getRouteById,
    getRouteByPath,
    isCurrentRoute,
    isRouteInHistory
  };

  // Return hook interface
  return {
    ...state,
    ...actions
  };
};