#!/usr/bin/env python3
"""
Integration Tests for Workflow Orchestrator

These tests generate real files in the tests directory to verify:
1. Complete application generation
2. Correct file and folder structure  
3. Cross-generator consistency
4. Chess training app generation
"""

import unittest
import sys
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))

from workflow_orchestrator import WorkflowOrchestrator


class TestWorkflowOrchestrator(unittest.TestCase):
    """Integration tests for the complete workflow orchestrator"""
    
    def setUp(self):
        """Set up test environment with real output directory"""
        # Use tests directory for real file output verification
        self.test_output = Path(__file__).parent / "integration_output"
        
        # Clean up any existing test output
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
        
        self.test_output.mkdir(parents=True)
        self.orchestrator = WorkflowOrchestrator(self.test_output)
    
    def tearDown(self):
        """Keep generated files for verification - don't clean up"""
        # Intentionally NOT cleaning up so we can verify the generated structure
        print(f"\n📁 Generated files available for verification at: {self.test_output}")
    
    def test_complete_chess_application_generation(self):
        """Test generating the complete chess training application"""
        print("\n🚀 Testing complete chess application generation...")
        
        result = self.orchestrator.generate_chess_training_app()
        
        # Verify generation was successful
        self.assertTrue(result['success'])
        self.assertIn('stats', result)
        self.assertIn('generated_files', result)
        
        # Verify statistics
        stats = result['stats']
        self.assertEqual(stats['services'], 5)  # 5 entities
        self.assertEqual(stats['types'], 5)     # 5 type files
        self.assertEqual(stats['hooks'], 5)     # 5 hook files
        self.assertEqual(stats['components'], 15)  # 3 components per entity × 5
        self.assertEqual(stats['pages'], 15)    # 3 pages per entity × 5
        
        # Verify domains
        expected_domains = {'chess', 'training', 'theory', 'user', 'gamification'}
        self.assertEqual(stats['domains'], expected_domains)
        
        # Print file structure for verification
        self._print_generated_structure()
        
        # Verify key directories exist
        self._verify_directory_structure()
        
        # Verify key files exist
        self._verify_key_files()
        
        # Verify file contents are correct
        self._verify_file_contents()
    
    def test_custom_backend_config_generation(self):
        """Test generating from custom backend configuration"""
        print("\n🔧 Testing custom backend configuration...")
        
        custom_config = {
            "tournaments": {
                "entity": "Tournament",
                "properties": {
                    "id": "string",
                    "name": "string",
                    "start_date": "datetime",
                    "end_date": "datetime",
                    "participants": "number"
                },
                "methods": ["createTournament", "getTournamentById", "listTournaments"]
            },
            "matches": {
                "entity": "Match",
                "properties": {
                    "id": "string",
                    "tournament_id": "string",
                    "player1_id": "string",
                    "player2_id": "string",
                    "result": "string"
                },
                "methods": ["createMatch", "getMatchById", "listMatches", "updateMatch"]
            }
        }
        
        custom_output = self.test_output / "custom_app"
        custom_orchestrator = WorkflowOrchestrator(custom_output)
        
        result = custom_orchestrator.generate_complete_application(custom_config)
        
        # Verify custom generation
        self.assertTrue(result['success'])
        stats = result['stats']
        self.assertEqual(stats['services'], 2)
        self.assertEqual(stats['types'], 2)
        self.assertEqual(stats['hooks'], 2)
        
        # Verify custom files exist
        self.assertTrue((custom_output / "services" / "other" / "tournamentsService.ts").exists())
        self.assertTrue((custom_output / "services" / "other" / "matchesService.ts").exists())
    
    def test_special_routing_entities_skipped(self):
        """Test that entities with special_routing are properly skipped"""
        print("\n🔀 Testing special routing entity handling...")
        
        config_with_special = {
            "games": {
                "entity": "Game",
                "properties": {"id": "string", "name": "string"},
                "methods": ["createGame", "listGames"]
            },
            "auth": {
                "entity": "Auth",
                "special_routing": True,
                "properties": {"token": "string"},
                "methods": ["login", "register"]
            }
        }
        
        special_output = self.test_output / "special_routing_app"
        special_orchestrator = WorkflowOrchestrator(special_output)
        
        result = special_orchestrator.generate_complete_application(config_with_special)
        
        # Should only generate for games, not auth
        stats = result['stats']
        self.assertEqual(stats['services'], 1)  # Only games
        
        # Verify auth files were NOT created
        auth_service = special_output / "services" / "other" / "authService.ts"
        self.assertFalse(auth_service.exists())
        
        # Verify games files WERE created
        games_service = special_output / "services" / "chess" / "gamesService.ts"
        self.assertTrue(games_service.exists())
    
    def test_config_validation(self):
        """Test backend configuration validation"""
        print("\n✅ Testing configuration validation...")
        
        # Test empty config
        with self.assertRaises(ValueError):
            self.orchestrator.generate_complete_application({})
        
        # Test invalid config structure
        with self.assertRaises(ValueError):
            self.orchestrator.generate_complete_application("not a dict")
        
        # Test missing entity field
        with self.assertRaises(ValueError):
            invalid_config = {
                "test": {
                    "methods": ["test"]
                    # Missing 'entity' field
                }
            }
            self.orchestrator.generate_complete_application(invalid_config)
        
        # Test missing methods field
        with self.assertRaises(ValueError):
            invalid_config = {
                "test": {
                    "entity": "Test"
                    # Missing 'methods' field
                }
            }
            self.orchestrator.generate_complete_application(invalid_config)
    
    def test_barrel_exports_generation(self):
        """Test that barrel export files are correctly generated"""
        print("\n📦 Testing barrel exports generation...")
        
        result = self.orchestrator.generate_chess_training_app()
        self.assertTrue(result['success'])
        
        # Check that index.ts files are created in each domain
        domains = ['chess', 'training', 'theory', 'user', 'gamification']
        
        for domain in domains:
            services_index = self.test_output / "services" / domain / "index.ts"
            types_index = self.test_output / "types" / domain / "index.ts" 
            hooks_index = self.test_output / "hooks" / domain / "index.ts"
            
            self.assertTrue(services_index.exists(), f"Services index missing for {domain}")
            self.assertTrue(types_index.exists(), f"Types index missing for {domain}")
            self.assertTrue(hooks_index.exists(), f"Hooks index missing for {domain}")
            
            # Verify barrel export content
            with open(services_index, 'r') as f:
                content = f.read()
                self.assertIn("Generated barrel exports", content)
                self.assertIn("export", content)
    
    def test_app_integration_generation(self):
        """Test that App.tsx integration file is generated"""
        print("\n🏗️ Testing App.tsx integration...")
        
        result = self.orchestrator.generate_chess_training_app()
        self.assertTrue(result['success'])
        
        app_file = self.test_output / "App.tsx"
        self.assertTrue(app_file.exists())
        
        # Verify App.tsx content
        with open(app_file, 'r') as f:
            content = f.read()
            self.assertIn("Generated App.tsx", content)
            self.assertIn("BrowserRouter", content)
            self.assertIn("Routes", content)
            self.assertIn("Route", content)
            
            # Should have routes for each domain
            self.assertIn('/chess', content)
            self.assertIn('/training', content)
            self.assertIn('/theory', content)
            self.assertIn('/user', content)
            self.assertIn('/gamification', content)
    
    def _verify_directory_structure(self):
        """Verify the generated directory structure is correct"""
        expected_dirs = [
            "services/chess",
            "services/training", 
            "services/theory",
            "services/user",
            "services/gamification",
            "types/chess",
            "types/training",
            "types/theory", 
            "types/user",
            "types/gamification",
            "hooks/chess",
            "hooks/training",
            "hooks/theory",
            "hooks/user", 
            "hooks/gamification",
            "components/chess",
            "components/training",
            "components/theory",
            "components/user",
            "components/gamification",
            "pages/chess",
            "pages/training", 
            "pages/theory",
            "pages/user",
            "pages/gamification"
        ]
        
        for dir_path in expected_dirs:
            full_path = self.test_output / dir_path
            self.assertTrue(full_path.exists(), f"Directory missing: {dir_path}")
            self.assertTrue(full_path.is_dir(), f"Path is not a directory: {dir_path}")
    
    def _verify_key_files(self):
        """Verify that key files are generated correctly"""
        # Service files
        self.assertTrue((self.test_output / "services/chess/gamesService.ts").exists())
        self.assertTrue((self.test_output / "services/training/puzzlesService.ts").exists())
        self.assertTrue((self.test_output / "services/theory/openingsService.ts").exists())
        
        # Type files
        self.assertTrue((self.test_output / "types/chess/games.ts").exists())
        self.assertTrue((self.test_output / "types/training/puzzles.ts").exists())
        self.assertTrue((self.test_output / "types/theory/openings.ts").exists())
        
        # Hook files
        self.assertTrue((self.test_output / "hooks/chess/useGame.ts").exists())
        self.assertTrue((self.test_output / "hooks/training/usePuzzle.ts").exists())
        self.assertTrue((self.test_output / "hooks/theory/useOpening.ts").exists())
        
        # Component files (List, Detail, Form for each entity)
        self.assertTrue((self.test_output / "components/chess/GameList.tsx").exists())
        self.assertTrue((self.test_output / "components/chess/GameDetail.tsx").exists())
        self.assertTrue((self.test_output / "components/chess/GameForm.tsx").exists())
        
        # Page files
        self.assertTrue((self.test_output / "pages/chess/GamePage.tsx").exists())
        self.assertTrue((self.test_output / "pages/chess/GameDetailPage.tsx").exists())
        self.assertTrue((self.test_output / "pages/chess/GameFormPage.tsx").exists())
        
        # App integration
        self.assertTrue((self.test_output / "App.tsx").exists())
    
    def _verify_file_contents(self):
        """Verify that generated file contents are correct"""
        # Check service file content
        games_service = self.test_output / "services/chess/gamesService.ts"
        with open(games_service, 'r') as f:
            content = f.read()
            self.assertIn("class GameService", content)
            self.assertIn("async createGame", content)
            self.assertIn("export const gameService", content)
        
        # Check type file content  
        games_types = self.test_output / "types/chess/games.ts"
        with open(games_types, 'r') as f:
            content = f.read()
            self.assertIn("export interface Game", content)
            self.assertIn("id: string", content)
            self.assertIn("userId: string", content)  # snake_case converted to camelCase
        
        # Check hook file content
        games_hook = self.test_output / "hooks/chess/useGame.ts"
        with open(games_hook, 'r') as f:
            content = f.read()
            self.assertIn("export const useGame", content)
            self.assertIn("useState", content)
            self.assertIn("gameService", content)
        
        # Check component file content
        games_list = self.test_output / "components/chess/GameList.tsx"
        with open(games_list, 'r') as f:
            content = f.read()
            self.assertIn("export const GameList", content)
            self.assertIn("interface GameListProps", content)
            self.assertIn("Game[]", content)
    
    def _print_generated_structure(self):
        """Print the generated file structure for manual verification"""
        print(f"\n📁 Generated File Structure in {self.test_output}:")
        
        def print_tree(directory, prefix="", max_depth=3, current_depth=0):
            if current_depth >= max_depth:
                return
                
            items = sorted(directory.iterdir())
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            
            # Print directories first
            for i, dir_path in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0
                print(f"{prefix}{'└── ' if is_last_dir else '├── '}{dir_path.name}/")
                
                extension = "    " if is_last_dir else "│   "
                print_tree(dir_path, prefix + extension, max_depth, current_depth + 1)
            
            # Print files
            for i, file_path in enumerate(files):
                is_last = i == len(files) - 1
                print(f"{prefix}{'└── ' if is_last else '├── '}{file_path.name}")
        
        print_tree(self.test_output)
        
        # Print summary
        all_files = list(self.test_output.rglob("*"))
        file_count = len([f for f in all_files if f.is_file()])
        dir_count = len([f for f in all_files if f.is_dir()])
        
        print(f"\n📊 Summary: {dir_count} directories, {file_count} files generated")


