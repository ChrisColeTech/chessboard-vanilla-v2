# Complete Project Structure Example

## Project Overview

This is a complete, production-ready project structure for the React Chessboard component library following all architectural principles outlined in the previous documents.

---

## Full Directory Structure

```
react-chessboard/
├── .github/                     # GitHub workflows and templates
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── release.yml
│   │   └── test.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── .vscode/                     # VS Code workspace settings
│   ├── settings.json
│   ├── extensions.json
│   └── launch.json
├── assets/                      # Static assets for piece sets
│   └── pieces/
│       ├── classic/
│       │   ├── bB.svg
│       │   ├── bK.svg
│       │   ├── bN.svg
│       │   ├── bP.svg
│       │   ├── bQ.svg
│       │   ├── bR.svg
│       │   ├── wB.svg
│       │   ├── wK.svg
│       │   ├── wN.svg
│       │   ├── wP.svg
│       │   ├── wQ.svg
│       │   └── wR.svg
│       ├── modern/
│       ├── tournament/
│       ├── executive/
│       └── conqueror/
├── docs/                        # Architecture and API documentation
│   ├── 00-research-questions.md
│   ├── 01-research-findings.md
│   ├── 02-architecture-guide.md
│   ├── 03-type-definitions.md
│   ├── 04-hooks-architecture.md
│   ├── 05-services-architecture.md
│   ├── 06-component-architecture.md
│   ├── 07-project-structure-example.md
│   ├── 08-anti-patterns-safeguards.md
│   └── API.md
├── examples/                    # Usage examples
│   ├── basic-chessboard/
│   │   ├── src/
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── index.html
│   │   ├── package.json
│   │   └── vite.config.ts
│   ├── game-replay/
│   │   └── [similar structure]
│   └── puzzle-mode/
│       └── [similar structure]
├── src/                         # Source code
│   ├── components/              # React components (presentation layer)
│   │   ├── ui/                  # Generic reusable UI components
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.types.ts
│   │   │   │   ├── Button.styles.css
│   │   │   │   ├── Button.test.tsx
│   │   │   │   └── index.ts
│   │   │   ├── LoadingSpinner/
│   │   │   │   ├── LoadingSpinner.tsx
│   │   │   │   ├── LoadingSpinner.types.ts
│   │   │   │   ├── LoadingSpinner.styles.css
│   │   │   │   └── index.ts
│   │   │   └── index.ts
│   │   └── chessboard/          # Chess-specific components
│   │       ├── Chessboard/
│   │       │   ├── Chessboard.tsx
│   │       │   ├── Chessboard.types.ts
│   │       │   ├── Chessboard.styles.css
│   │       │   ├── Chessboard.test.tsx
│   │       │   └── index.ts
│   │       ├── Board/
│   │       │   ├── Board.tsx
│   │       │   ├── Board.types.ts
│   │       │   ├── Board.styles.css
│   │       │   ├── Board.test.tsx
│   │       │   └── index.ts
│   │       ├── Square/
│   │       │   ├── Square.tsx
│   │       │   ├── Square.types.ts
│   │       │   ├── Square.styles.css
│   │       │   ├── Square.test.tsx
│   │       │   └── index.ts
│   │       ├── Piece/
│   │       │   ├── Piece.tsx
│   │       │   ├── Piece.types.ts
│   │       │   ├── Piece.styles.css
│   │       │   ├── Piece.test.tsx
│   │       │   └── index.ts
│   │       ├── SquareHighlight/
│   │       │   ├── SquareHighlight.tsx
│   │       │   ├── SquareHighlight.types.ts
│   │       │   ├── SquareHighlight.styles.css
│   │       │   └── index.ts
│   │       ├── CoordinateLabels/
│   │       │   ├── CoordinateLabels.tsx
│   │       │   ├── CoordinateLabels.types.ts
│   │       │   ├── CoordinateLabels.styles.css
│   │       │   └── index.ts
│   │       ├── BoardOverlay/
│   │       │   ├── BoardOverlay.tsx
│   │       │   ├── BoardOverlay.types.ts
│   │       │   ├── BoardOverlay.styles.css
│   │       │   └── index.ts
│   │       └── index.ts
│   ├── hooks/                   # Custom React hooks (state management)
│   │   ├── useChessGame.ts
│   │   ├── useChessGame.test.ts
│   │   ├── useDragAndDrop.ts
│   │   ├── useDragAndDrop.test.ts
│   │   ├── useChessAnimation.ts
│   │   ├── useChessAnimation.test.ts
│   │   ├── useResponsiveBoard.ts
│   │   ├── useResponsiveBoard.test.ts
│   │   ├── useChessValidation.ts
│   │   ├── useChessValidation.test.ts
│   │   ├── useChessEvents.ts
│   │   ├── useChessEvents.test.ts
│   │   ├── useChessMaster.ts
│   │   ├── useChessMaster.test.ts
│   │   └── index.ts
│   ├── services/                # Business logic (no React dependencies)
│   │   ├── chess/
│   │   │   ├── ChessGameService.ts
│   │   │   ├── ChessGameService.test.ts
│   │   │   ├── FenService.ts
│   │   │   ├── FenService.test.ts
│   │   │   ├── MoveValidationService.ts
│   │   │   ├── MoveValidationService.test.ts
│   │   │   └── index.ts
│   │   ├── animation/
│   │   │   ├── AnimationService.ts
│   │   │   ├── AnimationService.test.ts
│   │   │   └── index.ts
│   │   ├── storage/
│   │   │   ├── GameStorageService.ts
│   │   │   ├── GameStorageService.test.ts
│   │   │   └── index.ts
│   │   ├── ServiceFactory.ts
│   │   ├── ServiceFactory.test.ts
│   │   └── index.ts
│   ├── types/                   # TypeScript type definitions
│   │   ├── chess.types.ts
│   │   ├── ui.types.ts
│   │   ├── component.types.ts
│   │   ├── hooks.types.ts
│   │   ├── services.types.ts
│   │   ├── events.types.ts
│   │   ├── animation.types.ts
│   │   ├── utility.types.ts
│   │   └── index.ts
│   ├── utils/                   # Pure utility functions
│   │   ├── chess.utils.ts
│   │   ├── chess.utils.test.ts
│   │   ├── validation.utils.ts
│   │   ├── validation.utils.test.ts
│   │   ├── coordinate.utils.ts
│   │   ├── coordinate.utils.test.ts
│   │   ├── ui.utils.ts
│   │   ├── ui.utils.test.ts
│   │   ├── piece.utils.ts
│   │   ├── piece.utils.test.ts
│   │   └── index.ts
│   ├── constants/               # Application constants
│   │   ├── chess.constants.ts
│   │   ├── ui.constants.ts
│   │   ├── animation.constants.ts
│   │   └── index.ts
│   ├── providers/               # React context providers
│   │   ├── ChessProvider.tsx
│   │   ├── ChessProvider.test.tsx
│   │   ├── ThemeProvider.tsx
│   │   ├── ThemeProvider.test.tsx
│   │   └── index.ts
│   ├── styles/                  # Global styles and CSS variables
│   │   ├── variables.css
│   │   ├── global.css
│   │   ├── themes.css
│   │   └── animations.css
│   └── index.ts                 # Main export file
├── tests/                       # Test utilities and setup
│   ├── setup.ts
│   ├── mocks/
│   │   ├── chess.mocks.ts
│   │   ├── dom.mocks.ts
│   │   └── index.ts
│   └── utils/
│       ├── test.utils.tsx
│       └── index.ts
├── .eslintrc.json              # ESLint configuration
├── .prettierrc                 # Prettier configuration
├── .gitignore                  # Git ignore rules
├── jest.config.js              # Jest test configuration
├── tsconfig.json               # TypeScript configuration
├── tsconfig.build.json         # Build TypeScript configuration
├── vite.config.ts              # Vite build configuration
├── package.json                # Package dependencies and scripts
├── README.md                   # Project documentation
├── CHANGELOG.md                # Version changelog
├── LICENSE                     # MIT License
└── rollup.config.js            # Rollup build configuration
```

