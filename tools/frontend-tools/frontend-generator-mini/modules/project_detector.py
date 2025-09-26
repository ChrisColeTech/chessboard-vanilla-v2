"""
Project Capability Detector for scanning existing project structure and hooks.
"""

from pathlib import Path
from typing import List, Dict, Optional
import re
import logging
import sys

# Add parent directory to path so we can import shared modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from shared.name_standardizer import NameStandardizer

try:
    from .config import ProjectCapabilities
except ImportError:
    from config import ProjectCapabilities


class ProjectDetectionError(Exception):
    """Raised when project detection fails."""
    pass


class ProjectCapabilityDetector:
    """Detects project capabilities and existing structure."""
    
    def __init__(self, frontend_root: Path, hooks_path: Optional[str] = None, components_ui_path: Optional[str] = None):
        self.frontend_root = frontend_root
        self.hooks_core_path = hooks_path or "src/hooks/core"
        self.components_ui_path = components_ui_path or "src/components/ui"
        self._validate_frontend_root()
        
    def detect_capabilities(self) -> ProjectCapabilities:
        """Detect all project capabilities with error handling."""
        try:
            return ProjectCapabilities(
                has_page_hooks=self._detect_page_hooks(),
                has_mobile_hook=self._detect_mobile_hook(),
                has_data_table=self._detect_data_table(),
                existing_parents=self._scan_existing_parents(),
                existing_children=self._scan_existing_children()
            )
        except Exception as e:
            logging.error(f"Error detecting project capabilities: {e}")
            raise ProjectDetectionError(f"Failed to detect project capabilities: {e}") from e
    
    def _detect_page_hooks(self) -> bool:
        """Check if usePageInstructions and usePageActions hooks exist."""
        try:
            hooks_dir = self.frontend_root / self.hooks_core_path
            
            return (
                (hooks_dir / "usePageInstructions.ts").exists() and
                (hooks_dir / "usePageActions.ts").exists()
            )
        except (OSError, PermissionError) as e:
            logging.warning(f"Error accessing hooks directory {hooks_dir}: {e}")
            return False
    
    def _detect_mobile_hook(self) -> bool:
        """Check if useIsMobile hook exists."""
        try:
            hooks_dir = self.frontend_root / self.hooks_core_path
            return (hooks_dir / "useIsMobile.ts").exists()
        except (OSError, PermissionError) as e:
            logging.warning(f"Error accessing hooks directory {hooks_dir}: {e}")
            return False
    
    def _detect_data_table(self) -> bool:
        """Check if DataTable component exists."""
        try:
            ui_dir = self.frontend_root / self.components_ui_path
            return (ui_dir / "DataTable.tsx").exists()
        except (OSError, PermissionError) as e:
            logging.warning(f"Error accessing UI components directory {ui_dir}: {e}")
            return False
    
    def _scan_existing_parents(self) -> List[str]:
        """Scan for existing parent pages with error handling."""
        try:
            pages_dir = self.frontend_root / "src" / "pages"
            parents = []
            
            if not pages_dir.exists():
                logging.debug(f"Pages directory does not exist: {pages_dir}")
                return parents
                
            for item in pages_dir.iterdir():
                if item.is_dir():
                    # Look for main page file that indicates a parent
                    parent_page_pattern = f"{NameStandardizer.to_pascal_case(item.name)}Page.tsx"
                    parent_main_pattern = f"{NameStandardizer.to_pascal_case(item.name)}MainPage.tsx"
                    
                    if (item / parent_page_pattern).exists() or (item / parent_main_pattern).exists():
                        parents.append(item.name)
                        
            return sorted(parents)
        except (OSError, PermissionError) as e:
            logging.warning(f"Error scanning parent pages: {e}")
            return []
    
    def _scan_existing_children(self) -> Dict[str, List[str]]:
        """Scan for existing child pages within each parent with error handling."""
        try:
            pages_dir = self.frontend_root / "src" / "pages"
            children = {}
            
            if not pages_dir.exists():
                logging.debug(f"Pages directory does not exist: {pages_dir}")
                return children
                
            for parent_dir in pages_dir.iterdir():
                if not parent_dir.is_dir():
                    continue
                    
                parent_name = parent_dir.name
                children[parent_name] = []
                
                try:
                    # Look for child pages (files that don't match parent patterns)
                    parent_patterns = {
                        f"{NameStandardizer.to_pascal_case(parent_name)}Page.tsx",
                        f"{NameStandardizer.to_pascal_case(parent_name)}MainPage.tsx"
                    }
                    
                    for page_file in parent_dir.glob("*.tsx"):
                        if page_file.name not in parent_patterns:
                            # Extract child name from filename
                            child_name = self._extract_child_name_from_file(page_file.name)
                            if child_name and child_name not in children[parent_name]:
                                children[parent_name].append(child_name)
                    
                    # Sort child names
                    children[parent_name] = sorted(children[parent_name])
                except (OSError, PermissionError) as e:
                    logging.warning(f"Error scanning children in {parent_dir}: {e}")
                    children[parent_name] = []
            
            return children
        except (OSError, PermissionError) as e:
            logging.warning(f"Error scanning child pages: {e}")
            return {}
    
    def _extract_child_name_from_file(self, filename: str) -> str:
        """Extract child page name from filename."""
        # Remove .tsx extension
        name = filename[:-4] if filename.endswith('.tsx') else filename
        
        # Remove Page suffix if present
        if name.endswith('Page'):
            name = name[:-4]
            
        # Remove Mobile prefix if present (mobile variants)
        if name.startswith('Mobile'):
            name = name[6:]
        
        # Convert to lowercase for consistency
        return name.lower() if name else ""
    
    def check_parent_exists(self, parent_name: str) -> bool:
        """Check if a specific parent page exists."""
        parent_dir = self.frontend_root / "src" / "pages" / parent_name.lower()
        if not parent_dir.exists():
            return False
            
        # Check for parent page file
        parent_page_file = parent_dir / f"{NameStandardizer.to_pascal_case(parent_name)}Page.tsx"
        return parent_page_file.exists()
    
    def check_child_exists(self, parent_name: str, child_name: str) -> bool:
        """Check if a specific child page exists."""
        parent_dir = self.frontend_root / "src" / "pages" / parent_name.lower()
        if not parent_dir.exists():
            return False
            
        # Check for child page file
        child_page_file = parent_dir / f"{NameStandardizer.to_pascal_case(child_name)}Page.tsx"
        return child_page_file.exists()
    
    def get_project_summary(self) -> Dict:
        """Get a summary of the project structure."""
        capabilities = self.detect_capabilities()
        
        return {
            'frontend_root': str(self.frontend_root),
            'capabilities': {
                'has_page_hooks': capabilities.has_page_hooks,
                'has_mobile_hook': capabilities.has_mobile_hook,
                'has_data_table': capabilities.has_data_table
            },
            'structure': {
                'parents': capabilities.existing_parents,
                'children': capabilities.existing_children,
                'total_parents': len(capabilities.existing_parents),
                'total_children': sum(len(children) for children in capabilities.existing_children.values())
            }
        }
    
    def _validate_frontend_root(self) -> None:
        """Validate that frontend root exists and appears to be a valid project."""
        if not self.frontend_root.exists():
            raise ProjectDetectionError(f"Frontend root directory not found: {self.frontend_root}")
        
        if not self.frontend_root.is_dir():
            raise ProjectDetectionError(f"Frontend root is not a directory: {self.frontend_root}")
        
        # Check for basic project structure indicators
        src_dir = self.frontend_root / "src"
        if not src_dir.exists():
            logging.warning(f"No 'src' directory found in {self.frontend_root}. This may not be a React project.")
    
    def validate_project_structure(self) -> List[str]:
        """Validate project structure and return list of issues found."""
        issues = []
        
        # Check for required directories
        required_dirs = [
            "src",
            "src/pages",
            "src/components",
            "src/hooks",
            "src/constants",
            "src/services"
        ]
        
        for dir_path in required_dirs:
            full_path = self.frontend_root / dir_path
            if not full_path.exists():
                issues.append(f"Missing directory: {dir_path}")
        
        # Check for package.json
        package_json = self.frontend_root / "package.json"
        if not package_json.exists():
            issues.append("No package.json found - may not be a Node.js project")
        
        return issues