import os, math, sys, random
import numpy as np

shapes = [
    "cube",
    "sphere",
    "cylinder",
    "pyramid",
    "prism"
]

types = [
    "default",
    "default_colored",
    "grabbable",
    "grabbable_crumbling",
    "grapplable",
    "grapplable_lava",
    "ice",
    "lava"
]

levelNodes = [{
    "type": "default_colored",
    "shape": "cube",
    "position": [0, 0, 0],
    "rotation": [0, 0, 0, 1],
    "scale": [2, 1, 50],
    "color": [0.5, 0.5, 0.5]
},{
    "type": "lava",
    "shape": "cube",
    "position": [10000, 0, 25],
    "rotation": [0, 0, 0, 1],
    "scale": [20000, 100, 1]
},{
    "type": "lava",
    "shape": "cube",
    "position": [10000, 0, -25],
    "rotation": [0, 0, 0, 1],
    "scale": [20000, 100, 1]
},{
    "type": "lava",
    "shape": "cube",
    "position": [10000, 50, 0],
    "rotation": [0, 0, 0, 1],
    "scale": [20000, 1, 50]
},{
    "type": "lava",
    "shape": "cube",
    "position": [10000, -5, 0],
    "rotation": [0, 0, 0, 1],
    "scale": [20000, 1, 50]
}
]

def euler_to_quaternion(r):
    roll = r[0]
    pitch = r[1]
    yaw = r[2]
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    return [qx, qy, qz, qw]

def add_object(type, shape, position, rotation, scale, extra = [False, False]):
    if extra[0] == "color":
        levelNodes.append({
            "type": type,
            "shape": shape,
            "position": position,
            "rotation": rotation,
            "scale": scale,
            "color": extra[1]
        })
    elif extra[0] == "crumbling":
        levelNodes.append({
            "type": type,
            "shape": shape,
            "position": position,
            "rotation": rotation,
            "scale": scale,
            "stable_time": 2.0,
            "respawn_time": 2.0
        })
    else:
        levelNodes.append({
            "type": type,
            "shape": shape,
            "position": position,
            "rotation": rotation,
            "scale": scale
        })

def level_floating_jumps(position):
    previous = position
    type = types[random.randint(0, 3)]
    shape = shapes[random.randint(0, 2)]
    tall = random.randint(0, 1)
    for i in range(random.randint(10, 20)):
        pos = [previous[0] + random.randint(5, 10), previous[1] + random.randint(-1, 1), previous[2] + random.randint(-5, 5)]
        if pos[2] > 20:
            pos[2] = 20
        if pos[2] < -20:
            pos[2] = -20
        previous = pos
        rotation = [0, 0, 0]
        scale = 1
        if shape == "sphere":
            scale = random.randint(1, 3)
        height = scale
        if shape == "cylender":
            height = 2 * scale
            if random.randint(0, 1) == 0:
                rotation = [90, 0, 0]
        if shape == "cube" or shape == "cylender":
            if tall == 1:
                height = 10
                if rotation == [90, 0, 0]:
                    height = 50
        extra = [False, False]
        if type == "default_colored":
            extra[0] = "color"
            extra[1] = [random.randint(1, 254) / 255, random.randint(1, 254) / 255, random.randint(1, 254) / 255]
        if type == "grabbable_crumbling":
            extra[0] = "crumbling"
        add_object(type, shape, [pos[0], pos[1] - height / 2, pos[2]], euler_to_quaternion(rotation), [scale, height, scale], extra)
    return previous

def level_lava_jumps(position):
    previous = position
    type = types[random.randint(0, 3)]
    shape = shapes[random.randint(0, 3)]
    for i in range(random.randint(10, 20)):
        pos = [previous[0] + random.randint(5, 10), -5, previous[2] + random.randint(-5, 5)]
        if pos[2] > 20:
            pos[2] = 20
        if pos[2] < -20:
            pos[2] = -20
        previous = pos
        rotation = [0, 0, 0]
        scale = 1
        if shape == 'sphere' and random.randint(0, 1) == 0:
            scale = 2
        height = 1
        if shape == "cylender" or shape == "pyramid":
            height = 10
        extra = [False, False]
        if type == "default_colored":
            extra[0] = "color"
            extra[1] = [random.randint(1, 254) / 255, random.randint(1, 254) / 255, random.randint(1, 254) / 255]
        if type == "grabbable_crumbling":
            extra[0] = "crumbling"
        add_object(type, shape, [pos[0], pos[1] - height / 2, pos[2]], euler_to_quaternion(rotation), [scale, height, scale], extra)
    return previous

def level_floating_grapple(position):
    previous = position
    type = types[random.randint(4, 5)]
    shape = shapes[random.randint(1, 2)]
    for i in range(random.randint(10, 20)):
        pos = [previous[0] + random.randint(10, 20), 20, 0]
        scale = random.randint(2, 7)
        width = 1
        if shape == "cylender":
            width = 50
            rotation = [90, 0, 0]
        add_object(type, shape, pos, euler_to_quaternion(rotation), [scale, scale * width, scale])
    return previous

def generate_level(pos):
    n = random.randint(0, 1)
    if n == 0:
        end = level_floating_jumps(pos)
    if n == 1:
        end = level_lava_jumps(pos)
    return end

def generate_map(levels):
    pos = [0, 0, 0]
    for i in range(levels):
        pos = generate_level(pos)
        pos = [pos[0] + 5, 5, 0]
        add_object("default_colored", "cube", pos, [0, 0, 0, 1], [2, 1, 50], ["color", [0.5, 0.5, 0.5]])
    json = ('''{
    "title": "This level was not made by a human",
    "description": "Thats right. everything you see in this level was generated by an algorithm",
    "creators": "nskc7",
    "checkpoints": '''+str(levels)+''',

    "start": {
        "position": [0.0, 0.0, 0.0],
        "rotation": [0.0, 0.0, 0.0, 1.0],
        "radius": 0.5
    },
    "finish": {
        "position": '''+str(pos)+''',
        "radius": 0.5
    },

    "nodes": '''+str(levelNodes)+'''
    }''').replace("'", '"')
    print(json)

generate_map(30)