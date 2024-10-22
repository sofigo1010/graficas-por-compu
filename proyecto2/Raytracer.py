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
rt.envMap = Texture("textures/underfondo.bmp")

yellow_material = Material(diffuse=[1, 1, 0], spec=128, Ks=0.5, matType=OPAQUE)
orange_material = Material(diffuse=[1, 0.5, 0], spec=128, Ks=0.5, matType=OPAQUE)
black_material = Material(diffuse=[0, 0, 0], spec=128, Ks=0.5, matType=OPAQUE)
white_material = Material(diffuse=[1, 1, 1], spec=128, Ks=0.5, matType=OPAQUE)
grey_material = Material(diffuse=[0.5, 0.5, 0.5], spec=128, Ks=0.5, matType=OPAQUE)
transparent_material = Material(diffuse=[0.3, 0.3, 1], spec=128, Ks=0.1, matType=TRANSPARENT)
green_material = Material(diffuse=[0.2, 0.8, 0.2], spec=32, Ks=0.3, matType=OPAQUE)
light_green_material = Material(diffuse=[0.5, 1, 0.5], spec=32, Ks=0.3, matType=OPAQUE)

cuerpo_pez = Triangle(
    v0=[2.0, 0.5, -5],
    v1=[1.3, -0.5, -5],
    v2=[2.7, -0.5, -5],
    material=yellow_material
)
rt.scene.append(cuerpo_pez)

aleta_superior_izquierda = Triangle(
    v0=[1.4, 0.0, -5.05],
    v1=[1.86, 0.3, -5.05],
    v2=[1.6, -0.3, -5.05],
    material=orange_material
)
rt.scene.append(aleta_superior_izquierda)

aleta_derecha = Triangle(
    v0=[2.4, -0.1, -5],
    v1=[2.8, 0.2, -5],
    v2=[2.8, -0.4, -5],
    material=orange_material
)
rt.scene.append(aleta_derecha)

aleta_inferior = Triangle(
    v0=[2.0, -0.4, -4.95],
    v1=[2.1, -0.2, -4.95],
    v2=[1.9, -0.2, -4.95],
    material=orange_material
)
rt.scene.append(aleta_inferior)

ojo_blanco = Sphere(
    position=[1.65, -0.15, -4.9], 
    radius=0.06, 
    material=white_material
)
rt.scene.append(ojo_blanco)

ojo_negro = Sphere(
    position=[1.65, -0.15, -4.85],
    radius=0.03, 
    material=black_material
)
rt.scene.append(ojo_negro)

boca = Disk(
    position=[1.4, -0.2, -4.9],
    normal=[0, 1, 0],
    radius=0.1,
    material=black_material
)
rt.scene.append(boca)

sand_texture = Texture("textures/sand.bmp")
beige_material = Material(
    diffuse=[1.0, 0.75, 0.8], 
    spec=32,
    Ks=0.5,
    matType=OPAQUE,
    texture=sand_texture
)

sand_plane = Plane(
    position=[0, -6, -6], 
    normal=[0, 1, 0], 
    material=beige_material
)
rt.scene.append(sand_plane)

large_rock1 = Sphere(
    position=[-2.0, -3.5, -4.98],
    radius=1.0,
    material=grey_material
)
rt.scene.append(large_rock1)

large_rock2 = Sphere(
    position=[0.0, -3.8, -4.98],
    radius=1.2,
    material=grey_material
)
rt.scene.append(large_rock2)

large_rock3 = Sphere(
    position=[2.5, -3.2, -4.98],
    radius=0.9,
    material=grey_material
)
rt.scene.append(large_rock3)

starfish_texture = Texture("textures/pinkstar.bmp")
pink_material_with_texture = Material(
    diffuse=[1.0, 0.75, 0.8], 
    spec=32,
    Ks=0.5,
    matType=OPAQUE,
    texture=starfish_texture
)

starfish = Star(
    position=[0.0, -0.4, -5.5],
    size=0.5,
    material=pink_material_with_texture
)
rt.scene.append(starfish)

