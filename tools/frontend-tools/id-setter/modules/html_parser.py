"""
HTML Parser Module
Finds interactive elements in React/HTML components that need IDs
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Element:
    """Represents an interactive element that needs an ID"""
    tag: str
    start_pos: int
    end_pos: int
    attributes: Dict[str, str]
    text_content: str
    element_type: str  # 'button', 'input', 'link', 'interactive'
    existing_id: str = None


class HTMLParser:
    """Parses React components to find interactive elements"""
    
    INTERACTIVE_TAGS = {
        'button', 'a', 'input', 'textarea', 'select', 'option',
        'details', 'summary', 'dialog'
    }
    
    INTERACTIVE_ATTRIBUTES = {
        'onclick', 'onsubmit', 'onchange', 'onfocus', 'onblur',
        'onkeydown', 'onkeyup', 'onmousedown', 'onmouseup',
        'ontouchstart', 'ontouchend'
    }
    
    def __init__(self, skip_existing=False):
        self.skip_existing = skip_existing
        # Regex patterns for parsing JSX/React elements
        self.element_pattern = re.compile(
            r'<(\w+)([^>]*?)(?:/>|>.*?</\1>)',
            re.DOTALL | re.MULTILINE
        )
        self.attribute_pattern = re.compile(
            r'(\w+)=(?:"([^"]*)"|{([^}]*)})',
            re.DOTALL
        )
    
    def parse_file_content(self, content: str) -> List[Element]:
        """Parse file content and return list of interactive elements"""
        elements = []
        
        # Find all JSX elements
        for match in self.element_pattern.finditer(content):
            tag = match.group(1).lower()
            attributes_str = match.group(2)
            full_match = match.group(0)
            
            # Parse attributes
            attributes = self._parse_attributes(attributes_str)
            
            # Check if element needs an ID
            if self._should_add_id(tag, attributes):
                element = Element(
                    tag=tag,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    attributes=attributes,
                    text_content=self._extract_text_content(full_match),
                    element_type=self._determine_element_type(tag, attributes),
                    existing_id=attributes.get('id')
                )
                elements.append(element)
        
        return elements
    
    def _parse_attributes(self, attributes_str: str) -> Dict[str, str]:
        """Parse JSX attributes from string"""
        attributes = {}
        
        for match in self.attribute_pattern.finditer(attributes_str):
            attr_name = match.group(1)
            attr_value = match.group(2) or match.group(3) or ""
            attributes[attr_name.lower()] = attr_value.strip()
        
        return attributes
    
    def _should_add_id(self, tag: str, attributes: Dict[str, str]) -> bool:
        """Check if element needs an ID"""
        # Skip if already has ID and skip_existing is True
        if self.skip_existing and 'id' in attributes:
            return False
        
        # Skip script, style, and meta tags
        if tag in {'script', 'style', 'meta', 'link', 'title', 'head'}:
            return False
        
        # Include all meaningful HTML elements
        return True
    
    def _extract_text_content(self, element_html: str) -> str:
        """Extract text content from element for ID generation"""
        # Remove JSX tags and get inner text
        text = re.sub(r'<[^>]+>', '', element_html)
        text = re.sub(r'{[^}]*}', '', text)  # Remove JSX expressions
        return text.strip()[:50]  # Limit length
    
    def _determine_element_type(self, tag: str, attributes: Dict[str, str]) -> str:
        """Determine the type of element"""
        return tag