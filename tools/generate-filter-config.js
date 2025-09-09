#!/usr/bin/env node

/**
 * Filter Configuration Generator
 *
 * Reads CSS theme and filter files to automatically generate a configuration
 * that maps themes to appropriate filters for different chess game states.
 */

const fs = require("fs");
const path = require("path");

// Paths to CSS files (relative to project root)
const THEMES_PROFESSIONAL_PATH =
  "../src/styles/organized_themes/themes-professional.css";
const THEMES_GAMING_PATH = "../src/styles/organized_themes/themes-gaming.css";
const CHESS_FILTERS_PATH = "../src/styles/organized_themes/chess-filters.css";

// Output configuration file path
const OUTPUT_PATH = "../src/constants/chess/filter-config.constants.ts";

/**
 * Parse CSS file to extract theme class names
 */
function parseThemes(cssContent) {
  // Match theme class definitions: .theme-name { or .theme-name.dark {
  const themeRegex = /\.theme-([a-z-]+)(?:\.dark)?\s*{/g;
  const themes = new Set();

  let match;
  while ((match = themeRegex.exec(cssContent)) !== null) {
    themes.add(`theme-${match[1]}`);
  }

  return Array.from(themes).sort();
}

/**
 * Parse CSS file to extract filter class names
 */
function parseFilters(cssContent) {
  // Match various filter class patterns
  const filterRegexes = [
    /\.chess-square\.([a-z-]+)\s*{/g, // .chess-square.filter-name {
    /\.chess-dark-square\.([a-z-]+)\s*{/g, // .chess-dark-square.filter-name {
    /\.chess-light-square\.([a-z-]+)\s*{/g, // .chess-light-square.filter-name {
  ];

  const filters = new Set();

  // Game state filters to skip (we want visual effect filters)
  const gameStateFilters = [
    "selected",
    "king-in-check",
    "checkmate",
    "last-move",
    "valid-move",
    "capture-target",
    "under-attack",
    "promotion",
    "en-passant",
    "castling",
  ];

  filterRegexes.forEach((regex) => {
    let match;
    while ((match = regex.exec(cssContent)) !== null) {
      const filterName = match[1];
      if (!gameStateFilters.includes(filterName)) {
        filters.add(filterName);
      }
    }
  });

  // Also look for comments that describe filters (for comprehensive list)
  const commentRegex = /\/\*\s*\d+\.\s*([A-Za-z\s]+?)\s*\*\//g;
  let commentMatch;
  while ((commentMatch = commentRegex.exec(cssContent)) !== null) {
    const description = commentMatch[1].toLowerCase();
    // Convert descriptions to likely class names
    const className = description
      .replace(/\s+/g, "-")
      .replace(/[^a-z-]/g, "")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "");

    // Add some manual mappings for tricky cases
    const manualMappings = {
      "neon-glow-gaming": "neon-glow",
      "vintage-sepia-tone": "vintage",
      "high-contrast-gaming": "high-contrast",
      "cyberpunk-hue-shift": "cyberpunk",
      "frosted-glass-blur": "frosted",
      "holographic-iridescent": "holographic",
      "retro-game-invert": "retro-invert",
      "soft-shadow-depth": "soft-depth",
      "matrix-code-green": "matrix",
      "noir-black-white": "noir",
      "animated-shimmer": "shimmer",
      "gaming-rgb-pulse": "rgb-pulse",
      "luxury-gold-metallic": "luxury-gold",
      "accessibility-high-visibility": "high-visibility",
    };

    if (manualMappings[className]) {
      filters.add(manualMappings[className]);
    }
  }

  return Array.from(filters).sort();
}

/**
 * Create smart mappings between themes and filters
 */
function createSmartMappings(themes, filters) {
  const mappings = {};

  // Track which themes and filters have been matched
  const matchedThemes = new Set();
  const usedFilters = new Set();

  // Game states that need filter effects
  const states = ["selected", "valid-move"];

  console.log("🎯 Phase 1: Finding direct and semantic matches...");

  // PHASE 1: Find direct and semantic matches first
  themes.forEach((theme) => {
    const themeName = theme.replace("theme-", "");
    let selectedFilter = null;

    // Strategy 1: Direct name matching (highest priority)
    if (filters.includes(themeName)) {
      selectedFilter = themeName;
      console.log(`   ✓ Direct match: ${theme} → ${selectedFilter}`);
    }
    // Strategy 2: Semantic matching based on theme name
    else if (themeName.includes("matrix") && filters.includes("matrix")) {
      selectedFilter = "matrix";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    } else if (themeName.includes("neon") && filters.includes("neon-glow")) {
      selectedFilter = "neon-glow";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    } else if (themeName.includes("cyber") && filters.includes("cyberpunk")) {
      selectedFilter = "cyberpunk";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    } else if (themeName.includes("shadow") && filters.includes("noir")) {
      selectedFilter = "noir";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    } else if (
      (themeName.includes("royal") || themeName.includes("violet")) &&
      filters.includes("holographic")
    ) {
      selectedFilter = "holographic";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    } else if (
      (themeName.includes("gold") ||
        themeName.includes("bronze") ||
        themeName.includes("copper")) &&
      filters.includes("luxury-gold")
    ) {
      selectedFilter = "luxury-gold";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    } else if (themeName.includes("dragon") && filters.includes("shimmer")) {
      selectedFilter = "shimmer";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    } else if (themeName.includes("forest") && filters.includes("soft-depth")) {
      selectedFilter = "soft-depth";
      console.log(`   ✓ Semantic match: ${theme} → ${selectedFilter}`);
    }

    if (selectedFilter) {
      matchedThemes.add(theme);
      usedFilters.add(selectedFilter);

      // Create complementary filter for valid-move state
      const complementaryMap = {
        matrix: "cyberpunk",
        "neon-glow": "rgb-pulse",
        cyberpunk: "holographic",
        noir: "high-contrast",
        holographic: "shimmer",
        "luxury-gold": "glassmorphism",
        shimmer: "vintage",
        "soft-depth": "frosted",
      };

      const validMoveFilter = complementaryMap[selectedFilter];
      if (validMoveFilter && filters.includes(validMoveFilter)) {
        usedFilters.add(validMoveFilter);
      }

      mappings[theme] = {
        selected: selectedFilter,
        "valid-move": validMoveFilter || selectedFilter,
      };
    }
  });

  console.log(`   Found ${matchedThemes.size} semantic matches`);

  // PHASE 2: Distribute unmatched filters to unmatched themes one-by-one
  const unmatchedThemes = themes.filter((theme) => !matchedThemes.has(theme));
  const unmatchedFilters = filters.filter((filter) => !usedFilters.has(filter));

  console.log("🎯 Phase 2: Distributing unmatched filters...");
  console.log(`   Unmatched themes: ${unmatchedThemes.length}`);
  console.log(`   Unmatched filters: ${unmatchedFilters.length}`);

  // Create filter pools for smart assignment
  const dramaticFilters = ["rgb-pulse", "retro-invert", "high-contrast"].filter(
    (f) => unmatchedFilters.includes(f)
  );
  const subtleFilters = ["glassmorphism", "frosted", "vintage"].filter((f) =>
    unmatchedFilters.includes(f)
  );
  const specialFilters = ["high-visibility"].filter((f) =>
    unmatchedFilters.includes(f)
  );

  let filterIndex = 0;

  unmatchedThemes.forEach((theme, themeIndex) => {
    const themeName = theme.replace("theme-", "");

    // Determine if this is a gaming theme
    const isGamingTheme = [
      "cyber-neon",
      "dragon-gold",
      "shadow-knight",
      "forest-mystique",
      "royal-purple",
    ].some((g) => themeName.includes(g));

    let selectedFilter = null;
    let validMoveFilter = null;

    // Assign filters from appropriate pools, cycling through available ones
    if (isGamingTheme && dramaticFilters.length > 0) {
      selectedFilter = dramaticFilters[filterIndex % dramaticFilters.length];
      console.log(`   🎮 Gaming theme ${theme} → ${selectedFilter} (dramatic)`);
    } else if (subtleFilters.length > 0) {
      selectedFilter = subtleFilters[filterIndex % subtleFilters.length];
      console.log(
        `   💼 Professional theme ${theme} → ${selectedFilter} (subtle)`
      );
    } else if (specialFilters.length > 0) {
      selectedFilter = specialFilters[filterIndex % specialFilters.length];
      console.log(`   ⭐ Special theme ${theme} → ${selectedFilter} (special)`);
    }

    // For valid-move, try to use a different filter from the remaining pool
    const remainingFilters = unmatchedFilters.filter(
      (f) => f !== selectedFilter
    );
    if (remainingFilters.length > 0) {
      validMoveFilter =
        remainingFilters[(filterIndex + 1) % remainingFilters.length];
    } else {
      validMoveFilter = selectedFilter; // Fallback to same filter
    }

    if (selectedFilter) {
      mappings[theme] = {
        selected: selectedFilter,
        "valid-move": validMoveFilter,
      };

      filterIndex++;
    }
  });

  console.log(`   Distributed ${filterIndex} additional themes\n`);

  return mappings;
}

/**
 * Generate TypeScript configuration file content
 */
function generateConfigFile(themes, filters, mappings) {
  return `/**
 * Auto-generated Filter Configuration
 * 
 * This file maps chess themes to visual filter effects for different game states.
 * 
 * Generated on: ${new Date().toISOString()}
 * 
 * Themes found: ${themes.length}
 * Filters found: ${filters.length}
 */

// Available visual effect filters from chess-filters.css
export const AVAILABLE_FILTERS = [
${filters.map((filter) => `  '${filter}'`).join(",\n")}
] as const;

// Available themes from theme CSS files
export const AVAILABLE_THEMES = [
${themes.map((theme) => `  '${theme}'`).join(",\n")}
] as const;

// Game states that can trigger filter effects
export const FILTER_STATES = [
  'selected',
  'king-in-check',
  'valid-move', 
  'checkmate',
  'last-move',
  'capture-target',
  'under-attack',
  'promotion'
] as const;

// Theme to filter mappings for different game states
export const THEME_FILTER_CONFIG: Record<string, Partial<Record<typeof FILTER_STATES[number], typeof AVAILABLE_FILTERS[number]>>> = {
${Object.entries(mappings)
  .map(([theme, states]) => {
    const stateEntries = Object.entries(states)
      .map(([state, filter]) => `    '${state}': '${filter}'`)
      .join(",\n");
    return `  '${theme}': {\n${stateEntries}\n  }`;
  })
  .join(",\n")}
};

/**
 * Get the appropriate filter for a theme and game state
 */
export function getThemeFilter(theme: string, state: string): string | null {
  return THEME_FILTER_CONFIG[theme]?.[state as keyof typeof THEME_FILTER_CONFIG[string]] || null;
}

/**
 * Get all filter classes for a theme and list of states
 */
export function getThemeFilterClasses(theme: string, states: string[]): string[] {
  const filters: string[] = [];
  
  states.forEach(state => {
    const filter = getThemeFilter(theme, state);
    if (filter) {
      filters.push(filter);
    }
  });
  
  return [...new Set(filters)]; // Remove duplicates
}
`;
}

/**
 * Main execution function
 */
function main() {
  console.log("🎨 Chess Filter Configuration Generator");
  console.log("=====================================\n");

  try {
    // Read CSS files
    console.log("📖 Reading CSS files...");
    const professionalCSS = fs.readFileSync(
      path.resolve(__dirname, THEMES_PROFESSIONAL_PATH),
      "utf8"
    );
    const gamingCSS = fs.readFileSync(
      path.resolve(__dirname, THEMES_GAMING_PATH),
      "utf8"
    );
    const filtersCSS = fs.readFileSync(
      path.resolve(__dirname, CHESS_FILTERS_PATH),
      "utf8"
    );

    // Parse themes and filters
    console.log("🔍 Parsing themes and filters...");
    const professionalThemes = parseThemes(professionalCSS);
    const gamingThemes = parseThemes(gamingCSS);
    const allThemes = [...professionalThemes, ...gamingThemes];
    const filters = parseFilters(filtersCSS);

    console.log(`   Found ${professionalThemes.length} professional themes`);
    console.log(`   Found ${gamingThemes.length} gaming themes`);
    console.log(`   Found ${filters.length} visual filters`);
    console.log(`   Total themes: ${allThemes.length}\n`);

    // Create smart mappings
    console.log("🧠 Creating smart theme-to-filter mappings...");
    const mappings = createSmartMappings(allThemes, filters);

    console.log(
      `   Created mappings for ${Object.keys(mappings).length} themes\n`
    );

    // Generate configuration file
    console.log("📝 Generating configuration file...");
    const configContent = generateConfigFile(allThemes, filters, mappings);

    // Write output file
    const outputPath = path.resolve(__dirname, OUTPUT_PATH);
    fs.writeFileSync(outputPath, configContent, "utf8");

    console.log(`✅ Configuration file generated: ${outputPath}\n`);

    // Summary
    console.log("📊 Generation Summary:");
    console.log(`   • ${allThemes.length} themes processed`);
    console.log(`   • ${filters.length} filters available`);
    console.log(
      `   • ${Object.keys(mappings).length} themes with filter mappings`
    );
    console.log(`   • Configuration saved to filter-config.constants.ts\n`);

    console.log("🎉 Filter configuration generation complete!");
    console.log(
      "   You can now import and use THEME_FILTER_CONFIG in your components."
    );
  } catch (error) {
    console.error("❌ Error generating filter configuration:", error.message);
    process.exit(1);
  }
}

// Run the generator
if (require.main === module) {
  main();
}

module.exports = {
  parseThemes,
  parseFilters,
  createSmartMappings,
  generateConfigFile,
};
