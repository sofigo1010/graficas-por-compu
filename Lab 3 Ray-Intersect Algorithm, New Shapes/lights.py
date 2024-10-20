import math
from MathLib import *


class Light(object):
    def __init__(self, color=[1,1,1], intensity=1.0, LightType="None"):
        self.color = color
        self.intensity = intensity
        self.LightType = LightType

    def GetLightColor(self, intercept=None):  
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

class PointLight(Light):
    def __init__(self, color=[1,1,1], intensity=1, position=[0,0,0]):
        super().__init__(color, intensity,"Point")
        self.position = position

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            dir = [self.position[i] - intercept.point[i] for i in range(3)]
            R = math.sqrt(sum([d**2 for d in dir]))
            dir = [d / R for d in dir]

            intensity = sum([intercept.normal[i] * dir[i] for i in range(3)])
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)

            # Ley de cuadrados inversos
            # attenuation = intensity / R^2
            # R es la distancia del punto intercepto a la luz punto
            if R != 0:
                intensity /= R**2

            lightColor = [i * intensity for i in lightColor]

        return lightColor


    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = [self.position[i] - intercept.point[i] for i in range(3)]
            R = math.sqrt(sum([d**2 for d in dir]))
            dir = [d / R for d in dir]

            reflect = reflectVector(intercept.normal, dir)

            viewDir = [viewPos[i] - intercept.point[i] for i in range(3)]
            viewDir_magnitude = math.sqrt(sum([v**2 for v in viewDir]))
            viewDir = [v / viewDir_magnitude for v in viewDir]

            # Specular = (CV . R) ^ n * Ks
            specularity = max(0, sum([viewDir[i] * reflect[i] for i in range(3)])) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity

            if R != 0:
                specularity /= R**2

            specColor = [i * specularity for i in specColor]

        return specColor

class Spotlight(PointLight):
    def __init__(self, color=[1,1,1], intensity=1, position=[0,0,0], direction=[0,-1,0], innerAngle=50, outerAngle=60):
        super().__init__(color, intensity, position)
        self.direction = [d / math.sqrt(sum([x**2 for x in direction])) for d in direction] 
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.LightType = "Spot"


    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            lightColor = [i * self.SpotlightAttenuation(intercept) for i in lightColor]

        return lightColor


    def GetSpecularColor(self, intercept, viewPos):
        specularColor = super().GetSpecularColor(intercept, viewPos)

        if intercept:
            specularColor = [i * self.SpotlightAttenuation(intercept) for i in specularColor]

        return specularColor


    def SpotlightAttenuation(self, intercept=None):
        if intercept == None:
            return 0

        wi = [self.position[i] - intercept.point[i] for i in range(3)]
        wi_magnitude = math.sqrt(sum([wi[i]**2 for i in range(3)]))
        wi = [wi[i] / wi_magnitude for i in range(3)]  
        innerAngleRads = self.innerAngle * math.pi / 180
        outerAngleRads = self.outerAngle * math.pi / 180
        attenuation = (-sum([self.direction[i] * wi[i] for i in range(3)]) - math.cos(outerAngleRads)) / \
                    (math.cos(innerAngleRads) - math.cos(outerAngleRads))
        attenuation = min(1, max(0, attenuation))
        return attenuation

