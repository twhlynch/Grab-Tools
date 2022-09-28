# GRAB-Level-Format
GRAB level format specification and tools

Levels in GRAB are stored in .level files. The format is a [Google Protocol Buffer (proto3)](https://developers.google.com/protocol-buffers) written into a file. The files in the ```protofiles``` directory define the data layout and can be used to generate source files to read or write level files. For now only python files are pregenerated and can be found in the ```tools/generated``` directory.

To generate files for the language of your choice you need to install the protobuf compiler. ```GeneratePython.sh``` shows how to run it for python. To use the pre generated python files, you'll need to install the python protobuf module: ```pip install protobuf```.

On Windows:
GRAB stores everything in ```Documents/GRAB``` or ```Documents/GRAB-Demo```.

On Quest:
GRAB stores everything in ```Android/data/com.slindev.grab``` or ```Android/data/com.slindev.grab_demo```.

Your own levels that can be opened and saved in the editor are stored in ```levels/user``` The file name should have the ```.level``` extension, but the name itself can be anything. By default the game uses timestamps for the names to prevent any naming conflicts with already existing levels. Level file names only need to be unique for a user unless you want to update an existing level.

At the root there is the Level object which can have some basic properties:
* formatVersion - uint32 - This is used to filter out levels on old game versions that use new features. The current version is 6.
* title - string - The name of the level.
* creators - string - A comma seperated list of the names of the people that worked on the level.
* description - string - A short description of what to expect from the level.
* complexity - uint32 - The complexity value should be calculated from the levels levelNodes. It's the sum of each level nodes complexity. Start and finish cost 0, signs cost 5, crumbling nodes cost 3 and everything else costs 2. These costs might change and the server may verify the value in the future.
* maxCheckpointCount - uint32 - The maximum number of checkpoints that can be used in a level.

It also has a **levelNodes** property.
This is an array of all the level nodes the level is made of. Each level node defines one of the supported level building blocks. There are several different level node types with different properties. Check "types.proto" for details.

All shapes have dimensions of 1x1x1m with their origin at the center.

```ConvertToLevel.py``` is an example for converting from a simple json format (see sample.json) to a level file. It can be run with python 3: ```python3 ConvertToLevel.py sample.json sample.level```


