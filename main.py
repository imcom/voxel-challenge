from typing import Any
from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=1)
scene.set_directional_light((1, 1, 1), 0.1, (1, 1, 1))
scene.set_background_color((0.3, 0.4, 0.6))


@ti.func
def pie(r: int, y: int, color=vec3(0.9, 0.3, 0.3)):
    for i, k in ti.ndrange((-r, r), (-r, r)):
        x = ivec3(i, 0, k)
        if x.dot(x) < r * r * 0.6:
            scene.set_voxel(vec3(i, y, k), 1, color)


@ti.func
def donut(r: int, y: int, color=vec3(0.3, 0.3, 0.9)):
    for i, k in ti.ndrange((-r, r), (-r, r)):
        x = ivec3(i, 0, k)
        if x.dot(x) >= r * r * 0.5 and x.dot(x) < r * r * 0.8:
            scene.set_voxel(vec3(i, y, k), 1, color)


@ti.func
def cloud(offset: int, height: int, depth: int):
    r = 5
    for i, j, k in ti.ndrange((-r, r), (0, r), (-r, r)):
        x = ivec3(i, j, k)
        if x.dot(x) < r * r * 0.6:
            scene.set_voxel(vec3(i + offset, j+height, k + depth),
                            1, vec3(0.3, 0.9, 0.3))


@ti.kernel
def initialize_voxels():
    n = 30
    i = 1
    while i + 2 < n:
        if i % 2 == 0:
            pie(n-i, i)
            donut(n-i+2, i+2)
        else:
            pie(n-i, i, vec3(0.3, 0.3, 0.9))
            donut(n-i+2, i+2, vec3(0.9, 0.3, 0.3))
        i += 5

    cloud(-15, 15, 30)
    cloud(-10, 25, -15)
    cloud(0, 20, 30)
    cloud(10, 8, 20)
    cloud(18, 15, -20)


initialize_voxels()
scene.finish()
