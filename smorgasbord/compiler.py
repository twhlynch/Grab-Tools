import json, os

MAP_NODES = []

for file in os.listdir("levels"):
    with open(os.path.join("levels", file), "r") as f:
        data = json.load(f)
        levelNodes = data["levelNodes"]
        MAP_NODES += levelNodes

json_data = {
    "ambienceSettings": {
        "skyHorizonColor": {
            "a": 1.0,
            "b": 0.47449225,
            "g": 0.2982486,
            "r": 0.33895752
        },
        "skyZenithColor": {
            "a": 1.0
        },
        "sunAltitude": 38.50704,
        "sunAzimuth": 87.66088,
        "sunSize": 0.5868782
    },
    "complexity": 0,
    "creators": "BLUDUK, NSKC7 (.INDEX), BWLBUCK, LUHMAO, LUNIFOCC, LEVI8020, PEECHYY, THEWHITECRESCENT, TURTLEDUDE1274, ZAZIPOGCHAMP",
    "description": "SMORGASBORD IS A GROUP OF VERIFIED CREATORS THAT MAKE BI-WEEKLY MAPS FOR THE GRAB COMMUNITY. HOSTED BY BLUDUK & NSKC7(.INDEX). VERSION 2 CREATORS IN LEVEL ORDER: TURTLEDUDE, BLUDUK, PEECHYY, NSKC7(.INDEX), ZAZIPOGCHAMP, BWLBUCK, LUNIFOCC, LUHMAO, LEVI8020, THEWHITECRESCENT",
    "formatVersion": 6,
    "levelNodes": MAP_NODES,
    "maxCheckpointCount": 12,
    "title": "SMORGASBORD 2"
}
with open("output.json", "w") as f:
    json.dump(json_data, f, indent=4)

os.system("python GRAB-Level-Format-main/tools/ConvertToLevel.py output.json output.level")
