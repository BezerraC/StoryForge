# core/story.py

import json
import os
from typing import Optional

import pygame

IMAGE_DIR = "images/character"

class Story:
    """
    Class responsible for manipulating the game's story.

    Attributes:
        - scenes (Dict[str, Dict[str, Union[str, List[Tuple[str, str]]]]]): A dictionary that contains the game's scenes.
        - choices (Dict[Tuple[str, str], str]): A dictionary that maps choices made by the player for upcoming scenes.
        - current_scene (str): The name of the current scene.
        - character (Dict[str, Optional[str]]): A dictionary that contains information about the character, such as name.
        - default_player_name (Dict[str, str]): A dictionary containing the player's default name.

    Methods:
        - save_state(): Saves the current state of the game in a JSON file.
        - load_state() -> bool: Loads the previously saved state, if it exists.
        - create_empty_state(): Creates an empty state to start the game.
        - set_character_name(name: str): Sets the character's name.
        - add_scene(name: str, text: str, image: Optional[str] = None, character_image: Optional[str] = None, character_speech: Optional[str] = None):
            Adds a new scene to the story.
        - add_choice(from_scene: str, text: str, to_scene: str): Adds a choice that the player can make in a given scene.
        - has_choices() -> bool: Checks if there are choices available in the current scene.
        - validate_story(): Validates the consistency of the story, looking for inaccessible scenes.
        - run(): Runs the main game loop, showing the scenes, available options and processing the player's choices.
        - show_scene(): Displays the current game scene to standard output.
        - show_choices(): Displays the options available to the player on standard output.
        - make_choice(player_choice: str): Processes the player's choice and advances to the next corresponding scene.
     """
    def __init__(self, start_scene):
        self.scenes = {}
        self.choices = {}
        self.current_scene = start_scene
        self.character = {"name": None}
        self.character_name = None
        self.default_player_name = {"name": "BezerraC"}

    def save_state(self) -> None:
        """
        Saves the current game state to a JSON file.

        Return:
            None
        """
        print("Saving state...")
        data = {
            "current_scene": self.current_scene,
            "character_name": self.character["name"]
        }
        with open("story_state.json", "w") as file:
            json.dump(data, file)
        print("Saved state.")

    def load_state(self) -> bool:
        """
        Loads the previously saved state, if it exists.

        Return:
            bool: True if the state was loaded successfully, False otherwise.
        """
        try:
            with open("story_state.json", "r") as file:
                data = json.load(file)
                self.current_scene = data["current_scene"]
                if "character_name" in data:
                    self.character["name"] = data["character_name"]
                return True
        except FileNotFoundError:
            return False

    def create_empty_state(self) -> None:
        """
        Creates an empty state to start the game.

        Return:
            None
        """
        print("Creating empty state...")

        # Creates an empty initial state
        self.current_scene = "start"
        self.character["name"] = None

        # Call save_state to create story_state.json file
        self.save_state()
        print("Empty state created.")
        
    def set_character_name(self, name: str) -> None:
        """
        Sets the character's name.

        Parameters:
            - name (str): The character's name.

        Return:
            None
        """
        self.character["name"] = name

    def add_scene(self, name: str, text: str, image: Optional[str] = None, character_image: Optional[str] = None, character_speech: Optional[str] = None) -> None:
        """
        Adds a new scene to the story.

        Parameters:
            - name (str): The name of the scene.
            - text (str): The text of the scene.
            - image (Optional[str]): The name of the scene's image file.
            - character_image (Optional[str]): The name of the character image file in the scene.
            - character_speech (Optional[str]): The character's speech in the scene.

        Return:
            None
        """
        self.scenes[name] = {"text": text, "image": image, "character_image": character_image, "character_speech": character_speech, "choices": []}

    def add_choice(self, from_scene: str, text: str, to_scene: str) -> None:
        """
        Adds a choice the player can make in a given scene.

        Parameters:
            - from_scene (str): The name of the source scene of the choice.
            - text (str): The text of the choice.
            - to_scene (str): The name of the scene the choice leads to.

        Return:
            None
        """
        self.choices[(from_scene, text)] = to_scene
        self.scenes[from_scene]["choices"].append((text, to_scene))

    def has_choices(self) -> bool:
        """
        Checks whether there are choices available in the current scene.

        Return:
            bool: True if choices are available, False otherwise.
        """
        current_scene = self.scenes[self.current_scene]
        return bool(current_scene.get("choices"))

    def validate_story(self) -> None:
        """
        Validates the consistency of the story by looking for inaccessible scenes.

        Return:
            None
        """
        inaccessible_scenes = set(self.scenes.keys()) - set(self.choices.values())
        if self.current_scene in inaccessible_scenes:
            inaccessible_scenes.remove(self.current_scene)
        
        for scene_name in inaccessible_scenes:
            print(f"Warning: Inaccessible scene '{scene_name}'.")

    def run(self) -> None:
        """
        Runs the main game loop, showing the scenes, available options and processing the player's choices.

        Return:
            None
        """
         # Loads the saved state, if it exists
        if not self.load_state():
            # If it doesn't exist, it creates an empty state
            self.create_empty_state()
        
        while self.current_scene is not None:
            self.show_scene()
            self.show_choices()
            player_choice = input("Choose an option: ")
            self.make_choice(player_choice)
        # Call save_state before exiting the game
        self.save_state()

    def show_scene(self) -> None:
        """
        Displays the current game scene to standard output.

        Return:
            None
        """
        scene = self.scenes[self.current_scene]
        print(scene["text"])
        
        if scene["image"]:
            print("Showing background image:", scene["image"])
        
        if scene["character_image"]:
            character_image = pygame.image.load(os.path.join(IMAGE_DIR, scene["character_image"]))
            character_rect = character_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 0.8))
            self.screen.blit(character_image, character_rect)
            
        if scene["character_speech"]:
            print(f"{self.character['name']}: {scene['character_speech']}")

    def show_choices(self) -> None:
        """
        Displays the options available to the player on standard output.

        Return:
            None
        """
        for choice_text, _ in self.scenes[self.current_scene]["choices"]:
            print(choice_text)

    def make_choice(self, player_choice: str) -> None:
        """
        Processes the player's choice and advances to the next corresponding scene.

        Parameters
            - player_choice (str): The choice made by the player.

        Return:
            None
        """
        choices = self.scenes[self.current_scene]["choices"]
        if 1 <= int(player_choice) <= len(choices):
            selected_choice = choices[int(player_choice) - 1]
            self.current_scene = selected_choice[1]
        else:
            print("Invalid choice.")

    def save_state_to_json(self, filename: str) -> None:
        """
        Saves the current game state to a JSON file.

        Parameters:
            - filename (str): The name of the JSON file to save the state.

        Return:
            None
        """
        print("Saving state to JSON...")
        # Convertendo as chaves do dicionário choices para strings
        choices_str = {str(k): v for k, v in self.choices.items()}
        data = {
            "current_scene": self.current_scene,
            "character_name": self.character["name"],
            "scenes": self.scenes,
            "choices": choices_str  # Usando as chaves convertidas para strings
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Saved state to JSON.")