---

## Key Configuration Files

### 1. package.json

```json
{
  "name": "@your-org/react-chessboard",
  "version": "1.0.0",
  "description": "Modern, responsive React chessboard component",
  "keywords": ["react", "chess", "chessboard", "typescript", "npm-package"],
  "author": "Your Name <your.email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/your-org/react-chessboard.git"
  },
  "main": "dist/index.js",
  "module": "dist/index.esm.js",
  "types": "dist/index.d.ts",
  "files": [
    "dist",
    "assets",
    "README.md",
    "CHANGELOG.md"
  ],
  "exports": {
    ".": {
      "import": "./dist/index.esm.js",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./styles": "./dist/styles.css",
    "./package.json": "./package.json"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "build:lib": "rollup -c",
    "preview": "vite preview",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,css,md}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,css,md}\"",
    "prepare": "husky install",
    "prepublishOnly": "npm run build:lib",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  "dependencies": {
    "chess.js": "^1.0.0-beta.8",
    "framer-motion": "^10.16.4",
    "clsx": "^2.0.0"
  },
  "peerDependencies": {
    "react": ">=16.8.0",
    "react-dom": ">=16.8.0"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.4",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^14.5.1",
    "@types/jest": "^29.5.7",
    "@types/node": "^20.8.6",
    "@types/react": "^18.2.31",
    "@types/react-dom": "^18.2.14",
    "@typescript-eslint/eslint-plugin": "^6.7.5",
    "@typescript-eslint/parser": "^6.7.5",
    "@vitejs/plugin-react": "^4.1.0",
    "eslint": "^8.51.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "husky": "^8.0.3",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "lint-staged": "^15.0.2",
    "prettier": "^3.0.3",
    "rollup": "^4.1.4",
    "rollup-plugin-typescript2": "^0.36.0",
    "typescript": "^5.2.2",
    "vite": "^4.5.0"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{css,md}": ["prettier --write"]
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  }
}
```

