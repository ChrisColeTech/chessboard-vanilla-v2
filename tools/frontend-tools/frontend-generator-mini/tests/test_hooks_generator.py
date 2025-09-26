#!/usr/bin/env python3
"""
Tests for the Hooks Generator using template engine and name standardizer
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent / "shared"))

from generators.hooks.hooks_generator_new import HooksGenerator


class TestHooksGenerator(unittest.TestCase):
    """Test the Hooks Generator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.generator = HooksGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generate_game_hook(self):
        """Test generating Game hook"""
        endpoint_config = {
            'entity': 'Game',
            'methods': ['createGame', 'getGameById', 'listGames', 'updateGame', 'deleteGame']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        # Check if file was created
        expected_file = self.test_dir / "hooks" / "chess" / "useGame.ts"
        self.assertTrue(expected_file.exists(), f"Expected file not found: {expected_file}")
        
        # Check content
        with open(expected_file, 'r') as f:
            content = f.read()
            
        # Verify key components are present
        self.assertIn('export const useGame = () => {', content)
        self.assertIn('const [games, setGames] = useState<Game[]>([]);', content)
        self.assertIn('const [game, setGame] = useState<Game | null>(null);', content)
        self.assertIn('const [loading, setLoading] = useState(false);', content)
        self.assertIn('const [error, setError] = useState<string | null>(null);', content)
        
        # Check method implementations
        self.assertIn('const createGame = useCallback(async (data: any) => {', content)
        self.assertIn('const getGameById = useCallback(async (id: string) => {', content)
        self.assertIn('const listGames = useCallback(async () => {', content)
        self.assertIn('const updateGame = useCallback(async (id: string, data: any) => {', content)
        self.assertIn('const deleteGame = useCallback(async (id: string) => {', content)
        
        # Check return object
        self.assertIn('games,', content)
        self.assertIn('game,', content)
        self.assertIn('loading,', content)
        self.assertIn('error', content)
        self.assertIn('createGame', content)
        self.assertIn('getGameById', content)
        self.assertIn('listGames', content)
        self.assertIn('updateGame', content)
        self.assertIn('deleteGame', content)
    
    def test_import_determination(self):
        """Test React hook imports are determined correctly"""
        # Test with list methods (should include useEffect)
        endpoint_config = {
            'entity': 'Game',
            'methods': ['listGames', 'createGame']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        expected_file = self.test_dir / "hooks" / "chess" / "useGame.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Should import useEffect for auto-loading
        self.assertIn('import { useState, useCallback, useEffect } from \'react\';', content)
        self.assertIn('useEffect(() => {', content)
        self.assertIn('listGames();', content)
    
    def test_crud_methods_state_management(self):
        """Test CRUD methods update state correctly"""
        endpoint_config = {
            'entity': 'Puzzle',
            'methods': ['createPuzzle', 'updatePuzzle', 'deletePuzzle']
        }
        
        self.generator.generate('puzzles', endpoint_config, 'training')
        
        expected_file = self.test_dir / "hooks" / "training" / "usePuzzle.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check create method updates state
        self.assertIn('setPuzzles(prev => [...prev, newPuzzle]);', content)
        
        # Check update method updates state
        self.assertIn('setPuzzles(prev => prev.map(item =>', content)
        self.assertIn('item.id === id ? updatedPuzzle : item', content)
        
        # Check delete method updates state
        self.assertIn('setPuzzles(prev => prev.filter(item => item.id !== id));', content)
        self.assertIn('if (puzzle?.id === id) {', content)
        self.assertIn('setPuzzle(null);', content)
    
    def test_auth_methods_special_handling(self):
        """Test authentication methods have special handling"""
        endpoint_config = {
            'entity': 'User',
            'methods': ['login', 'register', 'logout', 'getCurrentUser']
        }
        
        self.generator.generate('auth', endpoint_config, 'auth')
        
        expected_file = self.test_dir / "hooks" / "auth" / "useUser.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check login method
        self.assertIn('const login = useCallback(async (credentials: any) => {', content)
        self.assertIn('authService.login(credentials);', content)
        
        # Check register method
        self.assertIn('const register = useCallback(async (userData: any) => {', content)
        self.assertIn('authService.register(userData);', content)
        
        # Check logout method
        self.assertIn('const logout = useCallback(async () => {', content)
        self.assertIn('setUser(null);', content)
        
        # Check getCurrentUser method
        self.assertIn('const getCurrentUser = useCallback(async () => {', content)
        self.assertIn('setUser(user);', content)
    
    def test_error_handling_implementation(self):
        """Test error handling is properly implemented"""
        endpoint_config = {
            'entity': 'Game',
            'methods': ['createGame']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        expected_file = self.test_dir / "hooks" / "chess" / "useGame.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check error handler function
        self.assertIn('const handleError = useCallback((err: any) => {', content)
        self.assertIn('const errorMessage = err?.message || \'An unexpected error occurred\';', content)
        self.assertIn('setError(errorMessage);', content)
        self.assertIn('setLoading(false);', content)
        self.assertIn('console.error(\'API Error:\', err);', content)
        
        # Check error handling in methods
        self.assertIn('} catch (err) {', content)
        self.assertIn('handleError(err);', content)
        self.assertIn('throw err;', content)
    
    def test_loading_state_management(self):
        """Test loading state is managed correctly"""
        endpoint_config = {
            'entity': 'Game',
            'methods': ['createGame', 'getGameById']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        expected_file = self.test_dir / "hooks" / "chess" / "useGame.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check loading is set at start of operations
        self.assertIn('setLoading(true);', content)
        self.assertIn('setError(null);', content)
        
        # Check loading is cleared on success
        self.assertIn('setLoading(false);', content)
    
    def test_special_routing_skip(self):
        """Test that special routing endpoints are skipped"""
        endpoint_config = {
            'entity': 'Auth',
            'special_routing': True,
            'methods': ['login', 'register']
        }
        
        self.generator.generate('auth', endpoint_config, 'auth')
        
        # Should not create file due to special routing
        expected_file = self.test_dir / "hooks" / "auth" / "useAuth.ts"
        self.assertFalse(expected_file.exists())
    
    def test_name_standardization(self):
        """Test name standardization is applied correctly"""
        endpoint_config = {
            'entity': 'UserProfile',
            'methods': ['createUserProfile', 'getUserProfileById']
        }
        
        self.generator.generate('user_profiles', endpoint_config, 'user')
        
        expected_file = self.test_dir / "hooks" / "user" / "useUserProfile.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check camelCase service name
        self.assertIn('userProfilesService.createUserProfile', content)
        self.assertIn('userProfilesService.getUserProfileById', content)
        
        # Check state variable names
        self.assertIn('userprofiles, setUserProfiles', content)
        self.assertIn('userprofile, setUserProfile', content)


if __name__ == '__main__':
    unittest.main()