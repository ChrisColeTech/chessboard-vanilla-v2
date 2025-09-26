import { useAuthStore } from "../stores/authStore";

export function useAuthStatus() {
  const { isAuthenticated, isLoading } = useAuthStore();
  
  return {
    isAuthenticated,
    isLoading
  };
}