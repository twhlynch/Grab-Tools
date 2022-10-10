import random


json1='''
{
    "levelNodeStatic": {
    "material": "DEFAULT_COLORED",
    "shape": "CUBE",
    "scale": {
        "x": 0.5,
        "y": 0.5,
        "z": 0.5
    },
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
    },
    "color": {
        "r": 1,
        "g": 1,
        "b": 1,
        "a": 1
    }
    },
    "animations": [
    {
        "name": "spin",
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
        }'''

json2='''
        ]
    }
    ]
}
'''

print(json1)



for i in range(10):
    
    anim = '''
    ,{
        "time": '''+str(i+1)+''',
        "position": {
        "x": 0,
        "y": 0,
        "z": 0
        },
        "rotation": {
        "x": '''+str(random.randint(-1000, 1000)/1000)+''',
        "y": '''+str(random.randint(-1000, 1000)/1000)+''',
        "z": '''+str(random.randint(-1000, 1000)/1000)+''',
        "w": '''+str(random.randint(-1000, 1000)/1000)+'''
        }
    }
    '''
    print(anim)


print(json2)