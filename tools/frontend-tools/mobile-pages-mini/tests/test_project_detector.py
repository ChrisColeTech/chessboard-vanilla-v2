"""
Tests for the Project Capability Detector module.
"""

import pytest
from pathlib import Path
import tempfile
import os
import sys

# Add the modules directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from project_detector import ProjectCapabilityDetector
from config import ProjectCapabilities


class TestProjectCapabilityDetector:
    """Test cases for ProjectCapabilityDetector class."""
    
    def setup_method(self):
        """Setup test environment with mock project structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        self.detector = ProjectCapabilityDetector(self.frontend_root)
        
        # Create basic directory structure
        self.src_dir = self.frontend_root / "src"
        self.hooks_core_dir = self.src_dir / "hooks" / "core"
        self.components_ui_dir = self.src_dir / "components" / "ui"
        self.pages_dir = self.src_dir / "pages"
        
        self.hooks_core_dir.mkdir(parents=True)
        self.components_ui_dir.mkdir(parents=True)
        self.pages_dir.mkdir(parents=True)
    
    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_detect_page_hooks_present(self):
        """Test detection when both page hooks exist."""
        # Create hook files
        (self.hooks_core_dir / "usePageInstructions.ts").write_text("// Hook content")
        (self.hooks_core_dir / "usePageActions.ts").write_text("// Hook content")
        
        assert self.detector._detect_page_hooks() is True
    
    def test_detect_page_hooks_missing_instructions(self):
        """Test detection when usePageInstructions is missing."""
        # Only create usePageActions
        (self.hooks_core_dir / "usePageActions.ts").write_text("// Hook content")
        
        assert self.detector._detect_page_hooks() is False
    
    def test_detect_page_hooks_missing_actions(self):
        """Test detection when usePageActions is missing."""
        # Only create usePageInstructions
        (self.hooks_core_dir / "usePageInstructions.ts").write_text("// Hook content")
        
        assert self.detector._detect_page_hooks() is False
    
    def test_detect_page_hooks_both_missing(self):
        """Test detection when both page hooks are missing."""
        assert self.detector._detect_page_hooks() is False
    
    def test_detect_mobile_hook_present(self):
        """Test detection when useIsMobile hook exists."""
        (self.hooks_core_dir / "useIsMobile.ts").write_text("// Mobile hook content")
        
        assert self.detector._detect_mobile_hook() is True
    
    def test_detect_mobile_hook_missing(self):
        """Test detection when useIsMobile hook is missing."""
        assert self.detector._detect_mobile_hook() is False
    
    def test_detect_data_table_present(self):
        """Test detection when DataTable component exists."""
        (self.components_ui_dir / "DataTable.tsx").write_text("// DataTable component")
        
        assert self.detector._detect_data_table() is True
    
    def test_detect_data_table_missing(self):
        """Test detection when DataTable component is missing."""
        assert self.detector._detect_data_table() is False
    
    def test_scan_existing_parents_empty(self):
        """Test parent scanning with no existing parents."""
        parents = self.detector._scan_existing_parents()
        assert parents == []
    
    def test_scan_existing_parents_with_parents(self):
        """Test parent scanning with existing parent pages."""
        # Create parent directories and files
        uitests_dir = self.pages_dir / "uitests"
        layout_dir = self.pages_dir / "layout"
        uitests_dir.mkdir()
        layout_dir.mkdir()
        
        # Create parent page files
        (uitests_dir / "UitestsPage.tsx").write_text("// Parent page")
        (layout_dir / "LayoutMainPage.tsx").write_text("// Parent main page")
        
        parents = self.detector._scan_existing_parents()
        assert set(parents) == {"layout", "uitests"}
    
    def test_scan_existing_children_empty(self):
        """Test child scanning with no existing children."""
        children = self.detector._scan_existing_children()
        assert children == {}
    
    def test_scan_existing_children_with_children(self):
        """Test child scanning with existing child pages."""
        # Create parent directory with children
        uitests_dir = self.pages_dir / "uitests"
        uitests_dir.mkdir()
        
        # Create parent and child files
        (uitests_dir / "UitestsPage.tsx").write_text("// Parent page")
        (uitests_dir / "UitestsMainPage.tsx").write_text("// Parent main page")
        (uitests_dir / "DragTestPage.tsx").write_text("// Child page")
        (uitests_dir / "LayoutTestPage.tsx").write_text("// Child page")
        (uitests_dir / "MobileDragTestPage.tsx").write_text("// Mobile child page")
        
        children = self.detector._scan_existing_children()
        
        assert "uitests" in children
        assert set(children["uitests"]) == {"dragtest", "layouttest"}
    
    def test_extract_child_name_from_file_regular(self):
        """Test child name extraction from regular page files."""
        assert self.detector._extract_child_name_from_file("DragTestPage.tsx") == "dragtest"
        assert self.detector._extract_child_name_from_file("LayoutTestPage.tsx") == "layouttest"
    
    def test_extract_child_name_from_file_mobile(self):
        """Test child name extraction from mobile page files."""
        assert self.detector._extract_child_name_from_file("MobileDragTestPage.tsx") == "dragtest"
        assert self.detector._extract_child_name_from_file("MobileLayoutTestPage.tsx") == "layouttest"
    
    def test_extract_child_name_from_file_no_page_suffix(self):
        """Test child name extraction from files without Page suffix."""
        assert self.detector._extract_child_name_from_file("DragTest.tsx") == "dragtest"
        assert self.detector._extract_child_name_from_file("MobileDragTest.tsx") == "dragtest"
    
    def test_check_parent_exists_true(self):
        """Test parent existence check when parent exists."""
        uitests_dir = self.pages_dir / "uitests"
        uitests_dir.mkdir()
        (uitests_dir / "UitestsPage.tsx").write_text("// Parent page")
        
        assert self.detector.check_parent_exists("uitests") is True
    
    def test_check_parent_exists_false(self):
        """Test parent existence check when parent doesn't exist."""
        assert self.detector.check_parent_exists("nonexistent") is False
    
    def test_check_child_exists_true(self):
        """Test child existence check when child exists."""
        uitests_dir = self.pages_dir / "uitests"
        uitests_dir.mkdir()
        (uitests_dir / "DragTestPage.tsx").write_text("// Child page")
        
        assert self.detector.check_child_exists("uitests", "DragTest") is True
    
    def test_check_child_exists_false(self):
        """Test child existence check when child doesn't exist."""
        uitests_dir = self.pages_dir / "uitests"
        uitests_dir.mkdir()
        
        assert self.detector.check_child_exists("uitests", "NonExistent") is False
    
    def test_detect_capabilities_complete(self):
        """Test complete capability detection."""
        # Setup all capabilities
        (self.hooks_core_dir / "usePageInstructions.ts").write_text("// Hook")
        (self.hooks_core_dir / "usePageActions.ts").write_text("// Hook")
        (self.hooks_core_dir / "useIsMobile.ts").write_text("// Hook")
        (self.components_ui_dir / "DataTable.tsx").write_text("// Component")
        
        # Create parent structure
        uitests_dir = self.pages_dir / "uitests"
        uitests_dir.mkdir()
        (uitests_dir / "UitestsPage.tsx").write_text("// Parent")
        (uitests_dir / "DragTestPage.tsx").write_text("// Child")
        
        capabilities = self.detector.detect_capabilities()
        
        assert capabilities.has_page_hooks is True
        assert capabilities.has_mobile_hook is True
        assert capabilities.has_data_table is True
        assert "uitests" in capabilities.existing_parents
        assert "dragtest" in capabilities.existing_children.get("uitests", [])
    
    def test_get_project_summary(self):
        """Test project summary generation."""
        # Setup minimal structure
        (self.hooks_core_dir / "usePageInstructions.ts").write_text("// Hook")
        (self.hooks_core_dir / "usePageActions.ts").write_text("// Hook")
        
        uitests_dir = self.pages_dir / "uitests"
        uitests_dir.mkdir()
        (uitests_dir / "UitestsPage.tsx").write_text("// Parent")
        (uitests_dir / "DragTestPage.tsx").write_text("// Child")
        
        summary = self.detector.get_project_summary()
        
        assert "frontend_root" in summary
        assert "capabilities" in summary
        assert "structure" in summary
        assert summary["capabilities"]["has_page_hooks"] is True
        assert summary["structure"]["total_parents"] == 1
        assert summary["structure"]["total_children"] == 1
    
    def test_pages_dir_missing(self):
        """Test behavior when pages directory doesn't exist."""
        # Remove pages directory
        import shutil
        shutil.rmtree(self.pages_dir)
        
        parents = self.detector._scan_existing_parents()
        children = self.detector._scan_existing_children()
        
        assert parents == []
        assert children == {}
    
    def test_hooks_dir_missing(self):
        """Test behavior when hooks directory doesn't exist."""
        # Remove hooks directory
        import shutil
        shutil.rmtree(self.hooks_core_dir)
        
        assert self.detector._detect_page_hooks() is False
        assert self.detector._detect_mobile_hook() is False