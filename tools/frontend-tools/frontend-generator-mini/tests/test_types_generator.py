#!/usr/bin/env python3
"""
Tests for the Types Generator using template engine and name standardizer
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

from generators.types.types_generator_new import TypesGenerator


class TestTypesGenerator(unittest.TestCase):
    """Test the Types Generator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.generator = TypesGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generate_game_types(self):
        """Test generating Game types"""
        endpoint_config = {
            'entity': 'Game',
            'properties': {
                'id': 'string',
                'user_id': 'string',
                'ai_level': 'number',
                'status': 'string',
                'created_at': 'datetime'
            }
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        # Check if file was created
        expected_file = self.test_dir / "types" / "chess" / "games.ts"
        self.assertTrue(expected_file.exists(), f"Expected file not found: {expected_file}")
        
        # Check content
        with open(expected_file, 'r') as f:
            content = f.read()
            
        # Verify key components are present
        self.assertIn('export interface Game {', content)
        self.assertIn('export interface GameCreate {', content)
        self.assertIn('export interface GameUpdate {', content)
        self.assertIn('export interface GameFilter {', content)
        self.assertIn('export default Game;', content)
        
        # Check properties are correctly mapped
        self.assertIn('id: string;', content)
        self.assertIn('userId: string;', content)  # snake_case to camelCase
        self.assertIn('aILevel: number;', content)  # snake_case to camelCase (note: ai -> aI)
        self.assertIn('status: string;', content)
        self.assertIn('createdAt: string;', content)  # datetime mapped to string
    
    def test_property_type_mapping(self):
        """Test TypeScript type mapping"""
        endpoint_config = {
            'entity': 'TestEntity',
            'properties': {
                'string_field': 'string',
                'number_field': 'number',
                'integer_field': 'integer',
                'boolean_field': 'boolean',
                'datetime_field': 'datetime',
                'json_field': 'json',
                'unknown_field': 'custom_type'
            }
        }
        
        self.generator.generate('test_entities', endpoint_config, 'test')
        
        expected_file = self.test_dir / "types" / "test" / "testEntities.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check type mappings
        self.assertIn('stringField: string;', content)
        self.assertIn('numberField: number;', content)
        self.assertIn('integerField: number;', content)  # integer -> number
        self.assertIn('booleanField: boolean;', content)
        self.assertIn('datetimeField: string;', content)  # datetime -> string
        self.assertIn('jsonField: object;', content)  # json -> object
        self.assertIn('unknownField: any;', content)  # unknown -> any
    
    def test_snake_case_to_camel_case_conversion(self):
        """Test snake_case property names are converted to camelCase"""
        endpoint_config = {
            'entity': 'UserProfile',
            'properties': {
                'user_id': 'string',
                'first_name': 'string',
                'last_name': 'string',
                'created_at': 'datetime',
                'updated_at': 'datetime'
            }
        }
        
        self.generator.generate('user_profiles', endpoint_config, 'user')
        
        expected_file = self.test_dir / "types" / "user" / "userProfiles.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Check snake_case is converted to camelCase
        self.assertIn('userId: string;', content)
        self.assertIn('firstName: string;', content)
        self.assertIn('lastName: string;', content)
        self.assertIn('createdAt: string;', content)
        self.assertIn('updatedAt: string;', content)
        
        # Ensure snake_case is not present
        self.assertNotIn('user_id:', content)
        self.assertNotIn('first_name:', content)
        self.assertNotIn('created_at:', content)
    
    def test_barrel_exports_generation(self):
        """Test barrel export files generation"""
        # Generate multiple type files
        configs = [
            ('games', {'entity': 'Game', 'properties': {'id': 'string'}}),
            ('puzzles', {'entity': 'Puzzle', 'properties': {'id': 'string'}}),
            ('openings', {'entity': 'Opening', 'properties': {'id': 'string'}})
        ]
        
        for endpoint_name, config in configs:
            self.generator.generate(endpoint_name, config, 'chess')
        
        # Generate barrel exports
        self.generator.generate_barrel_exports()
        
        # Check main barrel file
        main_barrel = self.test_dir / "types" / "index.ts"
        self.assertTrue(main_barrel.exists())
        
        with open(main_barrel, 'r') as f:
            content = f.read()
        
        self.assertIn("// Chess types", content)
        self.assertIn("export * from './chess';", content)
        
        # Check domain barrel file
        domain_barrel = self.test_dir / "types" / "chess" / "index.ts"
        self.assertTrue(domain_barrel.exists())
        
        with open(domain_barrel, 'r') as f:
            content = f.read()
        
        self.assertIn("export * from './games';", content)
        self.assertIn("export * from './puzzles';", content)
        self.assertIn("export * from './openings';", content)
    
    def test_special_routing_skip(self):
        """Test that special routing endpoints are skipped"""
        endpoint_config = {
            'entity': 'Auth',
            'special_routing': True,
            'properties': {'token': 'string'}
        }
        
        self.generator.generate('auth', endpoint_config, 'auth')
        
        # Should not create file due to special routing
        expected_file = self.test_dir / "types" / "auth" / "auth.ts"
        self.assertFalse(expected_file.exists())
    
    def test_empty_properties_handling(self):
        """Test handling of entities with no properties"""
        endpoint_config = {
            'entity': 'EmptyEntity',
            'properties': {}
        }
        
        self.generator.generate('empty_entities', endpoint_config, 'test')
        
        expected_file = self.test_dir / "types" / "test" / "emptyEntities.ts"
        with open(expected_file, 'r') as f:
            content = f.read()
        
        # Should still generate interfaces but with no properties comment
        self.assertIn('export interface EmptyEntity {', content)
        self.assertIn('// No properties defined', content)


if __name__ == '__main__':
    unittest.main()