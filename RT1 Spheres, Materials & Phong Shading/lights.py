import math
from MathLib import *


class Light(object):
    def __init__(self, color=[1,1,1], intensity=1.0, LightType="None"):
        self.color = color
        self.intensity = intensity
        self.LightType = LightType

    def GetLightColor(self):
        return [i * self.intensity for i in self.color]
    
    def GetSpecularColor(self, intercept, viewPos):
        return [0, 0, 0]

class AmbientLight(Light):
    def __init__(self, color=[1,1,1], intensity=1.0):
        super().__init__(color, intensity, "Ambient")

    def GetLightColor(self, intercept=None):
        return super().GetLightColor()

class DirectionalLight(Light):
    def __init__(self, color=[1,1,1], intensity=1.0, direction=[0,-1,0]):
        super().__init__(color, intensity, "Directional")
        norm_magnitude = math.sqrt(sum([d**2 for d in direction]))
        self.direction = [d / norm_magnitude for d in direction]

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor()

        if intercept:
            dir = [i * -1 for i in self.direction]
            intensity = sum([intercept.normal[i] * dir[i] for i in range(3)])
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [i * intensity for i in lightColor]

        return lightColor

    
    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = [i * -1 for i in self.direction]
            reflect = reflectVector(intercept.normal, dir)
            viewDir = [viewPos[i] - intercept.point[i] for i in range(3)]
            viewDir_magnitude = math.sqrt(sum([viewDir[i]**2 for i in range(3)]))
            viewDir = [viewDir[i] / viewDir_magnitude for i in range(3)]

            specularity = max(0, sum([viewDir[i] * reflect[i] for i in range(3)])) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity  
            specColor = [i * specularity for i in specColor]

        return specColor

