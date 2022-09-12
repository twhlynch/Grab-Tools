# GrabPixelGen

Levels in GRAB are stored in .level files.
On Windows:
GRAB stores everything in ```Documents/GRAB``` or ```Documents/GRAB-Demo```.

On Quest:
GRAB stores everything in ```Android/data/com.slindev.grab``` or ```Android/data/com.slindev.grab_demo```.

This tool allows you to generate a .level file from a .jpg or .png file. It will create a level with a small platform and a large block array that makes the pixel art.

## Usage

``` python3 GrabPixelGen.py img/input.jpg LevelName ``` or ``` python GrabPixelGen.py img/input.jpg LevelName ```, depending on your setup will output a .level file into the ```generation/level_output ``` folder and can be moved into your GRAB ```files\levels\user``` folder to open in the games editor.

The default resolution is 38x38 as it is the max that grab allows without breaking the complexity (if you have 3000 complexity). If you only have 1000 complexity, or you want a smaller or larger resolution you can add ```-q <resolution>``` to the command. The highest for 1000 complexity is 22x22 so use a max of ```-q 22```.

## Credits

The .proto files, ConvertToLevel.py, and everything in generation/generated was made by [Slin](https://slindev.com/), the creator of Grab.

Any use of the pixel art generator should leave "GrabPixelGen" as a creator of the level.