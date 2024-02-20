# Hi! This is the StoryForge example game. 

from storyforge.story import Story
from storyforge.ui import PygameUI

# Input your start scene name below.
story = Story("start")

# The game starts here.
ui = PygameUI(story)
ui.show_initial_menu() 


# Create your story :D
story.add_scene("start", "You wake up in a mysterious room.", "room.jpg",  "boy.png", character_speech="Where am I?")
story.add_choice("start", "Go through the door", "door_scene")
story.add_choice("start", "Look out the window", "window_scene")

story.add_scene("door_scene", "You find a hallway.", "corredor.jpg", character_speech="What do I do?")
story.add_choice("door_scene", "Go to the library", "lib_scene")
story.add_choice("door_scene", "Look out the window", "window_scene")

story.add_scene("window_scene", "You see a garden down there.", "jardim.jpg", "boy.png", character_speech="What place is this?")
story.add_choice("window_scene", "Go to the library", "lib_scene")
story.add_choice("window_scene", "Go to the backyard", "outside_scene")

# Ending 1
story.add_scene("outside_scene", "You leave the house.", "outside.jpg", character_speech="Let's go out...")

# Ending 2
story.add_scene("lib_scene", "You go to the library.", "biblioteca.jpg", character_speech="Let's look for a book...")

# Inaccessible scene 
story.add_scene("room_scene", "You go to the room.", "room.jpg", character_speech="Good room")

# After running the program, activate story shows if there are any inaccessible scenes
story.validate_story() 
ui.run()