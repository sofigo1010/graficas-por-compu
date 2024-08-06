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
modelo1.translate[2] = -10
modelo1.translate[0] = -2

modelo1.scale[0] = 2
modelo1.scale[1] = 2
modelo1.scale[2] = 2

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
                rend.camera.translate[0] -= 1
            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 1
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] += 1
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] -= 1
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            elif event.key == pygame.K_a:
                rend.camera.rotate[1] -= 5  
            elif event.key == pygame.K_d:
                rend.camera.rotate[1] += 5  
            elif event.key == pygame.K_z:
                rend.camera.rotate[2] -= 5  
            elif event.key == pygame.K_c:
                rend.camera.rotate[2] += 5  

    rend.glClear()
    rend.glRender()

    pygame.display.flip()
    rend.glGenerateFramebuffer("render.bmp")
    clock.tick(60)

pygame.quit()
