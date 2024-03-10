# storyforge/ui.py

import os
import sys
from typing import Optional, Tuple

import pygame
from pygame.locals import *

from storyforge.menu import StoryMenu
from storyforge.story import Story

IMAGE_SCENE = "images/scene"
IMAGE_CHAR = "images/character"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
CHOICE_COLOR_NORMAL = (0, 0, 0, 100)
CHOICE_COLOR_HOVER = (0, 0, 0, 180)

class PygameUI:
    """
    Class to manage game UI using Pygame.

    Attributes:
        - story (Story): The game's story object.

    Public Methods:
        - __init__(story: Story): Initializes the game's user interface.
        - show_initial_menu(): Displays the game's initial menu.
        - get_player_name(default_name: str) -> str: Gets the player's name when running the game.
        - render_text_with_background(text: str, height: int, bottom_aligned: bool = False, opacity: int = 128, speech_text: Optional[str] = None) -> pygame.Rect: Renders text with background.
        - render_input_screen(input_string: str, default_name: str) -> None: Renders the input screen for the player name.
        - show_input_screen(default_name: str) -> None: Displays the input screen for the player name.
        - render_choice(choice_text: str, x: int, y: int) -> Tuple[pygame.Rect, int]: Renders a choice on the screen.
        - render_text(text: str, x: int, y: int) -> pygame.Rect: Renders text on the screen.
        - show_scene() -> None: Displays the current game scene on the screen.
        - wait_for_click() -> None: Waits for a mouse click on the screen.
        - show_choices(hover_choice: Optional[int] = None) -> Optional[int]: Displays the choice options on the screen.
        - handle_events() -> None: Handles game events.
        - run() -> None: Starts running the game.
        - check_for_click() -> bool: Checks whether a click has occurred on the screen.
        - check_text_and_speech_displayed() -> bool: Checks whether the scene text and the character's speech (if any) have already been displayed.
        - process_click(pos: Tuple[int, int]) -> None: Processes the mouse click on the screen.
        - save_and_quit() -> None: Saves the current state and closes the game window.
    """

    def __init__(self, story: Story) -> None:
        """
        Initializes the game's user interface.

        Parameters:
            - story (Story): The game's story object.
        """
        self.story = story
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("StoryForge::")
        self.font = pygame.font.SysFont("Arial", 24)
        self.choice_rects = []
        self.player_name = ""
        self.show_character_speech  = False
        self.character_speech_text = ""
        self.show_text_displayed = False  
        self.show_speech_displayed = False 
        self.menu = StoryMenu(story, self)
        self.close_window = True
        pygame.event.set_allowed(pygame.QUIT)
        pygame.event.set_allowed(pygame.KEYDOWN)
        
    def welcome() -> None:
        """
    Displays the welcome message in terminal.

        Return:
            None
        """
        print("Welcome to StoryForge!")

        
    def show_initial_menu(self) -> None:
        """
    Displays the game's home menu on the screen.

        Return:
            None
        """
        self.menu.show_menu()  # Shows the home menu

    def get_player_name(self, default_name: str) -> str:
        """
        Gets the player's name when running the game.

        Parameters:
            - default_name (str): The default name of the player.

         Return:
             str: The player's name.
        """
        # Checks if the player name is already defined in the story object
        if self.story.character["name"]:
            return self.story.character["name"]  # Returns the name of the already defined player
        else:
        
            input_active = True
            input_text = []
            clock = pygame.time.Clock()

            while input_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text.append(event.unicode)

                input_string = "".join(input_text)
                self.render_input_screen(input_string, default_name)

                pygame.display.flip()
                clock.tick(30)

            return input_string if input_string else default_name  

    def render_text_with_background(self, text: str, height: int, bottom_aligned: bool = False, opacity: int = 128, speech_text: Optional[str] = None) -> pygame.Rect:
        """
        Renders text with background on the screen.

        Parameters:
            - text (str): The text to be rendered.
            - height (int): The height of the background rectangle.
            - bottom_aligned (bool): If True, the text is aligned at the bottom of the rectangle.
            - opacity (int): The opacity of the background.
            - speech_text (Optional[str]): The text of the character's speech.

        Return:
            pygame.Rect: The rectangle surrounding the rendered text.
        """
        width = self.screen.get_width()
        x = self.screen.get_width() // 2
        y = self.screen.get_height() - height if bottom_aligned else self.screen.get_height() // 2

        background_rect = pygame.Rect(x - width // 2, y, width, height)
        
        black_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        black_surface.fill((0, 0, 0, opacity))
        
        self.screen.blit(black_surface, background_rect.topleft)

        if speech_text:
            rendered_text = self.font.render(speech_text, True, (255, 255, 255))
        else:
            rendered_text = self.font.render(text, True, (255, 255, 255))

        text_rect = rendered_text.get_rect(center=(x, y + height // 2))
        self.screen.blit(rendered_text, text_rect)

        return background_rect
    
    
    def render_input_screen(self, input_string: str, default_name: str) -> None:
        """
        Renders the input screen for the player name.

        Parameters:
            - input_string (str): The currently entered player name.
            - default_name (str): The default name of the player.

        Return:
            None
        """
        self.screen.fill(BLACK)  # Black background
        
        # Renders white text stating that the default name is "BezerraC"
        default_text = f"Default name: {default_name}"
        default_rendered = self.font.render(default_text, True, WHITE)
        default_rect = default_rendered.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))
        self.screen.blit(default_rendered, default_rect)
        
        # Renders white text
        prompt_text = "Enter the character's name:"
        prompt_rendered = self.font.render(prompt_text, True, WHITE)
        prompt_rect = prompt_rendered.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        
        self.screen.blit(prompt_rendered, prompt_rect)

        # Add input field white text
        text = self.font.render(input_string, True, WHITE)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, prompt_rect.bottom + 35))
        self.screen.blit(text, text_rect)
       

    def show_input_screen(self, default_name: str) -> None:
        """
        Displays the input screen for the player name.

        Parameters:
            - default_name (str): The default name of the player.

        Return:
            None
        """
        self.screen.fill(WHITE)
        prompt_text = f"Enter the character's name: {default_name}"
        text = self.font.render(prompt_text, True, BLACK)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
    
    def render_choice(self, choice_text: str, x: int, y: int) -> Tuple[pygame.Rect, int]:
        """
        Renders a choice on the screen.

         Parameters:
             - choice_text (str): The text of the choice.
             - x (int): The x coordinate of the center of the pick.
             - y (int): The y-coordinate of the center of the pick.

         Return:
             Tuple[pygame.Rect, int]: A tuple containing the rectangle of the choice and the vertical space between choices.
        """
        rect_width = 600
        rect_height = 40
        space_between_choices = 50

        rect = pygame.Rect(x - rect_width // 2, y - rect_height // 2, rect_width, rect_height)
        is_hover = rect.collidepoint(pygame.mouse.get_pos())

        choice_color = CHOICE_COLOR_HOVER if is_hover else CHOICE_COLOR_NORMAL

        choice_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        choice_surface.fill(choice_color)

        rendered_text = self.font.render(choice_text, True, (255, 255, 255))
        text_rect = rendered_text.get_rect(center=(rect_width // 2, rect_height // 2))
        choice_surface.blit(rendered_text, text_rect)

        self.screen.blit(choice_surface, rect.topleft)

        return rect, space_between_choices

    def render_text(self, text: str, x: int, y: int) -> pygame.Rect:
        """
        Renders text on the screen.

        Parameters:
            - text (str): The text to be rendered.
            - x (int): The x-coordinate of the center of the text.
            - y (int): The y-coordinate of the center of the text.

        Return:
            pygame.Rect: The rectangle surrounding the rendered text.
        """
        rendered_text = self.font.render(text, True, (255, 255, 255))
        rect = rendered_text.get_rect(center=(x, y))
        self.screen.blit(rendered_text, rect)
        return rect

    def show_scene(self) -> None:
        """
        Displays the current game scene on the screen.

        Return:
            None
        """
        self.handle_events()
        scene = self.story.scenes[self.story.current_scene]

        if scene["image"]:
            background = pygame.image.load(os.path.join(IMAGE_SCENE, scene["image"]))
            self.screen.blit(background, (0, 0))

        if scene["character_image"]:
            character_image = pygame.image.load(os.path.join(IMAGE_CHAR, scene["character_image"]))
            character_rect = character_image.get_rect(center=(self.screen.get_width() // 2, 900))
            self.screen.blit(character_image, character_rect)

        # Checks for character_speech in the scene
        if scene["character_speech"]:
            if not self.show_character_speech:
                # If there is character_speech and the flag is not activated, render the scene text and wait for the click
                self.render_text_with_background(scene["text"], 150, bottom_aligned=True, opacity=180)
                pygame.display.flip()
                self.wait_for_click()  # Method that waits for click on the screen
                self.show_text_displayed = True  # Marks that the scene text has been displayed
                self.show_character_speech = True
                self.show_speech_displayed = False  # Resets the character's speech marking
                return

            # If the flag is activated, displays the character's speech
            full_speech_text = f"{self.story.character['name']}: {scene['character_speech']}"
            self.character_speech_text = scene["character_speech"]
            self.render_text_with_background(full_speech_text, 150, bottom_aligned=True, opacity=180)
            self.show_speech_displayed = True  # Mark that the character's speech was displayed

        elif not self.show_character_speech:
            # If the flag is not activated and there is no character speech, displays the scene's default text
            self.character_speech_text = ""  # Clears the text of the character's speech
            self.render_text_with_background(scene["text"], 150, bottom_aligned=True, opacity=180)
            self.show_text_displayed = True  # Marks that the scene text has been displayed
        

    def wait_for_click(self) -> None:
        """
        Wait for a mouse click on the screen.

        Returns:
            None
        """
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False
    

    def show_choices(self, hover_choice: Optional[int] = None) -> Optional[int]:
        """
        Displays choice options on the screen.

        Parameters:
            - hover_choice (Optional[int]): The number of the choice being highlighted by the mouse.

        Return:
            Optional[int]: The number of the choice highlighted by the mouse.
        """
        self.choice_rects = []

        y_position = 400

        scene = self.story.scenes[self.story.current_scene]

        # Check if "character_speech" exists in the scene
        if "character_speech" in scene:
            if scene["character_speech"]:
                if not self.show_character_speech:
                    # If there is character_speech and the flag is not activated, render the character_speech before the choice buttons
                    self.show_character_speech = True
                    self.show_scene()

        for i, (choice_text, _) in enumerate(scene["choices"], start=1):
            rect, space_between = self.render_choice(choice_text, self.screen.get_width() // 2, y_position)

            #print(f"Choice {i}: {rect}")
            if rect.collidepoint(pygame.mouse.get_pos()):  # Check hover directly here
                hover_choice = i

            y_position += space_between

        return hover_choice
        
    def handle_events(self) -> None:
        """
        Handles game events.

        Return:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_and_quit()  # Calls save_and_quit() when the window close event is triggered
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.process_click(event.pos)
            
    def run(self, max_iterations: int = None) -> None:
        """
        Starts running the game.

        Return:
            None
        """
        running = True
        clock = pygame.time.Clock()
        iterations = 0
       
        while running:
            if max_iterations is not None and iterations >= max_iterations:
                break
            # Gets the player's name while playing the game
            player_name = self.get_player_name(default_name=self.story.default_player_name["name"])
            # Sets the player's name
            self.story.set_character_name(player_name)

            self.handle_events()

            hover_choice = None
            for i, rect in enumerate(self.choice_rects):
                if rect.collidepoint(pygame.mouse.get_pos()):
                    hover_choice = i + 1
        
            self.show_scene()
            hover_choice = self.show_choices(hover_choice)
            
            pygame.display.flip()
            clock.tick(30)
            
            # Check if the story has come to an end
            if not self.story.has_choices():
                if os.path.exists("story_state.json"):
                    os.remove("story_state.json")

                # If there are no choices, check whether the scene text and the character's speech (if any) have already been read.
                if self.show_character_speech:
                    # If the character's speech has already been displayed and the screen is clicked, the game ends
                    if self.show_speech_displayed and self.check_for_click():
                        self.story.save_state()
                        print("If the character's speech has already been displayed and the screen is clicked, the game ends")
                        self.show_initial_menu()
                else:
                    # If there is no speech from the character, end the game by clicking on the screen
                    if self.check_for_click():
                        self.story.save_state()
                        print("If there is no speech from the character, end the game by clicking on the screen")
                        self.show_initial_menu()
            iterations += 1
                        
    def check_for_click(self) -> bool:
        """
        Checks whether a click has occurred on the screen.

        Return:
            bool: True if a click occurred, False otherwise.
        """
        # Checks whether a click has occurred on the screen
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # self.save_and_quit()
                return True
        return False

    def check_text_and_speech_displayed(self) -> bool:
        """
        Checks whether the scene text and character speech (if any) have already been displayed.

        Return:
            bool: True if the scene text and character speech have already been displayed, False otherwise.
        """
        # Checks whether the scene text and character speech (if any) have already been displayed
        return self.show_text_displayed and (not self.character_speech_text or self.show_speech_displayed)

    def process_click(self, pos: Tuple[int, int]) -> None:
        """
        Processes the mouse click on the screen.

        Parameters:
            - pos (Tuple[int, int]): The (x, y) coordinates of the mouse click.

        Return:
            None
        """
        y_position = 400
        scene = self.story.scenes[self.story.current_scene]

        for i, (choice_text, _) in enumerate(scene["choices"], start=1):
            rect_width = 600
            rect_height = 40
            space_between_choices = 50

            rect = pygame.Rect(self.screen.get_width() // 2 - rect_width // 2, y_position - rect_height // 2, rect_width, rect_height)

            if rect.collidepoint(pos):
                print(f"Choice made: {choice_text}, show_character_speech: {self.show_character_speech}")
                
                # Regardless of the value of show_character_speech, advance to the next scene
                self.story.make_choice(str(i))
                self.show_character_speech = False
                # If there is character_speech, switch between default text and character speech
                if scene["character_speech"]:
                    self.show_character_speech = not self.show_character_speech
                    if self.show_character_speech:
                        self.show_scene()  # Shows the character's speech
                
                break
            
            y_position += space_between_choices

        # Handle click on main screen
        if not any(rect.collidepoint(pos) for rect in self.choice_rects):
            # If clicked on the main screen and there is a character_speech, toggle between the default text and the character's speech
            if scene["character_speech"]:
                self.show_character_speech = not self.show_character_speech
                if self.show_character_speech:
                    self.show_scene()  # Shows the character's speech
                else:
                    pass  # Show default scene text

    def save_and_quit(self) -> None:
        """
        Saves the current state and closes the game window.

        Returns:
            None
        """
        self.screen.fill(BLACK)  # Black background

        # Asks the player if they want to save before exiting
        self.render_text("Do you really want to leave?", self.screen.get_width() // 2, 400)

        choices = ["Yes", "No"]
        rects = []
        for idx, choice in enumerate(choices):
            rect_choice, _ = self.render_choice(choice, self.screen.get_width() // 2, 450 + (idx * 50))
            rects.append(rect_choice)

        pygame.display.flip()
        print("Leaving...")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Checks whether the click was on the "Yes" or "No" options
                    for idx, rect in enumerate(rects):
                        if rect.collidepoint(event.pos):
                            print(choices[idx])
                            if choices[idx] == "Yes":
                                self.story.save_state()  # Saves the current state
                                pygame.quit()
                                sys.exit()
                            elif choices[idx] == "No":
                                pygame.event.clear()  # Clears all events from the pygame event queue
                                self.close_window = False  # Sets close_window to False
                                return  # Return to the game without saving