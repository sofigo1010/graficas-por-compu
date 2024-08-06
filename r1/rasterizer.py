import pygame
from pygame.locals import *
from gl import LINES, POINTS, Renderer
from model import Model
from shaders import vertexShader

width = 960
height = 540

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
rend = Renderer(screen) 
rend.vertexShader = vertexShader

modelo1 = Model("LowPolyToilet.obj")
modelo1.translate = [width / 2, height / 2, 0]
modelo1.scale = [80, 80, 80]
rend.models.append(modelo1)

rend.glColor(1, 1, 1)

isRunning = True

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_LEFT:
                modelo1.rotate[1] -= 5 
            elif event.key == pygame.K_RIGHT:
                modelo1.rotate[1] += 5 
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES

    rend.glClear()
    rend.glRender()

    pygame.display.flip()
    rend.glGenerateFramebuffer("render.bmp")
    clock.tick(60)
    rend.glRender()

pygame.quit()