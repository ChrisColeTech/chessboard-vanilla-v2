"""
ID Generator Module
Generates meaningful IDs for React components based on context and content
"""

import re
from typing import Dict, Set
from pathlib import Path


class IDGenerator:
    """Generates meaningful IDs for interactive elements"""
    
    def __init__(self):
        self.used_ids: Set[str] = set()
        self.page_contexts = {
            'game': 'game',
            'settings': 'settings',
            'menu': 'menu',
            'profile': 'profile',
            'board': 'board',
            'chat': 'chat',
            'analysis': 'analysis'
        }
    
    def generate_id(self, element, component_path: str, page_context: str = None) -> str:
        """Generate a meaningful ID for an element"""
        # Build ID components
        parts = []
        
        # Get element purpose first to determine if we have meaningful text
        element_purpose = self._determine_element_purpose(element)
        has_meaningful_text = element.text_content.strip() and len(element.text_content.strip()) > 0
        
        # If no meaningful text, add folder/page context for better specificity
        if not has_meaningful_text:
            folder_context = self._extract_folder_context(component_path)
            if folder_context:
                parts.append(folder_context)
        
        # Add component context
        component_base = self._extract_component_name(component_path)
        if component_base:
            parts.append(component_base)
        
        # Add element type/purpose
        if element_purpose:
            parts.append(element_purpose)
        
        # Create base ID
        base_id = '-'.join(parts)
        base_id = self._sanitize_id(base_id)
        
        # Ensure uniqueness
        final_id = self._ensure_unique_id(base_id)
        self.used_ids.add(final_id)
        
        return final_id
    
    def _extract_component_name(self, file_path: str) -> str:
        """Extract component name from file path"""
        path = Path(file_path)
        name = path.stem
        
        # Remove common suffixes
        name = re.sub(r'(Component|Page|Screen|View)$', '', name)
        
        # Convert PascalCase to kebab-case
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name).lower()
        
        return name
    
    def _extract_folder_context(self, file_path: str) -> str:
        """Extract folder context from file path for better ID specificity"""
        path = Path(file_path)
        
        # Get the parent folder name
        if len(path.parts) >= 2:
            parent_folder = path.parts[-2]  # Get immediate parent folder
            
            # Clean up folder names
            if parent_folder == 'components':
                # Look for grandparent if parent is generic 'components'
                if len(path.parts) >= 3:
                    grandparent = path.parts[-3]
                    return self._sanitize_folder_name(grandparent)
            else:
                return self._sanitize_folder_name(parent_folder)
        
        return None
    
    def _sanitize_folder_name(self, folder_name: str) -> str:
        """Clean up folder name for use in ID"""
        # Remove common folder prefixes/suffixes
        folder_name = folder_name.lower()
        folder_name = re.sub(r'(components?|pages?|views?)', '', folder_name)
        folder_name = folder_name.strip('-_')
        return folder_name if folder_name else None
    
    def _detect_page_context(self, file_path: str) -> str:
        """Auto-detect page context from file path"""
        path_lower = file_path.lower()
        
        # Check for page-specific directories or filenames
        if any(indicator in path_lower for indicator in ['game', 'board', 'chess']):
            return 'game'
        elif any(indicator in path_lower for indicator in ['settings', 'config', 'preferences']):
            return 'settings'
        elif any(indicator in path_lower for indicator in ['menu', 'navigation', 'nav']):
            return 'menu'
        elif any(indicator in path_lower for indicator in ['profile', 'user', 'account']):
            return 'profile'
        elif any(indicator in path_lower for indicator in ['chat', 'message', 'communication']):
            return 'chat'
        elif any(indicator in path_lower for indicator in ['analysis', 'analyze', 'review']):
            return 'analysis'
        elif any(indicator in path_lower for indicator in ['home', 'landing', 'welcome']):
            return 'home'
        
        # Check specific component patterns
        if 'tabbar' in path_lower or 'tab-bar' in path_lower:
            return 'nav'
        elif 'header' in path_lower:
            return 'header'
        elif 'footer' in path_lower:
            return 'footer'
        
        return None
    
    def _determine_element_purpose(self, element) -> str:
        """Determine the purpose/function of the element"""
        # Check element tag type first
        if element.tag == 'button':
            element_base = 'btn'
        elif element.tag == 'a':
            element_base = 'link'
        elif element.tag in ['input', 'textarea', 'select']:
            input_type = element.attributes.get('type', element.tag)
            element_base = f'{input_type}'
        else:
            element_base = element.tag
        
        # Check text content for semantic meaning
        text = element.text_content.lower().strip()
        
        # If there's meaningful text, use it as the identifier
        if text and len(text) > 0:
            # Clean up the text for use in ID
            text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special chars
            text_clean = re.sub(r'\s+', '-', text_clean.strip())  # Replace spaces with hyphens
            if text_clean:
                return f'{text_clean}-{element_base}'
        
        # Fallback to element type
        return element_base
    
    def _sanitize_id(self, id_string: str) -> str:
        """Sanitize ID string to be valid HTML ID"""
        # Replace invalid characters with hyphens
        id_string = re.sub(r'[^a-zA-Z0-9\-_]', '-', id_string)
        
        # Remove multiple consecutive hyphens
        id_string = re.sub(r'-+', '-', id_string)
        
        # Remove leading/trailing hyphens
        id_string = id_string.strip('-')
        
        # Ensure it starts with a letter
        if id_string and not id_string[0].isalpha():
            id_string = 'el-' + id_string
        
        return id_string or 'element'
    
    def _ensure_unique_id(self, base_id: str) -> str:
        """Ensure the ID is unique by adding a number if needed"""
        if base_id not in self.used_ids:
            return base_id
        
        counter = 1
        while f"{base_id}-{counter}" in self.used_ids:
            counter += 1
        
        return f"{base_id}-{counter}"
    
    def reset_used_ids(self):
        """Reset the set of used IDs (useful when processing new files)"""
        self.used_ids.clear()