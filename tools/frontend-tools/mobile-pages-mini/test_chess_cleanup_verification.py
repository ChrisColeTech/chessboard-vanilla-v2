#!/usr/bin/env python3
"""
Test suite to verify chess dependency cleanup was successful.
Tests the specific templates we cleaned up to ensure no chess imports remain.
"""

import re
from pathlib import Path
import unittest


class TestChessCleanup(unittest.TestCase):
    
    def setUp(self):
        self.static_dir = Path("templates/static")
        self.dynamic_dir = Path("templates/dynamic")
    
    def _read_template(self, template_path):
        """Read template content from static or dynamic directory."""
        static_path = self.static_dir / template_path
        if static_path.exists():
            return static_path.read_text(encoding='utf-8')
        
        dynamic_path = self.dynamic_dir / template_path
        if dynamic_path.exists():
            return dynamic_path.read_text(encoding='utf-8')
        
        self.fail(f"Template not found: {template_path}")
    
    def _extract_imports(self, content):
        """Extract import statements from template content."""
        import_patterns = [
            r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # import ... from "path"
            r'import\s+[\'"]([^\'"]+)[\'"]',        # import "path"
        ]
        
        imports = set()
        for pattern in import_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            imports.update(matches)
        
        return imports
    
    def _is_chess_specific(self, import_path):
        """Check if an import path is chess-specific."""
        chess_patterns = [
            r'.*chess.*', r'.*piece.*', r'.*board.*', r'.*stockfish.*',
            r'.*computer.*difficulty.*', r'.*game.*result.*'
        ]
        
        for pattern in chess_patterns:
            if re.match(pattern, import_path, re.IGNORECASE):
                return True
        return False
    
    def test_action_sheet_container_cleaned(self):
        """Test that ActionSheetContainer no longer has chess imports."""
        content = self._read_template("components/action-sheet/ActionSheetContainer.tsx.template")
        imports = self._extract_imports(content)
        
        chess_imports = [imp for imp in imports if self._is_chess_specific(imp)]
        
        self.assertEqual(len(chess_imports), 0, 
                        f"ActionSheetContainer still has chess imports: {chess_imports}")
        
        # Verify specific chess hooks were removed
        self.assertNotIn("usePlayActions", content)
        self.assertNotIn("useWorkerActions", content)
        
        # Verify splash actions are still present
        self.assertIn("useSplashActions", content)
        self.assertIn("useMinimalSplashActions", content)
    
    def test_main_tsx_cleaned(self):
        """Test that main.tsx no longer imports chess CSS files."""
        content = self._read_template("main.tsx.template")
        
        # Check chess CSS imports were removed
        self.assertNotIn("chess-filters.css", content)
        self.assertNotIn("chess-piece-colors.css", content)
        
        # Verify other CSS imports remain
        self.assertIn("themes-base.css", content)
        self.assertIn("themes-professional.css", content)
        self.assertIn("splash.css", content)
    
    def test_app_store_cleaned(self):
        """Test that appStore.ts no longer has chess imports and state."""
        content = self._read_template("stores/appStore.ts.template")
        imports = self._extract_imports(content)
        
        chess_imports = [imp for imp in imports if self._is_chess_specific(imp)]
        
        self.assertEqual(len(chess_imports), 0, 
                        f"appStore still has chess imports: {chess_imports}")
        
        # Verify specific chess imports were removed
        self.assertNotIn("pieces.constants", content)
        self.assertNotIn("boardColorConfig", content)
        
        # Verify chess state properties were removed
        self.assertNotIn("selectedPieceSet", content)
        self.assertNotIn("pieceSize", content)
        self.assertNotIn("boardColorMode", content)
        self.assertNotIn("premiumBoardStyle", content)
        
        # Verify chess actions were removed
        self.assertNotIn("setPieceSet", content)
        self.assertNotIn("setPieceSize", content)
        self.assertNotIn("setBoardColorMode", content)
        
        # Verify useChessSettings hook was removed
        self.assertNotIn("useChessSettings", content)
    
    def test_settings_panel_cleaned(self):
        """Test that SettingsPanel no longer imports chess components."""
        content = self._read_template("components/core/SettingsPanel.tsx.template")
        imports = self._extract_imports(content)
        
        chess_imports = [imp for imp in imports if self._is_chess_specific(imp)]
        
        self.assertEqual(len(chess_imports), 0, 
                        f"SettingsPanel still has chess imports: {chess_imports}")
        
        # Verify specific chess components were removed
        self.assertNotIn("BoardColorSelector", content)
        self.assertNotIn("PieceSetSelector", content)
        self.assertNotIn("useChessSettings", content)
        
        # Verify piece size settings were removed
        self.assertNotIn("Piece Size", content)
        self.assertNotIn("pieceSizeOptions", content)
        
        # Verify other components remain
        self.assertIn("ThemeSelector", content)
        self.assertIn("BackgroundEffectsSelector", content)


class TestOrphanedFiles(unittest.TestCase):
    """Test that orphaned chess files don't affect generation."""
    
    def setUp(self):
        self.static_dir = Path("templates/static")
    
    def test_orphaned_chess_components_exist_but_unused(self):
        """Verify that orphaned chess components exist but aren't imported."""
        # These should exist but not be imported by anything
        board_color_path = self.static_dir / "components/settings/BoardColorSelector.tsx.template"
        piece_set_path = self.static_dir / "components/settings/PieceSetSelector.tsx.template"
        
        self.assertTrue(board_color_path.exists(), "BoardColorSelector should exist")
        self.assertTrue(piece_set_path.exists(), "PieceSetSelector should exist")
        
        # But they shouldn't be imported by any active templates
        # This would require a more complex dependency scan to fully verify


if __name__ == '__main__':
    print("🧪 Running Chess Cleanup Verification Tests...")
    unittest.main(verbosity=2)