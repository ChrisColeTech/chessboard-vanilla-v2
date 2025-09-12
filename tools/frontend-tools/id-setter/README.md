# ID Setter CLI Tool

Automatically adds meaningful IDs to React components and interactive elements.

## Features

- **Smart Detection**: Finds interactive elements (buttons, links, inputs, etc.) that need IDs
- **Meaningful Names**: Generates descriptive IDs based on element purpose and context
- **Page-Aware**: Uses page context to create more specific IDs (e.g., `game-settings-btn` vs `menu-settings-btn`)
- **Safe Processing**: Dry-run mode to preview changes before applying
- **Modular Design**: Clean separation of concerns for easy maintenance

## Usage

```bash
# Process entire src directory
python main.py

# Dry run to preview changes
python main.py --dry-run

# Process specific component
python main.py --component components/TabBar.tsx

# Add page context for better ID naming
python main.py --page game --component components/GameControls.tsx

# Custom source directory
python main.py --src /path/to/react/src
```

## Examples

**Before:**
```jsx
<button className="tab-button tab-button-active" onClick={handleClick}>
  Settings
</button>
```

**After:**
```jsx
<button id="tab-settings-btn" className="tab-button tab-button-active" onClick={handleClick}>
  Settings
</button>
```

**With page context (`--page game`):**
```jsx
<button id="game-tab-settings-btn" className="tab-button tab-button-active" onClick={handleClick}>
  Settings
</button>
```

## Modules

- **`html_parser.py`**: Finds interactive elements in React/JSX files
- **`id_generator.py`**: Creates meaningful IDs based on element purpose and context
- **`file_processor.py`**: Updates files with generated IDs
- **`main.py`**: CLI interface

## ID Generation Logic

1. **Page Context**: Uses `--page` argument (game, settings, menu, etc.)
2. **Component Name**: Extracts from filename (TabBar.tsx → tab-bar)
3. **Element Purpose**: Analyzes text content and attributes
   - "Save" button → `save-btn`
   - "Cancel" button → `cancel-btn`
   - Tab with "active" class → `active-tab`
4. **Uniqueness**: Adds numbers if needed (`save-btn-2`)

## Supported Elements

- **Buttons**: `<button>`, elements with `onClick`, `.button` class
- **Links**: `<a>` tags
- **Inputs**: `<input>`, `<textarea>`, `<select>`
- **Interactive**: Elements with event handlers or interactive classes