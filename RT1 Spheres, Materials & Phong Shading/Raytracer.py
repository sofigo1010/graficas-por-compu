import pygame
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import * 

width = 560
height = 560
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rt = RendererRT(screen)

white = Material(diffuse = [1.0, 1.0, 1.0], spec = 128, Ks = 0.25)
black = Material(diffuse = [0.0, 0.0, 0.0], spec = 64, Ks = 0.2)
orange = Material(diffuse = [1.0, 0.5, 0.0], spec = 64, Ks = 0.2)

rt.Lights.append(DirectionalLight(direction = [-1, -0.5, -1], intensity = 0.4))
rt.Lights.append(AmbientLight(intensity = 0.5))

rt.scene.append(Sphere(position = [0, -2, -8], radius = 1.5, material = white))
rt.scene.append(Sphere(position = [0, 0, -8], radius = 1.0, material = white))
rt.scene.append(Sphere(position = [0, 1.0, -8], radius = 0.75, material = white))

rt.scene.append(Sphere(position = [0, 0.2, -5], radius = 0.12, material = black))
rt.scene.append(Sphere(position = [0, -0.5, -5], radius = 0.12, material = black))
rt.scene.append(Sphere(position = [0, -1.35, -5], radius = 0.12, material = black))

rt.scene.append(Sphere(position = [-0.2, 1.3, -7], radius = 0.08, material = white))
rt.scene.append(Sphere(position = [0.2, 1.3, -7], radius = 0.08, material = white))

rt.scene.append(Sphere(position = [-0.2, 1.3, -6.95], radius = 0.05, material = black))
rt.scene.append(Sphere(position = [0.2, 1.3, -6.95], radius = 0.05, material = black))

rt.scene.append(Sphere(position = [0, 1.2, -7], radius = 0.1, material = orange))

rt.scene.append(Sphere(position = [-0.25, 1.0, -7], radius = 0.04, material = black))
rt.scene.append(Sphere(position = [-0.125, 0.95, -7], radius = 0.04, material = black))
rt.scene.append(Sphere(position = [0, 0.9, -7], radius = 0.04, material = black))
rt.scene.append(Sphere(position = [0.125, 0.95, -7], radius = 0.04, material = black))
rt.scene.append(Sphere(position = [0.25, 1.0, -7], radius = 0.04, material = black))

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
