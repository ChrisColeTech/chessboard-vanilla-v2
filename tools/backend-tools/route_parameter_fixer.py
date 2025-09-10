#!/usr/bin/env python3
"""
Route Parameter Fixer
Fixes remaining TypeScript compilation errors by correcting parameter calls in route files
"""

import os
import re
from pathlib import Path


class RouteParameterFixer:
    def __init__(self, routes_path: str):
        self.routes_path = Path(routes_path)
        
    def fix_all_routes(self):
        """Fix parameter issues in all route files"""
        route_files = list(self.routes_path.glob('*.ts'))
        
        for route_file in route_files:
            if route_file.name == 'index.ts':
                continue
                
            self.fix_route_file(route_file)
            print(f"✅ Fixed parameters in {route_file.name}")
    
    def fix_route_file(self, file_path: Path):
        """Fix parameter issues in a single route file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match update* method calls with PUT /:id that only have req.params.id
        # This matches: methodName.updateSomething(req.params.id)
        # In the context of PUT /:id routes
        update_pattern = r'(router\.put\([\'"]/:id[\'"].*?await\s+\w+Service\.)(\w*update\w*)(\(req\.params\.id\))'
        
        def replace_update_call(match):
            prefix = match.group(1)
            method_name = match.group(2) 
            old_params = match.group(3)
            return f"{prefix}{method_name}(req.params.id, req.body)"
        
        content = re.sub(update_pattern, replace_update_call, content, flags=re.DOTALL)
        
        # Also handle enroll methods
        enroll_pattern = r'(router\.post\([\'"]/:id/\w+[\'"].*?await\s+\w+Service\.)(\w*enroll\w*|\w*update\w*)(\(req\.params\.id\))'
        content = re.sub(enroll_pattern, replace_update_call, content, flags=re.DOTALL)
        
        # Handle other POST /:id/* patterns that should have both parameters
        post_id_pattern = r'(router\.post\([\'"]/:id/[^\'\"]+[\'"].*?await\s+\w+Service\.)(\w+)(\(req\.params\.id\))'
        content = re.sub(post_id_pattern, replace_update_call, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)


def main():
    """Main function to fix route parameters"""
    backend_path = "/mnt/c/Projects/chessboard-vanilla-v2/backend-v2/src/routes"
    
    print("🔧 Route Parameter Fixer Starting...")
    fixer = RouteParameterFixer(backend_path)
    fixer.fix_all_routes()
    print("✅ All route parameter fixes completed!")


if __name__ == "__main__":
    main()