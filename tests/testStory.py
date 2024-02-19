import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

import unittest
from unittest.mock import MagicMock, patch
from core.story import Story

class TestStory(unittest.TestCase):
    def setUp(self):
        # Create a MagicMock object to represent the story
        self.mock_story = MagicMock()
        start_scene = "start"
        self.story = Story(start_scene)

    def test_init(self):
        start_scene = "start"
        story = Story(start_scene)
        self.assertEqual(story.current_scene, start_scene)
        self.assertEqual(story.scenes, {})
        self.assertEqual(story.choices, {})
        self.assertEqual(story.character, {"name": None})
        self.assertEqual(story.character_name, None)
        self.assertEqual(story.default_player_name, {"name": "BezerraC"})

    def test_save_state(self):
        start_scene = "start"
        story = Story(start_scene)
        story.current_scene = "start"
        story.character["name"] = "Test Character"
        
        with patch("builtins.print") as mock_print:
            story.save_state()
            mock_print.assert_called_with("Saved state.")

    def test_load_state(self):
        start_scene = "start"
        story = Story(start_scene)
        story.current_scene = "start"
        story.character["name"] = "Test Character"
        
        with patch("builtins.print") as mock_print:
            state_loaded = story.load_state()
            mock_print.assert_not_called()
            self.assertTrue(state_loaded)
            self.assertEqual(story.current_scene, "start")
            self.assertEqual(story.character["name"], "Test Character")

    def test_create_empty_state(self):
        start_scene = "start"
        story = Story(start_scene)
        
        with patch("builtins.print") as mock_print, patch.object(story, "save_state") as mock_save_state:
            story.create_empty_state()
            mock_print.assert_called_with("Empty state created.")

    def test_set_character_name(self):
        start_scene = "start"
        story = Story(start_scene)
        story.set_character_name("Test Character")
        self.assertEqual(story.character["name"], "Test Character")

    def test_add_scene(self):
        start_scene = "start"
        story = Story(start_scene)
        story.add_scene("scene1", "Scene 1 Text")
        self.assertIn("scene1", story.scenes)
        self.assertEqual(story.scenes["scene1"]["text"], "Scene 1 Text")

    def test_add_choice(self):
        start_scene = "start"
        story = Story(start_scene)
        story.add_scene("scene1", "Scene 1 Text")
        story.add_scene("scene2", "Scene 2 Text")
        story.add_choice("scene1", "Choice 1", "scene2")
        self.assertEqual(story.choices[("scene1", "Choice 1")], "scene2")
        self.assertIn(("Choice 1", "scene2"), story.scenes["scene1"]["choices"])

    def test_has_choices(self):
        start_scene = "start"
        story = Story(start_scene)
        story.add_scene(start_scene, "Text for start scene")  # Add initial scene
        self.assertFalse(story.has_choices())

    def test_validate_story(self):
        # First test: no inaccessible scenes
        start_scene = "start"
        story = Story(start_scene)
        story.add_scene("scene1", "Scene 1 Text")
        story.add_scene("scene2", "Scene 2 Text")
        story.add_choice("scene1", "Choice 1", "scene2")
        with patch("builtins.print") as mock_print:
            story.validate_story()

        # Second test: inaccessible scene
        start_scene = "start"
        story = Story(start_scene)
        story.add_scene("scene1", "Scene 1 Text")
        story.add_scene("scene2", "Scene 2 Text")
        # Here don't add a choice, so "scene2" becomes inaccessible
        story.current_scene = "scene1"  # Sets the current scene
        with patch("builtins.print") as mock_print:
            story.validate_story()
            mock_print.assert_called_with("Warning: Inaccessible scene 'scene2'.")

   
if __name__ == '__main__':
    unittest.main()
