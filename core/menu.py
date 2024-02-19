# core/menu.py
import pygame


class StoryMenu:
    """
    Class responsible for displaying and managing the game menu.

    Attributes:
        - story (Story): The game's story object.
        - ui (PygameUI): The game's user interface object.

    Methods:
        - show_menu(): Displays the game's main menu on the screen.
        - continue_story(): Continues the story from a saved state or starts a new story, as chosen by the player.
        - start_new_story(): Starts a new story, creating an empty state.
    """
    def __init__(self, story, ui):
        self.story = story
        self.ui = ui

    def show_menu(self) -> None:
        """
        Displays the game's main menu on the screen.

        Return:
            None
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            self.ui.screen.fill((0, 0, 0))  # Fill the background with black

            # Render the menu
            self.ui.render_text("StoryForge:", self.ui.screen.get_width() // 2, 400)
            rect_1, _ = self.ui.render_choice("Continue the story", self.ui.screen.get_width() // 2, 450)
            rect_2, _ = self.ui.render_choice("Start a new story", self.ui.screen.get_width() // 2, 500)
            rect_3, _ = self.ui.render_choice("Leave", self.ui.screen.get_width() // 2, 550)

            pygame.display.flip()
    
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica se o clique foi nas opções
                    if rect_1.collidepoint(event.pos):
                        print("Continue the story")
                        self.continue_story()
                        running = False
                    elif rect_2.collidepoint(event.pos):
                        print("Start a new story")
                        self.start_new_story()
                        running = False
                    elif rect_3.collidepoint(event.pos):
                        print("Leave")
                        self.ui.save_and_quit()

            clock.tick(30)

    def continue_story(self) -> None:
        """
        Continue the story from a saved state or start a new story, as chosen by the player.

        Return:
            None
        """
        if self.story.load_state():
            self.story.validate_story()
        else:
            print("There is no saved state. Starting new story.")
            self.start_new_story()

    def start_new_story(self) -> None:
        """
        Starts a new story, creating an empty state.

        Return:
            None
        """
        self.story.create_empty_state()