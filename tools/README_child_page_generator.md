# Child Page Generator Tool

A Python automation tool that generates child pages and all associated files for the responsive chessboard application, following the architecture patterns documented in `docs/47-navigation-action-sheets-architecture.md`.

## Features

✅ **Complete Automation**: Creates all files needed for child pages  
✅ **Pattern Following**: Follows exact conventions from existing codebase  
✅ **File Updates**: Automatically updates existing files with new mappings  
✅ **Type Safety**: Generates TypeScript code with proper typing  
✅ **Instructions**: Creates instruction files and service mappings  
✅ **Validation**: Checks for required paths and dependencies  

## What It Creates

### New Files Generated:
- `src/pages/{parent}/{ChildPage}.tsx` - Main child page component
- `src/components/{ChildPageWrapper}.tsx` - Wrapper with context hooks
- `src/hooks/use{Child}Actions.ts` - Actions hook for the child page
- `src/services/instructions/pages/{child}.instructions.ts` - Instructions file

### Files Updated:
- `src/constants/actions/page-actions.constants.ts` - Adds child page actions
- `src/hooks/use{Parent}Actions.ts` - Adds navigation functions
- `src/components/action-sheet/ActionSheetContainer.tsx` - Adds action mappings
- `src/pages/{parent}/{Parent}Page.tsx` - Adds routing logic
- `src/services/instructions/InstructionsService.ts` - Registers instructions

## Usage

### Basic Usage
```bash
python child_page_generator.py --parent uitests --children "newtest,anothertest"
```

### With Custom Actions
```bash
python child_page_generator.py \
  --parent uitests \
  --children "performancetest,memorytest" \
  --actions "run-test:Run Test:Play:default,clear-results:Clear Results:Trash2:secondary,export-data:Export Data:Download:default"
```

### Advanced Usage
```bash
python child_page_generator.py \
  --parent splash \
  --children "customsplash" \
  --actions "test-animation:Test Animation:Zap:default,restart:Restart:RotateCcw:secondary" \
  --base-path "/custom/path/to/project"
```

## Action Format

Actions are specified as comma-separated strings in the format:
```
id:label:icon:variant
```

**Example:**
```
test-action:Test Action:TestTube:default,clear-data:Clear Data:Trash2:destructive
```

### Valid Variants:
- `default` - Primary action styling
- `secondary` - Secondary action styling  
- `destructive` - Red/warning action styling

### Common Icons:
Use Lucide React icon names: `TestTube`, `Navigation`, `Settings`, `Play`, `Pause`, `RotateCcw`, `Trash2`, `Download`, `Upload`, `Eye`, `Volume2`, etc.

## Examples

### Create UI Test Pages
```bash
python child_page_generator.py \
  --parent uitests \
  --children "apitest,performancetest" \
  --actions "run-api-test:Run API Test:Globe:default,test-performance:Test Performance:Zap:default,clear-results:Clear Results:Trash2:secondary"
```

This creates:
- API Test child page with wrapper and actions
- Performance Test child page with wrapper and actions  
- Navigation actions in UI Tests parent
- All necessary file updates and mappings

### Create Splash Variations
```bash
python child_page_generator.py \
  --parent splash \
  --children "holidaysplash,themesplash" \
  --actions "change-theme:Change Theme:Palette:default,save-theme:Save Theme:Save:secondary"
```

### Create Game Mode Pages
```bash
python child_page_generator.py \
  --parent play \
  --children "tournamentmode,practicemode" \
  --actions "start-tournament:Start Tournament:Trophy:default,join-game:Join Game:Users:secondary,leave-game:Leave Game:LogOut:destructive"
```

## Generated File Structure

```
src/
├── pages/{parent}/
│   ├── {Child}Page.tsx              # ✨ New
│   └── {Parent}Page.tsx             # 🔧 Updated
├── components/
│   └── {Child}PageWrapper.tsx       # ✨ New
├── hooks/
│   ├── use{Child}Actions.ts         # ✨ New
│   └── use{Parent}Actions.ts        # 🔧 Updated
├── constants/actions/
│   └── page-actions.constants.ts    # 🔧 Updated
├── components/action-sheet/
│   └── ActionSheetContainer.tsx     # 🔧 Updated
└── services/instructions/
    ├── pages/{child}.instructions.ts # ✨ New
    └── InstructionsService.ts       # 🔧 Updated
```

## Validation & Safety

The tool includes several safety features:

1. **Path Validation**: Checks that all required project paths exist
2. **Duplicate Detection**: Won't overwrite existing pages or duplicate actions  
3. **Pattern Matching**: Uses regex to safely update existing files
4. **Error Handling**: Provides clear error messages and warnings
5. **Backup Recommended**: Always backup your project before running

## Troubleshooting

### Tool Won't Run
```bash
# Check Python version (requires 3.6+)
python --version

# Check if you're in the right directory
ls tools/child_page_generator.py
```

### Missing Required Paths
```
❌ Required path not found: /path/to/src/constants/actions/page-actions.constants.ts
```
- Ensure you're running from the project root
- Check the `--base-path` parameter
- Verify project structure matches expected layout

### Import Issues After Generation
- Check that all imports are correct in generated files
- Run TypeScript compiler to check for errors
- Verify icon names are valid Lucide React icons

### Action Mapping Not Working  
- Check ActionSheetContainer.tsx was updated correctly
- Verify hook names match the generated pattern
- Ensure parent actions hook exports the navigation functions

## Integration with Development Workflow

### After Running the Tool:

1. **Review Generated Files**: Check that components match your needs
2. **Implement Logic**: Add specific functionality to action hooks
3. **Test Navigation**: Verify parent → child → parent navigation works
4. **Update Instructions**: Customize the generated instruction content
5. **Add Styling**: Apply any specific CSS classes or styling
6. **Test Actions**: Ensure all action sheet buttons work correctly

### Recommended Workflow:
```bash
# 1. Generate pages
python tools/child_page_generator.py --parent uitests --children "newtest"

# 2. Start development server  
npm run dev

# 3. Test navigation and actions
# 4. Customize generated components
# 5. Run linting/type checking
npm run lint
npm run typecheck
```

## Extending the Tool

The tool is designed to be extensible. You can modify it to:

- Add custom component templates
- Generate additional file types
- Support different parent page structures  
- Add custom validation rules
- Generate tests alongside components

## Support

For issues or questions:
1. Check the main architecture documentation: `docs/47-navigation-action-sheets-architecture.md`
2. Review the quick guide: `docs/47.1-adding-child-pages-quick-guide.md`
3. Examine existing child pages for patterns: `src/components/DragTestPageWrapper.tsx`