import os
from PIL import Image
import numpy as np
import math
import sys

def getAverageColor(colors):
    red = 0
    green = 0
    blue = 0
    for color in colors:
        red += color[0]
        green += color[1]
        blue += color[2]
    red = (red / len(colors)) / 255
    green = (green / len(colors)) / 255
    blue = (blue / len(colors)) / 255
    if blue == 0:
        blue = 0.0001
    if green == 0:
        green = 0.0001
    if red == 0:
        red = 0.0001
    if blue == 1:
        blue = 0.9999
    if green == 1:
        green = 0.9999
    if red == 1:
        red = 0.9999
    return ([red, green, blue])

def main():
    if len(sys.argv) < 2:
        print('GrabPixelGen.py img/input.jpg LevelName')
        return
    quality = 38
    if len(sys.argv) == 4:
        if sys.argv[3] == '-q':
            quality = int(sys.argv[4])
    image = Image.open(sys.argv[1])
    pixels = np.array(image)
    width, height = image.size
    chunkWidth = math.floor(width / quality)
    chunkHeight = math.floor(height / quality)
    chunks = []
    for cy in range(quality):
        for cx in range(quality):
            # chunk
            chunkColors = []
            for y in range(chunkHeight):
                for x in range(chunkWidth):
                    chunkColors.append(pixels[cy * chunkHeight + y][cx * chunkWidth + x])
            chunkColor = getAverageColor(chunkColors)
            chunks.append(chunkColor)
    start = '''{
    "title": "'''+sys.argv[2]+'''",
    "description": "description",
    "creators": "GrabPixalGen",
    "checkpoints": 10,

    "start": {
        "position": [28.0, -'''+str(quality)+'''.0, 10.0],
        "rotation": [0.0, 0.0, 0.0, 1.0],
        "radius": 0.5
    },
    "finish": {
        "position": [26.0, -'''+str(quality)+'''.0, 10.0],
        "radius": 0.5
    },

    "nodes": [
        {
            "type": "default",
            "shape": "cube",
            "position": [27.0, -'''+str(quality)+'''.5, 10.0],
            "rotation": [0.0, 0.0, 0.0, 1.0],
            "scale": [4.0, 1.0, 2.0]
        }'''
    end = ''']
}'''
    xPos = 0
    yPos = 0
    json = ''
    for chunk in chunks:
        json += ''',
        {
            "type": "default_colored",
            "shape": "cube",
            "position": ['''+str(xPos)+'''.0, '''+str(yPos)+'''.0, 0.0],
            "rotation": [0.0, 0.0, 0.0, 1.0],
            "scale": [1.0, 1.0, 1.0],
            "color": ['''+str(chunk[0])+''', '''+str(chunk[1])+''', '''+str(chunk[2])+''']
        }'''
        xPos += 1
        if xPos == quality:
            xPos = 0
            yPos -= 1
    json = start + json + end
    with open("generation/pixels.json", "w") as f:
        f.write(json)
        try:
            os.system('python generation/ConvertToLevel.py generation/pixels.json "generation/level_output/'+sys.argv[2]+'.level"')
        except:
            os.system('python3 generation/ConvertToLevel.py generation/pixels.json "generation/level_output/'+sys.argv[2]+'.level"')


if __name__ == "__main__":
    main()