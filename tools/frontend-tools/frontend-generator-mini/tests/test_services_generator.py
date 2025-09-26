#!/usr/bin/env python3
"""
Tests for the Services Generator using template engine
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent / "generators"))
sys.path.append(str(Path(__file__).parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent / "shared"))

from services.services_generator_new import ServicesGenerator


class TestServicesGenerator(unittest.TestCase):
    """Test the Services Generator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.generator = ServicesGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generate_games_service(self):
        """Test generating a games service"""
        endpoint_config = {
            'entity': 'Game',
            'methods': ['createGame', 'getGameById', 'listGames', 'updateGame', 'deleteGame']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        # Check if file was created
        expected_file = self.test_dir / "services" / "chess" / "gamesService.ts"
        self.assertTrue(expected_file.exists(), f"Expected file not found: {expected_file}")
        
        # Check content
        with open(expected_file, 'r') as f:
            content = f.read()
            
        # Verify key components are present
        self.assertIn('class GameService', content)
        self.assertIn('async createGame', content)
        self.assertIn('async getGameById', content)
        self.assertIn('async listGames', content)
        self.assertIn('async updateGame', content)
        self.assertIn('async deleteGame', content)
        self.assertIn('export const gameService', content)
        self.assertIn("import type { Game } from '../../types/chess/games'", content)
    
    def test_generate_puzzles_service(self):
        """Test generating a puzzles service"""
        endpoint_config = {
            'entity': 'Puzzle',
            'methods': ['createPuzzle', 'getPuzzleById', 'listPuzzles']
        }
        
        self.generator.generate('puzzles', endpoint_config, 'training')
        
        # Check if file was created
        expected_file = self.test_dir / "services" / "training" / "puzzlesService.ts"
        self.assertTrue(expected_file.exists())
        
        # Check content
        with open(expected_file, 'r') as f:
            content = f.read()
            
        self.assertIn('class PuzzleService', content)
        self.assertIn('async createPuzzle', content)
        self.assertIn('async getPuzzleById', content)
        self.assertIn('async listPuzzles', content)
        self.assertIn('export const puzzlesService', content)
    
    def test_snake_to_camel_conversion(self):
        """Test snake_case to camelCase conversion"""
        endpoint_config = {
            'entity': 'UserProfile',
            'methods': ['createUserProfile']
        }
        
        self.generator.generate('user_profiles', endpoint_config, 'user')
        
        # Check if file was created with correct camelCase name
        expected_file = self.test_dir / "services" / "user" / "userProfilesService.ts"
        self.assertTrue(expected_file.exists())
        
        # Check that imports use camelCase
        with open(expected_file, 'r') as f:
            content = f.read()
            
        self.assertIn("import type { UserProfile } from '../../types/user/userProfiles'", content)
    
    def test_method_generation_types(self):
        """Test different method types generate correct implementations"""
        endpoint_config = {
            'entity': 'TestEntity',
            'methods': ['createTestEntity', 'getTestEntityById', 'listTestEntities', 'updateTestEntity', 'deleteTestEntity']
        }
        
        self.generator.generate('test_entities', endpoint_config, 'test')
        
        expected_file = self.test_dir / "services" / "test" / "testEntitiesService.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check create method
        self.assertIn('method: \'POST\'', content)
        self.assertIn('body: JSON.stringify(data)', content)
        
        # Check get by id method
        self.assertIn('async getTestEntityById(id: string)', content)
        self.assertIn('/test_entities/${id}', content)
        
        # Check list method
        self.assertIn('Promise<TestEntity[]>', content)
        
        # Check update method
        self.assertIn('method: \'PUT\'', content)
        
        # Check delete method
        self.assertIn('method: \'DELETE\'', content)
        self.assertIn('Promise<void>', content)
    
    def test_special_routing_skip(self):
        """Test that special routing endpoints are skipped"""
        endpoint_config = {
            'entity': 'Auth',
            'special_routing': True,
            'methods': ['login', 'register']
        }
        
        self.generator.generate('auth', endpoint_config, 'auth')
        
        # Should not create file due to special routing
        expected_file = self.test_dir / "services" / "auth" / "authService.ts"
        self.assertFalse(expected_file.exists())


class TestServiceGeneratorIntegration(unittest.TestCase):
    """Integration tests using real backend config data"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.generator = ServicesGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_chess_backend_entities(self):
        """Test with entities from actual chess backend config"""
        # Test games entity
        games_config = {
            'entity': 'Game',
            'methods': ['createGame', 'getGameById', 'updateGame', 'deleteGame', 'listGames']
        }
        
        # Test puzzles entity
        puzzles_config = {
            'entity': 'Puzzle', 
            'methods': ['createPuzzle', 'getPuzzleById', 'updatePuzzle', 'deletePuzzle', 'listPuzzles']
        }
        
        # Test openings entity
        openings_config = {
            'entity': 'Opening',
            'methods': ['createOpening', 'getOpeningById', 'updateOpening', 'deleteOpening', 'listOpenings']
        }
        
        # Generate all services
        self.generator.generate('games', games_config, 'chess')
        self.generator.generate('puzzles', puzzles_config, 'training')
        self.generator.generate('openings', openings_config, 'theory')
        
        # Verify all files were created
        games_file = self.test_dir / "services" / "chess" / "gamesService.ts"
        puzzles_file = self.test_dir / "services" / "training" / "puzzlesService.ts"
        openings_file = self.test_dir / "services" / "theory" / "openingsService.ts"
        
        self.assertTrue(games_file.exists())
        self.assertTrue(puzzles_file.exists())
        self.assertTrue(openings_file.exists())
        
        # Verify proper domain organization
        self.assertTrue((self.test_dir / "services" / "chess").exists())
        self.assertTrue((self.test_dir / "services" / "training").exists())
        self.assertTrue((self.test_dir / "services" / "theory").exists())


if __name__ == '__main__':
    unittest.main()