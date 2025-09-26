# Frontend Generator Mini

A combined tool that generates complete frontend applications from backend configurations, merging the best of Frontend Generator V2 and Mobile Pages Mini.

## What We Built

### ✅ **Phase 1: Foundation** 
- **Copied generators** from Frontend Generator V2
- **Extracted hardcoded templates** into proper .template files
- **Integrated template engine** from Mobile Pages Mini
- **Added name standardizer** for consistent naming

### ✅ **Phase 2: Template-Based Generation**
Created dynamic templates for:
- `templates/dynamic/api/service.ts.template` - API service classes
- `templates/dynamic/api/types.ts.template` - TypeScript interfaces
- `templates/dynamic/api/hook.ts.template` - React hooks
- `templates/dynamic/api/page.tsx.template` - Basic page components

### ✅ **Phase 3: Refactored Generator**
- **New Services Generator** using template engine instead of hardcoded strings
- **Smart method generation** based on endpoint configuration
- **Domain organization** (chess, training, theory, etc.)
- **Name standardization** using shared utilities

### ✅ **Phase 4: Comprehensive Tests**
- **Unit tests** for individual generator functions
- **Integration tests** with real chess backend entities
- **6 test cases** covering various scenarios
- **100% test pass rate**

## Current Structure

```
frontend-generator-mini/
├── generators/                          # API generators (from V2)
│   ├── services/services_generator_new.py   # ✅ Refactored with templates
│   ├── types/types_generator.py             # 🔄 Next: needs refactoring  
│   ├── hooks/hooks_generator.py             # 🔄 Next: needs refactoring
│   └── [others]                             # 🔄 Next: needs refactoring
├── templates/dynamic/api/                # ✅ Template files extracted
│   ├── service.ts.template               # ✅ Working
│   ├── types.ts.template                 # ✅ Created
│   ├── hook.ts.template                  # ✅ Created  
│   └── page.tsx.template                 # ✅ Created
├── modules/                              # From Mini
│   ├── template_engine.py                # ✅ Working
│   └── config.py                         # ✅ Working
├── shared/                               # Utilities
│   └── name_standardizer.py              # ✅ Working
└── tests/                                # ✅ Complete test suite
    └── test_services_generator.py        # ✅ 6 passing tests
```

## Demo: Generated Service

From backend config:
```json
{
  "games": {
    "entity": "Game",
    "methods": ["createGame", "getGameById", "listGames", "updateGame", "deleteGame"]
  }
}
```

Generates `services/chess/gamesService.ts`:
```typescript
// Generated service for Game
import type { Game } from '../../types/chess/games';

class GameService {
  // ... authentication, error handling
  
  async createGame(data: Partial<Game>): Promise<Game> { /* ... */ }
  async getGameById(id: string): Promise<Game> { /* ... */ }
  async listGames(): Promise<Game[]> { /* ... */ }
  async updateGame(id: string, data: Partial<Game>): Promise<Game> { /* ... */ }
  async deleteGame(id: string): Promise<void> { /* ... */ }
}

export const gamesService = new GameService();
```

## Key Improvements

### ✅ **Template-Based Architecture**
- **No more hardcoded strings** - everything uses .template files
- **Consistent template engine** - same system for all generation
- **Easy customization** - modify templates, not Python code

### ✅ **Proper Name Handling**
- **Name standardizer** handles snake_case → camelCase conversion
- **Consistent naming** across all generated files
- **No more manual string manipulation**

### ✅ **Domain Organization**
- **Services organized by domain** (chess, training, theory)
- **Logical grouping** of related functionality
- **Clean output structure**

### ✅ **Comprehensive Testing**
- **Real test scenarios** using actual chess backend entities
- **Error handling** and edge case coverage
- **Continuous validation** of generated output

## Next Steps

1. **Refactor remaining generators** (types, hooks, pages)
2. **Add Mobile Pages Mini UI generation** 
3. **Create entity mapper** for chess-specific page structure
4. **Build combined CLI** that orchestrates both API + UI generation

## Running Tests

```bash
python -m pytest tests/test_services_generator.py -v
```

## Usage Example

```python
from services.services_generator_new import ServicesGenerator

generator = ServicesGenerator(output_path)
generator.generate('games', {
    'entity': 'Game',
    'methods': ['createGame', 'getGameById', 'listGames']
}, 'chess')
```

This foundation sets us up perfectly for the full combined tool that will generate complete chess applications from backend configurations.