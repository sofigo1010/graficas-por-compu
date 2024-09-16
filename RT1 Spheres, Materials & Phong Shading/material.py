class Material(object):
    def __init__(self, diffuse, spec=1.0, Ks=0.0):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks


    def GetSurfaceColor(self, intercept, renderer):
        # Phong reflection model
        # LightColors = LightColor + Specular
        # FinalColor = DiffuseColor * LightColor
        
        lightColor = [0,0,0]
        finalColor = self.diffuse

        for Light in renderer.Lights:
            shadowIntercept = None

            if Light.LightType == "Directional":
                LightDir = [-i for i in Light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, LightDir, intercept.obj)

            if shadowIntercept == None:
                currentLightColor = Light.GetLightColor(intercept)
                currentSpecularColor = Light.GetSpecularColor(intercept, renderer.camera.translate)
                lightColor = [(lightColor[i] + currentLightColor[i] + currentSpecularColor[i]) for i in range(3)]

        finalColor = [(finalColor[i] * lightColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]

        return finalColor




