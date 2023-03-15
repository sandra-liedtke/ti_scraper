# Installation

This document describes how to initially prepare your environment, dependent libraries and the project for Windows and Linux and how to get started. 

## Windows

 - Install Python 3.9 or higher from https://www.python.org/downloads/
 - Open Command Prompt and type `python --version`
     - If Python is **not** recognized as a command, do the following:
     - Open the *Environment Variables* and add the path to the Python Installation to the *Path* variable
     - You might need to reboot for changes to take effect
     - After rebooting try again the `python --version` command
 - In Command Prompt type `pip --version`
     - If pip is not recognized as a command, download the script from https://bootstrap.pypa.io/get-pip.py
     - Back on Command Prompt, type `python get-pip.py`
     - Try again the `pip --version` command
 - In Command Prompt type `pip list`
     - Make sure that (among others) also the beautifulsoup4, requests and stem libraries are listed
     - If any of the libraries is **not** listed, type `pip install <libraryname>` to install it

## Linux

 - You might need to do an update on existing software before continuing. To do so, in the command line type `sudo apt update`
 - Type `sudo apt install python3.X`
 - Type `python3 --version`
 - Type `python3.X` and then `help("modules")` and make sure that (among others) also the beautifulsoup4, requests and stem libraries are listed
     - If any of the libraries is **not** listed, type `sudo apt-get install python3-<libraryname>` to install it

# Getting Started

 - Download the repository and extract it
 - Review the configurations in the related *_config.json and adjust them where necessary
 - In the Command Line, navigate to the extracted folder and then navigate to the scripts folder
 - Type `python <scriptname>.py` or - if on Linux - `python3 <scriptname>.py` to start the script
 - The Command Line should look something similar to the below:

    ![Windows Cmd Screenshot](/assets/images/getting_started.PNG "Windows Cmd Screenshot")