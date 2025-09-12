"""
File Processor Module
Processes React component files and updates them with generated IDs
"""

import re
from pathlib import Path
from typing import List, Optional
from .html_parser import HTMLParser, Element
from .id_generator import IDGenerator


class FileProcessor:
    """Processes React component files to add IDs"""
    
    def __init__(self, html_parser: HTMLParser, id_generator: IDGenerator, dry_run: bool = False):
        self.html_parser = html_parser
        self.id_generator = id_generator
        self.dry_run = dry_run
        
        # File extensions to process
        self.react_extensions = {'.tsx', '.jsx', '.ts', '.js'}
    
    def process_directory(self, directory: Path, page_context: Optional[str] = None):
        """Process all React files in a directory recursively"""
        processed_count = 0
        
        for file_path in directory.rglob('*'):
            if file_path.suffix in self.react_extensions:
                if self._should_process_file(file_path):
                    changes = self.process_file(file_path, page_context)
                    if changes > 0:
                        processed_count += 1
        
        print(f"Processed {processed_count} files")
    
    def process_file(self, file_path: Path, page_context: Optional[str] = None) -> int:
        """Process a single React component file"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse elements
            elements = self.html_parser.parse_file_content(content)
            
            if not elements:
                if not self.dry_run:
                    print(f"No interactive elements found in {file_path.name}")
                return 0
            
            # Generate IDs and update content
            updated_content = self._update_content_with_ids(
                content, elements, str(file_path), page_context
            )
            
            if updated_content != content:
                if self.dry_run:
                    self._print_changes_preview(file_path, elements)
                else:
                    # Write updated content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Updated {file_path.name} with {len(elements)} IDs")
                
                return len(elements)
            else:
                if not self.dry_run:
                    print(f"No changes needed for {file_path.name}")
                return 0
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed"""
        # Skip test files
        if any(test_indicator in file_path.name.lower() 
               for test_indicator in ['test', 'spec', '.test.', '.spec.']):
            return False
        
        # Skip node_modules and build directories
        if any(skip_dir in file_path.parts 
               for skip_dir in ['node_modules', 'build', 'dist', '.next']):
            return False
        
        return True
    
    def _update_content_with_ids(self, content: str, elements: List[Element], 
                                file_path: str, page_context: Optional[str]) -> str:
        """Update file content by adding IDs to elements"""
        # Sort elements by position (reverse order to maintain positions)
        elements_sorted = sorted(elements, key=lambda e: e.start_pos, reverse=True)
        
        updated_content = content
        
        for element in elements_sorted:
            # Generate ID
            generated_id = self.id_generator.generate_id(
                element, file_path, page_context
            )
            
            # Find the element in content and add ID
            element_text = content[element.start_pos:element.end_pos]
            updated_element = self._add_id_to_element(element_text, generated_id)
            
            # Replace in content
            updated_content = (
                updated_content[:element.start_pos] + 
                updated_element + 
                updated_content[element.end_pos:]
            )
        
        return updated_content
    
    def _add_id_to_element(self, element_html: str, id_value: str) -> str:
        """Add ID attribute to an element's HTML/JSX"""
        # Find the opening tag
        tag_match = re.match(r'<(\w+)([^>]*?)(/?>)', element_html, re.DOTALL)
        if not tag_match:
            return element_html
        
        tag_name = tag_match.group(1)
        attributes = tag_match.group(2)
        closing = tag_match.group(3)
        
        # Add ID attribute
        if attributes.strip():
            # Insert ID after existing attributes
            new_attributes = f'{attributes} id="{id_value}"'
        else:
            # No existing attributes
            new_attributes = f' id="{id_value}"'
        
        # Reconstruct the opening tag
        new_opening_tag = f'<{tag_name}{new_attributes}{closing}'
        
        # Replace in original element
        return element_html.replace(tag_match.group(0), new_opening_tag, 1)
    
    def _print_changes_preview(self, file_path: Path, elements: List[Element]):
        """Print preview of changes for dry run"""
        print(f"\n{file_path.name}:")
        for element in elements:
            element_preview = element.text_content[:30] + "..." if len(element.text_content) > 30 else element.text_content
            print(f"  - {element.tag} element: '{element_preview}' -> would get ID")
    
    def reset_for_new_file(self):
        """Reset state for processing a new file"""
        self.id_generator.reset_used_ids()