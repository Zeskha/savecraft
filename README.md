
# Savecraft

Savecraft is a simple and straightforward app that eases and improves the backup of files for Minecraft worlds.

## Features
All the features are found in the settings tab of the app 
- Save as a folder or a zip file
- Add the date to the file name
- Create a desktop shortcut for quickly saving a world(with the desired above settings)



## Installation
The application can be run using the   Savecraft.py file, the other files are not requiered for running the  app.

It also requires Python 3.x and the libraries listed in requirements

-------------

Another option is generating a .exe file, in which case you will need both icon images and the Savecraft.spec file in the same folder with Savecraft.py.
```bash
  git clone https://github.com/Zeskha/savecraft

```

 Also installing pyinstaller with pip
```bash
  pip install pyinstaller

```
Then you have to open a console in the folder or navigate to the folder in the console and run
```bash
  pyinstaller Savecraft.spec
```

    