import glm  # pip install PyGLM
from OpenGL.GL import *

from camera import Camera
from skybox import Skybox


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        self.filledMode = False
        self.ToggleFilledMode()

        glViewport(0, 0, self.width, self.height)

        self.camera = Camera(self.width, self.height)

        self.time = 0
        self.value = 0

        self.pointLight = glm.vec3(0, 0, 0)
        self.ambientLight = 0.1

        self.scene = []
        self.skybox = None

    def CreateSkybox(self, textureList):
        self.skybox = Skybox(textureList)

    def ToggleFilledMode(self):
        self.filledMode = not self.filledMode

        if self.filledMode:
            glEnable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT, GL_FILL)
        else:
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def Render(self):
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.Update()

        if self.skybox is not None:
            self.skybox.cameraRef = self.camera
            self.skybox.Render()

        for obj in self.scene:
            obj.Render(self.camera, self.time, self.pointLight, self.ambientLight)
