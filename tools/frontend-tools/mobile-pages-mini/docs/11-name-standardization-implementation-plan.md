# Document 11: Name Standardization Implementation Plan

## Overview
This document outlines the implementation plan for centralizing name standardization/sanitization across all generator modules to ensure consistent naming conventions and prevent cascading casing issues throughout the generation pipeline.

## Problem Statement
Currently identified during build error analysis, the system suffers from inconsistent naming across different generators:

### Current Issues
1. **Hook Import/Export Mismatches**: `useTestcenterActions` vs `useTestCenterActions`
2. **File Casing Conflicts**: `useGameCenterActions.ts` vs `useGamecenterActions.ts`  
3. **Component Casing Mismatches**: `PlayareaPageWrapper` vs `PlayAreaPageWrapper`
4. **Directory vs Class Name Inconsistencies**: lowercase directories but PascalCase classes

### Root Cause
Each generator module (VariableGenerator, NavigationGenerator, ParentGenerator, etc.) implements its own ad-hoc name transformations without a centralized standard, leading to:
- Inconsistent PascalCase conversion logic
- Different handling of compound words (GameCenter vs gamecenter)
- File path vs import name mismatches
- Hook name vs hook file name conflicts

## Implementation Plan

### Phase 1: Create Centralized Name Standardizer

#### 1.1 Create `NameStandardizer` Class
**Location**: `/tools/frontend-tools/shared/name_standardizer.py`

```python
class NameStandardizer:
    """Centralized name standardization for all generators"""
    
    @staticmethod
    def to_pascal_case(name: str) -> str:
        """Convert any name format to PascalCase"""
    
    @staticmethod  
    def to_camel_case(name: str) -> str:
        """Convert any name format to camelCase"""
        
    @staticmethod
    def to_kebab_case(name: str) -> str:
        """Convert any name format to kebab-case"""
        
    @staticmethod
    def to_snake_case(name: str) -> str:
        """Convert any name format to snake_case"""
        
    @staticmethod
    def to_directory_name(name: str) -> str:
        """Convert to directory-safe lowercase format"""
        
    @staticmethod
    def to_file_name(name: str, suffix: str = "") -> str:
        """Convert to filename with proper casing"""
        
    @staticmethod
    def to_component_name(name: str) -> str:
        """Convert to React component name (PascalCase + suffix)"""
        
    @staticmethod
    def to_hook_name(name: str, action_type: str = "Actions") -> str:
        """Convert to React hook name (use + PascalCase + suffix)"""
        
    @staticmethod
    def to_constant_name(name: str) -> str:
        """Convert to CONSTANT_CASE for constants"""
```

#### 1.2 Standardized Naming Rules
- **Page IDs**: Always lowercase, no spaces/special chars (e.g., `"gamecenter"`)
- **Directory Names**: Always lowercase, match page IDs (e.g., `src/pages/gamecenter/`)  
- **Component Names**: Always PascalCase + "Page" suffix (e.g., `"GameCenterPage"`)
- **Hook Names**: Always "use" + PascalCase + "Actions" (e.g., `"useGameCenterActions"`)
- **File Names**: Match component names exactly (e.g., `GameCenterPage.tsx`)
- **Import Paths**: Use lowercase directories with PascalCase filenames

### Phase 2: Refactor Existing Generators

#### 2.1 Update PageConfigManager
- Replace all ad-hoc name transformations with NameStandardizer calls
- Ensure consistent storage of standardized names in pages.config.json
- Add validation to reject non-conforming names

#### 2.2 Update VariableGenerator  
- Replace line 323-324 PascalCase logic with `NameStandardizer.to_pascal_case()`
- Fix hook import path generation using standardized names
- Ensure hook file names match import names exactly

#### 2.3 Update NavigationGenerator
- Replace `_to_pascal_case()` method with `NameStandardizer.to_pascal_case()`
- Ensure page imports use standardized component names
- Fix page routing generation with consistent casing

#### 2.4 Update ParentGenerator & ChildGenerator
- Standardize all component name generation
- Ensure file names match import names
- Fix wrapper component naming consistency

### Phase 3: Add Comprehensive Testing

#### 3.1 Unit Tests for NameStandardizer
```python
def test_pascal_case_conversion():
    assert NameStandardizer.to_pascal_case("game center") == "GameCenter"
    assert NameStandardizer.to_pascal_case("gamecenter") == "GameCenter"  
    assert NameStandardizer.to_pascal_case("gameCenter") == "GameCenter"

def test_hook_name_generation():
    assert NameStandardizer.to_hook_name("gamecenter") == "useGameCenterActions"
    assert NameStandardizer.to_hook_name("test center") == "useTestCenterActions"
```

#### 3.2 Integration Tests
- Test full page generation pipeline with standardized names
- Verify TypeScript compilation success
- Ensure import/export consistency

### Phase 4: Migration Strategy

#### 4.1 Backward Compatibility
- Add migration utilities to update existing configs
- Provide warning messages for deprecated name formats
- Gradual rollout with fallback support

#### 4.2 Documentation Updates
- Update all generator documentation with new naming standards
- Create naming convention guide for developers
- Add troubleshooting guide for naming conflicts

