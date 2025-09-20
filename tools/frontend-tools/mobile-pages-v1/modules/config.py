"""
Configuration and data structures for the Template-Based Page Generator v2.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from pathlib import Path


@dataclass
class PageConfig:
    """Configuration for page generation with proper name normalization."""
    name: str
    parent: Optional[str] = None
    mobile: bool = False
    icon: str = "Navigation"
    description: str = ""
    
    def __post_init__(self):
        """Normalize the name to avoid duplicate 'Page' suffix."""
        if self.name.endswith('Page'):
            # Remove the "Page" suffix since we'll add it back in file generation
            self.base_name = self.name[:-4].capitalize()  # Remove "Page" and capitalize
        else:
            self.base_name = self.name.capitalize()  # Capitalize for proper component names
    
    @property
    def page_name(self) -> str:
        """Get the name with 'Page' suffix for components."""
        return f"{self.base_name}Page"
    
    @property
    def display_name(self) -> str:
        """Get the clean base name for display purposes."""
        return self.base_name
    
    @property
    def parent_id(self) -> str:
        """Get lowercase parent ID."""
        return self.parent.lower() if self.parent else ""
    
    @property
    def page_id(self) -> str:
        """Get lowercase page ID."""
        return self.base_name.lower()


@dataclass
class ProjectCapabilities:
    """Detected project capabilities and structure."""
    has_page_hooks: bool = False        # usePageInstructions, usePageActions exist
    has_mobile_hook: bool = False       # useIsMobile exists  
    has_data_table: bool = False        # DataTable component exists
    existing_parents: List[str] = None  # Discovered parent pages
    existing_children: Dict[str, List[str]] = None  # Parent -> children mapping
    
    def __post_init__(self):
        if self.existing_parents is None:
            self.existing_parents = []
        if self.existing_children is None:
            self.existing_children = {}


@dataclass
class GenerationContext:
    """Context for a generation operation."""
    frontend_root: Path
    config: PageConfig
    capabilities: ProjectCapabilities
    variables: Dict[str, str]
    
    @property
    def pages_dir(self) -> Path:
        return self.frontend_root / "src" / "pages"
    
    @property
    def components_dir(self) -> Path:
        return self.frontend_root / "src" / "components"
    
    @property
    def hooks_dir(self) -> Path:
        return self.frontend_root / "src" / "hooks"
    
    @property
    def actions_dir(self) -> Path:
        return self.frontend_root / "src" / "constants" / "actions" / "pages"
    
    @property
    def instructions_dir(self) -> Path:
        return self.frontend_root / "src" / "services" / "instructions" / "pages"


class WrapperType:
    """Constants for wrapper template types."""
    FULL_HOOKS = "child-wrapper-full-hooks.tsx.template"
    BASIC_HOOKS = "child-wrapper-basic-hooks.tsx.template"
    NO_HOOKS = "child-wrapper-no-hooks.tsx.template"
    NO_MOBILE = "child-wrapper-no-mobile.tsx.template"