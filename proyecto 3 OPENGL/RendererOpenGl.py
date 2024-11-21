import pygame
from pygame.locals import *

from gl import Renderer
from model import Model
from shaders import *

width = 1280
height = 720

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("tumbalacasa.mp3")  
pygame.mixer.music.play(-1)  
pygame.mixer.music.set_volume(0.7) 

screen = pygame.display.set_mode(
    (width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

skyboxTextures = [
    "skybox/right.jpg",
    "skybox/left.jpg",
    "skybox/top.jpg",
    "skybox/bottom.jpg",
    "skybox/front.jpg",
    "skybox/back.jpg"
]

rend.CreateSkybox(skyboxTextures)

# Models
bob = Model("models/SpongeBob.obj")
bob.AddTexture("textures/Special_SpongebobRyan.bmp")
bob.translation.z = -5
bob.translation.y = 0.25
bob.translation.x = -0.1
bob.scale.x = 0.5
bob.scale.z = 0.5
bob.scale.y = 0.5
bob.SetShaders(spiral_shader, electric_shader)

house = Model("models/sponge-bob_celshading_star.obj")
house.AddTexture("textures/BaseColor_Opacity.bmp")
house.translation.z = -7
house.scale.x = 0.1
house.scale.y = 0.1
house.scale.z = 0.1
house.SetShaders(speaker_vertex_shader, speaker_fragment_shader)

patrick = Model("models/patrick.obj")
patrick.AddTexture("textures/patrick.bmp")
patrick.translation.z = -5
patrick.translation.y = 0.25
patrick.rotation.y = -90
patrick.translation.x = 0.7
patrick.scale.x = 0.03
patrick.scale.y = 0.03
patrick.scale.z = 0.03
patrick.SetShaders(star_expand_shader, disintegration_shader)

squidward = Model("models/Squidward.obj")
squidward.AddTexture(
    "textures/Squidward_Expressions_BaseColor-resources.assets-8039.bmp")
squidward.AddTexture(
    "textures/Squidward_Costume01_BaseColor-resources.assets-8349.bmp")
squidward.translation.z = -5
squidward.translation.y = 0.25
squidward.rotation.y = 90
squidward.translation.x = -0.7
squidward.scale.x = 0.005
squidward.scale.y = 0.005
squidward.scale.z = 0.005
squidward.SetShaders(explosion_shader, aura_shader)


squidward.SetUniform("explosionIntensity", 5.0)
squidward.SetUniform("explosionCenter", squidward.translation)

rend.scene.append(bob)
rend.scene.append(house)
rend.scene.append(patrick)
rend.scene.append(squidward)

camDistance = 5
camAngle = 0
camAngleY = 0

target = bob

isRunning = True

while isRunning:
    deltaTime = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()
    mouseVel = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.MOUSEWHEEL:

            if event.y < 0 and camDistance < 10:
                camDistance -= event.y * deltaTime * 10

            if event.y > 0 and camDistance > 2:
                camDistance -= event.y * deltaTime * 10

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_SPACE:
                rend.ToggleFilledMode()

            elif event.key == pygame.K_1:
                target = bob

            elif event.key == pygame.K_2:
                target = house

            elif event.key == pygame.K_3:
                target = patrick

            elif event.key == pygame.K_4:
                target = squidward

            elif event.key == pygame.K_5:
                bob.SetShaders(vertex_shader, fragment_shader)
                house.SetShaders(vertex_shader, fragment_shader)
                patrick.SetShaders(vertex_shader, fragment_shader)
                squidward.SetShaders(vertex_shader, fragment_shader)
                bob.uniforms = {}
                house.uniforms = {}
                patrick.uniforms = {}
                squidward.uniforms = {}

            elif event.key == pygame.K_6:
                bob.SetShaders(spiral_shader, electric_shader)
                house.SetShaders(speaker_vertex_shader, speaker_fragment_shader)
                patrick.SetShaders(star_expand_shader, disintegration_shader)
                squidward.SetShaders(explosion_shader, aura_shader)
                bob.uniforms = {}
                house.uniforms = {}
                patrick.uniforms = {}
                squidward.uniforms = {}

            elif event.key == pygame.K_p:
                pygame.mixer.music.pause()
            elif event.key == pygame.K_r:
                pygame.mixer.music.unpause()
            elif event.key == pygame.K_m:
                pygame.mixer.music.set_volume(0.0)
            elif event.key == pygame.K_n:
                pygame.mixer.music.set_volume(0.7)

    if keys[K_w]:
        if camDistance > 2:
            camDistance -= 2 * deltaTime
    if keys[K_s]:
        if camDistance < 10:
            camDistance += 2 * deltaTime

    if keys[K_LEFT]:
        camAngle -= 45 * deltaTime
    if keys[K_RIGHT]:
        camAngle += 45 * deltaTime

    if keys[K_UP]:
        if rend.camera.position.y < 2:
            rend.camera.position.y += 5 * deltaTime
    if keys[K_DOWN]:
        if rend.camera.position.y > -2:
            rend.camera.position.y -= 5 * deltaTime

    if pygame.mouse.get_pressed()[0]:
        camAngle -= mouseVel[0] * deltaTime * 5

        if mouseVel[1] > 0 and rend.camera.position.y < 2:
            rend.camera.position.y += mouseVel[1] * deltaTime

        if mouseVel[1] < 0 and rend.camera.position.y > -2:
            rend.camera.position.y += mouseVel[1] * deltaTime

    rend.camera.Orbit(target.translation, camDistance, camAngle)
    rend.camera.LookAt(target.translation)

    rend.Render()

    rend.time += deltaTime
    pygame.display.flip()

pygame.quit()