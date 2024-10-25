import pygame
from pygame.locals import *
from OpenGL.GL import *  
from gl import Renderer
from buffer import *
from shaders import *
from model import *
import glm
import imageio
from PIL import Image

width = 540
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF) 

clock = pygame.time.Clock()

rend = Renderer(screen)

faceModel = Model("models/face.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.translation.z = -5
faceModel.scale.x = 2
faceModel.scale.y = 2
faceModel.scale.z = 2

rend.scene.append(faceModel)

isRunning = True

vShader = vertex_shader
fShader = fragment_shader
rend.SetShaders(vShader, fShader)


frames = []

while isRunning: 
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
            
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                
            if event.key == pygame.K_1:
                rend.FilledMode()
                
            if event.key == pygame.K_2:
                rend.WireframeMode()
                
            if event.key == pygame.K_3:
                explosion_intensity = 1.0  
                explosion_center = glm.vec3(0.0, 0.0, 0.0)
                vShader = explosion_shader
                rend.SetShaders(vShader, fShader)
                glUseProgram(rend.active_shaders)
                explosion_location = glGetUniformLocation(rend.active_shaders, "explosionIntensity")
                explosion_center_location = glGetUniformLocation(rend.active_shaders, "explosionCenter")

                if explosion_location != -1 and explosion_center_location != -1:
                    glUniform1f(explosion_location, explosion_intensity)
                    glUniform3fv(explosion_center_location, 1, glm.value_ptr(explosion_center))

            if event.key == pygame.K_4:
                vShader = star_expand_shader
                rend.SetShaders(vShader, fShader)
                
            if event.key == pygame.K_5:
                vShader = spiral_shader
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_6:
                fShader = electric_shader 
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_7:
                fShader = aura_shader
                rend.SetShaders(vShader, fShader)   

            if event.key == pygame.K_8:
                fShader = disintegration_shader
                rend.SetShaders(vShader, fShader)                 

    if keys[K_LEFT]:
        rend.pointLight.x -= 1 * deltaTime
    
    if keys[K_RIGHT]:
        rend.pointLight.x += 1 * deltaTime

    if keys[K_UP]:
        rend.pointLight.z += 1 * deltaTime
    
    if keys[K_DOWN]:
        rend.pointLight.z -= 1 * deltaTime

    if keys[K_PAGEUP]:
        rend.pointLight.y += 1 * deltaTime
    
    if keys[K_PAGEDOWN]:
        rend.pointLight.y -= 1 * deltaTime

    if keys[K_a]:
        rend.camera.position.x -= 1 * deltaTime
    
    if keys[K_d]:
        rend.camera.position.x += 1 * deltaTime

    if keys[K_w]:
        rend.camera.position.y += 1 * deltaTime

    if keys[K_s]:
        rend.camera.position.y -= 1 * deltaTime 

    rend.time += deltaTime
    rend.Render()
    pygame.display.flip()


    frame_data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), frame_data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  
    frames.append(image)

pygame.quit()


imageio.mimsave('output_video.mp4', frames, fps=30)
