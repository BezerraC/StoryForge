import pathlib

import setuptools
from setuptools import find_packages

setuptools.setup(
    name="StoryForge",
    version="0.0.1",
    author="BezerraC",
    author_email="<cbezerraneto@gmail.com>",
    description="Engine to create interactive stories",
    long_description_content_type="text/markdown",
    long_description="StoryForge allows users to create and play their own interactive stories. Players can make decisions that affect the course of the story, providing an engaging and personalized experience.",
    project_urls={
        "Documentation": "https://storyforge.readthedocs.io/en/latest/",
        "Source": "https://github.com/BezerraC/StoryForge"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities" ,
    ],
    install_requires=['pillow', 'pygame', 'pyinstaller', 'Sphinx', 'sphinx-rtd-theme'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "StoryForge = storyforge.ui:PygameUI.welcome",  
        ],
    },
)

