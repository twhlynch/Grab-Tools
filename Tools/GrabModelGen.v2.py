from re import X
from tkinter import Y
import numpy as np
import open3d as o3d
import os, sys, math
def main():
    def get_gradients(vec1, vec2, vec3):
        x1 = vec1[0]
        y1 = vec1[1]
        z1 = vec1[2]
        x2 = vec2[0]
        y2 = vec2[1]
        z2 = vec2[2]
        x3 = vec3[0]
        y3 = vec3[1]
        z3 = vec3[2]

        # Calculate the gradients
        x_grad = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
        y_grad = (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1)
        z_grad = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

        # Normalize the gradients
        length = math.sqrt(x_grad * x_grad + y_grad * y_grad + z_grad * z_grad)
        x_grad /= length
        y_grad /= length
        z_grad /= length

        return [x_grad, y_grad, z_grad]


        # rotate z until highest and lowest x are same y
        # rotate y until highest and lowest x are same z
        # get gradient of y(x)
        # rotate z until highest and lowest y are same z
        # rotate y until highest and lowest y are same x
        # get gradient of y(y)
        # rotate z until highest and lowest z are same x
        # rotate y until highest and lowest z are same y
        # get gradient of y(z)

        print()
    def euler_to_quaternion(roll, pitch, yaw):
        # xyz
        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw]

    if len(sys.argv) < 2:
        print('GrabModelGen.v2.py models/input.obj LevelName')
        return
    mesh = o3d.io.read_triangle_mesh(sys.argv[1])
    # print(mesh)
    v = np.asarray(mesh.vertices)
    t = np.asarray(mesh.triangles)
    # print(t)
    # print(v)
    triangles = []
    for i in range(len(t)):
        triangles.append([v[t[i][0]], v[t[i][1]], v[t[i][2]]])
        # triangles.append([v[t[0]], v[t[1]], v[t[2]]])
    # print(triangles[7])
    # triangles = [[[x,y,z],[x,y,z],[x,y,z]], [[x,y,z],[x,y,z],[x,y,z]]]

    for i in range(len(triangles)):
        x1 = triangles[i][0][0]
        y1 = triangles[i][0][1]
        z1 = triangles[i][0][2]
        x2 = triangles[i][1][0]
        y2 = triangles[i][1][1]
        z2 = triangles[i][1][2]
        x3 = triangles[i][2][0]
        y3 = triangles[i][2][1]
        z3 = triangles[i][2][2]
        center = [(x1+x2+x3)/3,(y1+y2+y3)/3,(z1+z2+z3)/3]
        triangles[i].append(center)
    # triangles = [[[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz]], [[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz]]]
    for i in range(len(triangles)):
        min = 0
        for p in range(3):
            x1 = triangles[i][p][0]
            y1 = triangles[i][p][1]
            z1 = triangles[i][p][2]
            x2 = triangles[i][3][0]
            y2 = triangles[i][3][1]
            z2 = triangles[i][3][2]
            #print(x1, x2, y1, y2, z1, z2)
            d = math.sqrt(((int(x2) - int(x1))**2 + (int(y2) - int(y1))**2 + (int(z2) - int(z1))**2))
            if min == 0 or d < min:
                min = d
        triangles[i].append(min)
    # triangles = [[[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz],d], [[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz],d]]
    for i in range(len(triangles)):
        x1 = triangles[i][0][0]
        y1 = triangles[i][0][1]
        z1 = triangles[i][0][2]
        x2 = triangles[i][1][0]
        y2 = triangles[i][1][1]
        z2 = triangles[i][1][2]
        x3 = triangles[i][2][0]
        y3 = triangles[i][2][1]
        z3 = triangles[i][2][2]
        p12 = [(x1+x2)/2,(y1+y2)/2,(z1+z2)/2]
        p23 = [(x2+x3)/2,(y2+y3)/2,(z2+z3)/2]
        p31 = [(x3+x1)/2,(y3+y1)/2,(z3+z1)/2]
        triangles[i].append(p12)
        triangles[i].append(p23)
        triangles[i].append(p31)
    # triangles = [[[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz],d,[x12,y12,z12],[x23,y23,z23],[x31,y31,z31]], [[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz],d,[x12,y12,z12],[x23,y23,z23],[x31,y31,z31]]]
    for i in range(len(triangles)):
        g = get_gradients(triangles[i][0], triangles[i][1], triangles[i][2])
        g = [math.atan(g[0]), math.atan(g[1]), math.atan(g[2])]
        qu = euler_to_quaternion(g[0], g[1], g[2])
        triangles[i].append(qu)
    # triangles = [[[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz],d,[x12,y12,z12],[x23,y23,z23],[x31,y31,z31], [qx, qy, qz, qw]], [[x,y,z],[x,y,z],[x,y,z],[cx, cy, cz],d,[x12,y12,z12],[x23,y23,z23],[x31,y31,z31], [qx, qy, qz, qw]]]
        # get lowest point
        # get highest point
        # get gradients:
        #     X
        #     Y
        #     Z
        # eulers rotatin [xyz]
        # append
        # euler_to_quaternion()

    # get angle to xyz rotations


    # mesh.triangles = o3d.utility.Vector3iVector(
    #     np.asarray(mesh.triangles)[:3000])
    # mesh.triangle_normals = o3d.utility.Vector3dVector(
    #     np.asarray(mesh.triangle_normals)[:3000])
    # print(mesh)
    # o3d.visualization.draw_geometries([mesh])

    start = '''{
        "title": "'''+sys.argv[2]+'''",
        "description": "description",
        "creators": "GrabModelGen",
        "checkpoints": 10,

        "start": {
            "position": [0.0, 0.5, 0.0],
            "rotation": [0.0, 0.0, 0.0, 1.0],
            "radius": 0.5
        },
        "finish": {
            "position": [2.0, 0.5, 0.0],
            "radius": 0.5
        },

        "nodes": [
            {
                "type": "default",
                "shape": "cube",
                "position": [1.0, -0.5, 0.0],
                "rotation": [0.0, 0.0, 0.0, 1.0],
                "scale": [4.0, 1.0, 2.0]
            }'''
    end = ''']
    }'''

    json = ''
    for i in range(len(triangles)):
        x = triangles[i][3][0] / 35
        y = triangles[i][3][1] / 35
        z = triangles[i][3][2] / 35
        s = triangles[i][4] / 15
        qx = triangles[i][8][0]
        qy = triangles[i][8][1]
        qz = triangles[i][8][2]
        qw = triangles[i][8][3]
        json += ''',
            {
                "type": "default_colored",
                "shape": "prism",
                "position": ['''+str(x)+''', '''+str(y)+''', '''+str(z)+'''],
                "rotation": ['''+str(-qz)+''', '''+str(qy)+''', '''+str(qx)+''', '''+str(-qw)+'''],
                "scale": ['''+str(s)+''', 0.001, '''+str(s)+'''],
                "color": [0.2, 0.2, 0.2]
            }'''
    json = start + json + end
    with open("generation/pixels.json", "w") as f:
            f.write(json)
            try:
                os.system('python generation/ConvertToLevel.py generation/pixels.json "generation/level_output/'+sys.argv[2]+'.level"')
            except:
                os.system('python3 generation/ConvertToLevel.py generation/pixels.json "generation/level_output/'+sys.argv[2]+'.level"')


if __name__ == '__main__':
    main()