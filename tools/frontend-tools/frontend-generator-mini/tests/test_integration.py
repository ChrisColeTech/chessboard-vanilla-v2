#!/usr/bin/env python3
"""
Integration tests for the complete Frontend Generator Mini system
"""

import unittest
import sys
import tempfile
import shutil
import json
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent / "shared"))

from generators.services.services_generator_new import ServicesGenerator
from generators.types.types_generator_new import TypesGenerator
from generators.hooks.hooks_generator_new import HooksGenerator
from generators.pages.pages_generator_new import PagesGenerator
from generators.components.components_generator_new import ComponentsGenerator


class TestCompleteChessAppGeneration(unittest.TestCase):
    """Test complete chess application generation"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Initialize all generators
        self.services_gen = ServicesGenerator(self.test_dir)
        self.types_gen = TypesGenerator(self.test_dir)
        self.hooks_gen = HooksGenerator(self.test_dir)
        self.pages_gen = PagesGenerator(self.test_dir)
        self.components_gen = ComponentsGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_complete_chess_app_generation(self):
        """Test generating a complete chess application from backend config"""
        
        # Realistic chess backend configuration
        chess_entities = {
            'games': {
                'entity': 'Game',
                'properties': {
                    'id': 'string',
                    'user_id': 'string',
                    'ai_level': 'number',
                    'user_color': 'string',
                    'ai_color': 'string',
                    'current_fen': 'string',
                    'pgn': 'string',
                    'status': 'string',
                    'result': 'string',
                    'time_control': 'string',
                    'started_at': 'datetime',
                    'completed_at': 'datetime',
                    'created_at': 'datetime',
                    'updated_at': 'datetime'
                },
                'methods': ['createGame', 'getGameById', 'listGames', 'updateGame', 'deleteGame']
            },
            'puzzles': {
                'entity': 'Puzzle',
                'properties': {
                    'id': 'string',
                    'title': 'string',
                    'description': 'text',
                    'fen_position': 'string',
                    'solution_moves': 'string',
                    'difficulty': 'number',
                    'rating': 'number',
                    'tags': 'json',
                    'created_at': 'datetime',
                    'updated_at': 'datetime'
                },
                'methods': ['createPuzzle', 'getPuzzleById', 'listPuzzles', 'updatePuzzle', 'deletePuzzle']
            },
            'puzzle_attempts': {
                'entity': 'PuzzleAttempt',
                'properties': {
                    'id': 'string',
                    'user_id': 'string',
                    'puzzle_id': 'string',
                    'solved': 'boolean',
                    'time_taken': 'number',
                    'attempts_count': 'number',
                    'created_at': 'datetime'
                },
                'methods': ['createPuzzleAttempt', 'getPuzzleAttemptById', 'listPuzzleAttempts']
            },
            'openings': {
                'entity': 'Opening',
                'properties': {
                    'id': 'string',
                    'name': 'string',
                    'eco_code': 'string',
                    'moves': 'string',
                    'description': 'text',
                    'popularity': 'number',
                    'created_at': 'datetime',
                    'updated_at': 'datetime'
                },
                'methods': ['createOpening', 'getOpeningById', 'listOpenings', 'updateOpening', 'deleteOpening']
            },
            'user_profiles': {
                'entity': 'UserProfile',
                'properties': {
                    'id': 'string',
                    'user_id': 'string',
                    'username': 'string',
                    'email': 'string',
                    'rating': 'number',
                    'games_played': 'number',
                    'games_won': 'number',
                    'puzzles_solved': 'number',
                    'preferred_time_control': 'string',
                    'created_at': 'datetime',
                    'updated_at': 'datetime'
                },
                'methods': ['createUserProfile', 'getUserProfileById', 'updateUserProfile', 'deleteUserProfile']
            },
            'achievements': {
                'entity': 'Achievement',
                'properties': {
                    'id': 'string',
                    'name': 'string',
                    'description': 'text',
                    'icon': 'string',
                    'criteria': 'json',
                    'points': 'number',
                    'rarity': 'string',
                    'created_at': 'datetime'
                },
                'methods': ['createAchievement', 'getAchievementById', 'listAchievements']
            }
        }
        
        # Generate all entities across different domains
        domain_mapping = {
            'games': 'chess',
            'puzzles': 'training',
            'puzzle_attempts': 'training',
            'openings': 'theory',
            'user_profiles': 'user',
            'achievements': 'gamification'
        }
        
        # Generate all components for each entity
        for endpoint_name, config in chess_entities.items():
            domain = domain_mapping[endpoint_name]
            
            # Generate all layers
            self.services_gen.generate(endpoint_name, config, domain)
            self.types_gen.generate(endpoint_name, config, domain)
            self.hooks_gen.generate(endpoint_name, config, domain)
            self.pages_gen.generate(endpoint_name, config, domain)
            self.components_gen.generate(endpoint_name, config, domain)
        
        # Generate barrel exports
        self.types_gen.generate_barrel_exports()
        
        # Verify complete file structure was created
        self._verify_complete_structure()
        
        # Verify cross-entity consistency
        self._verify_cross_entity_consistency()
        
        # Verify chess-specific logic
        self._verify_chess_specific_features()
        
        print("🎉 Complete chess application generated successfully!")
    
    def _verify_complete_structure(self):
        """Verify that all expected files were created"""
        
        # Expected domains
        expected_domains = ['chess', 'training', 'theory', 'user', 'gamification']
        
        # Verify services structure
        services_dir = self.test_dir / "services"
        for domain in expected_domains:
            domain_dir = services_dir / domain
            self.assertTrue(domain_dir.exists(), f"Services domain directory missing: {domain}")
        
        # Verify types structure  
        types_dir = self.test_dir / "types"
        for domain in expected_domains:
            domain_dir = types_dir / domain
            self.assertTrue(domain_dir.exists(), f"Types domain directory missing: {domain}")
        
        # Verify barrel exports were created
        main_types_barrel = types_dir / "index.ts"
        self.assertTrue(main_types_barrel.exists(), "Main types barrel export missing")
        
        # Verify hooks structure
        hooks_dir = self.test_dir / "hooks"
        for domain in expected_domains:
            domain_dir = hooks_dir / domain
            self.assertTrue(domain_dir.exists(), f"Hooks domain directory missing: {domain}")
        
        # Verify pages structure
        pages_dir = self.test_dir / "pages"
        for domain in expected_domains:
            domain_dir = pages_dir / domain
            self.assertTrue(domain_dir.exists(), f"Pages domain directory missing: {domain}")
        
        # Verify components structure
        components_dir = self.test_dir / "components"
        for domain in expected_domains:
            domain_dir = components_dir / domain
            self.assertTrue(domain_dir.exists(), f"Components domain directory missing: {domain}")
    
    def _verify_cross_entity_consistency(self):
        """Verify consistency across all generated entities"""
        
        # Test games entity consistency
        self._verify_entity_consistency('games', 'Game', 'chess')
        
        # Test puzzles entity consistency
        self._verify_entity_consistency('puzzles', 'Puzzle', 'training')
        
        # Test user profiles entity consistency
        self._verify_entity_consistency('user_profiles', 'UserProfile', 'user')
    
    def _verify_entity_consistency(self, endpoint_name: str, entity_name: str, domain: str):
        """Verify consistency for a specific entity across all layers"""
        
        # Service file
        service_file = self.test_dir / "services" / domain / f"{endpoint_name}Service.ts"
        self.assertTrue(service_file.exists())
        
        with open(service_file, 'r') as f:
            service_content = f.read()
        
        # Verify service imports types correctly
        self.assertIn(f"import type {{ {entity_name} }} from '../../types/{domain}/{endpoint_name}';", service_content)
        self.assertIn(f"class {entity_name}Service", service_content)
        self.assertIn(f"export const {endpoint_name}Service", service_content)
        
        # Types file
        types_file = self.test_dir / "types" / domain / f"{endpoint_name}.ts"
        self.assertTrue(types_file.exists())
        
        with open(types_file, 'r') as f:
            types_content = f.read()
        
        self.assertIn(f"export interface {entity_name} {{", types_content)
        self.assertIn(f"export interface {entity_name}Create {{", types_content)
        self.assertIn(f"export interface {entity_name}Update {{", types_content)
        self.assertIn(f"export default {entity_name};", types_content)
        
        # Hook file
        hook_file = self.test_dir / "hooks" / domain / f"use{entity_name}.ts"
        self.assertTrue(hook_file.exists())
        
        with open(hook_file, 'r') as f:
            hook_content = f.read()
        
        self.assertIn(f"import type {{ {entity_name} }} from '../../types/{domain}/{endpoint_name}';", hook_content)
        self.assertIn(f"import {endpoint_name}Service from '../../services/{domain}/{endpoint_name}Service';", hook_content)
        self.assertIn(f"export const use{entity_name} = () => {{", hook_content)
        
        # Page files
        page_file = self.test_dir / "pages" / domain / f"{entity_name}Page.tsx"
        self.assertTrue(page_file.exists())
        
        with open(page_file, 'r') as f:
            page_content = f.read()
        
        self.assertIn(f"import {{ use{entity_name} }} from '../../hooks/{domain}/use{entity_name}';", page_content)
        
        # Component files
        list_component = self.test_dir / "components" / domain / f"{entity_name}List.tsx"
        self.assertTrue(list_component.exists())
        
        with open(list_component, 'r') as f:
            component_content = f.read()
        
        self.assertIn(f"import type {{ {entity_name} }} from '../../types/{domain}/{endpoint_name}';", component_content)
    
    def _verify_chess_specific_features(self):
        """Verify chess-specific features are correctly generated"""
        
        # Verify Game entity has chess-specific properties
        games_types_file = self.test_dir / "types" / "chess" / "games.ts"
        with open(games_types_file, 'r') as f:
            content = f.read()
        
        # Check for chess-specific properties (converted to camelCase)
        self.assertIn('currentFen: string;', content)
        self.assertIn('pgn: string;', content)
        self.assertIn('userColor: string;', content)
        self.assertIn('aILevel: number;', content)  # Note: ai_level -> aILevel
        
        # Verify Puzzle entity has puzzle-specific properties
        puzzles_types_file = self.test_dir / "types" / "training" / "puzzles.ts"
        with open(puzzles_types_file, 'r') as f:
            content = f.read()
        
        self.assertIn('fenPosition: string;', content)
        self.assertIn('solutionMoves: string;', content)
        self.assertIn('difficulty: number;', content)
        self.assertIn('rating: number;', content)
        
        # Verify Opening entity has theory-specific properties  
        openings_types_file = self.test_dir / "types" / "theory" / "openings.ts"
        with open(openings_types_file, 'r') as f:
            content = f.read()
        
        self.assertIn('ecoCode: string;', content)
        self.assertIn('moves: string;', content)
        self.assertIn('popularity: number;', content)
    
    def test_name_standardization_across_system(self):
        """Test that name standardization is consistent across the entire system"""
        
        # Generate a test entity with various naming challenges
        test_config = {
            'entity': 'ChessGameAnalysis',
            'properties': {
                'game_id': 'string',
                'ai_evaluation': 'number',
                'best_move': 'string',
                'worst_move': 'string',
                'opening_name': 'string',
                'end_game_type': 'string'
            },
            'methods': ['createChessGameAnalysis', 'getChessGameAnalysisByGameId']
        }
        
        # Generate all components
        self.services_gen.generate('chess_game_analyses', test_config, 'analysis')
        self.types_gen.generate('chess_game_analyses', test_config, 'analysis')
        self.hooks_gen.generate('chess_game_analyses', test_config, 'analysis')
        
        # Verify consistent naming
        service_file = self.test_dir / "services" / "analysis" / "chessGameAnalysesService.ts"
        types_file = self.test_dir / "types" / "analysis" / "chessGameAnalyses.ts"
        hook_file = self.test_dir / "hooks" / "analysis" / "useChessGameAnalysis.ts"
        
        # All files should exist
        self.assertTrue(service_file.exists())
        self.assertTrue(types_file.exists())
        self.assertTrue(hook_file.exists())
        
        # Check property name conversion consistency
        with open(types_file, 'r') as f:
            types_content = f.read()
        
        # snake_case should be converted to camelCase consistently
        self.assertIn('gameId: string;', types_content)
        self.assertIn('aIEvaluation: number;', types_content)  # ai_evaluation -> aIEvaluation
        self.assertIn('bestMove: string;', types_content)
        self.assertIn('worstMove: string;', types_content)
        self.assertIn('openingName: string;', types_content)
        self.assertIn('endGameType: string;', types_content)
        
        print("✅ Name standardization verified across complete system")


class TestGeneratorOrchestration(unittest.TestCase):
    """Test orchestration of multiple generators"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generator_execution_order(self):
        """Test that generators can be run in any order without conflicts"""
        
        # Simple test config
        config = {
            'entity': 'TestEntity',
            'properties': {'id': 'string', 'name': 'string'},
            'methods': ['createTestEntity', 'getTestEntityById']
        }
        
        # Test different execution orders
        orders = [
            [ServicesGenerator, TypesGenerator, HooksGenerator],
            [TypesGenerator, ServicesGenerator, HooksGenerator],
            [HooksGenerator, TypesGenerator, ServicesGenerator]
        ]
        
        for order in orders:
            test_subdir = self.test_dir / f"test_{len(order)}"
            test_subdir.mkdir()
            
            # Execute generators in this order
            for generator_class in order:
                generator = generator_class(test_subdir)
                generator.generate('test_entities', config, 'test')
            
            # Verify all files were created regardless of order
            self.assertTrue((test_subdir / "services" / "test" / "testEntitiesService.ts").exists())
            self.assertTrue((test_subdir / "types" / "test" / "testEntities.ts").exists())
            self.assertTrue((test_subdir / "hooks" / "test" / "useTestEntity.ts").exists())


if __name__ == '__main__':
    unittest.main()