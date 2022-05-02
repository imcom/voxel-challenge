from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0.06, exposure=3)
scene.set_floor(-0.05, (0.1, 0.5, 0.9))
scene.set_directional_light((-1, 2.8, 1.1), 0, (0.3, 0.3, 0.3))


def stick(start, length: int, diff: int, z: int):
    for i, j in ti.ndrange((start[0], length), (start[1], length)):
        if (j - i) == diff:
            if j % 3 == 0:
                scene.set_voxel(vec3(i, j, z), 2, vec3(0.1, 0.1, 0.1))
            elif j % 5 == 0:
                scene.set_voxel(vec3(i, j, z), 2, vec3(0.1, 0.1, 0.1))
            else:
                scene.set_voxel(vec3(i, j, z), 2, vec3(0.1, 0.1, 0.1))


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    for i, j, k in ti.ndrange((-7, 0), (0, 12), (0, 7)):
        if (3 <= k <= 6) and (-6 < i < -2) and (4 < j < 10):
            scene.set_voxel(vec3(i, j, k), 0, vec3(0.1, 0.1, 0.1))
            continue
        if (k == 2) and (-6 < i < -2) and (4 < j < 10):
            scene.set_voxel(vec3(i, j, k), 1, vec3(0.8, 0.8, 0.1))
            continue
        if j % 3 == 0:
            scene.set_voxel(vec3(i, j, k), 2, vec3(0.1, 0.5, 0.9))
        elif j % 5 == 0:
            scene.set_voxel(vec3(i, j, k), 2, vec3(0.5, 0.6, 0.7))
        else:
            scene.set_voxel(vec3(i, j, k), 2, vec3(0.3, 0.1, 0.1))

    stick((-4, 7), 25, 7, 3)
    stick((-4, 7), 25, 7, 4)
    stick((-4, 6), 25, 6, 4)
    stick((-4, 6), 25, 6, 4)

    for i, j in ti.ndrange((-15, 6), (15, 25)):
        # letter E
        if (i == -13 and 15 < j < 23) or (-13 < i <= -10 and (j == 16 or j == 19 or j == 22)):
            scene.set_voxel(vec3(i, j, 19), 1, vec3(0.8, 0.8, 0.1))
            scene.set_voxel(vec3(i, j, 25), 2, vec3(0.8, 0.8, 0.1))
        else:
            scene.set_voxel(vec3(i, j, 19), 2, vec3(0.2, 0.6, 0.2))

        # letter T
        if (i == -5 and 15 < j < 23) or (-8 < i < -2 and j == 22):
            scene.set_voxel(vec3(i, j, 19), 1, vec3(0.8, 0.1, 0.8))
            scene.set_voxel(vec3(i, j, 25), 2, vec3(0.1, 0.8, 0.8))

        # letter C
        if (i == 0 and 15 < j < 23) or (0 < i <= 3 and (j == 16 or j == 22)):
            scene.set_voxel(vec3(i, j, 19), 1, vec3(0.8, 0.1, 0.8))
            scene.set_voxel(vec3(i, j, 25), 2, vec3(0.8, 0.3, 0.8))


initialize_voxels()

scene.finish()
