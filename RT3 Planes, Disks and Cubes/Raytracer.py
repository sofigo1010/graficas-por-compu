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

grayMaterial = Material(diffuse=[0.2, 0.2, 0.2], spec=128, Ks=0.25)
darkNavyBlueMaterial = Material(diffuse=[0.0, 0.0, 0.3], spec=128, Ks=0.25)
whiteMaterial = Material(diffuse=[1.0, 1.0, 1.0], spec=128, Ks=0.1)
bedTexture = Material(texture=Texture("textures/bed.bmp"), spec=128, Ks=0.25)
NSTexture = Material(texture=Texture("textures/nights.bmp"), spec=128, Ks=0.25)
mirrorMaterial = Material(diffuse=[1.0, 1.0, 1.0], spec=128, Ks=0.8, matType=REFLECTIVE)

rt.Lights.append(AmbientLight(intensity=0.3))
rt.Lights.append(Spotlight(position=[0, 2, -5], direction=[0, -1, 0], intensity=10.0, innerAngle=30, outerAngle=45))

rt.scene.append(Plane(position=[0, -1, 0], normal=[0, 1, 0], material=grayMaterial))
rt.scene.append(Plane(position=[0, 3, 0], normal=[0, -1, 0], material=whiteMaterial))
rt.scene.append(Plane(position=[0, 0, -10], normal=[0, 0, 1], material=darkNavyBlueMaterial))
rt.scene.append(Plane(position=[-3, 0, 0], normal=[1, 0, 0], material=darkNavyBlueMaterial))
rt.scene.append(Plane(position=[3, 0, 0], normal=[-1, 0, 0], material=darkNavyBlueMaterial))

rt.scene.append(Disk(position=[0, -0.99, -5], normal=[0, 1, 0], radius=1.5, material=mirrorMaterial))

rt.scene.append(AABB(position=[0, -0.75, -5], sizes=[1.5, 0.5, 2], material=bedTexture))

rt.scene.append(AABB(position=[0, -0.5, -5], sizes=[0.7, 0.7, 0.7], material=NSTexture))

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
