import math, json

def animate_object(node, px, py, pz, xmax, zmax):
    x = 1000
    y1 = (1/(-px/(xmax/2))) * (x-px) - (px**2)/xmax
    z = 1000
    y2 = (1/(-pz/(zmax/2))) * (z-pz) - (pz**2)/zmax
    y = (y1 + y2)/2 + py

    group_json = {
        "levelNodeGroup": {
            "childNodes": [
                node
            ]
        },
        "animations": [
            {
                "name": "NAME",
                "direction": "CYCLE",
                "frames": [
                    {
    "time": 0,
    "position": {
        "x": 0,
        "y": 0,
        "z": 0
    },
    "rotation": {
        "x": 0,
        "y": 0,
        "z": 0,
        "w": 1
    }
},
{
    "time": 10000,
    "position": {
        "x": x,
        "y": y,
        "z": z
    },
    "rotation": {
        "x": 0,
        "y": 0,
        "z": 0,
        "w": 1
    }
}
                ]
            }
        ]
    }
    return group_json

with open('smrgsbd.json') as json_file:
    json_obj = json.load(json_file)
    xmax = 0
    zmax = 0
    for node in json_obj["levelNodes"]:
        try:
            if math.sqrt(node[0]["levelNodeStatic"]["position"]["x"] ** 2) > xmax:
                xmax = math.sqrt(node[0]["levelNodeStatic"]["position"]["x"] ** 2)
            if math.sqrt(node[0]["levelNodeStatic"]["position"]["y"] ** 2) > zmax:
                zmax = math.sqrt(node[0]["levelNodeStatic"]["position"]["y"] ** 2)
        except:
            pass
    for node in json_obj["levelNodes"]:
        try:
            x = node[0]["levelNodeStatic"]["position"]["x"]
            y = node[0]["levelNodeStatic"]["position"]["y"]
            z = node[0]["levelNodeStatic"]["position"]["z"]
            node = animate_object(node, x, y, z, xmax, zmax)
        except:
            pass
with open('explosion.json', 'w') as outfile:
    json.dump(json_obj, outfile, indent=4)