class TestWorkflowOrchestratorValidation(unittest.TestCase):
    """Additional validation tests that don't need file output"""
    
    def test_domain_determination(self):
        """Test domain determination logic"""
        orchestrator = WorkflowOrchestrator("/tmp/test")
        
        # Test chess domain
        game_config = {"entity": "Game", "methods": []}
        self.assertEqual(orchestrator._determine_domain("games", game_config), "chess")
        
        # Test training domain  
        puzzle_config = {"entity": "Puzzle", "methods": []}
        self.assertEqual(orchestrator._determine_domain("puzzles", puzzle_config), "training")
        
        # Test theory domain
        opening_config = {"entity": "Opening", "methods": []}
        self.assertEqual(orchestrator._determine_domain("openings", opening_config), "theory")
        
        # Test user domain
        user_config = {"entity": "UserProfile", "methods": []}
        self.assertEqual(orchestrator._determine_domain("user_profiles", user_config), "user")
        
        # Test gamification domain
        achievement_config = {"entity": "Achievement", "methods": []}
        self.assertEqual(orchestrator._determine_domain("achievements", achievement_config), "gamification")
        
        # Test fallback to 'other'
        unknown_config = {"entity": "Unknown", "methods": []}
        self.assertEqual(orchestrator._determine_domain("unknown", unknown_config), "other")
    
    def test_chess_training_config(self):
        """Test that chess training config is properly structured"""
        orchestrator = WorkflowOrchestrator("/tmp/test")
        config = orchestrator._get_chess_training_config()
        
        # Verify structure
        self.assertIsInstance(config, dict)
        self.assertEqual(len(config), 5)  # 5 entities
        
        # Verify each entity has required fields
        for endpoint_name, endpoint_config in config.items():
            self.assertIn('entity', endpoint_config)
            self.assertIn('properties', endpoint_config)
            self.assertIn('methods', endpoint_config)
            self.assertIsInstance(endpoint_config['methods'], list)
            self.assertGreater(len(endpoint_config['methods']), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)