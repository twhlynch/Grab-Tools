import json, os

MAP_NODES = []

for file in os.listdir("levels"):
    if file.endswith(".json"):
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
    "creators": "BLUDUK,.INDEX,ANTIIQX,CHOOCHOO,CJBEAST,CONVRIST,SPARKS,JEFFBOB,DARING,CHRISTSAM",
    "description": "SMORGASBORD IS A GROUP OF VERIFIED CREATORS THAT MAKE BI-WEEKLY MAPS FOR THE GRAB COMMUNITY. HOSTED BY BLUDUK & NSKC7(.INDEX). VERSION 2 CREATORS: ANTIIQX, BLUDUK, CHOOCHOOISCOOL, NSKC7(.INDEX), CJBEAST, CONVRIST, EB.SPARKS, JEFFBOBDUDE, TTV_DARING, CHRISTSAM36",
    "formatVersion": 6,
    "levelNodes": MAP_NODES,
    "maxCheckpointCount": 12,
    "title": "SMORGASBORD 4"
}
with open("output.json", "w") as f:
    json.dump(json_data, f, indent=4)

os.system("python GRAB-Level-Format-main/tools/ConvertToLevel.py output.json output.level")