bottle_body = Cylinder(
    position=[-1.5, -0.6, -5.5],
    radius=0.1,
    height=0.5,
    material=transparent_material
)
rt.scene.append(bottle_body)

bottle_cap = Hemisphere(
    position=[-1.5, -0.1, -5.5],
    radius=0.1,
    material=grey_material,
    orientation='up'
)
rt.scene.append(bottle_cap)

bubble_material = Material(
    diffuse=[0.8, 0.9, 1],
    spec=64,
    Ks=0.1,
    matType=TRANSPARENT
)
bubble = Ellipsoid(
    position=[1.0, 1.0, -4.8],
    radii=[0.15, 0.2, 0.15],
    material=bubble_material
)
rt.scene.append(bubble)

plant1 = Triangle(
    v0=[-1.8, -3.0, -4.95],
    v1=[-2.0, -0.4, -4.95],
    v2=[-1.6, -3.0, -4.95],
    material=green_material
)
rt.scene.append(plant1)

plant2 = Triangle(
    v0=[-2.2, -3.0, -4.95],
    v1=[-2.4, -0.6, -4.95],
    v2=[-2.0, -3.0, -4.95],
    material=light_green_material
)
rt.scene.append(plant2)

plant3 = Triangle(
    v0=[0.2, -3.5, -4.95],
    v1=[0.1, -0.5, -4.95],
    v2=[0.5, -3.5, -4.95],
    material=green_material
)
rt.scene.append(plant3)

plant4 = Triangle(
    v0=[1.8, -3.2, -4.95],
    v1=[2.2, -0.7, -4.95],
    v2=[1.4, -3.2, -4.95],
    material=light_green_material
)
rt.scene.append(plant4)

plant5 = Triangle(
    v0=[-1.0, -3.0, -4.95],
    v1=[-1.4, -0.3, -4.95],
    v2=[-0.6, -3.0, -4.95],
    material=green_material
)
rt.scene.append(plant5)

plant6 = Triangle(
    v0=[0.5, -3.5, -4.95],
    v1=[0.2, -0.8, -4.95],
    v2=[0.8, -3.5, -4.95],
    material=light_green_material
)
rt.scene.append(plant6)

plant7 = Triangle(
    v0=[-1.5, -3.3, -4.95],
    v1=[-1.8, -0.2, -4.95],
    v2=[-1.2, -3.3, -4.95],
    material=green_material
)
rt.scene.append(plant7)

plant8 = Triangle(
    v0=[1.0, -3.5, -4.95],
    v1=[1.3, -1.0, -4.95],
    v2=[0.7, -3.5, -4.95],
    material=green_material
)
rt.scene.append(plant8)

plant9 = Triangle(
    v0=[1.5, -3.4, -4.95],
    v1=[1.8, -0.9, -4.95],
    v2=[1.2, -3.4, -4.95],
    material=light_green_material
)
rt.scene.append(plant9)

plant10 = Triangle(
    v0=[0.8, -3.3, -4.95],
    v1=[1.0, -0.6, -4.95],
    v2=[0.6, -3.3, -4.95],
    material=green_material
)
rt.scene.append(plant10)

fish_texture = Texture("textures/fish2.bmp")
fish_material_with_texture = Material(
    diffuse=[1.0, 1.0, 1.0],  
    spec=64,
    Ks=0.3,
    matType=OPAQUE,
    texture=fish_texture
)

purple_material = Material(
    diffuse=[0.5, 0, 0.5], 
    spec=128, Ks=0.5, 
    matType=OPAQUE)

fish_body = Ellipsoid(
    position=[-1.45, 0.5, -5.5],  
    radii=[0.5, 0.3, 0.2],  
    material=fish_material_with_texture
)
rt.scene.append(fish_body)


fish_tail1 = Triangle(
    v0=[-1.0, 0.5, -5.7],  
    v1=[-0.8, 0.8, -5.7],
    v2=[-1.0, 0.2, -5.7],
    material=purple_material
)
rt.scene.append(fish_tail1)

