
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
import unittest
from unittest.mock import MagicMock, patch
from core.menu import StoryMenu


class TestStoryMenu(unittest.TestCase):
    def setUp(self):
        # Create a test instance of StoryMenu
        self.mock_story = MagicMock()
        self.mock_ui = MagicMock()
        self.story_menu = StoryMenu(self.mock_story, self.mock_ui)

    def test_show_menu(self):
        # Test whether show_menu method runs without errors
        with patch("core.menu.pygame") as mock_pygame:
            # Mocking clock object
            mock_pygame.time.Clock.return_value = MagicMock()
            # Mocking pygame.MOUSEBUTTONDOWN event
            mock_pygame.MOUSEBUTTONDOWN = 1
            mock_pygame.event.get.return_value = [MagicMock(type=mock_pygame.MOUSEBUTTONDOWN, pos=(0, 0))]
            
            # Mocking render_choice method to return the expected values
            mock_rect = MagicMock()
            mock_surface = MagicMock()
            self.mock_ui.render_choice.return_value = (mock_rect, mock_surface)

            # Call the method
            self.story_menu.show_menu()
            
            # Assert that pygame.display.flip() was called after filling the screen with black
            self.mock_ui.screen.fill.assert_called_once_with((0, 0, 0))
         

    def test_continue_story(self):
        # Test whether continue_story method calls load_state and validate_story
        with patch.object(self.mock_story, "load_state") as mock_load_state, \
                patch.object(self.mock_story, "validate_story") as mock_validate_story:
            # Call the method
            self.story_menu.continue_story()
            # Assert that load_state and validate_story were called
            mock_load_state.assert_called_once()
            mock_validate_story.assert_called_once()

    def test_start_new_story(self):
        # Test whether start_new_story method calls create_empty_state
        with patch.object(self.mock_story, "create_empty_state") as mock_create_empty_state:
            # Call the method
            self.story_menu.start_new_story()
            # Assert that create_empty_state was called
            mock_create_empty_state.assert_called_once()


if __name__ == '__main__':
    unittest.main()
