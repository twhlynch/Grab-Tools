# Grab-Tools

A collection of tools and resources created/used for Grab VR by slindev.com

## Overview

This repository contains some resources and tools I have created, or aquired that are useful in Grab VR. Currently I have an image to pixel art converter, a 3d model loader, .JSON and .level type converters, and the old lobbies .level files.

Levels in GRAB are stored in .level files.
On Windows:
GRAB stores everything in ```Documents/GRAB``` or ```Documents/GRAB-Demo```.

On Quest:
GRAB stores everything in ```Android/data/com.slindev.grab``` or ```Android/data/com.slindev.grab_demo```.

## Pixel Art

### GrabPixelGen

This tool allows you to generate a .level file from an image file. It will create a level with a small platform and a large colored cube array that makes the pixel art.

#### Usage

``` python3 GrabPixelGen.py img/input.jpg LevelName ``` or ``` python GrabPixelGen.py img/input.jpg LevelName ```, depending on your setup will output a .level file into the ```generation/level_output ``` folder and can be moved into your GRAB ```files\levels\user``` folder to open in the games editor.

The default resolution is 38x38 as it is the max that grab allows without breaking the complexity (if you have 3000 complexity). If you only have 1000 complexity, or you want a smaller or larger resolution you can add ```-q <resolution>``` to the command. The highest for 1000 complexity is 22x22 so use a max of ```-q 22```.

#### Credits

The .proto files, ConvertToLevel.py, and everything in generation/generated was made by [Slin](https://slindev.com/), the creator of Grab.

Any use of the pixel art generator should add "GrabPixelGen", "nskc7", or ".index" as a creator of the level.

### Minecraft Block to Pixel art

This tool allows you to generate a .level file from a Minecraft block. It will create a level with a small platform and a large colored cube that makes the block.

## 3D Models

### GrabPointCloudGen

This tool allows you to generate a .level file from a .obj file. It will create a level with a small platform and a bunch of circles at the vertices of each triangle in the models point cloud.

#### Usage

``` python3 GrabPointCloudGen.py models/input.obj LevelName ``` or ``` python GrabPointCloudGen.py models/input.obj LevelName ```, depending on your setup will output a .level file into the ```generation/level_output ``` folder and can be moved into your GRAB ```files\levels\user``` folder to open in the games editor.

#### Credits

The .proto files, ConvertToLevel.py, and everything in generation/generated was made by [Slin](https://slindev.com/), the creator of Grab.

Any use of the model generator should add "GrabModelGen", "GrabPointCloudGen", "nskc7", or ".index" as a creator of the level.

### GrabPolyGen (Work in progress)

This tool allows you to generate a .level file from a .obj file. It will create a level with a small platform and a polygon mesh of triangles that will make the model.

#### Usage

``` python3 GrabPolyGen.py models/input.obj LevelName ``` or ``` python GrabPolyGen.py models/input.obj LevelName ```, depending on your setup will output a .level file into the ```generation/level_output ``` folder and can be moved into your GRAB ```files\levels\user``` folder to open in the games editor.

#### Credits

The .proto files, ConvertToLevel.py, and everything in generation/generated was made by [Slin](https://slindev.com/), the creator of Grab.

Any use of the model generator should add "GrabModelGen", "GrabPolyGen", "nskc7", or ".index" as a creator of the level.

## Old Lobbies

in ``` /lobbies ``` are the old lobbies that were used in the game in prior updates. They are stored in .level files and can be opened in the games editor by putting them in ```files\levels\user```.

## JSON To Level

```ConverToJSON.py``` is a tool that converts a .JSON file to a .level file.

### Usage

```python3 ConvertToLevel.py sample.json sample.level``` or ```python ConvertToLevel.py sample.json sample.level```, depending on your setup will output a .level file into the ```generation/level_output ``` folder and can be moved into your GRAB ```files\levels\user``` folder to open in the games editor.

## Level To JSON

```ConverToJSON.py``` is a tool that converts a .level file to a .JSON file.

### Usage

```python3 ConvertToJSON.py sample.level sample.json``` or ```python ConvertToJSON.py sample.level sample.json```, depending on your setup will output a .json file into the ```JSON .level/generated ``` folder.
