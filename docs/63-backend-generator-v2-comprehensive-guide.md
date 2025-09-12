# Backend Generator v2 - Comprehensive Guide

## Project Structure

```
/mnt/c/Projects/chessboard-vanilla-v2/
└── tools/
    └── backend-tools/                           # Backend Generator v2 Root Directory
        ├── backend_generator_v2.py              # Main orchestrator
        ├── backend_config.json                  # Configuration file
        ├── config.py                           # Configuration system
        ├── pattern_analyzer.py                 # Pattern analysis
        ├── template_generator.py               # Model & route generation
        ├── service_generator.py                # Service class generation
        ├── infrastructure_generator.py         # Infrastructure setup
        ├── parameter_mapper.py                 # Route parameter mapping
        ├── db_update_tool.py                   # Database utilities
        ├── route_parameter_fixer.py            # Route parameter fixes
        ├── backend_generator_refactored.py     # Alternative implementation
        ├── method_generators/                  # Method generation modules
        │   ├── __init__.py
        │   ├── base_generator.py               # Abstract base class
        │   ├── auth_methods.py                 # Authentication methods
        │   ├── puzzle_methods.py               # Chess puzzle methods
        │   ├── game_methods.py                 # Chess game methods
        │   ├── user_methods.py                 # User management methods
        │   ├── learning_path_methods.py        # Learning path methods
        │   └── generic_methods.py              # Standard CRUD methods
        ├── payload-generator/                  # Test payload generation
        │   ├── payload_generator.py
        │   ├── db_query.py
        │   ├── generated_payloads.json
        │   └── real_test_ids.json
        └── missing-columns/                    # Database column utilities
            └── missing-columns.py
```

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Modules](#core-modules)
4. [Configuration System](#configuration-system)
5. [Method Generation System](#method-generation-system)
6. [Usage Guide](#usage-guide)
7. [Advanced Features](#advanced-features)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Extension Guide](#extension-guide)

---

## Overview

The Backend Generator v2 is a sophisticated, modular Python system designed to automatically generate complete TypeScript backend applications. Built specifically for chess applications but extensible to any domain, it transforms JSON configuration into production-ready Express.js backends with TypeScript, PostgreSQL integration, JWT authentication, and comprehensive API endpoints.

### Key Features

- **Configuration-Driven**: Generate entire backends from JSON configuration
- **Modular Architecture**: 11 specialized modules working together
- **22+ Entity Support**: Users, Auth, Puzzles, Games, Learning, Analytics, and more
- **Production Ready**: PostgreSQL, JWT auth, error handling, logging
- **Extensible**: Plugin-based method generators for custom functionality
- **TypeScript First**: Complete type safety throughout the generated code

### Generated Output

```
backend-v2/
├── src/
│   ├── models/           # TypeScript interfaces and types
│   ├── services/         # Business logic classes
│   ├── routes/           # Express.js route handlers
│   ├── middleware/       # Authentication and validation
│   ├── utils/           # Database utilities and helpers
│   └── app.ts           # Main application entry point
```

---

## Architecture

The system follows a modular, orchestrated architecture with clear separation of concerns:

```
Backend Generator v2 (Main Orchestrator)
├── Pattern Analyzer         # Extracts patterns from existing code
├── Template Generator       # Generates models and routes
├── Service Generator        # Creates business logic services
├── Infrastructure Generator # Sets up middleware and utilities
├── Parameter Mapper         # Maps HTTP params to service calls
├── Configuration System     # Manages paths and settings
├── Database Tools           # Database utilities and column management
├── Route Parameter Fixer    # Route parameter corrections
└── Method Generators/       # Specialized method implementations
    ├── Base Generator       # Abstract interface
    ├── Generic Methods      # Standard CRUD operations
    ├── Auth Methods         # Authentication system
    ├── Puzzle Methods       # Chess puzzle functionality
    ├── Game Methods         # Chess game management
    ├── User Methods         # User profile management
    └── Learning Path Methods # Learning path and tutorial system
```

---

## Core Modules

### 1. Backend Generator v2 (`backend_generator_v2.py`)

**Purpose**: Main orchestrator that coordinates all other modules and provides the primary interface.

#### Key Classes

**`GenerationOptions`**
- `dry_run: bool = False` - Preview without creating files
- `verbose: bool = False` - Detailed output logging
- `validate_config: bool = True` - Validate configuration before generation
- `backup_existing: bool = False` - Backup existing files (disabled by default)
- `force_overwrite: bool = False` - Overwrite existing files
- `output_format: str = "typescript"` - Target language (typescript/javascript)
- `include_tests: bool = False` - Generate test files (future feature)
- `include_docs: bool = False` - Generate documentation (future feature)

**`BackendGeneratorV2`**

**Methods:**

- **`__init__(self, backend_path: str = None)`**
  - Initializes the generator with backend path
  - Sets up all component modules (pattern analyzer, template generator, etc.)
  - Configures logging system

- **`generate_endpoint(self, config: Dict[str, Any], options: GenerationOptions = None) -> bool`**
  - Generates a single endpoint from configuration
  - Validates configuration if enabled
  - Creates model, service, and route files
  - Returns success/failure status

- **`generate_multiple_endpoints(self, config_file: Union[str, Path], options: GenerationOptions = None) -> Dict[str, bool]`**
  - Generates all endpoints from a configuration file
  - Creates infrastructure files once at the beginning
  - Returns dictionary of endpoint names to success status

- **`_validate_config(self, config: Dict[str, Any]) -> List[str]`**
  - Validates entity names (alphanumeric + underscores only)
  - Ensures required fields are present (entity, properties)
  - Validates property names and types
  - Warns about custom methods that may not be supported

- **`_preview_generation(self, config: Dict[str, Any])`**
  - Shows what files would be generated (dry run mode)
  - Lists properties and methods that would be included
  - Helps verify configuration before actual generation

#### CLI Interface

**Arguments:**
- `endpoint` - Specific endpoint name to generate
- `--config, -c` - Configuration file path (default: backend_config.json)
- `--dry-run` - Preview generation without creating files
- `--verbose, -v` - Enable verbose output
- `--force` - Force overwrite existing files
- `--all` - Generate all endpoints from config
- `--backend-path` - Custom backend directory path

**Example Usage:**
```bash
# Navigate to the backend tools directory
cd tools/backend-tools

# Generate all endpoints
python backend_generator_v2.py --all

# Generate specific endpoint with dry run
python backend_generator_v2.py puzzles --dry-run

# Generate with verbose output
python backend_generator_v2.py auth --verbose --force
```

---

### 2. Configuration System (`config.py`)

**Purpose**: Manages paths, settings, and provides intelligent backend path detection.

#### Functions

- **`get_backend_path() -> str`**
  - Checks environment variable `BACKEND_PATH` first
  - Searches for project root by looking for `.git` or `package.json`
  - Prefers `backend-v2` over `backend` directory
  - Provides fallback path if detection fails

#### Classes

**`GeneratorConfig`**
- `backend_path: str` - Target backend directory
- `backup_enabled: bool = False` - Backup existing files
- `verbose: bool = False` - Verbose output
- `dry_run: bool = False` - Preview mode

**Methods:**
- **`get_path(self) -> Path`** - Returns backend path as Path object

---

### 3. Pattern Analyzer (`pattern_analyzer.py`)

**Purpose**: Analyzes existing backend files to extract code patterns for consistent generation.

#### Class: `PatternAnalyzer`

**Methods:**

- **`__init__(self, backend_path: str = None)`**
  - Sets up backend path for pattern analysis

- **`analyze_existing_pattern(self, reference_service: str = "puzzles") -> Dict`**
  - Analyzes existing service files to extract patterns
  - Returns dictionary with route, service, and model patterns
  - Currently uses default patterns but designed for future file parsing

- **`_analyze_route_pattern(self, filename: str) -> Dict`**
  - Extracts routing patterns from existing route files
  - Returns route template with imports and structure

- **`_analyze_service_pattern(self, filename: str) -> Dict`**
  - Analyzes service file patterns
  - Returns service template with method patterns

- **`_analyze_model_pattern(self, filename: str) -> Dict`**
  - Extracts model interface patterns
  - Returns TypeScript interface templates

#### Default Patterns

**Route Pattern:**
```typescript
import { Router } from 'express';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
// ... service and model imports
const router = Router();
// ... route handlers
export default router;
```

**Service Pattern:**
```typescript
import { Database } from '../utils/database';
import { ModelTypes } from '../models/ModelName';

export class ServiceClass {
  private db = Database.getInstance();
  // ... service methods
}
```

---

### 4. Template Generator (`template_generator.py`)

**Purpose**: Generates TypeScript model interfaces and Express.js route files.

#### Class: `TemplateGenerator`

**Methods:**

- **`generate_model(self, entity: str, properties: Dict[str, str], config: Dict[str, Any] = None) -> None`**
  - Generates TypeScript model file with interfaces
  - Creates `EntityResponse`, `CreateEntityRequest`, and `UpdateEntityRequest` interfaces
  - Handles special property mappings (e.g., `solutionMoves` → `solution_moves`)
  - Special handling for auth entity with predefined interfaces

- **`generate_route(self, entity: str, entities: str, endpoints: List[Dict], config: Dict[str, Any] = None) -> None`**
  - Generates Express.js route file
  - Ensures complete CRUD operations are available
  - Adds authentication middleware based on `auth_required` flag
  - Uses parameter mapper for correct handler parameters
  - Converts snake_case filenames to camelCase

- **`_generate_auth_model(self) -> str`**
  - Returns predefined auth model with comprehensive interfaces:
    - `LoginRequest`, `RegisterRequest`, `LoginResponse`
    - `UserInfo`, `MeResponse`, `UserProgress`
    - `ForgotPasswordRequest`, `ResetPasswordRequest`
    - `ChangePasswordRequest`, `UpdateProfileRequest`
    - `TokenVerificationResponse`, `AvailabilityResponse`

- **`_get_handler_params(self, handler_name: str, path: str, method: str) -> str`**
  - Maps handler names to correct Express.js parameters
  - Handles entity-specific cases (puzzles, games, auth, users)
  - Falls back to parameter mapper for generic cases

#### Model Generation Logic

**Standard Properties:**
- Automatically excludes `id`, `created_at`, `updated_at` from Create interfaces
- Makes all properties optional in Update interfaces
- Handles JSON field mapping for complex data types

**Special Cases:**
- **Auth Entity**: Uses predefined comprehensive auth interfaces
- **JSON Fields**: Parses string fields that store JSON data
- **Database Mapping**: Maps camelCase properties to snake_case database columns

---

### 5. Service Generator (`service_generator.py`)

**Purpose**: Creates TypeScript service classes with database operations and business logic.

#### Class: `ServiceGenerator`

**Methods:**

- **`generate_service(self, entity: str, entities: str, table_name: str, methods: List[str], config: Dict[str, Any]) -> None`**
  - Generates complete service class file
  - Ensures all standard CRUD methods are included
  - Uses specialized method generators based on entity type
  - Adds entity-specific format methods
  - Includes special helper methods for auth service

- **`generate_service_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str`**
  - Routes method generation to appropriate specialized generator
  - **Puzzle Methods**: `getNext`, `solve`, `getHint`, `getCategories`
  - **Game Methods**: `getGame`, `createGame`, `updateGame`, `analyze`
  - **Auth Methods**: `register`, `login`, `logout`, `verifyToken`, etc.
  - **User Methods**: `getUser`, `updateUser`
  - **Generic Methods**: Standard CRUD operations

- **`_generate_format_method(self, entity_upper: str, properties: dict) -> str`**
  - Creates entity-specific response formatting method
  - Handles JSON field parsing (themes, solution_moves)
  - Special formatting for auth entities (UserInfo format)

#### Service Structure

**Generated Service Class:**
```typescript
import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { ModelTypes } from '../models/EntityName';

export class EntityService {
  private db = Database.getInstance();

  // Generated methods...
  
  private formatEntityResponse(row: any): EntityResponse {
    return {
      // Property mapping...
    };
  }
}
```

---

### 6. Infrastructure Generator (`infrastructure_generator.py`)

**Purpose**: Creates essential infrastructure files required by the backend.

#### Class: `InfrastructureGenerator`

**Methods:**

- **`generate_infrastructure(self) -> bool`**
  - Creates all required infrastructure files
  - Sets up directory structure
  - Returns success/failure status

- **`_create_directories(self)`**
  - Creates necessary directory structure:
    - `src/middleware`, `src/utils`, `src/models`
    - `src/services`, `src/routes`

- **`_generate_database_utils(self)`**
  - Creates `src/utils/database.ts` with PostgreSQL connection
  - **Supabase Optimized**: Connection pooling, SSL handling
  - **Error Handling**: Automatic reconnection on connection termination
  - **Pool Management**: Configurable pool size and timeouts
  - **Query Method**: Parameterized queries with retry logic

- **`_generate_auth_middleware(self)`**
  - Creates `src/middleware/auth.ts`
  - **JWT Verification**: Token validation and user extraction
  - **AuthenticatedRequest Interface**: Extended Express request type
  - **Optional Auth**: Middleware for optional authentication

- **`_generate_validation_middleware(self)`**
  - Creates `src/middleware/validation.ts`
  - **express-validator Integration**: Request validation
  - **Schema Validation**: Joi schema validation support

- **`_generate_app_file(self)`**
  - Creates main `src/app.ts` file
  - **Dynamic Route Registration**: Loads routes from tools/backend-tools/backend_config.json
  - **Middleware Setup**: CORS, JSON parsing, request/response logging
  - **Error Handling**: Comprehensive error middleware
  - **Health Check**: Basic health check endpoint

#### Database Configuration

**Connection Settings (Supabase Optimized):**
```typescript
{
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
  max: 5,                           // Lower max for pooler compatibility
  min: 1,                           // Lower min to prevent exhaustion
  idleTimeoutMillis: 10000,         // Shorter idle timeout
  connectionTimeoutMillis: 10000,   // Connection timeout
  allowExitOnIdle: false,           // Keep pool alive
  keepAlive: true,                  // Enable TCP keepalive
  keepAliveInitialDelayMillis: 10000
}
```

---

### 7. Parameter Mapper (`parameter_mapper.py`)

**Purpose**: Provides intelligent parameter mapping for route handlers based on HTTP method, path patterns, and handler names.

#### Class: `ParameterMapper`

**Methods:**

- **`get_parameters(self, method: str, path: str, handler_name: str) -> str`**
  - Returns appropriate parameters for Express.js route handler
  - Checks path-specific overrides first (most specific)
  - Falls back to method-specific logic
  - Handles special handler patterns

- **`_handle_get_method(self, path: str, handler_name: str) -> str`**
  - GET with `:id` → `req.params.id`
  - GET without params → empty string

- **`_handle_post_method(self, path: str, handler_name: str) -> str`**
  - POST with `:id` → `req.params.id, req.body` (actions on existing resources)
  - POST without `:id` → `req.body` (create new resources)

- **`_handle_put_method(self, path: str, handler_name: str) -> str`**
  - PUT with `:id` → `req.params.id, req.body`
  - PUT without `:id` → `req.body`

- **`_handle_delete_method(self, path: str, handler_name: str) -> str`**
  - DELETE with `:id` → `req.params.id`
  - DELETE without `:id` → `req.body` (bulk delete)

- **`analyze_pattern(self, method: str, path: str, handler_name: str) -> Dict[str, str]`**
  - Returns detailed analysis for debugging
  - Classifies pattern type (update_by_id, create_new, etc.)

#### Special Handler Overrides

**Path-Specific Overrides:**
```python
{
    ('PUT', '/update', 'updateProgress'): 'req.body.userId, req.body',
    ('POST', '/:id/complete', 'completeTutorial'): 'req.params.id',
}
```

**Special Handlers:**
```python
{
    'updateUserSettings': 'req.body',
    'getUserSettings': '',
    'updateUserPreferences': 'req.body',
    'getUserPreferences': '',
}
```

### 8. Database Tools (`db_update_tool.py`)

**Purpose**: Provides database utilities and column management functionality.

#### Key Features
- Database schema analysis
- Column existence verification
- Database update utilities
- Schema migration support

### 9. Route Parameter Fixer (`route_parameter_fixer.py`)

**Purpose**: Fixes and validates route parameter mappings.

#### Key Features
- Route parameter validation
- Parameter mapping corrections
- Express.js route parameter compliance
- Parameter type checking

### 10. Payload Generator (`payload-generator/`)

**Purpose**: Generates test payloads and manages test data for endpoint testing.

#### Components
- **`payload_generator.py`**: Main payload generation logic
- **`db_query.py`**: Database query utilities for test data
- **`generated_payloads.json`**: Generated test payload data
- **`real_test_ids.json`**: Real database IDs for testing

#### Key Features
- Realistic test data generation
- Database-backed test IDs
- Endpoint-specific payload creation
- Validation test data

### 11. Missing Columns Tool (`missing-columns/`)

**Purpose**: Identifies and manages missing database columns.

#### Key Features
- Database schema comparison
- Missing column detection
- Column addition suggestions
- Schema synchronization

---

## Method Generation System

The method generation system uses a plugin-based architecture with specialized generators for different entity types.

### Base Generator (`base_generator.py`)

**Abstract Base Class**: `BaseMethodGenerator`

**Methods:**
- **`generate_method(self, method_name: str, entity_upper: str, entity_lower: str, table_name: str) -> str`**
  - Abstract method implemented by all generators
- **`_create_stub_method(self, method_name: str, table_name: str = None, entity_upper: str = None) -> str`**
  - Creates production-ready generic method implementation
  - When table_name and entity_upper provided: queries entity table and returns formatted results
  - Fallback: returns empty array for backward compatibility

### Generic Methods (`generic_methods.py`)

**Purpose**: Handles standard CRUD operations and common patterns.

#### Key Method Patterns

**Standard CRUD:**
- **`getById`**: Single record retrieval with error handling
- **`getAll`**: List retrieval with pagination support  
- **`create`**: New record creation with UUID generation
- **`update`**: Record updates with timestamp management
- **`delete`**: Record deletion

**Specialized Handlers:**
- **Progress Methods**: `enrollInPath`, `updateProgress`, `getUserProgress`
- **Achievement Methods**: `getUserAchievements`, `unlockAchievement`
- **Opening Methods**: `searchOpenings`, `getOpeningByEco`
- **Analysis Methods**: `analyzePosition`, `getPositionAnalysis`
- **Tutorial Methods**: `completeTutorial`, `resetTutorial`

**Example Generated Method:**
```typescript
async getEntityById(id: string): Promise<EntityResponse> {
  const result = await this.db.query('SELECT * FROM table_name WHERE id = $1', [id]);
  if (!result.rows.length) throw new Error('Entity not found');
  
  return this.formatEntityResponse(result.rows[0]);
}
```

### Auth Methods (`auth_methods.py`)

**Purpose**: Complete authentication system implementation.

#### Core Auth Methods

- **`register(registerData: any) -> any`**
  - Validates unique email/username
  - Hashes password with bcrypt (12 rounds)
  - Creates user with default ELO ratings
  - Returns formatted user info

- **`login(loginData: any) -> any`**
  - Finds user by email
  - Verifies password with bcrypt
  - Generates JWT token (7-day expiry)
  - Returns user info and token

- **`getCurrentUser(userId: string) -> any`**
  - Retrieves user information
  - Gets or creates user progress record
  - Returns combined user and progress data

- **`updateProfile(userId: string, profileData: any) -> any`**
  - Dynamic field updates
  - Validates required fields
  - Handles JSON preference updates
  - Returns updated user info

- **`changePassword(userId: string, passwordData: any) -> void`**
  - Verifies current password
  - Hashes new password
  - Updates database record

- **`verifyToken(token: string) -> any`**
  - Validates JWT token
  - Returns updated user information
  - Handles token expiration

#### Utility Methods

- **`checkEmailAvailability(emailData: any) -> any`**
- **`checkUsernameAvailability(usernameData: any) -> any`**
- **`forgotPassword(forgotData: any) -> void`** (placeholder for email integration)
- **`resetPassword(resetData: any) -> void`** (placeholder for email integration)
- **`deleteAccount(userId: string) -> void`** (cascading user deletion)

### Puzzle Methods (`puzzle_methods.py`)

**Purpose**: Chess puzzle-specific functionality.

#### Core Puzzle Methods

- **`getNextPuzzle(userId: string) -> any`**
  - Finds appropriate puzzle based on user rating
  - Excludes recently solved puzzles
  - Implements rating-based difficulty matching

- **`solvePuzzle(puzzleId: string, solutionData: any) -> any`**
  - Validates solution moves
  - Updates user progress and rating
  - Records puzzle attempt
  - Returns feedback and rating changes

- **`getPuzzleHint(puzzleId: string) -> any`**
  - Returns progressive hints
  - Tracks hint usage
  - May affect rating calculation

- **`getPuzzleCategories() -> any`**
  - Returns available puzzle themes
  - Includes puzzle counts per category

### Game Methods (`game_methods.py`)

**Purpose**: Chess game management and analysis.

#### Core Game Methods

- **`getGames(userId?: string) -> any`**
  - Returns user's game history
  - Includes game metadata and results

- **`createGame(gameData: any) -> any`**
  - Creates new game record
  - Sets initial position and metadata
  - Handles AI opponent selection

- **`updateGame(gameId: string, updateData: any) -> any`**
  - Updates game state
  - Records moves in PGN format
  - Updates completion status

- **`analyzeGame(gameId: string, analysisData: any) -> any`**
  - Integrates with chess engine analysis
  - Stores analysis results
  - Identifies key positions and blunders

### User Methods (`user_methods.py`)

**Purpose**: User profile and preference management.

#### Core User Methods

- **`getUserProfile(userId: string) -> any`**
- **`updateUserProfile(userId: string, profileData: any) -> any`**
- **`getUserPreferences(userId: string) -> any`**
- **`updateUserPreferences(userId: string, preferences: any) -> any`**

### Learning Path Methods (`learning_path_methods.py`)

**Purpose**: Learning path and tutorial system management.

#### Core Learning Path Methods

- **`getLearningPaths() -> LearningPathResponse[]`**
  - Returns all available learning paths
  - Ordered by creation date
  - Limited to 50 results

- **`getLearningPathById(id: string) -> LearningPathResponse`**
  - Returns specific learning path details
  - Throws error if path not found

- **`enrollInPath(pathId: string, userId: string) -> any`**
  - Enrolls user in a learning path
  - Verifies path exists and user not already enrolled
  - Creates enrollment record with initial progress
  - Returns learning path with enrollment status

- **`updateProgress(pathId: string, userId: string, progressData: any) -> any`**
  - Updates user's progress in learning path
  - Requires existing enrollment
  - Updates progress percentage and timestamp
  - Returns updated learning path with progress

#### Standard CRUD Methods

- **`getAllLearningPaths() -> LearningPathResponse[]`**
- **`createLearningPath(data: CreateLearningPathRequest) -> LearningPathResponse`**
- **`updateLearningPath(id: string, data: UpdateLearningPathRequest) -> LearningPathResponse`**
- **`deleteLearningPath(id: string) -> void`**

---

## Configuration System

The entire backend is driven by the `tools/backend-tools/backend_config.json` file, which defines all entities, their properties, methods, and API endpoints.

### Configuration Structure

```json
{
  "endpoints": {
    "entity-name": {
      "entity": "EntityName",
      "entities": "entity_names",
      "table_name": "database_table",
      "properties": {
        "field_name": "typescript_type"
      },
      "methods": ["method1", "method2"],
      "endpoints": [
        {
          "method": "HTTP_METHOD",
          "path": "/api/path",
          "handler": "methodName",
          "auth_required": boolean
        }
      ]
    }
  },
  "database": {
    "type": "postgresql",
    "connection": { /* connection details */ }
  },
  "generation_options": {
    "overwrite_existing": false,
    "create_tests": true,
    "add_validation": true
  },
  "target_directory": "../backend-v2"
}
```

### Supported Entities

The system currently supports 22+ entities covering:

**Core Entities:**
- `users` - User account management
- `auth` - Authentication system
- `sessions` - Session management

**Chess Functionality:**
- `puzzles` - Chess puzzle system
- `games` - Game management
- `openings` - Opening database
- `endgames` - Endgame training
- `analysis` - Position analysis
- `ai-opponents` - AI opponent configurations

**Learning System:**
- `tutorials` - Interactive tutorials
- `learning` - Learning paths
- `learning-modules` - Individual learning modules
- `learning-paths` - Learning path management (with specialized methods)
- `tutorial-steps` - Tutorial step management

**Progress Tracking:**
- `progress` - User progress tracking
- `achievements` - Achievement system
- `stats` - Statistical data
- `analytics` - User analytics

**Content Management:**
- `historic-games` - Famous game database
- `game-reviews` - Game review system
- `puzzle-attempts` - Puzzle attempt tracking
- `puzzle-sources` - Puzzle source management

**User Features:**
- `profiles` - Extended user profiles
- `study-plans` - Personalized study plans
- `subscriptions` - Subscription management
- `help` - Help system

### Configuration Options

**Entity Configuration:**
- `entity` - Singular entity name (PascalCase)
- `entities` - Plural entity name (snake_case or kebab-case)
- `table_name` - Database table name
- `properties` - Field definitions with TypeScript types
- `methods` - Service methods to generate
- `endpoints` - API endpoint definitions

**Endpoint Configuration:**
- `method` - HTTP method (GET, POST, PUT, DELETE)
- `path` - API endpoint path (supports :param syntax)
- `handler` - Service method name to call
- `auth_required` - Whether authentication is required (default: true)

**Property Types:**
- `string`, `number`, `boolean` - Basic types
- Complex types are handled as JSON strings in the database

---

## Usage Guide

### Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   ```

2. **Configure Backend Path:**
   ```bash
   export BACKEND_PATH="/path/to/your/backend"
   # Or let the system auto-detect
   ```

3. **Generate All Endpoints:**
   ```bash
   cd tools/backend-tools
   python backend_generator_v2.py --all
   ```

4. **Generate Specific Endpoint:**
   ```bash
   cd tools/backend-tools
   python backend_generator_v2.py puzzles
   ```

### Configuration Workflow

1. **Edit `tools/backend-tools/backend_config.json`:**
   ```json
   {
     "endpoints": {
       "my-entity": {
         "entity": "MyEntity",
         "entities": "my_entities",
         "table_name": "my_entities",
         "properties": {
           "id": "string",
           "name": "string",
           "description": "string",
           "created_at": "string"
         },
         "methods": [
           "getAllMyEntities",
           "getMyEntityById",
           "createMyEntity"
         ],
         "endpoints": [
           {
             "method": "GET",
             "path": "/",
             "handler": "getAllMyEntities"
           }
         ]
       }
     }
   }
   ```

2. **Validate Configuration:**
   ```bash
   python backend_generator_v2.py my-entity --dry-run
   ```

3. **Generate Backend:**
   ```bash
   python backend_generator_v2.py my-entity --verbose
   ```

### Advanced Usage

**Environment Variables:**
- `BACKEND_PATH` - Override backend directory
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - JWT signing secret

**Custom Method Generators:**
1. Create new generator in `method_generators/`
2. Extend `BaseMethodGenerator`
3. Implement `generate_method()` 
4. Register in `service_generator.py`

**Configuration Validation:**
- Entity names must be alphanumeric + underscores
- Property names must follow same rules
- Required fields: `entity`, `properties`
- Methods are automatically validated against generators

---

## Advanced Features

### Dry Run Mode

Preview generation without creating files:
```bash
python backend_generator_v2.py --all --dry-run
```

**Benefits:**
- Verify configuration before generation
- Preview file structure and content
- Identify potential conflicts
- Test new configurations safely

### Intelligent Path Detection

The system automatically finds your backend directory:

1. **Environment Variable**: `BACKEND_PATH`
2. **Project Root Detection**: Searches for `.git` or `package.json`
3. **Directory Preference**: `backend-v2` > `backend`
4. **Fallback**: Relative path from generator location

### Database Integration

**PostgreSQL with Supabase Optimization:**
- Connection pooling for high performance
- SSL support for production deployments
- Automatic reconnection on connection termination
- Query retry logic for reliability
- Statement timeout protection

**Query Patterns:**
- Parameterized queries prevent SQL injection
- UUID primary keys for distributed systems
- Automatic timestamp management
- JSON field support for complex data

### Authentication System

**JWT-Based Authentication:**
- 7-day token expiration
- Secure password hashing (bcrypt, 12 rounds)
- Token verification middleware
- Optional authentication support

**User Management:**
- Registration with validation
- Profile updates with dynamic fields
- Password change with current password verification
- Email/username availability checking

### Error Handling

**Service Layer:**
- Consistent error messages
- Database error handling
- Validation error reporting
- Business logic error handling

**Route Layer:**
- Try-catch blocks around all handlers
- Structured error responses
- HTTP status code management
- Request/response logging

### Logging System

**Request/Response Logging:**
- Timestamp-based logs
- HTTP method and path tracking
- Request body and query parameter logging
- Response status and error logging

**Component Logging:**
- Module-specific loggers
- Configurable log levels
- Structured log messages with emojis
- Progress tracking during generation

---

## Best Practices

### Configuration Design

**Entity Naming:**
- Use PascalCase for entity names (`User`, `ChessPuzzle`)
- Use snake_case for plural forms (`users`, `chess_puzzles`)
- Keep table names simple and consistent

**Property Definition:**
- Use TypeScript types consistently
- Avoid complex nested objects (use JSON strings)
- Include standard fields (`id`, `created_at`, `updated_at`)

**Method Organization:**
- Group related methods together
- Use descriptive method names
- Follow naming conventions (`getXById`, `createX`, `updateX`)

### Database Schema Design

**Table Structure:**
- UUID primary keys for distributed systems
- Consistent timestamp columns
- JSON columns for flexible data storage
- Proper indexing on query fields

**Relationships:**
- Use foreign key constraints
- Consider cascade behavior
- Document relationship patterns

### Security Considerations

**Authentication:**
- Strong JWT secrets (use environment variables)
- Appropriate token expiration times
- Secure password hashing parameters
- Input validation on all endpoints

**Database Security:**
- Parameterized queries only
- Connection string security
- SSL/TLS for production
- Connection pooling limits

### Performance Optimization

**Database Connections:**
- Appropriate pool sizing for your workload
- Connection timeout configuration
- Statement timeout protection
- Connection monitoring

**Query Optimization:**
- Limit result sets appropriately
- Use pagination for large datasets
- Index frequently queried columns
- Consider query complexity

### Code Organization

**File Structure:**
- Consistent naming conventions
- Logical directory organization
- Clear import/export patterns
- Documentation in complex areas

**Error Handling:**
- Consistent error response format
- Appropriate HTTP status codes
- Meaningful error messages
- Error logging for debugging

---

## Troubleshooting

### Common Issues

**1. Backend Path Detection Fails**

*Symptoms:* Generator creates files in wrong location

*Solutions:*
```bash
# Set explicit path
export BACKEND_PATH="/path/to/backend"

# Or use command line argument
python backend_generator_v2.py --backend-path /path/to/backend --all
```

**2. Configuration Validation Errors**

*Symptoms:* Validation errors during generation

*Solutions:*
- Check entity names (alphanumeric + underscores only)
- Ensure required fields are present (`entity`, `properties`)
- Validate JSON syntax in configuration file
- Use dry-run mode to identify issues

**3. Database Connection Issues**

*Symptoms:* Generated backend fails to connect to database

*Solutions:*
- Verify `DATABASE_URL` environment variable
- Check PostgreSQL connection parameters
- Ensure database exists and is accessible
- Verify SSL configuration for production

**4. Authentication Middleware Errors**

*Symptoms:* JWT token validation fails

*Solutions:*
- Set `JWT_SECRET` environment variable
- Ensure token format is correct (`Bearer <token>`)
- Check token expiration
- Verify middleware order in routes

**5. Method Generation Issues**

*Symptoms:* Methods not implemented or incorrect

*Solutions:*
- Check method name spelling in configuration
- Verify entity type is recognized by generators
- Add custom methods to generic generator
- Use verbose mode to see generation details

### Debugging Techniques

**Verbose Mode:**
```bash
cd tools/backend-tools
python backend_generator_v2.py --verbose --all
```

**Dry Run Analysis:**
```bash
cd tools/backend-tools
python backend_generator_v2.py entity-name --dry-run
```

**Configuration Validation:**
```bash
cd tools/backend-tools
python -m json.tool backend_config.json
```

**Database Testing:**
```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

### Log Analysis

**Generator Logs:**
- Look for emoji indicators (🚀, ✅, ❌)
- Check file creation messages
- Monitor validation warnings
- Track generation progress

**Backend Logs:**
- Request/response logging
- Database connection events
- Authentication attempts
- Error stack traces

---

## Extension Guide

### Adding Custom Entities

1. **Update Configuration:**
   ```json
   {
     "endpoints": {
       "custom-entity": {
         "entity": "CustomEntity",
         "entities": "custom_entities",
         "table_name": "custom_entities",
         "properties": {
           "id": "string",
           "custom_field": "string"
         },
         "methods": ["getCustomEntity", "createCustomEntity"],
         "endpoints": [
           {
             "method": "GET",
             "path": "/:id",
             "handler": "getCustomEntity"
           }
         ]
       }
     }
   }
   ```

2. **Generate Entity:**
   ```bash
   cd tools/backend-tools
   python backend_generator_v2.py custom-entity
   ```

### Creating Custom Method Generators

1. **Create Generator File:**
   ```python
   # method_generators/custom_methods.py
   from base_generator import BaseMethodGenerator

   class CustomMethodGenerator(BaseMethodGenerator):
       def generate_method(self, method_name: str, entity_upper: str, 
                         entity_lower: str, table_name: str) -> str:
           if method_name == "customMethod":
               return f'''  async {method_name}(): Promise<any> {{
                   // Custom implementation
                   return {{ message: "Custom method implemented" }};
               }}'''
           
           return self._create_stub_method(method_name)
   ```

2. **Register Generator:**
   ```python
   # In service_generator.py
   from custom_methods import CustomMethodGenerator

   # Add to generator selection logic
   elif 'custom' in entity_lower:
       generator = CustomMethodGenerator()
   ```

### Adding Custom Middleware

1. **Create Middleware File:**
   ```typescript
   // src/middleware/custom.ts
   import { Request, Response, NextFunction } from 'express';

   export const customMiddleware = (req: Request, res: Response, next: NextFunction) => {
       // Custom logic
       next();
   };
   ```

2. **Register in Routes:**
   ```typescript
   // In generated route file
   import { customMiddleware } from '../middleware/custom';

   router.get('/custom', customMiddleware, async (req, res) => {
       // Handler logic
   });
   ```

### Extending Database Utilities

1. **Add Utility Functions:**
   ```typescript
   // In src/utils/database.ts
   export class Database {
       // ... existing methods

       async transaction(callback: (client: any) => Promise<void>) {
           const client = await this.pool.connect();
           try {
               await client.query('BEGIN');
               await callback(client);
               await client.query('COMMIT');
           } catch (error) {
               await client.query('ROLLBACK');
               throw error;
           } finally {
               client.release();
           }
       }
   }
   ```

### Custom Validation Rules

1. **Extend Validation Middleware:**
   ```typescript
   // src/middleware/validation.ts
   import { body, param } from 'express-validator';

   export const validateCustomEntity = [
       body('custom_field').isLength({ min: 1 }).withMessage('Custom field required'),
       body('email').isEmail().withMessage('Valid email required'),
       validate
   ];
   ```

2. **Use in Routes:**
   ```typescript
   // In route file
   import { validateCustomEntity } from '../middleware/validation';

   router.post('/', authenticate, validateCustomEntity, async (req, res) => {
       // Handler with validation
   });
   ```

### Performance Monitoring

1. **Add Monitoring Middleware:**
   ```typescript
   // src/middleware/monitoring.ts
   export const performanceMonitoring = (req: Request, res: Response, next: NextFunction) => {
       const start = Date.now();
       
       res.on('finish', () => {
           const duration = Date.now() - start;
           console.log(`${req.method} ${req.path} - ${duration}ms`);
       });
       
       next();
   };
   ```

---

## Conclusion

The Backend Generator v2 is a powerful, extensible system that transforms configuration into production-ready backends. Its modular architecture makes it easy to understand, maintain, and extend for specific needs.

**Key Strengths:**
- **Configuration-Driven**: Easy to modify and extend
- **Type-Safe**: Complete TypeScript integration
- **Production-Ready**: Authentication, validation, error handling
- **Extensible**: Plugin-based architecture for customization
- **Comprehensive**: Covers all aspects of backend development

**Best Use Cases:**
- Rapid prototyping of backend APIs
- Consistent code generation across teams
- Educational projects requiring complete backends
- Chess applications with complex entity relationships
- Any project needing standardized CRUD operations

The system continues to evolve with new features and improvements, making it an invaluable tool for modern web application development.