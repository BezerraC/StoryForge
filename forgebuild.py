#build.py

import argparse
import ast
import json
import os
import platform
import shutil
import subprocess
from typing import List, Set, Tuple

from PIL import Image


def resize_images(resolution: str) -> None:
    """
    Resizes scene images according to the specified resolution.

    Parameters:
        - resolution (str): The target resolution for resizing ('hd', 'fullhd' or '4k').

    Return:
        None
    """
    if resolution == 'hd':
        target_resolution = (1280, 720)
    elif resolution == 'fullhd':
        target_resolution = (1920, 1080)
    elif resolution == '4k':
        target_resolution = (3840, 2160)
    else:
        raise ValueError("Invalid resolution. Choose between 'hd', 'fullhd' and '4k'.")

    image_dir = os.path.join(os.getcwd(), "images/scene")
    for filename in os.listdir(image_dir):
        filepath = os.path.join(image_dir, filename)
        if os.path.isfile(filepath):
            with Image.open(filepath) as img:
                img_resized = img.resize(target_resolution)
                img_resized.save(filepath)

def compile_bootloader(platform_name: str) -> None:
    """
    Compiles the bootloader for the specific platform.

    Parameters:
        - platform_name (str): The name of the target platform ('windows' or 'linux').

    Return:
        None
    """
    # Check current platform
    current_platform = platform.system().lower()
    
    # Define compilation commands for each platform
    if current_platform == 'windows':
        if platform_name == 'windows':
            compile_command = 'python ./waf all --target-arch=64bit'
        else:
            compile_command = 'python ./waf all --target-arch=32bit'
    elif current_platform == 'linux':
        compile_command = 'python ./waf all'
    else:
        print("Platform not supported.")
        return
    
    # Run the build command
    subprocess.run(compile_command, shell=True)


def extract_scenes(file_path: str) -> Tuple[List[str], Set[str], Set[str]]:
    """
    Extracts scenes, mentioned choices, and mentioned scenes from the specified file.

    Parameters:
        - file_path (str): The path to the file containing the story.

    Return:
        Tuple[List[str], Set[str], Set[str]]: A tuple containing lists of scenes, mentioned choices,
        and mentioned scenes.
    """
    with open(file_path, "r") as file:
        code = file.read()
        tree = ast.parse(code)
        scenes = []
        mentioned_choices = set()
        mentioned_scenes = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == "add_scene":
                        scenes.append(node.args[0].value)
                    elif node.func.attr == "add_choice":
                        mentioned_choices.update([arg.value for arg in node.args[1:]])
                        mentioned_scenes.add(node.args[0].value)
        return scenes, mentioned_choices, mentioned_scenes
    
def print_warning(message: str) -> None:
    """
    Prints a warning message with orange color in the terminal.

    Parameters:
        - message (str): The warning message to be printed.

    Return:
        None
    """
    # ANSI code for the color orange
    orange_color_code = '\033[33m'
    # ANSI code to reset terminal color
    reset_color_code = '\033[0m'
    # Print the warning in orange
    print(f"{orange_color_code}Warning: {message}{reset_color_code}")


def build(platform: str, resolutions: List[str], languages: List[str], history_file) -> None:
    """
    Builds the project for the specified platforms, resolutions, and languages.

    Parameters:
        - platform (str): The target platform for the build ('windows' or 'linux').
        - resolutions (List[str]): The resolutions to build to ('hd', 'fullhd' or '4k').
        - languages (List[str]): The languages to build for ('en' or 'pt').
        - history_file (str): The name of the file containing the story.

    Return:
        None
    """

    # Get the path of the history file (example.py) file
    history_path =  os.path.join(os.getcwd(), history_file)
    current_dir = os.getcwd()  # Get current directory

    # Extract the scenes from the example.py file
    mentioned_scenes, mentioned_choices, defined_scenes = extract_scenes(history_path)

    # Add the scenes mentioned in the choices to the defined scenes
    defined_scenes.update(mentioned_choices)

    # Scene validation
    inaccessible_scenes = [scene for scene in mentioned_scenes if scene not in defined_scenes]
    
    if inaccessible_scenes:
        print_warning("The following scenes are mentioned but not defined:")
        for scene in inaccessible_scenes:
            print_warning(f"- {scene}")
    else:
        print("All scenes are accessible.")


    for resolution in resolutions:
        for language in languages:

            print(f"Building for platform: {platform}, resolution: {resolution}, language: {language}")
            # Resize images according to resolution
            resize_images(resolution)
            
            # Build the executable using PyInstaller and specify the bootloader to use
            subprocess.run(["pyinstaller", history_file, "--onefile"])

            # Change working directory to 'dist' directory
            os.chdir(os.path.join(current_dir, "dist"))
            # Copy 'images' directory to 'dist'
            shutil.copytree(os.path.join(current_dir, "images"), "images", dirs_exist_ok=True)
            # Restore the original working directory
            os.chdir(current_dir)
            
if __name__ == "__main__":
    # Configure command-line argument parsing
    parser = argparse.ArgumentParser(description="Build script for pygame project")
    parser.add_argument("--history-file", help="Name of the file containing the story")
    parser.add_argument("--platform", choices=["windows", "linux"], help="Platform to build on")
    parser.add_argument("--resolution", nargs="+", choices=["hd", "fullhd", "4k"], help="Resolutions to build towards")
    parser.add_argument("--language", nargs="+", choices=["en", "pt"], help="Languages to build for")

    args = parser.parse_args()

    # Call the construction function with the given arguments
    build(args.history_file,args.platform, args.resolution, args.language)
