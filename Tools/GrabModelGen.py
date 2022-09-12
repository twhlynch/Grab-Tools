# https://towardsdatascience.com/5-step-guide-to-generate-3d-meshes-from-point-clouds-with-python-36bad397d8ba
# https://medium.com/@alexeyyurasov/3d-modeling-with-python-c21296756db2
# http://www.open3d.org/docs/release/tutorial/geometry/mesh.html
# http://www.open3d.org/docs/0.9.0/tutorial/Basic/file_io.html

import numpy as np
import open3d as o3d
import os, sys
def main():
    if len(sys.argv) < 2:
        print('GrabModelGen.py models/input.obj LevelName')
        return
    # print("Testing IO for meshes ...")
    # mesh = o3d.io.read_triangle_mesh(input_path+dataname)
    # print(mesh)

    # print("Testing IO for textured meshes ...")
    mesh = o3d.io.read_triangle_mesh(sys.argv[1])
    print(mesh)

    # print('Vertices:')
    # print(np.asarray(mesh.vertices))
    # print('Triangles:')
    # print(np.asarray(mesh.triangles))

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
    for i in range(len(np.asarray(mesh.vertices))):
        x = np.asarray(mesh.vertices)[i][0] / 60
        y = np.asarray(mesh.vertices)[i][1] / 60
        z = np.asarray(mesh.vertices)[i][2] / 60
        json += ''',
            {
                "type": "default_colored",
                "shape": "sphere",
                "position": ['''+str(x)+''', '''+str(y)+''', '''+str(z)+'''],
                "rotation": [0.0, 0.0, 0.0, 1.0],
                "scale": [0.2, 0.2, 0.2],
                "color": [0.3, 0.3, 0.3]
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