![StoryForge Banner](https://raw.githubusercontent.com/BezerraC/StoryForge/main/docs/StoryForge.png)
# StoryForge

StoryForge is an interactive storytelling engine developed in Python.

## Description

StoryForge allows users to create and play their own interactive stories. Players can make decisions that affect the course of the story, providing an engaging and personalized experience.

[Click here to view the documentation](https://github.com/BezerraC/StoryForge/docs/_build/html/index.html)

## Features

- Creation of stories with multiple scenes and choices for players.
- Intuitive user interface using pygame for graphical rendering.
- Ability to save and load game state.
- Options to continue a story or start a new one.
- Support for background images and character sprites.

## 💻 Installation

1. Clone the repository:

```
git clone https://github.com/BezerraC/StoryForge.git 
```

2. Create the virtual environment:

Linux and macOS:

```
python3 -m venv venv

source venv/bin/activate
or
source venv/bin/activate.csh
```

Windows:
```
python -m venv venv

venv\Scripts\activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## 🚀 Usage

To start StoryForge, run the following command in the terminal:
```
python example.py
```

This will open the main menu, where you can choose to continue a story or start a new one.

## 🧪 Unit Tests
You can also run integration tests to verify the behavior of the system as a whole. Integration tests ensure that different parts of the system work correctly together.

```
python .\tests\testUi.py
```
To test the user interface

```
python .\tests\testStory.py
```
To test the story building

```
python .\tests\testMenu.py
```
To test menu functionalities

## ⚒ Build

To build the project, you'll need to have Python installed on your system. The build.py script can be used to compile the project for different platforms and resolutions.

### Prerequisites

Make sure you have the following requirements met before building the project:

- Python 3.12 or higher installed on your system.
- Python dependencies installed. You can install them by running `pip install -r requirements.txt`.

### How to Use

1. Open a terminal.
2. Navigate to the root directory of your project.
3. Run the build script providing the necessary arguments. For example:

```python
python build.py --platform <platform> --resolution <resolution>
```

## 📫 Contributing to StoryForge

To contribute to StoryForge, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name> / <location>`
5. Create the pull request.

Alternatively, see the GitHub documentation at [how to create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


## 📝 Author

<img src="https://avatars.githubusercontent.com/u/41126326?v=4" width="150" style="border-radius:15px;" alt="Exemplo imagem">

[@Bezerrac](https://github.com/BezerraC)

