import json, random, os

suffixes = [
    "-beach",
    "-cave",
    "-christmas",
    "-dojo",
    "-temple",
    "",
    "-treehouse"
]
materials = [
    # 0 - 9?
    "default",
    "default_colored",
    "grabbable",
    "grabbable_crumbling",
    "grapplable",
    "grapplable_lava",
    "ice",
    "lava",
    9
]
for i in range(len(suffixes)):
    with open('lobby'+suffixes[i]+'.json', 'r') as f:
        data = json.load(f)
        nodes = data["levelNodes"]
        for j in range(len(nodes)):
            try:
                nodes[j]["levelNodeStatic"]["material"] = (materials[random.randint(0, len(materials)-1)]).upper()
            except:
                pass
        with open('randomized/lobby'+suffixes[i]+'-randomized+bounce.json', 'w') as n:
            json.dump(data, n, indent=4)
    os.system('python ConvertToLevel.py randomized/lobby'+suffixes[i]+'-randomized+bounce.json randomized/lobby'+suffixes[i]+'-randomized+bounce.level')