### 2. tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/hooks/*": ["src/hooks/*"],
      "@/services/*": ["src/services/*"],
      "@/types/*": ["src/types/*"],
      "@/utils/*": ["src/utils/*"],
      "@/constants/*": ["src/constants/*"],
      "@/providers/*": ["src/providers/*"],
      "@/styles/*": ["src/styles/*"]
    }
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "examples"]
}
```

### 3. .eslintrc.json

```json
{
  "env": {
    "browser": true,
    "es2020": true,
    "node": true,
    "jest": true
  },
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:react/jsx-runtime"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "plugins": [
    "react-refresh",
    "@typescript-eslint"
  ],
  "rules": {
    "react-refresh/only-export-components": [
      "warn",
      { "allowConstantExport": true }
    ],
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "error",
    "@typescript-eslint/prefer-readonly": "error",
    "react-hooks/exhaustive-deps": "error",
    "react/prop-types": "off",
    "react/display-name": "error",
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "prefer-const": "error",
    "no-var": "error",
    "object-shorthand": "error",
    "prefer-template": "error"
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
```

### 4. jest.config.js

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss)$': 'identity-obj-proxy'
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{ts,tsx}',
    '!src/**/index.ts',
    '!src/types/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testPathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/dist/',
    '<rootDir>/examples/'
  ]
};
```

### 5. vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/index.ts'),
      name: 'ReactChessboard',
      formats: ['es', 'umd'],
      fileName: (format) => `react-chessboard.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
  css: {
    postcss: {
      plugins: [],
    },
  },
});
```

---

## Main Export File

### src/index.ts

```typescript
// Main component exports
export { Chessboard } from './components/chessboard/Chessboard';
export { Board } from './components/chessboard/Board';
export { Square } from './components/chessboard/Square';
export { Piece } from './components/chessboard/Piece';

// Hook exports
export { useChessGame } from './hooks/useChessGame';
export { useDragAndDrop } from './hooks/useDragAndDrop';
export { useChessAnimation } from './hooks/useChessAnimation';
export { useResponsiveBoard } from './hooks/useResponsiveBoard';
export { useChessValidation } from './hooks/useChessValidation';
export { useChessMaster } from './hooks/useChessMaster';

// Service exports (for advanced usage)
export { ChessGameService } from './services/chess/ChessGameService';
export { FenService } from './services/chess/FenService';
export { ServiceFactory } from './services/ServiceFactory';

// Type exports
export type {
  ChessboardProps,
  ChessGameState,
  ChessMove,
  ChessPiece,
  ChessPosition,
  PieceType,
  PieceColor,
  BoardOrientation,
  PieceSet,
  SquareNotation
} from './types';

// Provider exports
export { ChessProvider } from './providers/ChessProvider';
export { ThemeProvider } from './providers/ThemeProvider';

// Utility exports
export { 
  positionToSquareNotation,
  squareNotationToPosition,
  createChessGameState
} from './utils';

// Constant exports
export {
  DEFAULT_FEN,
  PIECE_SETS,
  DEFAULT_THEME
} from './constants';

// Version
export const VERSION = '1.0.0';
```

---

## Example Usage Files

### examples/basic-chessboard/src/App.tsx

```typescript
import React from 'react';
import { Chessboard, ChessProvider } from '@your-org/react-chessboard';
import '@your-org/react-chessboard/styles';

function App() {
  return (
    <ChessProvider>
      <div className="app">
        <h1>React Chessboard Example</h1>
        <Chessboard
          orientation="white"
          pieceSet="classic"
          showCoordinates
          allowDragAndDrop
          onMove={(move) => {
            console.log('Move made:', move);
            return true;
          }}
        />
      </div>
    </ChessProvider>
  );
}

export default App;
```

---

## GitHub Workflows

### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - run: npm ci
    - run: npm run lint
    - run: npm run type-check
    - run: npm run test:coverage
    - run: npm run build
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
```

This complete project structure provides:

✅ **Clean Architecture** - Proper separation of concerns  
✅ **TypeScript Coverage** - Comprehensive type safety  
✅ **Testing Setup** - Unit tests with coverage requirements  
✅ **Build Pipeline** - Multiple output formats  
✅ **Developer Experience** - ESLint, Prettier, Husky  
✅ **Documentation** - Comprehensive guides and examples  
✅ **CI/CD** - Automated testing and deployment  
✅ **Accessibility** - Screen reader support built-in  
✅ **Performance** - Optimized rendering and bundling