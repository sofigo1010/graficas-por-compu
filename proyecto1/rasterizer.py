import pygame
from pygame.locals import *
from gl import LINES, POINTS, TRIANGLES, Renderer
from model import Model
from shaders import *

width = 960
height = 540


screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
rend = Renderer(screen) 
rend.glLoadBackground("textures\ok.bmp")
rend.vertexShader = vertexShader
rend.fragmentShader = fragmentShader

modelo1 = Model("models\squidward.obj")
modelo1.LoadTexture("textures\squidward.bmp")
modelo1.vertexShader= vertexShader
modelo1.fragmentShader=fragmentShader
modelo1.translate[2] = -5
#modelo1.translate[1] = -2
modelo1.scale[0] = 1
modelo1.scale[1] = 1
modelo1.scale[2] = 1
#modelo1.rotate[0] = 90

#modelo1.fragmentShader=whitengrayShader
# modelo1.translate[2] = -5
# modelo1.translate[0] = -2
# modelo1.translate[1] = -2
# modelo1.scale[0] = 5
# modelo1.scale[1] = 5
# modelo1.scale[2] = 5

modelo2 = Model("models\Puss.obj")
modelo2.LoadTexture("textures/t_puss_c.bmp")
modelo2.vertexShader= vertexShader
modelo2.fragmentShader=lineShader
modelo2.translate[2] = -5
modelo2.translate[0] = -2
modelo2.translate[1] = -2
modelo2.scale[0] = 0.25
modelo2.scale[1] = 0.25
modelo2.scale[2] = 0.25

modelo3 = Model("models\Donkey.obj")
modelo3.LoadTexture("textures/t_Donkey_c.bmp")
modelo3.vertexShader= vertexShader
modelo3.fragmentShader=infraredShader
modelo3.translate[2] = -5
modelo3.translate[0] = 2
modelo3.scale[0] = 0.25
modelo3.scale[1] = 0.25
modelo3.scale[2] = 0.25
modelo3.translate[1] = -1

rend.models.append(modelo1)
rend.models.append(modelo2)
rend.models.append(modelo3)



puntoA = [50, 50, 0]
puntoB = [250, 500, 0]
puntoC = [500, 50, 0]

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
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES
            elif event.key == pygame.K_a:
                rend.camera.rotate[1] -= 5  
            elif event.key == pygame.K_d:
                rend.camera.rotate[1] += 5  
            elif event.key == pygame.K_z:
                rend.camera.rotate[2] -= 5  
            elif event.key == pygame.K_c:
                rend.camera.rotate[2] += 5  

    rend.glClear()
    rend.glClearBackground()
    rend.glRender()
    # rend.glTriangle(puntoA, puntoB, puntoC)
    pygame.display.flip()
    rend.glGenerateFramebuffer("render.bmp")
    clock.tick(60)

pygame.quit()