## Expected Benefits

### 1. Consistency
- All generators will produce identical naming for identical inputs
- No more casing mismatches between modules
- Predictable file structure and imports

### 2. Maintainability  
- Single source of truth for name transformations
- Easy to update naming rules globally
- Reduced debugging of casing issues

### 3. Developer Experience
- Clear, documented naming conventions
- Fewer TypeScript compilation errors
- More predictable generated code structure

### 4. Reliability
- Comprehensive test coverage for all name transformations
- Validation of naming consistency across pipeline
- Prevention of runtime import errors

## Implementation Priority

### High Priority (Immediate)
1. Create NameStandardizer class with core methods
2. Fix VariableGenerator hook naming issues
3. Update NavigationGenerator for consistent App.tsx generation

### Medium Priority (Next Sprint)
1. Refactor all generators to use NameStandardizer  
2. Add comprehensive unit tests
3. Create migration utilities

### Low Priority (Future)
1. Advanced naming features (custom prefixes/suffixes)
2. Integration with external naming standards
3. Performance optimizations

## Migration Notes

### Current State Analysis
From build error analysis, the following inconsistencies need immediate attention:
- Hook imports: `useTestcenterActions` → `useTestCenterActions`
- Component imports: `PlayareaPageWrapper` → `PlayAreaPageWrapper`
- File casing conflicts between generated files and imports

### Rollout Strategy
1. **Phase 1**: Fix critical build errors with minimal NameStandardizer implementation
2. **Phase 2**: Gradually migrate all generators  
3. **Phase 3**: Add comprehensive testing and validation
4. **Phase 4**: Full enforcement with migration utilities

This approach ensures we can fix immediate build issues while laying groundwork for long-term naming consistency.

## Mobile Pages Mini: Modules Requiring NameStandardizer Integration

Focus only on modules actually used by the mobile-pages-mini tool to fix current build issues:

### 🔥 **Critical Priority - Mobile Pages Mini Dependencies**

#### Core Mobile Pages Mini Modules
- **`mobile-pages-mini/modules/variable_generator.py`**
  - Line 324: `''.join(word.capitalize() for word in page_name.lower().split())`
  - Replace with: `NameStandardizer.to_pascal_case(page_name)`
  - Impact: Fixes hook naming (`useTestcenterActions` → `useTestCenterActions`)

- **`mobile-pages-mini/modules/config.py`**
  - Line 23-25: `_to_pascal_case()` method
  - Line 27: Custom PascalCase logic
  - Replace with: `NameStandardizer.to_pascal_case()`

- **`mobile-pages-mini/modules/hook_integrator.py`**
  - Line 216: `_to_pascal_case()` method  
  - Multiple calls throughout (lines 164, 225, 232, 239, 247, 300, 309, 409)
  - Replace with: `NameStandardizer.to_pascal_case()`

#### Shared Dependencies (Used by Mobile Pages Mini)
- **`shared/navigation_generator.py`**
  - Line 228: `self._to_pascal_case(page.component_name)`
  - Line 233-235: `_to_pascal_case()` method
  - Line 244: `self._to_pascal_case(page.component_name)`
  - Replace with: `NameStandardizer.to_pascal_case()`
  - Impact: Fixes App.tsx component import consistency

- **`shared/page_config_manager.py`**
  - Component name handling in page configuration
  - Standardize component naming through NameStandardizer

### 📋 **Implementation Checklist - Mobile Pages Mini Only**

#### Phase 1: Fix Current Build Issues
- [ ] Update `mobile-pages-mini/modules/variable_generator.py` line 324
- [ ] Replace `mobile-pages-mini/modules/config.py` `_to_pascal_case()` method
- [ ] Replace `mobile-pages-mini/modules/hook_integrator.py` `_to_pascal_case()` method
- [ ] Update `shared/navigation_generator.py` `_to_pascal_case()` method
- [ ] Update `shared/page_config_manager.py` component naming

### 🎯 **Expected Impact - Mobile Pages Mini**

**Immediate Benefits:**
- ✅ Fixes compound word issues: `"testcenter"` → `"TestCenter"` (not `"Testcenter"`)
- ✅ Eliminates hook import/export mismatches (`useTestcenterActions` → `useTestCenterActions`)
- ✅ Prevents component naming conflicts (`PlayareaPageWrapper` → `PlayAreaPageWrapper`)
- ✅ Enables successful TypeScript compilation

**Long-term Benefits:**
- Single source of truth for name transformations within mobile-pages-mini
- Consistent behavior with shared modules
- Foundation for future NameStandardizer expansion to other tools

### 🧪 **Testing Strategy - Mobile Pages Mini**

Focus on modules that mobile-pages-mini actually uses:
1. **Before/After comparison tests** - Verify NameStandardizer produces correct results for mobile-pages-mini naming
2. **Build tests** - Ensure TypeScript compilation succeeds after changes
3. **Integration tests** - Test mobile-pages-mini + shared modules work together
4. **Regression tests** - Confirm existing mobile-pages-mini functionality works

This focused approach fixes the immediate build issues while laying groundwork for broader NameStandardizer adoption.