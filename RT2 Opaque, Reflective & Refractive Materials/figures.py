from math import*
import math
from intercept import *

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        L = [self.position[i] - orig[i] for i in range(3)]
        tca = sum([L[i] * dir[i] for i in range(3)])
        L_magnitude = math.sqrt(sum([L[i]**2 for i in range(3)]))
        d = math.sqrt(L_magnitude**2 - tca**2)
        if d > self.radius:
            return None
        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        P = [orig[i] + dir[i] * t0 for i in range(3)]
        normal = [P[i] - self.position[i] for i in range(3)]
        norm_magnitude = math.sqrt(sum([normal[i]**2 for i in range(3)]))
        normal = [normal[i] / norm_magnitude for i in range(3)]

        u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = acos(-normal[1]) / pi

        return Intercept(
            point = P,
            normal = normal,
            distance = t0,
            texCoords = [u, v],
            rayDirection = dir,
            obj = self
        )

