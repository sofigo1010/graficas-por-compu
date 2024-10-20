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

class Plane(Shape):
    def __init__(self, position, normal, material): 
        super().__init__(position, material)
        self.normal = [n / math.sqrt(sum(x**2 for x in normal)) for n in normal]
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = sum(d * n for d, n in zip(dir, self.normal))  

        if math.isclose(denom, 0):
            return None

        num = sum((p - o) * n for p, o, n in zip(self.position, orig, self.normal))  
        t = num / denom
        if t < 0:
            return None

        P = [o + d * t for o, d in zip(orig, dir)]  

        return Intercept(
            point=P,
            normal=self.normal,
            distance=t,
            texCoords=None,
            rayDirection=dir,
            obj=self
        )


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)

        if planeIntercept is None:
            return None

        contact = [p - s for p, s in zip(planeIntercept.point, self.position)]
        contact = math.sqrt(sum(c ** 2 for c in contact))

        if contact > self.radius:
            return None

        return planeIntercept

class AABB(Shape):
    # Axis Aligned Bounding Box
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        self.planes = []

        rightPlane = Plane([position[0] + sizes[0] / 2, position[1], position[2]], [1, 0, 0], material)
        leftPlane = Plane([position[0] - sizes[0] / 2, position[1], position[2]], [-1, 0, 0], material)

        upPlane = Plane([position[0], position[1] + sizes[1] / 2, position[2]], [0, 1, 0], material)
        downPlane = Plane([position[0], position[1] - sizes[1] / 2, position[2]], [0, -1, 0], material)

        frontPlane = Plane([position[0], position[1], position[2] + sizes[2] / 2], [0, 0, 1], material)
        backPlane = Plane([position[0], position[1], position[2] - sizes[2] / 2], [0, 0, -1], material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        # Bounds
        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i] / 2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i] / 2)

    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")

        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:
                planePoint = planeIntercept.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept

        if intercept == None:
            return None

        u, v = 0, 0

        if abs(intercept.normal[0]) > 0:
            # Mapear las uvs para el eje x, usando las coordenadas de Y y Z
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[1]) > 0:
            # Mapear las uvs para el eje y, usando las coordenadas de X y Z
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[2]) > 0:
            # Mapear las uvs para el eje z, usando las coordenadas de X y Y
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
        
        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))


        return Intercept(
            point=intercept.point,
            normal=intercept.normal,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )

class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        super().__init__(position=None, material=material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.type = "Triangle"

    def ray_intersect(self, orig, dir):
        epsilon = 1e-6
        edge1 = [self.v1[i] - self.v0[i] for i in range(3)]
        edge2 = [self.v2[i] - self.v0[i] for i in range(3)]
        h = [dir[1] * edge2[2] - dir[2] * edge2[1], dir[2] * edge2[0] - dir[0] * edge2[2], dir[0] * edge2[1] - dir[1] * edge2[0]]
        a = sum([edge1[i] * h[i] for i in range(3)])
        
        if abs(a) < epsilon:
            return None

        f = 1.0 / a
        s = [orig[i] - self.v0[i] for i in range(3)]
        u = f * sum([s[i] * h[i] for i in range(3)])
        if u < 0.0 or u > 1.0:
            return None

        q = [s[1] * edge1[2] - s[2] * edge1[1], s[2] * edge1[0] - s[0] * edge1[2], s[0] * edge1[1] - s[1] * edge1[0]]
        v = f * sum([dir[i] * q[i] for i in range(3)])
        if v < 0.0 or u + v > 1.0:
            return None

        t = f * sum([edge2[i] * q[i] for i in range(3)])
        if t > epsilon:
            P = [orig[i] + dir[i] * t for i in range(3)]
            normal = [
                edge1[1] * edge2[2] - edge1[2] * edge2[1],
                edge1[2] * edge2[0] - edge1[0] * edge2[2],
                edge1[0] * edge2[1] - edge1[1] * edge2[0]
            ]
            norm_magnitude = math.sqrt(sum([normal[i] ** 2 for i in range(3)]))
            normal = [normal[i] / norm_magnitude for i in range(3)]


            texCoords = [u, v]

            return Intercept(
                point=P,
                normal=normal,
                distance=t,
                texCoords=texCoords,
                rayDirection=dir,
                obj=self
            )

        return None
    
class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"

    def ray_intersect(self, orig, dir):

        dx, dy = dir[0], dir[2]
        ox, oy = orig[0] - self.position[0], orig[2] - self.position[2]

        a = dx * dx + dy * dy
        b = 2 * (ox * dx + oy * dy)
        c = ox * ox + oy * oy - self.radius * self.radius

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None

        sqrt_disc = math.sqrt(discriminant)
        t0 = (-b - sqrt_disc) / (2 * a)
        t1 = (-b + sqrt_disc) / (2 * a)

        if t0 > t1:
            t0, t1 = t1, t0


        y0 = orig[1] + dir[1] * t0
        if not (self.position[1] <= y0 <= self.position[1] + self.height):
            y1 = orig[1] + dir[1] * t1
            if not (self.position[1] <= y1 <= self.position[1] + self.height):
                return None
            t0 = t1

        if t0 < 0:
            return None

        P = [orig[i] + dir[i] * t0 for i in range(3)]
        normal = [(P[0] - self.position[0]) / self.radius, 0, (P[2] - self.position[2]) / self.radius]
        

        u = (math.atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = (P[1] - self.position[1]) / self.height

        return Intercept(
            point=P,
            normal=normal,
            distance=t0,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )

