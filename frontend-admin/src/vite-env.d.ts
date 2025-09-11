/// <reference types="vite/client" />

// Extend CSS Properties for WebKit-specific properties without overriding React module
declare global {
  namespace React {
    interface CSSProperties {
      WebkitAppRegion?: 'drag' | 'no-drag';
    }
  }
}
