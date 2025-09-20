# Integration Orchestrator

The Integration Orchestrator is a command-line tool for testing and running the specialized integration modules for mobile-pages-v2.

## Specialized Modules

The system includes four specialized modules following SRP (Single Responsibility Principle):

1. **ActionRegistryManager** - Handles PAGE_ACTIONS and COMMON_ACTIONS registry integration
2. **ContainerIntegrator** - Manages ActionSheetContainer system integration  
3. **HookIntegrator** - Generates functional hooks with real navigation methods
4. **IntegrationValidator** - Provides comprehensive validation across all modules

## Quick Start

### Check Integration Status
```bash
python integration_orchestrator.py status /path/to/frontend
```

### Validate Complete Project
```bash
python integration_orchestrator.py validate /path/to/frontend
```

### Integrate a Specific Page
```bash
python integration_orchestrator.py integrate /path/to/frontend settings
```

### Run Full Test Suite
```bash
python integration_orchestrator.py test /path/to/frontend
```

### Fix Integration Issues
```bash
# Fix specific page
python integration_orchestrator.py fix /path/to/frontend dashboard

# Fix entire project
python integration_orchestrator.py fix /path/to/frontend
```

## All Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `status` | Show integration status summary | `status <frontend_root>` |
| `validate` | Validate complete project integration | `validate <frontend_root>` |
| `validate-page` | Validate specific page integration | `validate-page <frontend_root> <page_id>` |
| `integrate` | Integrate specific page (auto-detects parent/child) | `integrate <frontend_root> <page_id>` |
| `fix` | Fix integration issues | `fix <frontend_root> [page_id]` |
| `test` | Run comprehensive integration tests | `test <frontend_root>` |

## Configuration-Driven

All modules use `pages.config.json` as the single source of truth for:
- Page relationships (parent/child)
- Sibling navigation generation  
- Hook method creation
- Registry integration

## Test Suite

### Run All Tests
```bash
python run_tests.py
```

### Run Unit Tests Only
```bash
python -m pytest tests/ -v
```

### Run Integration Tests Only
```bash
python integration_orchestrator.py test /path/to/frontend
```

## Integration Workflow

When integrating a page, the orchestrator automatically:

### For Parent Pages:
1. Registers parent actions in PAGE_ACTIONS registry
2. Integrates with ActionSheetContainer system
3. Generates functional parent hook with navigation methods
4. Processes all child pages (if any exist)

### For Child Pages:
1. Registers child actions with `mergeWithCommonActions()`
2. Adds sibling navigation to COMMON_ACTIONS
3. Integrates with ActionSheetContainer system
4. Generates functional child hooks with sibling navigation

### Validation:
1. Checks registry integration
2. Validates container connections
3. Verifies functional hooks (no placeholder code)
4. Cross-validates relationships between modules

## Benefits

- **No Hardcoded Values**: Everything driven by configuration
- **Comprehensive Testing**: Unit tests + integration tests
- **Automatic Issue Detection**: Detailed validation reporting
- **Issue Resolution**: Automatic fixing capabilities  
- **Modular Design**: Each module handles single responsibility
- **Config-Driven**: Uses pages.config.json as source of truth

## Example Output

```bash
$ python integration_orchestrator.py status /path/to/frontend

🚀 Integration Orchestrator initialized for: /path/to/frontend
============================================================
📊 INTEGRATION STATUS SUMMARY
============================================================
📋 Project Overview:
  Total pages: 3
  Parent pages: 1
  Child pages: 2

📁 Critical Files:
  ✅ pages.config.json: pages.config.json
  ✅ PAGE_ACTIONS: src/constants/actions/page-actions.constants.ts
  ✅ COMMON_ACTIONS: src/constants/actions/common-actions.constants.ts
  ✅ ActionSheetContainer: src/components/shared/ActionSheetContainer.tsx

🔍 Quick Validation:
  ✅ Integration status: COMPLETE
```