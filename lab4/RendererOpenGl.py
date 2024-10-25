
import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model
import glm

width = 540
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF) 

clock = pygame.time.Clock()

rend  = Renderer(screen)

faceModel =Model("models/face.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.translation.z =-5
faceModel.scale.x = 2
faceModel.scale.y = 2
faceModel.scale.z = 2


rend.scene.append(faceModel)

isRunning = True

vShader =vertex_shader
fShader = fragment_shader
rend.SetShaders(vShader, fShader)


while isRunning: 
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed() #teclas presionadas en este momento
    
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
            
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                
            if event.key == pygame.K_1:
                rend.filledMode()
                
            if event.key == pygame.K_2:
                rend.wireframeMode()
                
            if event.key == pygame.K_3:
                vShader =vertex_shader
                rend.SetShaders(vShader, fShader)
           
            if event.key == pygame.K_4:
                vShader =fat_shader
                rend.SetShaders(vShader, fShader)
                
            if event.key == pygame.K_5:
                vShader =water_shader
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_6:
                fShader =fragment_shader
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_7:
                fShader =negative_shader
                rend.SetShaders(vShader, fShader)                
                

  
    if keys[K_LEFT]:
        rend.pointLight.x -= 1*deltaTime
    
    if keys[K_RIGHT]:
        rend.pointLight.x += 1*deltaTime

    if keys[K_UP]:
        rend.pointLight.z += 1*deltaTime
    
    if keys[K_DOWN]:
        rend.pointLight.z -= 1*deltaTime

    if keys[K_PAGEUP]:
        rend.pointLight.y += 1*deltaTime
    
    if keys[K_PAGEDOWN]:
        rend.pointLight.y -= 1*deltaTime


    if keys[K_a]:
        rend.camera.position.x -= 1 * deltaTime
    
    if keys[K_d]:
        rend.camera.position.x += 1 * deltaTime


    if keys[K_w]:
        rend.camera.position.y += 1 * deltaTime

    if keys[K_s]:
        rend.camera.position.y -= 1 * deltaTime 

        
    rend.time += deltaTime 
    #print(deltaTime)
    
    #rend.camera.LookAt( faceModel.translation )
    rend.Render()
    pygame.display.flip()
    

pygame.quit()

