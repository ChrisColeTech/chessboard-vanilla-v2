#!/usr/bin/env python3
"""
Tests for the Pages Generator using template engine and name standardizer
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

from generators.pages.pages_generator_new import PagesGenerator


class TestPagesGenerator(unittest.TestCase):
    """Test the Pages Generator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.generator = PagesGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generate_game_pages(self):
        """Test generating Game pages"""
        endpoint_config = {
            'entity': 'Game',
            'methods': ['createGame', 'getGameById', 'listGames', 'updateGame', 'deleteGame']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        # Check if all page types were created
        list_page = self.test_dir / "pages" / "chess" / "GamePage.tsx"
        detail_page = self.test_dir / "pages" / "chess" / "GameDetailPage.tsx"
        form_page = self.test_dir / "pages" / "chess" / "GameFormPage.tsx"
        
        self.assertTrue(list_page.exists(), f"List page not created: {list_page}")
        self.assertTrue(detail_page.exists(), f"Detail page not created: {detail_page}")
        self.assertTrue(form_page.exists(), f"Form page not created: {form_page}")
        
        # Check list page content
        with open(list_page, 'r') as f:
            list_content = f.read()
        
        self.assertIn("import { useGame } from '../../hooks/chess/useGame';", list_content)
        self.assertIn("export const GamePage = () => {", list_content)
        self.assertIn("const { games, loading, error } = useGame();", list_content)
        self.assertIn('className="games-page"', list_content)
        
        # Check detail page content
        with open(detail_page, 'r') as f:
            detail_content = f.read()
        
        self.assertIn("import { useParams } from 'react-router-dom';", detail_content)
        self.assertIn("export const GameDetailPage = () => {", detail_content)
        self.assertIn("const { id } = useParams<{ id: string }>();", detail_content)
        self.assertIn("getGameById(id);", detail_content)
        
        # Check form page content
        with open(form_page, 'r') as f:
            form_content = f.read()
        
        self.assertIn("import { useState } from 'react';", form_content)
        self.assertIn("import { useNavigate } from 'react-router-dom';", form_content)
        self.assertIn("export const GameFormPage = () => {", form_content)
        self.assertIn("const { createGame } = useGame();", form_content)
    
    def test_list_page_generation_only(self):
        """Test generating only list page when only list methods exist"""
        endpoint_config = {
            'entity': 'Achievement',
            'methods': ['listAchievements']
        }
        
        self.generator.generate('achievements', endpoint_config, 'gamification')
        
        # Should create list page
        list_page = self.test_dir / "pages" / "gamification" / "AchievementPage.tsx"
        self.assertTrue(list_page.exists())
        
        # Should not create detail or form pages (no getById or create methods)
        detail_page = self.test_dir / "pages" / "gamification" / "AchievementDetailPage.tsx"
        form_page = self.test_dir / "pages" / "gamification" / "AchievementFormPage.tsx"
        self.assertFalse(detail_page.exists())
        self.assertFalse(form_page.exists())
    
    def test_detail_page_generation(self):
        """Test detail page specific features"""
        endpoint_config = {
            'entity': 'Puzzle',
            'methods': ['getPuzzleById', 'updatePuzzle']
        }
        
        self.generator.generate('puzzles', endpoint_config, 'training')
        
        detail_page = self.test_dir / "pages" / "training" / "PuzzleDetailPage.tsx"
        self.assertTrue(detail_page.exists())
        
        with open(detail_page, 'r') as f:
            content = f.read()
        
        # Check detail page specific features
        self.assertIn("useEffect(() => {", content)
        self.assertIn("if (id) {", content)
        self.assertIn("getPuzzleById(id);", content)
        self.assertIn("if (!puzzle) {", content)
        self.assertIn("return <div className=\"not-found\">Puzzle not found</div>;", content)
    
    def test_form_page_generation(self):
        """Test form page specific features"""
        endpoint_config = {
            'entity': 'Opening',
            'methods': ['createOpening', 'updateOpening']
        }
        
        self.generator.generate('openings', endpoint_config, 'theory')
        
        form_page = self.test_dir / "pages" / "theory" / "OpeningFormPage.tsx"
        self.assertTrue(form_page.exists())
        
        with open(form_page, 'r') as f:
            content = f.read()
        
        # Check form page specific features
        self.assertIn("const [formData, setFormData] = useState({});", content)
        self.assertIn("const handleSubmit = async (e: React.FormEvent) => {", content)
        self.assertIn("e.preventDefault();", content)
        self.assertIn("await createOpening(formData);", content)
        self.assertIn("navigate('/openings');", content)
        self.assertIn("const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {", content)
    
    def test_name_standardization_in_pages(self):
        """Test name standardization is applied correctly in pages"""
        endpoint_config = {
            'entity': 'UserProfile',
            'methods': ['createUserProfile', 'getUserProfileById', 'listUserProfiles']
        }
        
        self.generator.generate('user_profiles', endpoint_config, 'user')
        
        list_page = self.test_dir / "pages" / "user" / "UserProfilePage.tsx"
        with open(list_page, 'r') as f:
            content = f.read()
        
        # Check name standardization
        self.assertIn("import { useUserProfile } from '../../hooks/user/useUserProfile';", content)
        self.assertIn("const { userProfiles, loading, error } = useUserProfile();", content)
        self.assertIn('className="user-profiles-page"', content)  # kebab-case for CSS
        self.assertIn('className="userprofile-list"', content)
    
    def test_special_routing_skip(self):
        """Test that special routing endpoints are skipped"""
        endpoint_config = {
            'entity': 'Auth',
            'special_routing': True,
            'methods': ['login', 'register']
        }
        
        self.generator.generate('auth', endpoint_config, 'auth')
        
        # Should not create any pages due to special routing
        auth_dir = self.test_dir / "pages" / "auth"
        if auth_dir.exists():
            pages = list(auth_dir.glob("*.tsx"))
            self.assertEqual(len(pages), 0, "Should not create pages for special routing")
    
    def test_navigation_routes(self):
        """Test that pages include proper navigation routes"""
        endpoint_config = {
            'entity': 'Game',
            'methods': ['createGame', 'getGameById', 'listGames']
        }
        
        self.generator.generate('games', endpoint_config, 'chess')
        
        # Check form page navigation
        form_page = self.test_dir / "pages" / "chess" / "GameFormPage.tsx"
        with open(form_page, 'r') as f:
            content = f.read()
        
        # Should navigate to list page after creation
        self.assertIn("navigate('/games');", content)
        
        # Should have cancel button that navigates back
        self.assertIn("onClick={() => navigate('/games')}", content)
    
    def test_error_handling_in_pages(self):
        """Test error handling in generated pages"""
        endpoint_config = {
            'entity': 'Puzzle',
            'methods': ['createPuzzle', 'listPuzzles']
        }
        
        self.generator.generate('puzzles', endpoint_config, 'training')
        
        # Check list page error handling
        list_page = self.test_dir / "pages" / "training" / "PuzzlePage.tsx"
        with open(list_page, 'r') as f:
            list_content = f.read()
        
        self.assertIn("if (loading) {", list_content)
        self.assertIn("return <div className=\"loading\">Loading puzzles...</div>;", list_content)
        self.assertIn("if (error) {", list_content)
        self.assertIn("return <div className=\"error\">Error: {error}</div>;", list_content)
        
        # Check form page error handling
        form_page = self.test_dir / "pages" / "training" / "PuzzleFormPage.tsx"
        with open(form_page, 'r') as f:
            form_content = f.read()
        
        self.assertIn("{error && <div className=\"error\">Error: {error}</div>}", form_content)
        self.assertIn("} catch (err) {", form_content)
        self.assertIn("console.error('Failed to create puzzle:', err);", form_content)
    
    def test_multiple_page_types_generated(self):
        """Test that all appropriate page types are generated based on methods"""
        endpoint_config = {
            'entity': 'Content',
            'methods': [
                'createContent',      # Should generate form page
                'getContentById',     # Should generate detail page  
                'listContent',        # Should generate list page
                'updateContent',      # Should enhance form page
                'deleteContent'       # Should enhance detail page
            ]
        }
        
        self.generator.generate('content', endpoint_config, 'learning')
        
        # All three page types should be generated
        list_page = self.test_dir / "pages" / "learning" / "ContentPage.tsx"
        detail_page = self.test_dir / "pages" / "learning" / "ContentDetailPage.tsx"
        form_page = self.test_dir / "pages" / "learning" / "ContentFormPage.tsx"
        
        self.assertTrue(list_page.exists())
        self.assertTrue(detail_page.exists())
        self.assertTrue(form_page.exists())
        
        # Verify they have correct imports and structure
        with open(list_page, 'r') as f:
            self.assertIn("useContent", f.read())
        
        with open(detail_page, 'r') as f:
            self.assertIn("getContentById", f.read())
        
        with open(form_page, 'r') as f:
            self.assertIn("createContent", f.read())


if __name__ == '__main__':
    unittest.main()