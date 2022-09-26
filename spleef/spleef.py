import json

with open('lobby-dojo.json', 'r') as f:
    level = json.load(f)
    nodes = level['levelNodes']
    for i in range(len(nodes)):
        try:
            nodeData = nodes[i]['levelNodeStatic']
            nodeData['respawnTime'] = 1200.0
            nodeData['stableTime'] = 10.0
            try:
                del nodeData['color']
            except:
                pass
            newNode = {
                'levelNodeCrumbling': nodeData
            }
            nodes[i] = newNode
        except:
            pass
    level['levelNodes'] = nodes
    with open('Faded.json', 'w') as n:
        json.dump(level, n)