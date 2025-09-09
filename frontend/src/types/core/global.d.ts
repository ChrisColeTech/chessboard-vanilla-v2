declare module 'react' {
  interface CSSProperties {
    WebkitAppRegion?: 'drag' | 'no-drag';
  }
}

declare global {
  namespace NodeJS {
    interface Timeout {}
  }
}

export {};