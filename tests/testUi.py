
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

import unittest
from typing import Tuple
from unittest.mock import patch, MagicMock, ANY
from storyforge.ui import *
import pygame



class PygameUITestCase(unittest.TestCase):
    def setUp(self):
        self.mock_story = MagicMock()
        

    def test_init(self):
        ui = PygameUI(self.mock_story)
        self.assertEqual(ui.story, self.mock_story)
        self.assertTrue(ui.close_window)
        
    
    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    def test_init_pygame(self, mock_set_caption, mock_set_mode, mock_init):
        ui = PygameUI(self.mock_story)
        mock_init.assert_called_once()
        mock_set_mode.assert_called_once_with((0, 0), pygame.FULLSCREEN)
        mock_set_caption.assert_called_once_with("StoryForge::")

    def test_show_initial_menu(self):
        ui = PygameUI(self.mock_story)
        ui.menu.show_menu = MagicMock()
        ui.show_initial_menu()
        ui.menu.show_menu.assert_called_once()

    def test_get_player_name_with_existing_name(self):
        # Mocking an existing player name
        existing_name = "Existing Player"
        self.mock_story.character = {"name": existing_name}
        
        with patch.object(PygameUI, 'render_input_screen'), patch('pygame.event.get') as mock_event_get:
            # Mocking a pygame.KEYDOWN event to simulate ENTER key press
            mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)]
            
            ui = PygameUI(self.mock_story)
            player_name = ui.get_player_name(default_name="BezerraC")
            
            self.assertEqual(player_name, existing_name)

    def test_get_player_name_without_existing_name(self):
        # Mocking an empty player name
        self.mock_story.character = {"name": "Player1"}
        
        with patch.object(PygameUI, 'render_input_screen'), patch('pygame.event.get') as mock_event_get:
            # Mocking a series of pygame.KEYDOWN events to input a new name
            mock_event_get.side_effect = [
                [pygame.event.Event(pygame.KEYDOWN, key=ord('a'))],
                [pygame.event.Event(pygame.KEYDOWN, key=ord('b'))],
                [pygame.event.Event(pygame.KEYDOWN, key=ord('c'))],
                [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)]
            ]
            
            ui = PygameUI(self.mock_story)
            player_name = ui.get_player_name(default_name="BezerraC")
            
            self.assertEqual(player_name, "Player1")
    
    @patch('pygame.display.set_mode')
    @patch('pygame.font.SysFont')
    def test_render_text_with_background(self, mock_sysfont, mock_set_mode):
        # Mocks
        mock_screen = MagicMock()
        mock_font = MagicMock()
        mock_rendered_text = MagicMock()

        mock_sysfont.return_value = mock_font
        mock_font.render.return_value = mock_rendered_text

        ui = PygameUI(self.mock_story)
        ui.screen = mock_screen

        # Input data
        text = "Hello, world!"
        height = 50
        bottom_aligned = False
        opacity = 128
        speech_text = None

        # Run the function
        background_rect = ui.render_text_with_background(text, height, bottom_aligned, opacity, speech_text)

        # Assertions
        mock_sysfont.assert_called_once_with('Arial', 24)  # Check if the font is initialized correctly with the expected arguments
        mock_font.render.assert_called_once_with(text, True, (255, 255, 255))  # Check if text is rendered with the correct color
        mock_screen.blit.assert_called_with(mock_rendered_text, mock_rendered_text.get_rect(center=(mock_screen.get_width() // 2, (mock_screen.get_height() // 2) + (height // 2))))

    @patch('pygame.display.set_mode')
    @patch('pygame.font.SysFont')
    def test_render_input_screen(self, mock_sysfont, mock_set_mode):
        # Mocks
        mock_screen = MagicMock()
        mock_font = MagicMock()

        mock_sysfont.return_value = mock_font

        ui = PygameUI(self.mock_story)
        ui.screen = mock_screen

        # Input data
        input_string = "Player1"
        default_name = "BezerraC"

        # Run the function
        ui.render_input_screen(input_string, default_name)

        # Assertions
        mock_screen.fill.assert_called_once_with((0, 0, 0))  # Check if the screen is filled with black color
        mock_font.render.assert_any_call(f"Default name: {default_name}", True, (255, 255, 255))  # Check if the default name text is rendered
        mock_font.render.assert_any_call("Enter the character's name:", True, (255, 255, 255))  # Check if the prompt text is rendered
        mock_font.render.assert_any_call(input_string, True, (255, 255, 255))  # Check if the input string text is rendered

    @patch('pygame.display.set_mode')
    @patch('pygame.font.SysFont')
    @patch('pygame.display.flip')
    def test_show_input_screen(self, mock_display_flip, mock_sysfont, mock_set_mode):
        # Mocks
        mock_screen = MagicMock()
        mock_font = MagicMock()

        mock_sysfont.return_value = mock_font

        ui = PygameUI(self.mock_story)
        ui.screen = mock_screen

        # Input data
        default_name = "BezerraC"

        # Run the function
        ui.show_input_screen(default_name)

        # Assertions
        mock_screen.fill.assert_called_once_with((255, 255, 255))  # Check if the screen is filled with white color
        mock_font.render.assert_called_once_with(f"Enter the character's name: {default_name}", True, (0, 0, 0))  # Check if the prompt text is rendered with the correct color
        mock_screen.blit.assert_called_once()  # Check if the text is blitted onto the screen
        mock_display_flip.assert_called_once()  # Check if the display is flipped

    @patch('pygame.font.SysFont')
    def test_render_choice(self, mock_sysfont):
        # Mocks
        mock_screen = MagicMock()
        mock_font = MagicMock()
        mock_surface = MagicMock()

        mock_sysfont.return_value = mock_font
        pygame.mouse.get_pos = MagicMock(return_value=(300, 200))

        # Mocking the Surface
        pygame.Surface = MagicMock(return_value=mock_surface)

        ui = PygameUI(self.mock_story)
        ui.screen = mock_screen

        # Input data
        choice_text = "Option 1"
        x = 300
        y = 200

        # Run the function
        returned_rect, returned_space = ui.render_choice(choice_text, x, y)

        # Assertions
        self.assertIsInstance(returned_rect, pygame.Rect)
        self.assertIsInstance(returned_space, int)

    @patch('pygame.font.SysFont')
    def test_render_text(self, mock_sysfont):
        # Mocks
        mock_screen = MagicMock()
        mock_font = MagicMock()
        mock_rendered_text = MagicMock()  # Change this to a Surface

        mock_sysfont.return_value = mock_font
        mock_font.render.return_value = mock_rendered_text  # Return the Surface

        ui = PygameUI(self.mock_story)
        ui.screen = mock_screen

        # Mock the Rect object
        mock_rect = MagicMock(spec=pygame.Rect)

        # Set the return value of the get_rect method of the rendered text to the mocked Rect object
        mock_rendered_text.get_rect.return_value = mock_rect

        # Input data
        text = "Hello, world!"
        x = 300
        y = 200

        # Run the function
        returned_rect = ui.render_text(text, x, y)

        # Assertions
        self.assertIsInstance(returned_rect, pygame.Rect)
        
    @patch('storyforge.ui.pygame.event.get')
    def test_wait_for_click(self, mock_event_get):
        # Setting up the mock for pygame event
        mock_event = MagicMock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event_get.side_effect = [[], [mock_event]]  # First call returns empty list, second call returns list with mouse click event

        ui = PygameUI(MagicMock())  # Mocking the Story object

        # Calling the function
        ui.wait_for_click()

        # Assertions
        mock_event_get.assert_called_with()  # Ensure pygame.event.get is called
        self.assertTrue(mock_event_get.call_count >= 2)  # Ensure pygame.event.get is called at least twice

    @patch('storyforge.ui.pygame.mouse')
    @patch('storyforge.ui.PygameUI.render_choice')
    def test_show_choices(self, mock_render_choice, mock_mouse):
        # Mocking necessary objects
        ui = PygameUI(MagicMock())  # Mocking the Story object
        ui.story.current_scene = "start"
        mock_screen = MagicMock()
        ui.screen = mock_screen

        # Mocking scene with choices
        scene = {
            "choices": [("Choice 1", None), ("Choice 2", None)]
        }
        ui.story.scenes = {"start": scene}

        # Mocking render_choice return values
        mock_render_choice.side_effect = [(MagicMock(), 50), (MagicMock(), 50)]

        # Mocking mouse position
        mock_mouse.get_pos.return_value = (400, 450)  # Hovering over Choice 2

        # Calling the function
        hover_choice = ui.show_choices()

        # Assertions
        self.assertEqual(hover_choice, 2)  # Choice 2 should be hovered
        mock_render_choice.assert_any_call("Choice 1", ANY, ANY)  # Ensure render_choice is called with Choice 1
        mock_render_choice.assert_any_call("Choice 2", ANY, ANY)  # Ensure render_choice is called with Choice 2

    def test_run(self):
        # Mocks
        mock_story = MagicMock()
        mock_story.default_player_name = {"name": "DefaultName"}
        mock_story.has_choices.return_value = True
        mock_story.character = MagicMock()

        mock_ui = PygameUI(mock_story)
        mock_ui.choice_rects = [MagicMock() for _ in range(3)]
        mock_ui.show_character_speech = True
        mock_ui.show_speech_displayed = True

        # Mocking return values
        with patch.object(PygameUI, 'get_player_name', return_value="Player1"), \
            patch.object(PygameUI, 'handle_events'), \
            patch.object(PygameUI, 'show_scene'), \
            patch.object(PygameUI, 'show_choices', return_value=None), \
            patch.object(PygameUI, 'check_for_click', side_effect=[False, True]):
            
            # Calling the function with a maximum of 10 iterations
            mock_ui.run(max_iterations=10)

            
    @patch('pygame.event.get')
    def test_check_for_click_when_click_occurs(self, mock_event_get):
        # Mocking a MOUSEBUTTONDOWN event with button 1
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mock_event_get.return_value = [mock_event]

        mock_ui = PygameUI(MagicMock())  # Mocking the Story object

        # Calling the function
        result = mock_ui.check_for_click()

        # Assertions
        self.assertTrue(result)  # Ensure True is returned when a click occurs
        mock_event_get.assert_called_once()  # Ensure pygame.event.get is called

    @patch('pygame.event.get')
    def test_check_for_click_when_no_click_occurs(self, mock_event_get):
        # Mocking no events in the event queue
        mock_event_get.return_value = []

        mock_ui = PygameUI(MagicMock())  # Mocking the Story object

        # Calling the function
        result = mock_ui.check_for_click()

        # Assertions
        self.assertFalse(result)  # Ensure False is returned when no click occurs
        mock_event_get.assert_called_once()  # Ensure pygame.event.get is called

    def test_check_text_and_speech_displayed_when_both_displayed(self):
        # Mocking show_text_displayed and show_speech_displayed as True
        mock_ui = PygameUI(MagicMock())  # Mocking the Story object
        mock_ui.show_text_displayed = True
        mock_ui.show_speech_displayed = True

        # Calling the function
        result = mock_ui.check_text_and_speech_displayed()

        # Assertions
        self.assertTrue(result)  # Ensure True is returned when both text and speech are displayed

    def test_check_text_and_speech_displayed_when_text_not_displayed(self):
        # Mocking show_text_displayed as False
        mock_ui = PygameUI(MagicMock())  # Mocking the Story object
        mock_ui.show_text_displayed = False

        # Calling the function
        result = mock_ui.check_text_and_speech_displayed()

        # Assertions
        self.assertFalse(result)  # Ensure False is returned when text is not displayed

    def test_process_click_choice_made(self):
        ui = PygameUI(self.mock_story)
        ui.story.current_scene = "test_scene"
        ui.show_character_speech = False

        # Mocking scene with choices
        scene = {
            "choices": [("Choice 1", None), ("Choice 2", None)],
            "character_speech": None
        }
        ui.story.scenes = {"test_scene": scene}

        # Mocking mouse position
        pos = (ui.screen.get_width() // 2, 400)

        # Calling the function
        ui.process_click(pos)

        # Assertions
        self.mock_story.make_choice.assert_called_once_with("1")  # Ensure make_choice is called with the correct choice number
        self.assertFalse(ui.show_character_speech)  # Ensure show_character_speech is set to False after making a choice

    def test_process_click_toggle_character_speech(self):
        ui = PygameUI(self.mock_story)
        ui.story.current_scene = "test_scene"
        ui.show_character_speech = False

        # Mocking scene with choices and character_speech (including image)
        scene = {
            "choices": [("Choice 1", None), ("Choice 2", None)],
            "character_speech": "Character speech text",
            "image": "room.jpg",
            "character_image": "boy.png"
        }
        ui.story.scenes = {"test_scene": scene}

        # Mocking mouse position
        pos = (ui.screen.get_width() // 2, 400)

        # Calling the function
        ui.process_click(pos)

        # Assertions
        self.mock_story.make_choice.assert_called_once_with("1")  # Ensure make_choice is called with the correct choice numbe


    

if __name__ == "__main__":
    unittest.main()
