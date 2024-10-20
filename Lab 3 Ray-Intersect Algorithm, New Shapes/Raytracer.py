import pygame
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *
from texture import *

width = 540
height = 540
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/background.bmp")

space = Material(texture = Texture("textures/pyramid.bmp"), spec = 128, Ks = 0.5, matType = OPAQUE)
marble = Material(texture = Texture("textures/tree.bmp"), spec = 512, Ks = 0.3, diffuse = [1.0, 1.0, 1.0], matType = OPAQUE)
RED = Material(texture = Texture("textures/rainbow.bmp"), spec = 512, Ks = 1.8, ior = 15, matType = REFLECTIVE)
diamondReflective = Material(diffuse = [0.8, 0.8, 1.0], spec = 512, Ks = 0.9, matType = REFLECTIVE)
bluega = Material(diffuse = [0.5, 0.5, 1.0], spec = 128, Ks = 0.2, ior = 1.5, matType = TRANSPARENT)
yellowGlass = Material(diffuse = [1.0, 1.0, 0.0], spec = 128, Ks = 0.2, ior = 2.5, matType = TRANSPARENT)


rt.Lights.append(DirectionalLight(direction = [-1, -1, -1], intensity = 0.8))
rt.Lights.append(AmbientLight(intensity = 0.1))

rt.scene.append(Triangle(v0=[-1.5, 0.7, -5], v1=[-1.0, 1.7, -5], v2=[-0.5, 0.7, -5], material=space))


rt.scene.append(Triangle(v0=[-0.8, 1.0, -4.5], v1=[-0.2, 2.2, -4.5], v2=[0.4, 1.0, -4.5], material=RED))


rt.scene.append(Triangle(v0=[0.5, 0.7, -6], v1=[1.0, 1.7, -6], v2=[1.5, 0.7, -6], material=yellowGlass))


rt.scene.append(Cylinder(position=[-1.3, -0.7, -5], radius=0.6, height=1.2, material=marble))


rt.scene.append(Cylinder(position=[0, -1.0, -6], radius=1.0, height=2.0, material=diamondReflective))


rt.scene.append(Cylinder(position=[1.3, -0.5, -5.5], radius=0.4, height=0.8, material=bluega))



rt.glRender()

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    pygame.display.flip()
    rt.glGenerateFramebuffer("render.bmp")
    clock.tick(60)

pygame.quit()