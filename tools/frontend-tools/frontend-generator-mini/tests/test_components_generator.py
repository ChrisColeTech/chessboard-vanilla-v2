#!/usr/bin/env python3
"""
Tests for the Components Generator using template engine and name standardizer
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

from generators.components.components_generator_new import ComponentsGenerator


class TestComponentsGenerator(unittest.TestCase):
    """Test the Components Generator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.generator = ComponentsGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generate_game_components(self):
        """Test generating Game components"""
        endpoint_config = {
            'entity': 'Game',
            'properties': {
                'id': 'string',
                'user_id': 'string',
                'ai_level': 'number',
                'status': 'string',
                'current_fen': 'string',
                'created_at': 'datetime'
            },
            'methods': ['createGame', 'getGameById', 'listGames', 'updateGame', 'deleteGame']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        # Check if all component types were created
        list_component = self.test_dir / "components" / "chess" / "GameList.tsx"
        detail_component = self.test_dir / "components" / "chess" / "GameDetail.tsx"
        form_component = self.test_dir / "components" / "chess" / "GameForm.tsx"
        
        self.assertTrue(list_component.exists(), f"List component not created: {list_component}")
        self.assertTrue(detail_component.exists(), f"Detail component not created: {detail_component}")
        self.assertTrue(form_component.exists(), f"Form component not created: {form_component}")
        
        # Check list component content
        with open(list_component, 'r') as f:
            list_content = f.read()
        
        self.assertIn("import type { Game } from '../../types/chess/games';", list_content)
        self.assertIn("interface GameListProps {", list_content)
        self.assertIn("items: Game[];", list_content)
        self.assertIn("export const GameList: React.FC<GameListProps> = ({", list_content)
        self.assertIn("items.map((item) => (", list_content)
        self.assertIn('className="games-list"', list_content)
        
        # Check properties are displayed
        self.assertIn("<strong>User Id:</strong> {item.userId}", list_content)
        self.assertIn("<strong>AI Level:</strong> {item.aILevel}", list_content)  # aI_level -> aILevel
        self.assertIn("<strong>Status:</strong> {item.status}", list_content)
        self.assertIn("<strong>Current Fen:</strong> {item.currentFen}", list_content)
    
    def test_detail_component_generation(self):
        """Test detail component specific features"""
        endpoint_config = {
            'entity': 'Puzzle',
            'properties': {
                'id': 'string',
                'title': 'string',
                'difficulty': 'number',
                'rating': 'number',
                'solved': 'boolean'
            },
            'methods': ['getPuzzleById', 'updatePuzzle', 'deletePuzzle']
        }
        
        self.generator.generate('puzzles', endpoint_config, 'training')
        
        detail_component = self.test_dir / "components" / "training" / "PuzzleDetail.tsx"
        self.assertTrue(detail_component.exists())
        
        with open(detail_component, 'r') as f:
            content = f.read()
        
        # Check detail component specific features
        self.assertIn("interface PuzzleDetailProps {", content)
        self.assertIn("item: Puzzle;", content)
        self.assertIn("onEdit?: (item: Puzzle) => void;", content)
        self.assertIn("onDelete?: (id: string) => void;", content)
        
        # Check action buttons
        self.assertIn("{onEdit && (", content)
        self.assertIn('<button onClick={() => onEdit(item)} className="btn-edit">', content)
        self.assertIn("{onDelete && (", content)
        self.assertIn("if (window.confirm('Are you sure you want to delete this puzzle?'))", content)
        self.assertIn("onDelete(item.id);", content)
    
    def test_form_component_generation(self):
        """Test form component specific features"""
        endpoint_config = {
            'entity': 'Opening',
            'properties': {
                'id': 'string',
                'name': 'string',
                'eco_code': 'string',
                'moves': 'string',
                'popularity': 'number',
                'is_popular': 'boolean'
            },
            'methods': ['createOpening', 'updateOpening']
        }
        
        self.generator.generate('openings', endpoint_config, 'theory')
        
        form_component = self.test_dir / "components" / "theory" / "OpeningForm.tsx"
        self.assertTrue(form_component.exists())
        
        with open(form_component, 'r') as f:
            content = f.read()
        
        # Check form component structure
        self.assertIn("interface OpeningFormProps {", content)
        self.assertIn("initialData?: Partial<Opening>;", content)
        self.assertIn("onSubmit: (data: Partial<Opening>) => void;", content)
        self.assertIn("onCancel?: () => void;", content)
        self.assertIn("loading?: boolean;", content)
        
        # Check form fields generation
        self.assertIn('<label htmlFor="name">Name:</label>', content)
        self.assertIn('<input type="text" id="name"', content)
        
        self.assertIn('<label htmlFor="ecoCode">Eco Code:</label>', content)  # snake_case -> camelCase
        self.assertIn('<input type="text" id="ecoCode"', content)
        
        self.assertIn('<label htmlFor="popularity">Popularity:</label>', content)
        self.assertIn('<input type="number" id="popularity"', content)
        
        # Check boolean field (checkbox)
        self.assertIn('<input type="checkbox" id="isPopular"', content)
        self.assertIn('checked={formData.isPopular || false}', content)
    
    def test_property_type_handling_in_components(self):
        """Test different property types are handled correctly in components"""
        endpoint_config = {
            'entity': 'TestEntity',
            'properties': {
                'string_field': 'string',
                'number_field': 'number',
                'boolean_field': 'boolean',
                'datetime_field': 'datetime',
                'json_field': 'json'
            },
            'methods': ['createTestEntity', 'listTestEntities']
        }
        
        self.generator.generate('test_entities', endpoint_config, 'test')
        
        # Check list component property display
        list_component = self.test_dir / "components" / "test" / "TestEntityList.tsx"
        with open(list_component, 'r') as f:
            list_content = f.read()
        
        # String/text fields
        self.assertIn("{item.stringField}", list_content)
        
        # Number fields
        self.assertIn("{item.numberField}", list_content)
        
        # Boolean fields (special handling)
        self.assertIn("{item.booleanField ? 'Yes' : 'No'}", list_content)
        
        # Datetime fields (formatted)
        self.assertIn("new Date(item.datetimeField).toLocaleDateString()", list_content)
        
        # Check form component field types
        form_component = self.test_dir / "components" / "test" / "TestEntityForm.tsx"
        with open(form_component, 'r') as f:
            form_content = f.read()
        
        # Text input for strings
        self.assertIn('<input type="text" id="stringField"', form_content)
        
        # Number input for numbers
        self.assertIn('<input type="number" id="numberField"', form_content)
        
        # Checkbox for booleans
        self.assertIn('<input type="checkbox" id="booleanField"', form_content)
        
        # Datetime input for datetime
        self.assertIn('<input type="datetime-local" id="datetimeField"', form_content)
    
    def test_name_standardization_in_components(self):
        """Test name standardization in component generation"""
        endpoint_config = {
            'entity': 'UserProfile',
            'properties': {
                'user_id': 'string',
                'first_name': 'string',
                'last_name': 'string',
                'created_at': 'datetime'
            },
            'methods': ['createUserProfile', 'listUserProfiles']
        }
        
        self.generator.generate('user_profiles', endpoint_config, 'user')
        
        list_component = self.test_dir / "components" / "user" / "UserProfileList.tsx"
        with open(list_component, 'r') as f:
            content = f.read()
        
        # Check property name conversion
        self.assertIn("{item.userId}", content)  # user_id -> userId
        self.assertIn("{item.firstName}", content)  # first_name -> firstName
        self.assertIn("{item.lastName}", content)  # last_name -> lastName
        self.assertIn("{item.createdAt}", content)  # created_at -> createdAt
        
        # Check CSS class names (kebab-case)
        self.assertIn('className="user-profiles-list"', content)
        self.assertIn('className="userprofile-item"', content)
    
    def test_special_routing_skip(self):
        """Test that special routing endpoints are skipped"""
        endpoint_config = {
            'entity': 'Auth',
            'special_routing': True,
            'properties': {'token': 'string'},
            'methods': ['login', 'register']
        }
        
        self.generator.generate('auth', endpoint_config, 'auth')
        
        # Should not create any components due to special routing
        auth_dir = self.test_dir / "components" / "auth"
        if auth_dir.exists():
            components = list(auth_dir.glob("*.tsx"))
            self.assertEqual(len(components), 0, "Should not create components for special routing")
    
    def test_component_props_and_callbacks(self):
        """Test component props and callback handling"""
        endpoint_config = {
            'entity': 'Achievement',
            'properties': {
                'id': 'string',
                'name': 'string',
                'points': 'number'
            },
            'methods': ['getAchievementById', 'deleteAchievement']
        }
        
        self.generator.generate('achievements', endpoint_config, 'gamification')
        
        # Check list component callbacks
        list_component = self.test_dir / "components" / "gamification" / "AchievementList.tsx"
        with open(list_component, 'r') as f:
            list_content = f.read()
        
        self.assertIn("onItemClick?: (item: Achievement) => void;", list_content)
        self.assertIn("onClick={() => onItemClick?.(item)}", list_content)
        self.assertIn("cursor: onItemClick ? 'pointer' : 'default'", list_content)
        
        # Check detail component callbacks
        detail_component = self.test_dir / "components" / "gamification" / "AchievementDetail.tsx"
        with open(detail_component, 'r') as f:
            detail_content = f.read()
        
        self.assertIn("onEdit?: (item: Achievement) => void;", detail_content)
        self.assertIn("onDelete?: (id: string) => void;", detail_content)
    
    def test_form_field_generation_edge_cases(self):
        """Test form field generation for edge cases"""
        endpoint_config = {
            'entity': 'ComplexEntity',
            'properties': {
                'id': 'string',          # Should be skipped (auto-generated)
                'email_address': 'string',  # Should use email input type
                'password_field': 'string', # Should use password input type
                'created_at': 'datetime',   # Should be skipped (auto-generated)
                'updated_at': 'datetime',   # Should be skipped (auto-generated)
                'date_only': 'date',        # Should use date input type
                'description': 'text'       # Should use text input
            },
            'methods': ['createComplexEntity']
        }
        
        self.generator.generate('complex_entities', endpoint_config, 'test')
        
        form_component = self.test_dir / "components" / "test" / "ComplexEntityForm.tsx"
        with open(form_component, 'r') as f:
            content = f.read()
        
        # Auto-generated fields should be skipped
        self.assertNotIn('id="id"', content)
        self.assertNotIn('id="createdAt"', content)
        self.assertNotIn('id="updatedAt"', content)
        
        # Email field should use email input type
        self.assertIn('<input type="email" id="emailAddress"', content)
        
        # Password field should use password input type
        self.assertIn('<input type="password" id="passwordField"', content)
        
        # Date field should use date input type
        self.assertIn('<input type="date" id="dateOnly"', content)
    
    def test_empty_properties_handling(self):
        """Test handling of entities with no properties"""
        endpoint_config = {
            'entity': 'EmptyEntity',
            'properties': {},
            'methods': ['createEmptyEntity', 'listEmptyEntities']
        }
        
        self.generator.generate('empty_entities', endpoint_config, 'test')
        
        list_component = self.test_dir / "components" / "test" / "EmptyEntityList.tsx"
        with open(list_component, 'r') as f:
            content = f.read()
        
        # Should handle empty properties gracefully
        self.assertIn("// No properties defined", content)
        
        form_component = self.test_dir / "components" / "test" / "EmptyEntityForm.tsx"
        with open(form_component, 'r') as f:
            content = f.read()
        
        self.assertIn("{/* No editable fields */}", content)


if __name__ == '__main__':
    unittest.main()