#!/usr/bin/env python3
"""
Enhanced Parameter Mapper Module
Provides intelligent parameter mapping for route handlers based on HTTP method, path, and handler name patterns.
"""

from typing import Dict, List, Tuple
import re


class ParameterMapper:
    """Intelligent parameter mapping for route handlers"""
    
    def __init__(self):
        self.method_patterns = {
            'GET': self._handle_get_method,
            'POST': self._handle_post_method,
            'PUT': self._handle_put_method,
            'PATCH': self._handle_patch_method,
            'DELETE': self._handle_delete_method
        }
        
        # Special handler patterns that need custom parameter mapping
        self.special_handlers = {
            'updateUserSettings': 'req.user.id, req.body',
            'updateUserPreferences': 'req.user.id, req.body',
            'updateUserProfile': 'req.user.id, req.body',
            'getUserSettings': 'req.user.id',
            'getUserPreferences': 'req.user.id',
            'getUserProfile': 'req.user.id',
            'enrollInPath': 'req.params.id, req.user.id',
            'updateProgress': 'req.params.id, req.user.id, req.body',
        }
        
        # Path-specific handler overrides for special cases
        self.path_handler_overrides = {
            # Progress update without ID parameter (uses userId from body)
            ('PUT', '/update', 'updateProgress'): 'req.user.id, req.body',
            # Progress update with ID parameter (path ID, user ID, body)
            ('PUT', '/:id/progress', 'updateProgress'): 'req.params.id, req.user.id, req.body',
            # Tutorial completion only needs the ID
            ('POST', '/:id/complete', 'completeTutorial'): 'req.params.id',
        }
        
    def get_parameters(self, method: str, path: str, handler_name: str) -> str:
        """
        Get the appropriate parameters for a route handler
        
        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            path: Route path (e.g., '/', '/:id', '/:id/complete')
            handler_name: Handler method name (e.g., 'updateAchievement', 'getUser')
            
        Returns:
            String of parameters to pass to the handler
        """
        # Check for path-specific overrides first (most specific)
        override_key = (method.upper(), path, handler_name)
        if override_key in self.path_handler_overrides:
            return self.path_handler_overrides[override_key]
        
        # Check for special handlers (handler name specific)
        if handler_name in self.special_handlers:
            return self.special_handlers[handler_name]
        
        # Use method-specific logic
        method_upper = method.upper()
        if method_upper in self.method_patterns:
            return self.method_patterns[method_upper](path, handler_name)
        
        # Fallback for unknown methods
        return self._fallback_handler(path, handler_name)
    
    def _handle_get_method(self, path: str, handler_name: str) -> str:
        """Handle GET method parameter mapping"""
        if ':id' in path:
            return 'req.params.id'
        return ''
    
    def _handle_post_method(self, path: str, handler_name: str) -> str:
        """Handle POST method parameter mapping"""
        if ':id' in path:
            # POST with :id usually means action on existing resource
            if handler_name.startswith('create'):
                # Creating sub-resource: POST /:parentId/children
                return 'req.params.id, req.body'
            else:
                # Action on existing resource: POST /:id/complete
                return 'req.params.id, req.body'
        else:
            # Regular creation: POST /
            return 'req.body'
    
    def _handle_put_method(self, path: str, handler_name: str) -> str:
        """Handle PUT method parameter mapping"""
        if ':id' in path:
            return 'req.params.id, req.body'
        else:
            return 'req.body'
    
    def _handle_patch_method(self, path: str, handler_name: str) -> str:
        """Handle PATCH method parameter mapping"""
        if ':id' in path:
            return 'req.params.id, req.body'
        else:
            return 'req.body'
    
    def _handle_delete_method(self, path: str, handler_name: str) -> str:
        """Handle DELETE method parameter mapping"""
        if ':id' in path:
            return 'req.params.id'
        else:
            return 'req.body'  # Bulk delete with filters
    
    def _fallback_handler(self, path: str, handler_name: str) -> str:
        """Fallback parameter mapping for unknown methods"""
        if ':id' in path:
            if handler_name.startswith(('update', 'enroll', 'cancel', 'modify', 'edit')):
                return 'req.params.id, req.body'
            elif handler_name.startswith(('delete', 'remove')):
                return 'req.params.id'
            elif handler_name.startswith('get'):
                return 'req.params.id'
            else:
                return 'req.params.id, req.body'
        else:
            if handler_name.startswith('get'):
                return ''
            else:
                return 'req.body'
    
    def analyze_pattern(self, method: str, path: str, handler_name: str) -> Dict[str, str]:
        """
        Analyze a route pattern and return detailed mapping information
        
        Returns:
            Dictionary with analysis details for debugging
        """
        return {
            'method': method,
            'path': path,
            'handler_name': handler_name,
            'has_id_param': ':id' in path,
            'parameters': self.get_parameters(method, path, handler_name),
            'pattern_type': self._get_pattern_type(method, path, handler_name)
        }
    
    def _get_pattern_type(self, method: str, path: str, handler_name: str) -> str:
        """Classify the route pattern type for debugging"""
        if handler_name in self.special_handlers:
            return 'special_handler'
        elif ':id' in path:
            if method.upper() in ['PUT', 'PATCH']:
                return 'update_by_id'
            elif method.upper() == 'DELETE':
                return 'delete_by_id'
            elif method.upper() == 'GET':
                return 'get_by_id'
            elif method.upper() == 'POST':
                return 'action_by_id'
        else:
            if method.upper() == 'GET':
                return 'list_all'
            elif method.upper() == 'POST':
                return 'create_new'
            else:
                return 'bulk_operation'
        
        return 'unknown'


# Global instance for use in generators
parameter_mapper = ParameterMapper()


def get_route_parameters(method: str, path: str, handler_name: str) -> str:
    """Convenience function to get route parameters"""
    return parameter_mapper.get_parameters(method, path, handler_name)


if __name__ == "__main__":
    # Test the parameter mapper
    mapper = ParameterMapper()
    
    test_cases = [
        ('PUT', '/:id', 'updateAchievement'),
        ('GET', '/:id', 'getAchievementById'),
        ('POST', '/', 'createAchievement'),
        ('DELETE', '/:id', 'deleteAchievement'),
        ('POST', '/:id/complete', 'completeTutorial'),  # Should be req.params.id only
        ('PUT', '/update', 'updateProgress'),  # Should be req.body.userId, req.body
        ('GET', '/', 'getAllAchievements'),
        ('PUT', '/settings', 'updateUserSettings'),
        ('GET', '/profile', 'getUserProfile'),
        ('PUT', '/profile', 'updateUserProfile'),
        ('GET', '/preferences', 'getUserPreferences'),
        ('PUT', '/preferences', 'updateUserPreferences'),
        ('GET', '/settings', 'getUserSettings'),
    ]
    
    print("Parameter Mapping Test Results:")
    print("=" * 50)
    
    for method, path, handler in test_cases:
        analysis = mapper.analyze_pattern(method, path, handler)
        print(f"{method:6} {path:15} {handler:20} -> {analysis['parameters']:20} ({analysis['pattern_type']})")