import json

group_json = {
    "levelNodeGroup": {
        "childNodes": [
        ]
    },
    "animations": [
        {
            "name": "NAME",
            "direction": "CYCLE",
            "frames": [
            ]
        }
    ]
}

frames_json = [{
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
},{
    "time": 1000,
    "position": {
        "x": 1000,
        "y": 1000,
        "z": 1000
    },
    "rotation": {
        "x": 0,
        "y": 0,
        "z": 0,
        "w": 1
    }
}
]

with open('level.json') as json_file:
    data = json.load(json_file)
    nodes_json = data["levelNodes"]
    group_json["levelNodeGroup"]["childNodes"] = nodes_json
    group_json["animations"][0]["frames"] = frames_json
    data["levelNodes"] = [group_json]

with open('level.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)