fish_tail2 = Triangle(
    v0=[-1.0, 0.5, -5.7],  
    v1=[-0.8, 0.2, -5.7],
    v2=[-1.0, 0.8, -5.7],
    material=purple_material
)
rt.scene.append(fish_tail2)


fish_eye_white = Sphere(
    position=[-1.8, 0.55, -5.35],  
    radius=0.06, 
    material=white_material
)
rt.scene.append(fish_eye_white)

fish_eye_black = Sphere(
    position=[-1.8, 0.55, -5.3], 
    radius=0.03, 
    material=black_material
)
rt.scene.append(fish_eye_black)


pufferfish_yellow_material_texture = Texture("textures/fish3.bmp")
pufferfish_yellow_material_with_texture = Material(
    diffuse=[1.0, 1.0, 1.0],  
    spec=64,
    Ks=0.3,
    matType=OPAQUE,
    texture=pufferfish_yellow_material_texture
)



pufferfish_body = Sphere(
    position=[0.6, 0.5, -5.4], 
    radius=0.3,  
    material=pufferfish_yellow_material_with_texture
)
rt.scene.append(pufferfish_body)


pufferfish_fin1 = Triangle(
    v0=[0.6, 0.65, -5.3],  
    v1=[0.65, 0.75, -5.3],
    v2=[0.55, 0.75, -5.3],
    material=orange_material
)
rt.scene.append(pufferfish_fin1)

pufferfish_fin2 = Triangle(
    v0=[0.85, 0.5, -5.4],  
    v1=[1.0, 0.6, -5.4],
    v2=[0.85, 0.4, -5.4],
    material=orange_material
)
rt.scene.append(pufferfish_fin2)

pufferfish_fin3 = Triangle(
    v0=[0.35, 0.5, -5.4],  
    v1=[0.2, 0.6, -5.4],
    v2=[0.35, 0.4, -5.4],
    material=orange_material
)
rt.scene.append(pufferfish_fin3)


eye_radius = 0.15  
pupil_radius = 0.08  


pufferfish_eye_white1 = Sphere(
    position=[0.62, 0.55, -5.24],  
    radius=eye_radius, 
    material=white_material
)
rt.scene.append(pufferfish_eye_white1)

pufferfish_eye_black1 = Sphere(
    position=[0.55, 0.55, -5.15],  
    radius=pupil_radius, 
    material=black_material
)
rt.scene.append(pufferfish_eye_black1)


pufferfish_eye_white2 = Sphere(
    position=[0.55, 0.55, -5.25],  
    radius=eye_radius, 
    material=white_material
)
rt.scene.append(pufferfish_eye_white2)

pufferfish_eye_black2 = Sphere(
    position=[0.625, 0.55, -5.15],  
    radius=pupil_radius, 
    material=black_material
)
rt.scene.append(pufferfish_eye_black2)







rt.Lights.append(AmbientLight(intensity=0.6))

sunlight = DirectionalLight(
    color=[1, 1, 0.9],
    intensity=1.0,
    direction=[-1, -1, -1]
)
rt.Lights.append(sunlight)

star_spotlight = Spotlight(
    color=[1, 0.5, 0.5],
    intensity=1.2,
    position=[0.0, 0.5, -5.5],
    direction=[0, -1, 0],
    innerAngle=20, 
    outerAngle=30
)
rt.Lights.append(star_spotlight)

fish_spotlight = Spotlight(
    color=[1, 1, 0.8],
    intensity=1.0,
    position=[2.0, 0.8, -5.0],
    direction=[0, -1, 0],
    innerAngle=25,
    outerAngle=35
)
rt.Lights.append(fish_spotlight)

eye_and_fin_spotlight = Spotlight(
    color=[1, 1, 0.8],
    intensity=1.5,
    position=[1.5, 0.2, -4.9],
    direction=[0, -1, 0],
    innerAngle=30,
    outerAngle=40
)
rt.Lights.append(eye_and_fin_spotlight)

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
