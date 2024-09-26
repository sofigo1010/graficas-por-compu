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
rt.envMap = Texture("textures/peppermint_powerplant_2.bmp")


space = Material(texture = Texture("textures/space.bmp"), spec = 512, Ks = 0.3, diffuse = [1.0, 1.0, 1.0], matType = OPAQUE)
marble = Material(texture = Texture("textures/whiteMarble.bmp"), spec = 512, Ks = 0.3, diffuse = [1.0, 1.0, 1.0], matType = OPAQUE)
RED = Material(texture = Texture("textures/red.bmp"), spec = 512, Ks = 1.8, ior = 15, matType = REFLECTIVE)
diamondReflective = Material(diffuse = [0.8, 0.8, 1.0], spec = 512, Ks = 0.9, matType = REFLECTIVE)
bluega = Material(diffuse = [0.5, 0.5, 1.0], spec = 128, Ks = 0.2, ior = 0.5, matType = TRANSPARENT)
yellowGlass = Material(diffuse = [1.0, 1.0, 0.0], spec = 128, Ks = 0.2, ior = 2.5, matType = TRANSPARENT)

rt.Lights.append(DirectionalLight(direction = [-1, -1, -1], intensity = 0.8))
rt.Lights.append(AmbientLight(intensity = 0.1))


rt.scene.append(Sphere(position = [-1.3, 0.7, -5], radius = 0.6, material = space))
rt.scene.append(Sphere(position = [-1.3, -0.7, -5], radius = 0.6, material = marble))
rt.scene.append(Sphere(position = [0,0.7, -5], radius = 0.6, material = RED))
rt.scene.append(Sphere(position = [0, -0.7, -5], radius = 0.6, material = diamondReflective))
rt.scene.append(Sphere(position = [1.3, 0.7, -5], radius = 0.6, material = yellowGlass))
rt.scene.append(Sphere(position = [1.3, -0.7, -5], radius = 0.6, material = bluega))

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
