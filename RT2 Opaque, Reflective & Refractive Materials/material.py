from MathLib import *
from refractionFunctions import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse = [1,1,1], spec = 1.0, Ks = 0.0, ior =1, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks
        self.ior = ior
        self.texture = texture
        self.matType = matType


    def GetSurfaceColor(self, intercept, renderer, recursion = 0):
        lightColor = [0,0,0]
        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        finalColor = self.diffuse
        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [finalColor[i] * textureColor[i] for i in range(3)]

        for light in renderer.Lights:
            shadowIntercept = None

            if light.LightType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            if shadowIntercept == None:
                lightColor = [(lightColor[i] + light.GetSpecularColor(intercept, renderer.camera.translate)[i]) for i in range(3)]

                if self.matType == OPAQUE:
                    lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]

        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectIntercept = renderer.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

        elif self.matType == TRANSPARENT:
            outside = dot_product(intercept.normal, intercept.rayDirection) < 0
            bias = [i * 0.001 for i in intercept.normal]
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)

            if outside:
                reflectOrig = vector_add(intercept.point, bias)
            else:
                reflectOrig = vector_subtract(intercept.point, bias)

            reflectIntercept = renderer.glCastRay(reflectOrig, reflect, None, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

            if not totalInternalReflection(intercept.normal, intercept.rayDirection, 1.0, self.ior):
                refract = refractVector(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                refractOrig = vector_subtract(intercept.point, bias) if outside else vector_add(intercept.point, bias)
                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)

                if refractIntercept != None:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, refract)

                Kr, Kt = fresnel(intercept.normal, intercept.rayDirection, 1.0, self.ior)

                reflectColor = [i * Kr for i in reflectColor]
                refractColor = [i * Kt for i in refractColor]
            else:
                reflectColor = [i for i in reflectColor]

        finalColor = [(finalColor[i] * (lightColor[i] + reflectColor[i] + refractColor[i])) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]

        return finalColor





